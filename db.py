import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS symptoms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        synonyms TEXT DEFAULT '[]'
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS diseases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        symptoms TEXT DEFAULT '[]'
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS hospitals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        contact TEXT,
        ambulance_available INTEGER DEFAULT 1,
        capacity_level TEXT DEFAULT 'medium'
    )
    ''')
    conn.commit()
    conn.close()


def add_symptom(name, synonyms=None):
    if not name:
        raise ValueError('name required')
    
    # Handle synonyms as string (comma-separated) or list
    if synonyms is None:
        synonyms = []
    elif isinstance(synonyms, str):
        # Split comma-separated string into list
        synonyms = [s.strip() for s in synonyms.split(',') if s.strip()]
    elif not isinstance(synonyms, list):
        synonyms = []
    
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO symptoms (name, synonyms) VALUES (?, ?)', (name, json.dumps(synonyms)))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        # merge synonyms
        cur.execute('SELECT synonyms FROM symptoms WHERE name=?', (name,))
        row = cur.fetchone()
        if row:
            existing = json.loads(row['synonyms'])
            merged = list(dict.fromkeys(existing + synonyms))
            cur.execute('UPDATE symptoms SET synonyms=? WHERE name=?', (json.dumps(merged), name))
            conn.commit()
        return None
    finally:
        conn.close()


def list_symptoms():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT rowid, name, synonyms, age_groups FROM symptoms ORDER BY name')
    rows = []
    for r in cur.fetchall():
        rows.append({
            'id': r[0],  # rowid
            'name': r[1],  # name  
            'synonyms': json.loads(r[2]),  # synonyms
            'age_groups': json.loads(r[3]) if r[3] else []  # age_groups
        })
    conn.close()
    return rows


def lookup_symptom(token):
    if not token:
        return None
    token = token.strip().lower()
    conn = get_conn()
    cur = conn.cursor()
    # exact name match
    cur.execute('SELECT name, synonyms FROM symptoms')
    for r in cur.fetchall():
        name = r['name']
        if name.lower() == token:
            conn.close()
            return name
        syns = json.loads(r['synonyms'])
        for s in syns:
            if str(s).strip().lower() == token:
                conn.close()
                return name
    conn.close()
    return None


def add_disease(name, symptoms=None):
    if not name:
        raise ValueError('name required')
    symptoms = symptoms or []
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO diseases (name, symptoms) VALUES (?, ?)', (name, json.dumps(symptoms)))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        cur.execute('SELECT symptoms FROM diseases WHERE name=?', (name,))
        row = cur.fetchone()
        if row:
            existing = json.loads(row['symptoms'])
            merged = list(dict.fromkeys(existing + symptoms))
            cur.execute('UPDATE diseases SET symptoms=? WHERE name=?', (json.dumps(merged), name))
            conn.commit()
        return None
    finally:
        conn.close()


def list_diseases():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, symptoms FROM diseases ORDER BY name')
    rows = [{'id': r['id'], 'name': r['name'], 'symptoms': json.loads(r['symptoms'])} for r in cur.fetchall()]
    conn.close()
    return rows


def add_rule(rule_id=None, rule_json=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS rules (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, rule_json TEXT)')
    if rule_id is None:
        # insert
        cur.execute('INSERT INTO rules (name, rule_json) VALUES (?, ?)', (rule_json.get('name', 'unnamed'), json.dumps(rule_json)))
        conn.commit()
        rid = cur.lastrowid
        conn.close()
        return rid
    else:
        # update by id
        cur.execute('UPDATE rules SET rule_json=? WHERE id=?', (json.dumps(rule_json), rule_id))
        conn.commit()
        conn.close()
        return rule_id


def list_rules():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS rules (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, rule_json TEXT)')
    cur.execute('SELECT id, name, rule_json FROM rules ORDER BY id')
    rows = []
    for r in cur.fetchall():
        try:
            rule = json.loads(r['rule_json'])
        except Exception:
            rule = None
        rows.append({'id': r['id'], 'name': r['name'], 'rule': rule})
    conn.close()
    return rows


def get_rule(rule_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, rule_json FROM rules WHERE id=?', (rule_id,))
    r = cur.fetchone()
    conn.close()
    if not r:
        return None
    try:
        rule = json.loads(r['rule_json'])
    except Exception:
        rule = None
    return {'id': r['id'], 'name': r['name'], 'rule': rule}


def delete_rule(rule_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM rules WHERE id=?', (rule_id,))
    conn.commit()
    conn.close()
    return True


def add_hospital(name, latitude, longitude, contact=None, ambulance_available=True, capacity_level='medium'):
    """Add a hospital to the database"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO hospitals (name, latitude, longitude, contact, ambulance_available, capacity_level) VALUES (?, ?, ?, ?, ?, ?)',
            (name, latitude, longitude, contact, 1 if ambulance_available else 0, capacity_level)
        )
        conn.commit()
        hid = cur.lastrowid
        conn.close()
        return hid
    except sqlite3.IntegrityError:
        # Update existing
        cur.execute(
            'UPDATE hospitals SET latitude=?, longitude=?, contact=?, ambulance_available=?, capacity_level=? WHERE name=?',
            (latitude, longitude, contact, 1 if ambulance_available else 0, capacity_level, name)
        )
        conn.commit()
        conn.close()
        return None


def list_hospitals():
    """List all hospitals"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, latitude, longitude, contact, ambulance_available, capacity_level FROM hospitals ORDER BY name')
    rows = [{
        'id': r['id'], 
        'name': r['name'], 
        'latitude': r['latitude'], 
        'longitude': r['longitude'],
        'contact': r['contact'],
        'ambulance_available': bool(r['ambulance_available']),
        'capacity_level': r['capacity_level']
    } for r in cur.fetchall()]
    conn.close()
    return rows


def find_nearest_hospitals(user_lat, user_lon, limit=5):
    """Find nearest hospitals using Haversine distance formula"""
    import math
    
    hospitals = list_hospitals()
    
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate distance in kilometers"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    for h in hospitals:
        h['distance_km'] = haversine_distance(user_lat, user_lon, h['latitude'], h['longitude'])
        # Estimate time: ambulance ~60km/h, matatu/uber ~40km/h in traffic
        h['eta_ambulance_min'] = int((h['distance_km'] / 60) * 60)
        h['eta_matatu_min'] = int((h['distance_km'] / 40) * 60)
    
    # Sort by distance
    hospitals.sort(key=lambda x: x['distance_km'])
    
    return hospitals[:limit]
