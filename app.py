from flask import Flask, jsonify, request, send_from_directory
import logging
import os
import clips
import re
from flask_cors import CORS
import uuid
import json
import time
import db
from shutil import copyfile
from location_service import location_service

# Flask application instance
app = Flask(__name__)

# Enable CORS for local/dev usage. Configure origins in production as needed.
CORS(app)

# Initialize CLIPS Environment at module import time for high performance
# CLIPS_ENV is a global Environment instance that will be reused across requests
CLIPS_ENV = clips.Environment()

# Load CLIPS knowledge base files once at startup
_kb_dir = os.path.join(os.path.dirname(__file__), "knowledge_base")
_templates_path = os.path.join(_kb_dir, "templates.clp")
_rules_path = os.path.join(_kb_dir, "rules.clp")

for _path in (_templates_path, _rules_path):
    try:
        if os.path.isfile(_path):
            CLIPS_ENV.load(_path)
            logging.info(f"Loaded CLIPS file: {_path}")
        else:
            logging.warning(f"CLIPS file not found (will skip): {_path}")
    except Exception as _e:
        logging.exception(f"Error loading CLIPS file {_path}: {_e}")

# Initialize local DB for symptoms/diseases
try:
    db.init_db()
    logging.info('Initialized local data.db')
except Exception:
    logging.exception('Failed to initialize DB')


@app.route('/health')
def health():
    """Return a simple JSON 'OK' response for health checks."""
    return jsonify({"status": "OK"})



@app.route('/')
def index():
    """Serve the simple, accessible frontend."""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    simple_path = os.path.join(static_dir, 'simple.html')
    if os.path.isfile(simple_path):
        return send_from_directory(static_dir, 'simple.html')
    return (
        "<h1>Not Found</h1><p>No frontend available.</p>",
        404,
    )


def _clone_environment():
    """Return a cloned CLIPS Environment based on the pre-loaded CLIPS_ENV.

    Prefer using CLIPS_ENV.clone() when available. If clone() is not
    available or fails, fall back to creating a fresh Environment and
    loading the same knowledge base files. This keeps the global
    preloaded environment untouched and provides per-request isolation.
    """
    if hasattr(CLIPS_ENV, 'clone'):
        try:
            return CLIPS_ENV.clone()
        except Exception:
            logging.exception("CLIPS_ENV.clone() failed; falling back to new Environment")
    # Fallback
    env = clips.Environment()
    for _path in (_templates_path, _rules_path):
        if os.path.isfile(_path):
            try:
                env.load(_path)
            except Exception:
                logging.exception(f"Failed to load CLIPS file into cloned env: {_path}")
    return env


@app.route('/api/symptoms', methods=['GET', 'POST'])
def api_symptoms():
    if request.method == 'GET':
        try:
            symptoms = db.list_symptoms()
            return jsonify({'symptoms': symptoms})
        except Exception as e:
            logging.exception('Failed to list symptoms')
            return jsonify({'error': str(e)}), 500

    # POST: add a symptom
    payload = request.get_json(force=True)
    if not isinstance(payload, dict):
        return jsonify({'error': 'invalid JSON'}), 400
    name = payload.get('name')
    synonyms = payload.get('synonyms') or []
    try:
        db.add_symptom(name, synonyms)
        return jsonify({'status': 'ok'})
    except Exception as e:
        logging.exception('Failed to add symptom')
        return jsonify({'error': str(e)}), 500


@app.route('/api/diseases', methods=['GET', 'POST'])
def api_diseases():
    if request.method == 'GET':
        try:
            return jsonify(db.list_diseases())
        except Exception as e:
            logging.exception('Failed to list diseases')
            return jsonify({'error': str(e)}), 500

    payload = request.get_json(force=True)
    if not isinstance(payload, dict):
        return jsonify({'error': 'invalid JSON'}), 400
    name = payload.get('name')
    symptoms = payload.get('symptoms') or []
    try:
        db.add_disease(name, symptoms)
        return jsonify({'status': 'ok'})
    except Exception as e:
        logging.exception('Failed to add disease')
        return jsonify({'error': str(e)}), 500


@app.route('/api/rules', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_rules():
    method = request.method
    if method == 'GET':
        try:
            return jsonify(db.list_rules())
        except Exception as e:
            logging.exception('Failed to list rules')
            return jsonify({'error': str(e)}), 500
    payload = request.get_json(force=True)
    if method == 'POST':
        # create new rule
        try:
            rid = db.add_rule(None, payload)
            return jsonify({'status': 'ok', 'id': rid})
        except Exception as e:
            logging.exception('Failed to add rule')
            return jsonify({'error': str(e)}), 500
    if method == 'PUT':
        rid = payload.get('id')
        try:
            db.add_rule(rid, payload.get('rule') or payload)
            return jsonify({'status': 'ok'})
        except Exception as e:
            logging.exception('Failed to update rule')
            return jsonify({'error': str(e)}), 500
    if method == 'DELETE':
        rid = payload.get('id')
        try:
            db.delete_rule(rid)
            return jsonify({'status': 'ok'})
        except Exception as e:
            logging.exception('Failed to delete rule')
            return jsonify({'error': str(e)}), 500


def translate_rules_to_clp(rules_list):
    """Translate a list of rule JSON objects to a CLIPS rulestring.

    Supported JSON schema (subset):
    {
      "name": "Rule name",
      "salience": 50,
      "conditions": [{"field":"age","operator":">","value":65}, {"field":"symptom","operator":"contains","value":"chest-pain"}],
      "actions": [{"set_triage_level":"RED"},{"set_transport":"ambulance"},{"set_rationale":"text"}]
    }
    """
    pieces = []
    for idx, r in enumerate(rules_list):
        name = r.get('name') or f'R_user_{idx}'
        sal = r.get('salience', 10)
        conds = r.get('conditions', [])
        actions = r.get('actions', [])

        # Build LHS
        lhs = []
        for c in conds:
            f = c.get('field')
            op = c.get('operator')
            v = c.get('value')
            if f == 'age' and op in ('>','<','>=','<=','=','!='):
                # (patient-demographics (age ?age&:(> ?age 65)))
                lhs.append(f"(patient-demographics (age ?age&:({op} ?age {int(v)})))")
            elif f == 'history' and op in ('=','contains'):
                val = str(v).replace(' ', '-')
                lhs.append(f"(patient-history (history {val}))")
            elif f == 'symptom' and op in ('contains','=','in'):
                val = str(v).replace(' ', '-')
                lhs.append(f"(patient-symptom (name {val}))")
            # More fields/operators can be added here

        # Build RHS actions
        rhs_parts = []
        rationale = None
        for a in actions:
            if 'set_triage_level' in a:
                lvl = a['set_triage_level']
                rhs_parts.append(f"(level {lvl})")
            if 'set_transport' in a:
                t = a['set_transport']
                rhs_parts.append(f"(transport {t})")
            if 'set_rationale' in a:
                rationale = a['set_rationale']
                # will be included below

        # Compose rule string
        rule_lines = [f"(defrule {name.replace(' ','_')}", f'  "{r.get("name","")}"', f'  (declare (salience {sal}))', '']
        for l in lhs:
            rule_lines.append('  ' + l)
        rule_lines.append('')
        rule_lines.append('  =>')
        # assert triage-result with slots
        triage_slots = []
        for part in rhs_parts:
            # part already like '(level RED)' or 'level RED' depending on construction; normalize
            if part.strip().startswith('('):
                triage_slots.append(part.strip())
            else:
                triage_slots.append('(' + part.strip() + ')')
        if rationale:
            # quote the rationale
            triage_slots.append(f'(rationale "{rationale}")')
        # default score omitted; authors can include in actions if desired
        rule_lines.append('  (assert (triage-result')
        # each triage slot should be a parenthesized item
        for ts in triage_slots:
            rule_lines.append('    ' + ts)
        rule_lines.append('  ))')
        rule_lines.append(')')
        pieces.append('\n'.join(rule_lines))

        body = '\n\n'.join(pieces)
        # Append a safe default fallback rule (low salience) so there's always a triage-result
        default_rule = '''
(defrule R0_Default_Triage
    "Safe default: non-urgent GREEN when no other triage-result asserted."
    (declare (salience 0))
    (not (triage-result))
    =>
    (assert (triage-result (level GREEN) (score 5) (transport none) (rationale "Default non-urgent triage. No high-priority rules matched.")))
)
'''
        return body + '\n\n' + default_rule


@app.route('/api/publish-rules', methods=['POST'])
def api_publish_rules():
    """Translate rules from DB to CLP, validate by loading in a temp CLIPS env, and if ok replace the active rules.clp."""
    try:
        rules = db.list_rules()
        rules_json = [r['rule'] for r in rules if r.get('rule')]
        if not rules_json:
            return jsonify({'error': 'no rules to publish'}), 400

        clp_text = translate_rules_to_clp(rules_json)
        kb_dir = os.path.join(os.path.dirname(__file__), 'knowledge_base')
        temp_path = os.path.join(kb_dir, 'user_rules_temp.clp')
        final_path = os.path.join(kb_dir, 'rules.clp')
        backup_path = os.path.join(kb_dir, 'rules.clp.bak')

        # write temp CLP
        with open(temp_path, 'w') as f:
            f.write(';; Generated by admin publish\n')
            f.write(clp_text)

        # Validate by loading into a fresh clips.Environment
        try:
            test_env = clips.Environment()
            # load templates first
            if os.path.isfile(_templates_path):
                test_env.load(_templates_path)
            test_env.load(temp_path)
        except Exception as e:
            logging.exception('Validation load failed')
            return jsonify({'error': 'validation failed', 'details': str(e)}), 400

        # Backup existing rules and replace
        try:
            if os.path.isfile(final_path):
                copyfile(final_path, backup_path)
            copyfile(temp_path, final_path)
        except Exception as e:
            logging.exception('Failed to replace rules file')
            return jsonify({'error': 'failed to replace rules file', 'details': str(e)}), 500

        # Reload global CLIPS_ENV: clear and load templates+rules
        try:
            if hasattr(CLIPS_ENV, 'clear'):
                CLIPS_ENV.clear()
            # reload files
            if os.path.isfile(_templates_path):
                CLIPS_ENV.load(_templates_path)
            if os.path.isfile(final_path):
                CLIPS_ENV.load(final_path)
        except Exception:
            logging.exception('Failed to reload CLIPS_ENV after publish')

        return jsonify({'status': 'ok'})
    except Exception as e:
        logging.exception('Publish failed')
        return jsonify({'error': str(e)}), 500


def assert_patient_facts(env, data):
    """Assert patient facts into the provided CLIPS environment.

    We assert each incoming key/value as a separate CLIPS fact to avoid
    requiring a specific deftemplate. For example, {'age':70,'history':'diabetes'}
    becomes the facts (age 70) and (history diabetes).
    Strings are quoted if they contain spaces.
    """
    if not isinstance(data, dict):
        raise TypeError("patient data must be a JSON object/dict")
    # Build and assert structured, templated facts expected by the rules:
    # - `patient-demographics`: uses keys `age` and `gender` (if present)
    # - `patient-history`: uses keys `history` and `mode-of-arrival` (if present)
    #
    # Any remaining keys (vital signs) are ignored for now and will be
    # handled in a later stage.
    # patient-demographics
    pd_slots = []
    age = data.get('age')
    if age is not None:
        pd_slots.append(f"(age {int(age)})")
    gender = data.get('gender')
    if gender is not None:
        # gender is treated as a symbol if single token, otherwise quoted string
        g = str(gender)
        if ' ' in g:
            g_val = '"' + g.replace('"', '\\"') + '"'
        else:
            g_val = g
        pd_slots.append(f"(gender {g_val})")

    if pd_slots:
        pd_fact = "(patient-demographics " + " ".join(pd_slots) + ")"
        env.assert_string(pd_fact)

    # patient-history
    ph_slots = []
    history = data.get('history')
    if history is not None:
        # history is defined as a SYMBOL in the template; convert spaces to hyphens
        h_raw = str(history).strip()
        if h_raw:
            h = h_raw.replace(' ', '-')
            ph_slots.append(f"(history {h})")
    moa = data.get('mode-of-arrival') or data.get('mode_of_arrival') or data.get('modeOfArrival')
    if moa is not None:
        m = str(moa).strip()
        if m:
            if ' ' in m:
                m_val = '"' + m.replace('"', '\\"') + '"'
            else:
                m_val = m
            ph_slots.append(f"(mode-of-arrival {m_val})")

    if ph_slots:
        ph_fact = "(patient-history " + " ".join(ph_slots) + ")"
        env.assert_string(ph_fact)

    # symptoms: accept list or comma-separated string
    symptoms = data.get('symptoms') or data.get('symptom') or data.get('symptoms_list')
    sym_list = []
    if symptoms is not None:
        if isinstance(symptoms, str):
            # allow comma-separated symptoms
            for s in [s.strip() for s in symptoms.split(',') if s.strip()]:
                sym_list.append(s)
        elif isinstance(symptoms, list):
            for s in symptoms:
                if isinstance(s, str) and s.strip():
                    sym_list.append(s.strip())

    for s in sym_list:
        # normalize symptom to symbol form (lowercase, spaces to hyphens)
        # Use DB synonyms lookup when available
        token = str(s).strip().lower()
        mapped = None
        try:
            mapped = db.lookup_symptom(token)
        except Exception:
            mapped = None
        if mapped:
            sn = str(mapped).lower().replace(' ', '-')
        else:
            sn = token.replace(' ', '-')
        # assert a patient-symptom fact: (patient-symptom (name chest-pain))
        try:
            env.assert_string(f"(patient-symptom (name {sn}))")
        except Exception:
            # If symbolify fails (contains illegal chars), quote it as string in slot
            safe = '"' + sn.replace('"', '\\"') + '"'
            env.assert_string(f"(patient-symptom (name {safe}))")


def _extract_triage_result(env):
    """Scan the environment facts and return a dict with triage_level and rationale
    if a (triage-result ...) fact is found. Returns None if not found.
    """
    for fact in env.facts():
        # Try to determine template name; fallback to string parsing
        try:
            tname = fact.template.name
        except Exception:
            tname = None

        fs = str(fact)
        if tname == 'triage-result' or fs.startswith('(triage-result'):
            level = None
            rationale = None
            score = None
            transport = None
            # Try slot access (clipspy exposes fact[slot])
            try:
                level = fact['level']
            except Exception:
                pass
            try:
                rationale = fact['rationale']
            except Exception:
                pass
            try:
                score = fact['score']
            except Exception:
                pass
            try:
                transport = fact['transport']
            except Exception:
                pass

            # Fallback to regex parse of the fact string
            if (level is None) or (rationale is None) or (score is None):
                m_level = re.search(r'\(level\s+([A-Za-z0-9_\-]+)\)', fs)
                m_r = re.search(r'\(rationale\s+"([^\"]*)"\)', fs)
                m_s = re.search(r'\(score\s+([0-9]+)\)', fs)
                m_t = re.search(r'\(transport\s+([A-Za-z0-9_\-]+)\)', fs)
                if m_level:
                    level = level or m_level.group(1)
                if m_r:
                    rationale = rationale or m_r.group(1)
                if m_s:
                    try:
                        score = score or int(m_s.group(1))
                    except Exception:
                        pass
                if m_t:
                    transport = transport or m_t.group(1)

            # Normalize/clean values for API consumers
            if isinstance(level, str):
                level = level.strip().upper()
            if isinstance(rationale, str):
                # Normalize internal whitespace/newlines to single spaces for API consumers
                rationale = re.sub(r'\s+', ' ', rationale).strip()

            result = {'triage_level': level, 'rationale': rationale}
            if score is not None:
                try:
                    result['score'] = int(score)
                except Exception:
                    pass
            if transport is not None:
                if isinstance(transport, str):
                    result['transport'] = transport.strip().lower()
                else:
                    result['transport'] = transport
            return result
    return None


@app.route('/dispatch', methods=['POST'])
def dispatch():
    """Simulated emergency dispatch endpoint.

    Accepts JSON payload with keys:
      - patient: object (original patient data)
      - triage: object (result with triage_level, rationale, score)
      - location: optional {lat, lon, description}

    This endpoint writes a timestamped alert to `alerts.log` and returns a UUID.
    """
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'invalid JSON body'}), 400

    alert = {
        'id': str(uuid.uuid4()),
        'timestamp': int(time.time()),
        'patient': data.get('patient'),
        'triage': data.get('triage'),
        'location': data.get('location')
    }

    try:
        log_path = os.path.join(os.path.dirname(__file__), 'alerts.log')
        with open(log_path, 'a') as f:
            f.write(json.dumps(alert) + '\n')
    except Exception as e:
        logging.exception('Failed to write alert')
        return jsonify({'error': 'failed to record alert', 'details': str(e)}), 500

    return jsonify({'status': 'ok', 'id': alert['id']})


@app.route('/triage', methods=['POST'])
def triage():
    """Main triage endpoint.

    Expects a JSON object with patient facts (e.g., {"age":70, "history":"diabetes"}).
    Clones the preloaded CLIPS environment, asserts the facts into the cloned
    environment, runs inference, extracts a (triage-result ...) fact, and
    returns the triage level and rationale.
    """
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'invalid JSON body, expected object'}), 400

    env = None
    try:
        env = _clone_environment()

        try:
            assert_patient_facts(env, data)
        except Exception as e:
            logging.exception("Failed to assert patient facts")
            return jsonify({'error': 'failed to assert facts', 'details': str(e)}), 500

        try:
            env.run()
        except Exception as e:
            logging.exception("Error running CLIPS engine")
            return jsonify({'error': 'inference failure', 'details': str(e)}), 500

        result = _extract_triage_result(env)
        if not result:
            # If no triage-result, return a safe default instead of 500 so frontends can render gracefully.
            return jsonify({
                'triage_level': 'GREEN',
                'rationale': 'Default non-urgent triage (no rule matched).',
                'score': 5,
                'transport': 'none'
            })

        # Ensure consistent schema: triage_level (string or null), rationale (string), score (int or omitted), transport
        normalized = {
            'triage_level': (result.get('triage_level') if result.get('triage_level') is not None else None),
            'rationale': (result.get('rationale') or ''),
            'transport': (result.get('transport') or 'none'),
        }
        if 'score' in result and result.get('score') is not None:
            try:
                normalized['score'] = int(result.get('score'))
            except Exception:
                pass

        return jsonify(normalized)
    finally:
        # Allow the temporary env to be cleaned up. Try some best-effort cleanup
        # (clear/reset) before deleting reference.
        try:
            if env is not None:
                if hasattr(env, 'clear'):
                    try:
                        env.clear()
                    except Exception:
                        pass
                if hasattr(env, 'reset'):
                    try:
                        env.reset()
                    except Exception:
                        pass
                del env
        except Exception:
            pass


@app.route('/api/hospitals', methods=['GET', 'POST'])
def api_hospitals():
    """Manage hospitals"""
    if request.method == 'GET':
        try:
            return jsonify(db.list_hospitals())
        except Exception as e:
            logging.exception('Failed to list hospitals')
            return jsonify({'error': str(e)}), 500
    
    # POST: add hospital
    payload = request.get_json(force=True)
    try:
        db.add_hospital(
            name=payload.get('name'),
            latitude=float(payload.get('latitude')),
            longitude=float(payload.get('longitude')),
            contact=payload.get('contact'),
            ambulance_available=payload.get('ambulance_available', True),
            capacity_level=payload.get('capacity_level', 'medium')
        )
        return jsonify({'status': 'ok'})
    except Exception as e:
        logging.exception('Failed to add hospital')
        return jsonify({'error': str(e)}), 500


@app.route('/api/nearest-hospitals', methods=['POST'])
def api_nearest_hospitals():
    """
    Find nearest hospitals - HYBRID APPROACH:
    1. Try to fetch live data from OpenStreetMap (works anywhere!)
    2. Fallback to local database if OSM fails
    
    This means it works in Nakuru, Mombasa, Kisumu, anywhere in Kenya!
    """
    payload = request.get_json(force=True)
    try:
        user_lat = float(payload.get('latitude'))
        user_lon = float(payload.get('longitude'))
        limit = int(payload.get('limit', 5))
        radius_km = float(payload.get('radius_km', 15))  # Default 15km radius
        
        # Try to fetch from OpenStreetMap first (live data!)
        from location_service import find_nearby_hospitals
        
        logging.info(f"Searching for hospitals near {user_lat}, {user_lon} (radius: {radius_km}km)")
        live_hospitals = find_nearby_hospitals(user_lat, user_lon, radius_km, limit)
        
        if live_hospitals and len(live_hospitals) > 0:
            logging.info(f"Found {len(live_hospitals)} hospitals from OpenStreetMap")
            # Format for frontend compatibility
            for h in live_hospitals:
                h['contact'] = h.get('phone', '')
                h['rating'] = None  # OSM doesn't have ratings
            return jsonify(live_hospitals)
        
        # Fallback to local database
        logging.info("No results from OSM, falling back to local database")
        nearest = db.find_nearest_hospitals(user_lat, user_lon, limit)
        return jsonify(nearest)
        
    except Exception as e:
        logging.exception('Failed to find nearest hospitals')
        return jsonify({'error': str(e)}), 500


@app.route('/api/sha-cost-estimate', methods=['POST'])
def api_sha_cost_estimate():
    """Estimate SHA coverage and patient cost based on condition"""
    payload = request.get_json(force=True)
    
    # SHA (Social Health Authority) cost estimation logic
    # This is simplified - in production, integrate with actual SHA API
    triage_level = payload.get('triage_level', 'GREEN')
    symptoms = payload.get('symptoms', '')
    
    # Basic cost estimation (KES)
    base_costs = {
        'RED': {'consultation': 0, 'ambulance': 0, 'emergency_care': 5000, 'sha_covers': 0.90},
        'YELLOW': {'consultation': 0, 'tests': 2000, 'medication': 1500, 'sha_covers': 0.85},
        'GREEN': {'consultation': 0, 'medication': 500, 'sha_covers': 0.80}
    }
    
    cost_breakdown = base_costs.get(triage_level, base_costs['GREEN'])
    total_cost = sum(v for k, v in cost_breakdown.items() if k != 'sha_covers')
    sha_coverage_percent = cost_breakdown.get('sha_covers', 0.80)
    sha_amount = total_cost * sha_coverage_percent
    patient_pays = total_cost - sha_amount
    
    return jsonify({
        'total_estimated_cost_kes': total_cost,
        'sha_covers_percent': int(sha_coverage_percent * 100),
        'sha_amount_kes': round(sha_amount, 2),
        'patient_pays_kes': round(patient_pays, 2),
        'breakdown': cost_breakdown,
        'note': 'Estimates based on SHA standard rates. Actual costs may vary.'
    })


@app.route('/api/notify-hospital', methods=['POST'])
def api_notify_hospital():
    """Send notification to hospital about incoming patient"""
    payload = request.get_json(force=True)
    
    notification = {
        'id': str(uuid.uuid4()),
        'timestamp': int(time.time()),
        'hospital_id': payload.get('hospital_id'),
        'patient_summary': {
            'age': payload.get('age'),
            'gender': payload.get('gender'),
            'symptoms': payload.get('symptoms'),
            'triage_level': payload.get('triage_level'),
            'transport_mode': payload.get('transport_mode'),
            'eta_minutes': payload.get('eta_minutes')
        },
        'status': 'sent'
    }
    
    try:
        # Log notification (in production, send via SMS/email/push)
        log_path = os.path.join(os.path.dirname(__file__), 'hospital_notifications.log')
        with open(log_path, 'a') as f:
            f.write(json.dumps(notification) + '\n')
        
        return jsonify({
            'status': 'ok',
            'notification_id': notification['id'],
            'message': f'Hospital notified. Patient ETA: {payload.get("eta_minutes", "unknown")} minutes'
        })
    except Exception as e:
        logging.exception('Failed to notify hospital')
        return jsonify({'error': str(e)}), 500


@app.route('/api/geocode', methods=['POST'])
def api_geocode():
    """Convert address to coordinates using professional location service (cached, with fallbacks)"""
    payload = request.get_json(force=True)
    address = payload.get('address')
    
    if not address:
        return jsonify({'error': 'address required'}), 400
    
    try:
        # Use professional location service with caching and fallbacks
        result = location_service.parse_location_input(address)
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Address not found'}), 404
    except Exception as e:
        logging.exception(f"Geocoding error for '{address}': {e}")
        return jsonify({'error': 'Geocoding service temporarily unavailable'}), 503


if __name__ == '__main__':
    # Simple runner for development
    app.run(host='0.0.0.0', port=7000, debug=True)

