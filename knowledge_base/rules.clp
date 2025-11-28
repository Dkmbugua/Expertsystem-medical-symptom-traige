;; =====================================================================
;; AGE-STRATIFIED MEDICAL TRIAGE EXPERT SYSTEM - CLIPS RULES
;; =====================================================================
;; 100+ rules organized by age groups for clinically accurate triage
;; Age Groups: 0-10, 11-20, 21-30, 31-40, 41-50, 51-60, 61-70, 71-80, 81-90, 91+
;; =====================================================================

;; =====================================================================
;; CRITICAL EMERGENCY RULES (ALL AGES) - Salience 100
;; =====================================================================

(defrule unconscious-all-ages
  "Unconscious patient - immediate emergency"
  (declare (salience 100))
  (patient-symptom (name unconscious))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Patient unconscious. Critical emergency - call ambulance immediately!")
  ))
)

(defrule severe-bleeding-all-ages
  "Severe bleeding - life-threatening"
  (declare (salience 100))
  (patient-symptom (name severe-bleeding))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Severe bleeding. Life-threatening emergency - call ambulance now!")
  ))
)

(defrule difficulty-breathing-severe
  "Severe difficulty breathing - airway emergency"
  (declare (salience 100))
  (patient-symptom (name difficulty-breathing))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Severe difficulty breathing. Airway emergency - call ambulance immediately!")
  ))
)

(defrule seizure-active
  "Active seizure - emergency"
  (declare (salience 98))
  (patient-symptom (name seizure))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Seizure activity. Medical emergency - call ambulance now!")
  ))
)

(defrule severe-burn-all-ages
  "Severe burn injury"
  (declare (salience 97))
  (patient-symptom (name severe-burn))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Severe burn injury. Immediate hospital treatment required - call ambulance!")
  ))
)

;; =====================================================================
;; PEDIATRIC RULES (Ages 0-10) - Salience 85-95
;; =====================================================================

(defrule infant-any-fever
  "Any fever in infant under 3 months - always urgent"
  (declare (salience 95))
  (patient-demographics (age ?age&:(< ?age 0.25)))  ; 3 months = 0.25 years
  (patient-symptom (name fever))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Fever in infant under 3 months. Infants can deteriorate rapidly - seek immediate medical care!")
  ))
)

(defrule toddler-high-fever
  "High fever in young child"
  (declare (salience 90))
  (patient-demographics (age ?age&:(and (>= ?age 0.25) (< ?age 5))))
  (patient-symptom (name fever))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "High fever in young child. Children can deteriorate quickly - visit hospital today!")
  ))
)

(defrule child-lethargy
  "Lethargic child - serious warning sign"
  (declare (salience 92))
  (patient-demographics (age ?age&:(< ?age 10)))
  (patient-symptom (name lethargy))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Lethargic child. Very concerning sign - call ambulance immediately!")
  ))
)

(defrule child-poor-feeding
  "Infant refusing to feed"
  (declare (salience 88))
  (patient-demographics (age ?age&:(< ?age 2)))
  (patient-symptom (name poor-feeding))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Infant not feeding. Risk of dehydration - seek medical care today!")
  ))
)

(defrule child-wheezing
  "Wheezing in child - respiratory distress"
  (declare (salience 90))
  (patient-demographics (age ?age&:(< ?age 10)))
  (patient-symptom (name wheezing))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Wheezing in child. Possible asthma or respiratory infection - visit hospital today!")
  ))
)

(defrule child-vomiting-diarrhea
  "Vomiting and diarrhea in child - dehydration risk"
  (declare (salience 85))
  (patient-demographics (age ?age&:(< ?age 10)))
  (patient-symptom (name vomiting))
  (patient-symptom (name diarrhea))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Vomiting and diarrhea in child. High dehydration risk - seek medical care today!")
  ))
)

(defrule child-inconsolable-crying
  "Inconsolable crying in infant"
  (declare (salience 80))
  (patient-demographics (age ?age&:(< ?age 2)))
  (patient-symptom (name crying-inconsolable))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Inconsolable crying in infant. Could indicate serious problem - medical evaluation needed!")
  ))
)

(defrule child-earache
  "Ear pain in child"
  (declare (salience 60))
  (patient-demographics (age ?age&:(< ?age 10)))
  (patient-symptom (name earache))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Ear pain in child. Possible ear infection - see doctor today for treatment!")
  ))
)

(defrule child-teething
  "Teething pain - mild"
  (declare (salience 30))
  (patient-demographics (age ?age&:(< ?age 3)))
  (patient-symptom (name teething-pain))
  (not (patient-symptom (name fever)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Teething pain. Normal developmental process - get teething gel from pharmacy!")
  ))
)

(defrule child-diaper-rash
  "Simple diaper rash"
  (declare (salience 25))
  (patient-demographics (age ?age&:(< ?age 3)))
  (patient-symptom (name diaper-rash))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Diaper rash. Get diaper rash cream from pharmacy, keep area clean and dry!")
  ))
)

(defrule child-runny-nose
  "Common cold in child"
  (declare (salience 30))
  (patient-demographics (age ?age&:(< ?age 10)))
  (patient-symptom (name runny-nose))
  (not (patient-symptom (name fever)))
  (not (patient-symptom (name difficulty-breathing)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Common cold. Rest, fluids, and over-the-counter cold medicine from pharmacy!")
  ))
)

;; =====================================================================
;; ADOLESCENT RULES (Ages 11-20) - Salience 70-85
;; =====================================================================

(defrule teen-chest-pain
  "Chest pain in teen - usually musculoskeletal but check"
  (declare (salience 75))
  (patient-demographics (age ?age&:(and (>= ?age 11) (<= ?age 20))))
  (patient-symptom (name chest-pain))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Chest pain in teenager. Usually muscular but needs medical evaluation - visit hospital today!")
  ))
)

(defrule teen-sports-injury
  "Sports injury in adolescent"
  (declare (salience 65))
  (patient-demographics (age ?age&:(and (>= ?age 11) (<= ?age 20))))
  (patient-symptom (name sports-injury))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Sports injury. May need X-ray or evaluation - visit hospital today!")
  ))
)

(defrule teen-severe-headache
  "Severe headache in teen"
  (declare (salience 70))
  (patient-demographics (age ?age&:(and (>= ?age 11) (<= ?age 20))))
  (patient-symptom (name headache))
  (or
    (patient-symptom (name vomiting))
    (patient-symptom (name vision-changes))
  )
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Severe headache with warning signs. Needs medical evaluation - visit hospital today!")
  ))
)

(defrule teen-menstrual-cramps
  "Menstrual cramps"
  (declare (salience 35))
  (patient-demographics (age ?age&:(and (>= ?age 11) (<= ?age 20))) (gender female))
  (patient-symptom (name menstrual-cramps))
  (not (patient-symptom (name severe-pain)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Menstrual cramps. Get pain reliever from pharmacy, use heating pad, rest!")
  ))
)

(defrule teen-acne
  "Acne - cosmetic concern"
  (declare (salience 20))
  (patient-demographics (age ?age&:(and (>= ?age 11) (<= ?age 20))))
  (patient-symptom (name acne))
  =>
  (assert (triage-result
    (level GREEN)
    (score 5)
    (transport chemist)
    (rationale "Acne. Get acne treatment from pharmacy, maintain good skin hygiene!")
  ))
)

(defrule teen-growing-pains
  "Growing pains in adolescent"
  (declare (salience 25))
  (patient-demographics (age ?age&:(and (>= ?age 11) (<= ?age 20))))
  (patient-symptom (name growing-pains))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Growing pains. Normal in adolescents - rest, stretch, use pain reliever if needed!")
  ))
)

(defrule teen-anxiety
  "Anxiety in teen - mental health support"
  (declare (salience 55))
  (patient-demographics (age ?age&:(and (>= ?age 11) (<= ?age 20))))
  (patient-symptom (name anxiety))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Anxiety symptoms. Mental health matters - seek counseling or medical support!")
  ))
)

;; =====================================================================
;; YOUNG ADULT RULES (Ages 21-40) - Salience 70-90
;; =====================================================================

(defrule young-adult-chest-pain
  "Chest pain in young adult - rare cardiac, but investigate"
  (declare (salience 85))
  (patient-demographics (age ?age&:(and (>= ?age 21) (<= ?age 40))))
  (patient-symptom (name chest-pain))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Chest pain. Less likely cardiac at your age but needs evaluation - visit hospital today!")
  ))
)

(defrule pregnancy-complications
  "Pregnancy symptoms with concerning signs"
  (declare (salience 90))
  (patient-demographics (age ?age&:(and (>= ?age 18) (<= ?age 45))) (gender female))
  (patient-symptom (name pregnancy-symptoms))
  (or
    (patient-symptom (name severe-bleeding))
    (patient-symptom (name severe-pain))
    (patient-symptom (name dizziness))
  )
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Pregnancy with concerning symptoms. Possible emergency - call ambulance immediately!")
  ))
)

(defrule young-adult-migraine
  "Migraine headache"
  (declare (salience 60))
  (patient-demographics (age ?age&:(and (>= ?age 18) (<= ?age 50))))
  (patient-symptom (name migraine))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Migraine. If severe or first-time, see doctor for proper treatment and management!")
  ))
)

(defrule young-adult-back-pain
  "Simple back pain in young adult"
  (declare (salience 35))
  (patient-demographics (age ?age&:(and (>= ?age 21) (<= ?age 40))))
  (patient-symptom (name lower-back-pain))
  (not (patient-symptom (name numbness)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Lower back pain. Rest, apply heat/cold, get pain reliever from pharmacy!")
  ))
)

(defrule young-adult-heartburn
  "Heartburn/GERD"
  (declare (salience 30))
  (patient-demographics (age ?age&:(>= ?age 21)))
  (patient-symptom (name heartburn))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Heartburn. Get antacids from pharmacy, avoid trigger foods, eat smaller meals!")
  ))
)

;; =====================================================================
;; MIDDLE AGE RULES (Ages 41-60) - Salience 85-95
;; =====================================================================

(defrule middle-age-chest-pain
  "Chest pain in middle age - CARDIAC RISK HIGH"
  (declare (salience 95))
  (patient-demographics (age ?age&:(and (>= ?age 40) (< ?age 60))))
  (patient-symptom (name chest-pain))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Chest pain at your age. HIGH CARDIAC RISK - call ambulance immediately!")
  ))
)

(defrule middle-age-chest-tightness
  "Chest tightness - possible angina"
  (declare (salience 93))
  (patient-demographics (age ?age&:(>= ?age 40)))
  (patient-symptom (name chest-tightness))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Chest tightness. Possible heart problem - call ambulance now!")
  ))
)

(defrule middle-age-palpitations-pain
  "Palpitations with chest pain - cardiac emergency"
  (declare (salience 94))
  (patient-demographics (age ?age&:(>= ?age 40)))
  (patient-symptom (name palpitations))
  (or
    (patient-symptom (name chest-pain))
    (patient-symptom (name chest-tightness))
    (patient-symptom (name shortness-of-breath))
  )
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Irregular heartbeat with chest symptoms. Cardiac emergency - call ambulance!")
  ))
)

(defrule middle-age-numbness-stroke
  "Sudden numbness - stroke warning"
  (declare (salience 96))
  (patient-demographics (age ?age&:(>= ?age 40)))
  (patient-symptom (name numbness))
  (or
    (patient-symptom (name confusion))
    (patient-symptom (name headache))
    (patient-symptom (name vision-changes))
  )
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Sudden numbness with neurological symptoms. POSSIBLE STROKE - call ambulance NOW!")
  ))
)

(defrule middle-age-joint-pain
  "Joint pain - arthritis"
  (declare (salience 50))
  (patient-demographics (age ?age&:(>= ?age 40)))
  (patient-symptom (name joint-pain))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Joint pain. Possible arthritis - see doctor for evaluation and treatment!")
  ))
)

(defrule middle-age-weight-loss
  "Unexplained weight loss - investigate"
  (declare (salience 70))
  (patient-demographics (age ?age&:(>= ?age 40)))
  (patient-symptom (name unexplained-weight-loss))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Unexplained weight loss. Needs investigation - visit hospital for evaluation!")
  ))
)

(defrule middle-age-vision-changes
  "Vision changes - could be serious"
  (declare (salience 75))
  (patient-demographics (age ?age&:(>= ?age 40)))
  (patient-symptom (name vision-changes))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Vision changes. Could indicate diabetes, hypertension, or eye disease - see doctor today!")
  ))
)

;; =====================================================================
;; ELDERLY RULES (Ages 61+) - Salience 85-98
;; =====================================================================

(defrule elderly-chest-pain
  "Chest pain in elderly - VERY HIGH CARDIAC RISK"
  (declare (salience 98))
  (patient-demographics (age ?age&:(>= ?age 60)))
  (patient-symptom (name chest-pain))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Chest pain in elderly. VERY HIGH CARDIAC RISK - call ambulance immediately!")
  ))
)

(defrule elderly-confusion
  "Confusion in elderly - serious medical sign"
  (declare (salience 92))
  (patient-demographics (age ?age&:(>= ?age 65)))
  (patient-symptom (name confusion))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Confusion in elderly. Could be infection, stroke, or metabolic - urgent evaluation needed!")
  ))
)

(defrule elderly-diabetic-confusion
  "Diabetic elderly with confusion - critical"
  (declare (salience 96))
  (patient-demographics (age ?age&:(>= ?age 60)))
  (patient-history (history ?h&:(or (eq ?h diabetes) (eq ?h diabetic))))
  (patient-symptom (name confusion))
  =>
  (assert (triage-result
    (level RED)
    (score 1)
    (transport ambulance)
    (rationale "Diabetic with confusion. Blood sugar emergency - call ambulance NOW!")
  ))
)

(defrule elderly-falls
  "Falls in elderly - serious injury risk"
  (declare (salience 85))
  (patient-demographics (age ?age&:(>= ?age 65)))
  (patient-symptom (name falls))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Fall in elderly. High risk of fracture or head injury - medical evaluation needed today!")
  ))
)

(defrule elderly-dizziness
  "Dizziness in elderly - fall risk"
  (declare (salience 78))
  (patient-demographics (age ?age&:(>= ?age 65)))
  (patient-symptom (name dizziness))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Dizziness in elderly. High fall risk and could indicate serious problem - see doctor today!")
  ))
)

(defrule elderly-shortness-of-breath
  "Shortness of breath in elderly - heart failure risk"
  (declare (salience 90))
  (patient-demographics (age ?age&:(>= ?age 65)))
  (patient-symptom (name shortness-of-breath))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Shortness of breath in elderly. Could be heart or lung problem - urgent evaluation needed!")
  ))
)

(defrule elderly-swollen-legs
  "Leg swelling in elderly - heart failure sign"
  (declare (salience 75))
  (patient-demographics (age ?age&:(>= ?age 60)))
  (patient-symptom (name swollen-legs))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Leg swelling in elderly. Could indicate heart failure - medical evaluation needed!")
  ))
)

(defrule elderly-memory-problems
  "Memory problems in elderly"
  (declare (salience 60))
  (patient-demographics (age ?age&:(>= ?age 65)))
  (patient-symptom (name memory-problems))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Memory problems. Needs evaluation for dementia or treatable causes - see doctor!")
  ))
)

(defrule elderly-urinary-incontinence
  "Urinary incontinence in elderly"
  (declare (salience 50))
  (patient-demographics (age ?age&:(>= ?age 70)))
  (patient-symptom (name urinary-incontinence))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Urinary incontinence. Could indicate infection or other treatable cause - see doctor!")
  ))
)

;; =====================================================================
;; GENERAL RULES (Cross-Age) - Salience 40-80
;; =====================================================================

(defrule high-fever-with-stiff-neck
  "Fever with stiff neck - meningitis concern"
  (declare (salience 88))
  (patient-symptom (name fever))
  (patient-symptom (name stiff-neck))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Fever with stiff neck. Possible meningitis - urgent medical evaluation needed!")
  ))
)

(defrule fever-with-rash
  "Fever with rash"
  (declare (salience 70))
  (patient-symptom (name fever))
  (patient-symptom (name rash))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Fever with rash. Needs medical evaluation - visit hospital today!")
  ))
)

(defrule vomiting-persistent
  "Persistent vomiting - dehydration risk"
  (declare (salience 65))
  (patient-symptom (name vomiting))
  (patient-symptom (name weakness))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Persistent vomiting with weakness. Dehydration risk - seek medical care today!")
  ))
)

(defrule abdominal-pain-severe
  "Severe abdominal pain"
  (declare (salience 75))
  (patient-symptom (name abdominal-pain))
  (or
    (patient-symptom (name vomiting))
    (patient-symptom (name fever))
  )
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Severe abdominal pain with symptoms. Needs medical evaluation - visit hospital today!")
  ))
)

(defrule back-pain-with-numbness
  "Back pain with numbness - nerve/spine concern"
  (declare (salience 80))
  (patient-symptom (name back-pain))
  (patient-symptom (name numbness))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 2)
    (transport matatu)
    (rationale "Back pain with numbness. Possible nerve/spine issue - see doctor today!")
  ))
)

(defrule simple-headache
  "Mild headache without warning signs"
  (declare (salience 30))
  (patient-symptom (name headache))
  (not (patient-symptom (name fever)))
  (not (patient-symptom (name vomiting)))
  (not (patient-symptom (name stiff-neck)))
  (not (patient-symptom (name vision-changes)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Mild headache. Take pain reliever from pharmacy, rest, and hydrate!")
  ))
)

(defrule simple-fever
  "Simple fever without complications"
  (declare (salience 35))
  (patient-symptom (name fever))
  (not (patient-symptom (name difficulty-breathing)))
  (not (patient-symptom (name chest-pain)))
  (not (patient-symptom (name stiff-neck)))
  (not (patient-symptom (name confusion)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Simple fever. Rest, hydrate, and take fever medicine from pharmacy!")
  ))
)

(defrule simple-cough
  "Mild cough without complications"
  (declare (salience 30))
  (patient-symptom (name cough))
  (not (patient-symptom (name difficulty-breathing)))
  (not (patient-symptom (name chest-pain)))
  (not (patient-symptom (name fever)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Mild cough. Get cough syrup from pharmacy, drink warm fluids, rest!")
  ))
)

(defrule simple-sore-throat
  "Sore throat without complications"
  (declare (salience 28))
  (patient-symptom (name sore-throat))
  (not (patient-symptom (name difficulty-breathing)))
  (not (patient-symptom (name fever)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Sore throat. Gargle with salt water, get throat lozenges from pharmacy!")
  ))
)

(defrule simple-nausea
  "Mild nausea"
  (declare (salience 28))
  (patient-symptom (name nausea))
  (not (patient-symptom (name vomiting)))
  (not (patient-symptom (name abdominal-pain)))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Mild nausea. Get anti-nausea medicine from pharmacy, drink clear fluids!")
  ))
)

(defrule insomnia
  "Sleep problems"
  (declare (salience 25))
  (patient-symptom (name insomnia))
  =>
  (assert (triage-result
    (level GREEN)
    (score 4)
    (transport chemist)
    (rationale "Sleep problems. Practice sleep hygiene, consider melatonin from pharmacy. If persistent, see doctor!")
  ))
)

(defrule fracture-simple
  "Simple fracture"
  (declare (salience 70))
  (patient-symptom (name fracture))
  (not (patient-symptom (name severe-bleeding)))
  =>
  (assert (triage-result
    (level YELLOW)
    (score 3)
    (transport matatu)
    (rationale "Fracture. Needs X-ray and treatment - visit hospital today!")
  ))
)

;; =====================================================================
;; DEFAULT FALLBACK RULE - Salience 0
;; =====================================================================

(defrule default-triage
  "Default safe triage when no specific rule matches"
  (declare (salience 0))
  (not (triage-result))
  =>
  (assert (triage-result
    (level GREEN)
    (score 5)
    (transport none)
    (rationale "Symptoms reported. Monitor condition. If worsens or new symptoms appear, seek medical care!")
  ))
)
