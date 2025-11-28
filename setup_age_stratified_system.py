#!/usr/bin/env python3
"""
AGE-STRATIFIED MEDICAL TRIAGE EXPERT SYSTEM
============================================
Phase 1: Database Setup - Age Groups & Symptom Mapping

Creates:
- Age groups table (10 age ranges: 0-10, 11-20, ..., 91-100)
- Age-specific symptoms (50+ total)
- Symptom-to-age-group mappings
"""

import sqlite3
import json

def create_age_groups_table():
    """Create age_groups table with 10 clinically relevant age ranges"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Create age_groups table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS age_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            min_age INTEGER NOT NULL,
            max_age INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            UNIQUE(min_age, max_age)
        )
    """)
    
    age_groups = [
        (0, 10, 'Infant/Child', 'Newborns, infants, toddlers, and young children'),
        (11, 20, 'Adolescent', 'Teenagers and young adults'),
        (21, 30, 'Young Adult', 'Early adulthood'),
        (31, 40, 'Adult', 'Middle adulthood'),
        (41, 50, 'Middle Age', 'Prime middle age'),
        (51, 60, 'Mature Adult', 'Late middle age'),
        (61, 70, 'Senior', 'Early elderly'),
        (71, 80, 'Elderly', 'Advanced elderly'),
        (81, 90, 'Geriatric', 'Very elderly'),
        (91, 120, 'Advanced Geriatric', 'Oldest elderly'),
    ]
    
    for min_age, max_age, name, desc in age_groups:
        cursor.execute("""
            INSERT OR IGNORE INTO age_groups (min_age, max_age, name, description)
            VALUES (?, ?, ?, ?)
        """, (min_age, max_age, name, desc))
    
    conn.commit()
    
    # Verify
    cursor.execute("SELECT * FROM age_groups ORDER BY min_age")
    groups = cursor.fetchall()
    print("\n✅ Created Age Groups:")
    print("-" * 70)
    for g in groups:
        print(f"   {g[0]}. Ages {g[1]:3d}-{g[2]:3d}: {g[3]:20s} - {g[4]}")
    
    conn.close()
    return len(groups)


def add_age_appropriate_symptoms():
    """Add comprehensive age-appropriate symptoms"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Add age_groups column to symptoms if not exists
    cursor.execute("PRAGMA table_info(symptoms)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'age_groups' not in columns:
        cursor.execute("ALTER TABLE symptoms ADD COLUMN age_groups TEXT DEFAULT '[]'")
    
    # Age-specific symptoms (name, synonyms, applicable_age_group_ids)
    # Age group IDs: 1=0-10, 2=11-20, 3=21-30, 4=31-40, 5=41-50, 6=51-60, 7=61-70, 8=71-80, 9=81-90, 10=91+
    
    new_symptoms = [
        # PEDIATRIC (0-10) - Group 1
        ('teething-pain', ['teething', 'baby teeth', 'tooth pain baby'], [1]),
        ('diaper-rash', ['nappy rash', 'diaper irritation'], [1]),
        ('earache', ['ear pain', 'ear infection', 'otitis'], [1, 2]),
        ('crying-inconsolable', ['excessive crying', 'wont stop crying', 'fussy baby'], [1]),
        ('poor-feeding', ['not eating', 'refusing food', 'feeding problems'], [1]),
        ('lethargy', ['very sleepy', 'not responsive', 'limp baby'], [1]),
        ('wheezing', ['difficulty breathing with sound', 'whistling breath'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('runny-nose', ['nasal congestion', 'stuffy nose', 'cold'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        
        # ADOLESCENT (11-20) - Group 2
        ('acne', ['pimples', 'spots', 'skin breakout'], [2, 3]),
        ('menstrual-cramps', ['period pain', 'dysmenorrhea', 'menstrual pain'], [2, 3, 4, 5]),
        ('sports-injury', ['sprain', 'strain', 'athletic injury'], [2, 3, 4]),
        ('growing-pains', ['leg pain at night', 'growth aches'], [1, 2]),
        ('anxiety', ['nervousness', 'panic', 'worried'], [2, 3, 4, 5, 6, 7, 8, 9, 10]),
        
        # YOUNG ADULT (21-40) - Groups 3-4
        ('pregnancy-symptoms', ['morning sickness', 'pregnancy nausea'], [3, 4]),
        ('lower-back-pain', ['lumbar pain', 'back strain'], [3, 4, 5, 6, 7, 8, 9, 10]),
        ('migraine', ['severe headache', 'visual disturbance headache'], [2, 3, 4, 5, 6]),
        ('heartburn', ['acid reflux', 'GERD', 'indigestion'], [3, 4, 5, 6, 7, 8, 9, 10]),
        ('insomnia', ['cant sleep', 'sleep problems'], [2, 3, 4, 5, 6, 7, 8, 9, 10]),
        
        # MIDDLE AGE (41-60) - Groups 5-6
        ('joint-pain', ['arthritis pain', 'knee pain', 'hip pain'], [4, 5, 6, 7, 8, 9, 10]),
        ('high-blood-pressure-symptoms', ['hypertension symptoms', 'BP symptoms'], [5, 6, 7, 8, 9, 10]),
        ('chest-tightness', ['tight chest', 'chest pressure'], [4, 5, 6, 7, 8, 9, 10]),
        ('palpitations', ['heart racing', 'irregular heartbeat'], [3, 4, 5, 6, 7, 8, 9, 10]),
        ('vision-changes', ['blurry vision', 'vision loss'], [5, 6, 7, 8, 9, 10]),
        ('numbness', ['tingling', 'pins and needles', 'loss of sensation'], [4, 5, 6, 7, 8, 9, 10]),
        ('unexplained-weight-loss', ['losing weight without trying'], [4, 5, 6, 7, 8, 9, 10]),
        
        # ELDERLY (61+) - Groups 7-10
        ('confusion', ['disoriented', 'altered mental state', 'delirium'], [7, 8, 9, 10]),
        ('memory-problems', ['forgetfulness', 'dementia symptoms'], [7, 8, 9, 10]),
        ('falls', ['fell down', 'loss of balance', 'tripped'], [6, 7, 8, 9, 10]),
        ('urinary-incontinence', ['cant hold urine', 'bladder control loss'], [7, 8, 9, 10]),
        ('shortness-of-breath', ['breathless', 'SOB', 'dyspnea'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('swollen-legs', ['leg edema', 'ankle swelling', 'fluid retention'], [5, 6, 7, 8, 9, 10]),
        ('chest-pain-exertion', ['chest pain with activity', 'angina'], [5, 6, 7, 8, 9, 10]),
        
        # COMMON ACROSS AGES (with age variations)
        ('nausea', ['feeling sick', 'queasy'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('fatigue', ['tiredness', 'exhaustion', 'no energy'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('chills', ['shivering', 'cold sweats'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('sore-throat', ['throat pain', 'pharyngitis'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('back-pain', ['spine pain', 'back ache'], [2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('loss-of-appetite', ['not hungry', 'no appetite'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ]
    
    added = 0
    updated = 0
    
    for name, synonyms, age_group_ids in new_symptoms:
        # Check if symptom exists
        cursor.execute("SELECT id FROM symptoms WHERE name = ?", (name,))
        existing = cursor.fetchone()
        
        if existing:
            # Update age_groups for existing symptom
            cursor.execute(
                "UPDATE symptoms SET age_groups = ? WHERE name = ?",
                (json.dumps(age_group_ids), name)
            )
            updated += 1
            print(f"   ↻  Updated: {name} → ages {age_group_ids}")
        else:
            # Insert new symptom with synonyms stored as JSON
            cursor.execute(
                "INSERT INTO symptoms (name, synonyms, age_groups) VALUES (?, ?, ?)",
                (name, json.dumps(synonyms), json.dumps(age_group_ids))
            )
            
            added += 1
            print(f"   ✅ Added: {name} → ages {age_group_ids}")
    
    # Update existing symptoms with appropriate age groups
    existing_mappings = [
        ('fever', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('headache', [2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('cough', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('vomiting', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('dizziness', [2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('abdominal-pain', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('rash', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('weakness', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('chest-pain', [3, 4, 5, 6, 7, 8, 9, 10]),  # Rare in children
        ('difficulty-breathing', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('stiff-neck', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('seizure', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('severe-bleeding', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('severe-burn', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('unconscious', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ('fracture', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ]
    
    for name, age_groups in existing_mappings:
        cursor.execute(
            "UPDATE symptoms SET age_groups = ? WHERE name = ?",
            (json.dumps(age_groups), name)
        )
    
    conn.commit()
    
    # Summary
    cursor.execute("SELECT COUNT(*) FROM symptoms")
    total = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n✅ Symptom Database Updated:")
    print(f"   - {added} new symptoms added")
    print(f"   - {updated} symptoms updated")
    print(f"   - {total} total symptoms in system")
    
    return added, updated, total


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 AGE-STRATIFIED EXPERT SYSTEM SETUP - PHASE 1")
    print("="*70)
    
    print("\n📊 Step 1: Creating Age Groups Table...")
    print("-"*70)
    num_groups = create_age_groups_table()
    
    print("\n📊 Step 2: Adding Age-Specific Symptoms...")
    print("-"*70)
    added, updated, total = add_age_appropriate_symptoms()
    
    print("\n" + "="*70)
    print("✅ PHASE 1 COMPLETE!")
    print("="*70)
    print(f"   ✓ {num_groups} age groups created")
    print(f"   ✓ {total} symptoms available")
    print(f"   ✓ Age-based filtering enabled")
    print("\n📋 Next: Phase 2 - Write 100+ age-stratified CLIPS rules")
    print("="*70 + "\n")
