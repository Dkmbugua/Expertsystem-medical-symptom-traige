# Medical Triage Expert System - Project Structure

## 🏗️ Architecture

```
Expertsystem-medical-symptom-traige/
├── app.py                      # Flask web server + REST API
├── db.py                       # SQLite database layer
├── location_service.py         # Geocoding + hospital finder
├── data.db                     # SQLite database
├── requirements.txt            # Python dependencies
├── start_server.sh            # Quick start script
├── README.md                   # Main documentation
│
├── knowledge_base/             # 🧠 EXPERT SYSTEM CORE
│   ├── rules.clp              # Production rules (forward-chaining)
│   └── templates.clp          # CLIPS fact templates
│
├── static/                     # Frontend
│   └── simple.html            # Main UI (React + Leaflet maps)
│
└── seed_*.py                   # Database seeding scripts
```

## 🤖 Expert System Components

### 1. Knowledge Base (`knowledge_base/rules.clp`)
- **70+ production rules** for symptom → diagnosis → triage
- Declarative knowledge representation
- Example rule:
  ```clips
  (defrule severe-chest-pain-emergency
    (patient (symptoms $? chest-pain $?))
    (patient (age ?age&:(>= ?age 40)))
    =>
    (assert (triage-level RED))
    (assert (recommendation "IMMEDIATE emergency care")))
  ```

### 2. Inference Engine (CLIPS)
- Forward-chaining reasoning
- Pattern matching on facts
- Runs in `app.py` via `CLIPS_ENV.run()`

### 3. Working Memory
- Patient facts (age, gender, symptoms, history)
- Inferred facts (triage-level, transport, recommendations)

### 4. User Interface
- `static/simple.html` - Web UI with:
  - Symptom selection
  - Location input (GPS or address)
  - Interactive maps (Leaflet + OpenStreetMap)
  - Triage results with hospital recommendations

## 🚀 Technology Stack

- **Expert System**: CLIPS (C Language Integrated Production System)
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: React (CDN), Tailwind CSS, Leaflet.js
- **Maps**: OpenStreetMap Nominatim, Overpass API
- **No API keys required** - 100% free services!

## 📊 Data Flow

1. User enters symptoms + location
2. Flask receives POST to `/triage`
3. App creates CLIPS facts from input
4. CLIPS inference engine fires rules
5. Results: triage level + transport + recommendations
6. Flask queries OpenStreetMap for nearby hospitals
7. Frontend displays results + interactive map

## 🎯 Expert System Characteristics

✅ **Separation of Knowledge and Control**
   - Rules in `.clp` files (knowledge)
   - CLIPS engine (control)

✅ **Declarative Programming**
   - Rules describe WHAT, not HOW
   - Pattern matching, not procedural

✅ **Inference**
   - Forward-chaining from facts to conclusions
   - Explanation via rule firing trace

✅ **Modularity**
   - Easy to add/modify rules
   - No code changes needed for new medical knowledge

## 🔧 Key Features

- **Live Hospital Data**: Fetches from OpenStreetMap (works anywhere!)
- **Caching**: Reduces API calls, improves performance
- **Fallback**: Multiple geocoding providers
- **Hybrid**: Local DB + live OSM data
- **Mobile-friendly**: Responsive design
- **Offline-capable**: Local SQLite database

## 📝 Files You Can Safely Delete

- Backup files (`.bak`)
- Temp files (`*_temp.clp`)
- Old logs (`*.log`)
- Extra markdown docs (keep only README.md)
- Duplicate HTML files

## 🚫 Files You Should NEVER Delete

- `app.py`, `db.py`, `location_service.py`
- `knowledge_base/rules.clp`, `knowledge_base/templates.clp`
- `static/simple.html`
- `data.db`, `requirements.txt`
- `README.md`
