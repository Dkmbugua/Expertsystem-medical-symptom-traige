"""Seed symptoms, diseases, and comprehensive rules"""
import db
import json

# Initialize DB
db.init_db()

# Common symptoms with synonyms
symptoms = [
    {"name": "chest-pain", "synonyms": "chest pain,heart pain,cardiac pain,angina"},
    {"name": "fever", "synonyms": "high temperature,pyrexia,hot,feverish"},
    {"name": "headache", "synonyms": "head pain,migraine,cephalgia"},
    {"name": "cough", "synonyms": "coughing,persistent cough,dry cough"},
    {"name": "difficulty-breathing", "synonyms": "shortness of breath,dyspnea,breathless,cant breathe"},
    {"name": "abdominal-pain", "synonyms": "stomach pain,belly pain,tummy ache"},
    {"name": "vomiting", "synonyms": "throwing up,nausea,emesis,sick"},
    {"name": "diarrhea", "synonyms": "loose stool,runny stomach,gastroenteritis"},
    {"name": "stiff-neck", "synonyms": "neck stiffness,rigid neck,nuchal rigidity"},
    {"name": "confusion", "synonyms": "disoriented,altered mental state,confused"},
    {"name": "severe-bleeding", "synonyms": "hemorrhage,blood loss,bleeding heavily"},
    {"name": "unconscious", "synonyms": "passed out,fainted,unresponsive,collapsed"},
    {"name": "seizure", "synonyms": "convulsions,fits,epileptic fit"},
    {"name": "severe-burn", "synonyms": "burn injury,thermal injury"},
    {"name": "fracture", "synonyms": "broken bone,bone fracture"},
    {"name": "weakness", "synonyms": "fatigue,tiredness,lethargy"},
    {"name": "dizziness", "synonyms": "vertigo,lightheaded,spinning"},
    {"name": "rash", "synonyms": "skin rash,eruption,skin irritation"},
]

print("Adding symptoms...")
for s in symptoms:
    try:
        db.add_symptom(s["name"], s["synonyms"])
        print(f"✓ Added: {s['name']}")
    except Exception as e:
        print(f"✗ Failed to add {s['name']}: {e}")

# Diseases with symptom associations
diseases = [
    {
        "name": "Heart Attack",
        "symptoms": "chest-pain,difficulty-breathing,sweating,nausea",
    },
    {
        "name": "Severe Flu",
        "symptoms": "fever,headache,cough,weakness",
    },
    {
        "name": "Meningitis",
        "symptoms": "fever,headache,stiff-neck,confusion",
    },
    {
        "name": "Acute Abdomen",
        "symptoms": "abdominal-pain,vomiting,fever",
    },
    {
        "name": "Respiratory Distress",
        "symptoms": "difficulty-breathing,cough,weakness",
    },
]

print("\nAdding diseases...")
for d in diseases:
    try:
        db.add_disease(d["name"], d["symptoms"])
        print(f"✓ Added: {d['name']}")
    except Exception as e:
        print(f"✗ Failed to add {d['name']}: {e}")

# Comprehensive multi-symptom rules
rules = [
    {
        "id": "R1",
        "name": "Critical_Cardiac_Emergency",
        "description": "Chest pain in elderly - likely heart attack",
        "salience": 100,
        "conditions": [
            {"type": "age", "operator": ">", "value": 50},
            {"type": "symptom", "name": "chest-pain"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "RED"},
            {"type": "set_transport", "value": "ambulance"},
            {"type": "set_rationale", "value": "Possible heart attack - immediate emergency transport required"}
        ]
    },
    {
        "id": "R2",
        "name": "Meningitis_Concern",
        "description": "Fever with stiff neck and headache - meningitis concern",
        "salience": 95,
        "conditions": [
            {"type": "symptom", "name": "fever"},
            {"type": "symptom", "name": "stiff-neck"},
            {"type": "symptom", "name": "headache"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "RED"},
            {"type": "set_transport", "value": "ambulance"},
            {"type": "set_rationale", "value": "Suspected meningitis - urgent hospital evaluation required"}
        ]
    },
    {
        "id": "R3",
        "name": "Severe_Respiratory_Distress",
        "description": "Difficulty breathing requiring immediate care",
        "salience": 90,
        "conditions": [
            {"type": "symptom", "name": "difficulty-breathing"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "RED"},
            {"type": "set_transport", "value": "ambulance"},
            {"type": "set_rationale", "value": "Severe respiratory distress - oxygen support needed immediately"}
        ]
    },
    {
        "id": "R4",
        "name": "Trauma_Emergency",
        "description": "Severe bleeding or unconsciousness",
        "salience": 100,
        "conditions": [
            {"type": "symptom", "name": "severe-bleeding"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "RED"},
            {"type": "set_transport", "value": "ambulance"},
            {"type": "set_rationale", "value": "Severe trauma with bleeding - immediate ambulance required"}
        ]
    },
    {
        "id": "R5",
        "name": "Unconscious_Patient",
        "description": "Patient unconscious or unresponsive",
        "salience": 100,
        "conditions": [
            {"type": "symptom", "name": "unconscious"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "RED"},
            {"type": "set_transport", "value": "ambulance"},
            {"type": "set_rationale", "value": "Unconscious patient - immediate emergency care required"}
        ]
    },
    {
        "id": "R6",
        "name": "Acute_Abdomen",
        "description": "Severe abdominal pain with vomiting",
        "salience": 70,
        "conditions": [
            {"type": "symptom", "name": "abdominal-pain"},
            {"type": "symptom", "name": "vomiting"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "YELLOW"},
            {"type": "set_transport", "value": "matatu"},
            {"type": "set_rationale", "value": "Acute abdominal condition - hospital evaluation needed within hours"}
        ]
    },
    {
        "id": "R7",
        "name": "Severe_Flu",
        "description": "Fever with cough and headache - flu symptoms",
        "salience": 60,
        "conditions": [
            {"type": "symptom", "name": "fever"},
            {"type": "symptom", "name": "cough"},
            {"type": "symptom", "name": "headache"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "YELLOW"},
            {"type": "set_transport", "value": "matatu"},
            {"type": "set_rationale", "value": "Flu-like symptoms - medical consultation recommended today"}
        ]
    },
    {
        "id": "R8",
        "name": "Diabetic_With_Fever",
        "description": "Diabetic patient with fever needs monitoring",
        "salience": 65,
        "conditions": [
            {"type": "history", "name": "diabetes"},
            {"type": "symptom", "name": "fever"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "YELLOW"},
            {"type": "set_transport", "value": "matatu"},
            {"type": "set_rationale", "value": "Diabetic with infection risk - hospital visit recommended"}
        ]
    },
    {
        "id": "R9",
        "name": "Mild_Headache",
        "description": "Simple headache without other symptoms",
        "salience": 20,
        "conditions": [
            {"type": "symptom", "name": "headache"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "GREEN"},
            {"type": "set_transport", "value": "self-care"},
            {"type": "set_rationale", "value": "Mild headache - over-the-counter medication recommended, visit chemist if persists"}
        ]
    },
    {
        "id": "R10",
        "name": "Simple_Fever",
        "description": "Fever alone without complications",
        "salience": 25,
        "conditions": [
            {"type": "symptom", "name": "fever"}
        ],
        "actions": [
            {"type": "set_triage_level", "value": "GREEN"},
            {"type": "set_transport", "value": "self-care"},
            {"type": "set_rationale", "value": "Mild fever - rest and fluids recommended, visit chemist for medication"}
        ]
    }
]

print("\nAdding comprehensive rules...")
for r in rules:
    try:
        rule_json = {
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "salience": r["salience"],
            "conditions": r["conditions"],
            "actions": r["actions"]
        }
        db.add_rule(r["id"], json.dumps(rule_json))
        print(f"✓ Added: {r['id']} - {r['name']}")
    except Exception as e:
        print(f"✗ Failed to add {r['id']}: {e}")

print(f"\nTotal symptoms: {len(db.list_symptoms())}")
print(f"Total diseases: {len(db.list_diseases())}")
print(f"Total rules: {len(db.list_rules())}")
