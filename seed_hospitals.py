"""Seed Kenya hospitals into the database"""
import db

# Initialize DB
db.init_db()

# Sample hospitals in Nairobi and surrounding areas
hospitals = [
    {
        "name": "Kenyatta National Hospital",
        "latitude": -1.3006,
        "longitude": 36.8070,
        "contact": "+254-20-2726300",
        "ambulance_available": True,
        "capacity_level": "high"
    },
    {
        "name": "Nairobi Hospital",
        "latitude": -1.2884,
        "longitude": 36.8105,
        "contact": "+254-20-2845000",
        "ambulance_available": True,
        "capacity_level": "high"
    },
    {
        "name": "Aga Khan University Hospital",
        "latitude": -1.2674,
        "longitude": 36.8090,
        "contact": "+254-20-3662000",
        "ambulance_available": True,
        "capacity_level": "high"
    },
    {
        "name": "MP Shah Hospital",
        "latitude": -1.2722,
        "longitude": 36.8067,
        "contact": "+254-20-4275000",
        "ambulance_available": True,
        "capacity_level": "medium"
    },
    {
        "name": "Gertrude's Children's Hospital",
        "latitude": -1.2625,
        "longitude": 36.7955,
        "contact": "+254-20-7202000",
        "ambulance_available": True,
        "capacity_level": "medium"
    },
    {
        "name": "Mama Lucy Kibaki Hospital",
        "latitude": -1.3196,
        "longitude": 36.8927,
        "contact": "+254-20-8003000",
        "ambulance_available": True,
        "capacity_level": "medium"
    },
    {
        "name": "Mbagathi District Hospital",
        "latitude": -1.3173,
        "longitude": 36.7466,
        "contact": "+254-20-6003100",
        "ambulance_available": True,
        "capacity_level": "medium"
    },
    {
        "name": "Karen Hospital",
        "latitude": -1.3228,
        "longitude": 36.7021,
        "contact": "+254-719-098000",
        "ambulance_available": True,
        "capacity_level": "high"
    },
    {
        "name": "Coptic Hospital",
        "latitude": -1.3047,
        "longitude": 36.7640,
        "contact": "+254-20-6001000",
        "ambulance_available": True,
        "capacity_level": "medium"
    },
    {
        "name": "Meridian Hospital",
        "latitude": -1.2524,
        "longitude": 36.7707,
        "contact": "+254-709-860000",
        "ambulance_available": True,
        "capacity_level": "medium"
    }
]

print("Adding hospitals to database...")
for h in hospitals:
    try:
        db.add_hospital(**h)
        print(f"✓ Added: {h['name']}")
    except Exception as e:
        print(f"✗ Failed to add {h['name']}: {e}")

print(f"\nTotal hospitals in database: {len(db.list_hospitals())}")
