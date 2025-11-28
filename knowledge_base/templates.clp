; MSTS - Knowledge Base Templates (Derived from Assignment 3 Design)

(deftemplate patient-demographics
;; Used to capture patient's baseline information
	(slot age (type INTEGER))
	(slot gender (type SYMBOL) (allowed-symbols male female other))
)

(deftemplate patient-history
;; High-Risk Markers for Hidden Critical Rules
	(slot history (type SYMBOL))
	(slot mode-of-arrival (type SYMBOL) (allowed-symbols ambulance walk-in))
)

(deftemplate triage-result
;; The final conclusion of the expert system
	(slot level (type SYMBOL) (allowed-symbols RED YELLOW GREEN))
	(slot score (type INTEGER)) ; ESI Level 1-5 or similar internal score
	(slot transport (type SYMBOL) (allowed-symbols ambulance matatu chemist none))
	(slot rationale (type STRING))
)


(deftemplate patient-symptom
  ;; One symptom fact per reported symptom
  (slot name (type SYMBOL)) ; symptom name as a symbol (e.g., chest-pain)
)
