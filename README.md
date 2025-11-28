# 🏥 Medical Triage Expert System

A production-ready CLIPS-based expert system for medical symptom triage with real-time hospital recommendations from OpenStreetMap.

## ✅ YES, This IS an Expert System

This project demonstrates a **proper CLIPS-based Expert System** with:

- **✓ Declarative Knowledge Base**: `knowledge_base/rules.clp` (20+ production rules)
- **✓ Inference Engine**: CLIPS forward-chaining engine
- **✓ Working Memory**: Patient facts (symptoms, age, history)
- **✓ Production Rules**: Pattern matching → actions
- **✓ Separation of Knowledge & Control**: Rules vs. inference mechanism

### Expert System Architecture

```
┌─────────────────────────────────────────────────┐
│  USER INPUT (symptoms, age, location)           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  WORKING MEMORY (CLIPS Facts)                   │
│  • (patient (age 55) (symptoms chest-pain))     │
│  • (history diabetes)                           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  INFERENCE ENGINE (CLIPS)                       │
│  • Pattern matching                             │
│  • Rule firing (forward-chaining)               │
│  • Conflict resolution                          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  KNOWLEDGE BASE (rules.clp)                     │
│  • (defrule emergency-chest-pain ...)           │
│  • (defrule fever-infection ...)                │
│  • 20+ production rules                         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  OUTPUT (triage level, transport, hospitals)    │
│  • RED/YELLOW/GREEN classification              │
│  • Ambulance/Matatu/Self-care recommendation    │
│  • Live hospital data from OpenStreetMap        │
└─────────────────────────────────────────────────┘
```

## 🌟 Key Features

### Expert System Features
- **Rule-Based Reasoning**: 20+ CLIPS production rules
- **Forward Chaining**: From symptoms → diagnosis → triage
- **Pattern Matching**: Complex multi-symptom analysis
- **Explainable AI**: Rule traces show reasoning path

### Application Features
- **Live Hospital Data**: Fetches from OpenStreetMap (works **anywhere** in Kenya!)
  - Works in Nakuru, Mombasa, Kisumu, any location
  - Real-time data (hospitals, clinics, pharmacies)
  - No static database limitations
- **Interactive Maps**: Leaflet + OpenStreetMap (no API key!)
- **Smart Geocoding**: 
  - Multi-provider fallback (Nominatim → Photon)
  - Caching for performance
  - Handles addresses OR coordinates
- **Responsive UI**: Mobile-friendly React interface
- **No API Keys Required**: 100% free services

## 🚀 Quick Start (Local Server)

```bash
# Option 1: Use the startup script
bash start_server.sh

# Option 2: Manual start
source venv/bin/activate
python app.py

# Open in browser
http://127.0.0.1:5000/static/simple.html
```

## � Project Structure (Clean)

## 📁 Project Structure (Clean)

```
Expertsystem-medical-symptom-traige/
├── app.py                      # Flask REST API + Web server
├── db.py                       # Database operations (SQLite)
├── location_service.py         # Geocoding + Hospital finder (OSM)
├── data.db                     # SQLite database
├── requirements.txt            # Python dependencies
├── start_server.sh            # Quick start script
├── README.md                   # This file
│
├── knowledge_base/             # 🧠 EXPERT SYSTEM CORE
│   ├── rules.clp              # Production rules (CLIPS)
│   └── templates.clp          # CLIPS templates
│
├── static/                     # Frontend
│   └── simple.html            # Main UI (React + Leaflet)
│
├── seed_symptoms_rules.py     # Database seeding
├── seed_hospitals.py          # Hospital seeding  
└── validate_hospital_data.py  # Data validator
```

**Note**: Redundant files removed by `cleanup_project.py`

## 📊 Current Capabilities

- **Symptoms**: 18+ with synonym matching
- **Production Rules**: 20+ CLIPS rules
- **Hospitals**: Dynamic fetching from OpenStreetMap
  - ✅ Works in Nairobi
  - ✅ Works in Nakuru  
  - ✅ Works in Mombasa
  - ✅ Works in Kisumu
  - ✅ Works **anywhere** in Kenya (and beyond!)
- **Maps**: Interactive with hospital markers + directions
- **Geocoding**: Cached, with provider fallbacks

## 🧪 Test Examples

### Test in Nakuru
```bash
curl -X POST http://127.0.0.1:5000/api/nearest-hospitals \
  -H "Content-Type: application/json" \
  -d '{"latitude": -0.3031, "longitude": 36.0800, "limit": 5}'
```

**Result**: Tazama Chemist, Bondeni Hospital, etc.

### Test in Mombasa
```bash
curl -X POST http://127.0.0.1:5000/api/nearest-hospitals \
  -H "Content-Type: application/json" \
  -d '{"latitude": -4.0435, "longitude": 39.6682, "limit": 3}'
```

**Result**: Aga Khan University Hospital, Coast General Hospital, etc.

### Test Triage
```bash
curl -X POST http://127.0.0.1:5000/triage \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 55,
    "gender": "male",
    "symptoms": "chest-pain, shortness-of-breath",
    "history": "diabetes",
    "mode_of_arrival": "walk-in"
  }'
```

**Result**: RED triage level → Ambulance required

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Expert System | **CLIPS** (C Language Integrated Production System) |
| Backend | **Flask** (Python REST API) |
| Database | **SQLite** (local storage) |
| Maps | **Leaflet.js** + OpenStreetMap tiles |
| Geocoding | **Nominatim** + Photon (free, no API key) |
| Hospital Data | **Overpass API** (OpenStreetMap live data) |
| Frontend | **React** (CDN), Tailwind CSS |
| Caching | In-memory (production: Redis) |

## 📝 API Endpoints

### Patient APIs
- `POST /triage` - Submit symptoms for triage
- `POST /api/nearest-hospitals` - Find nearest hospitals
- `POST /api/sha-cost-estimate` - Get SHA cost estimate
- `POST /api/notify-hospital` - Notify hospital

### Admin APIs
- `GET/POST /api/symptoms` - Manage symptoms
- `GET/POST /api/diseases` - Manage diseases
- `GET/POST/PUT/DELETE /api/rules` - Manage rules
- `POST /api/publish-rules` - Publish rules to CLIPS

## ✨ Accessibility Features

- ✅ Extra-large text (200-300% normal size)
- ✅ High contrast colors (WCAG AAA compliant)
- ✅ Keyboard navigation support
- ✅ Screen reader friendly
- ✅ Simple, clear language
- ✅ Visual indicators (emoji + color)
- ✅ No complex interactions required

## 🎯 Future Enhancements

- [ ] AI model integration (HuggingFace/OpenAI)
- [ ] Real-time hospital notifications (SMS/Email)
- [ ] Actual SHA (Kenya) API integration
- [ ] Patient location-based hospital search
- [ ] Multi-language support (Swahili)
- [ ] Authentication & authorization
- [ ] Mobile app version

## ⚠️ Important Notice

This system is a **TRIAGE HELPER TOOL**, not a medical diagnosis system. Always:
- Seek professional medical care when needed
- Call 999 for emergencies immediately
- Consult qualified healthcare providers
- Use this as a guide, not a replacement for medical advice

## 📄 License

Educational/Research Project

## 🤝 Contributing

This is an expert system project demonstrating CLIPS integration with modern web technologies.

## 📞 Support

For issues or questions, check:
- `HOW_TO_USE.md` - Patient instructions
- `ADMIN_GUIDE.md` - Admin instructions
- `SYSTEM_READY.md` - Complete documentation

---

**🎉 System is live at: http://127.0.0.1:5000/**
