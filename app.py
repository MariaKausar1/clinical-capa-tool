import streamlit as st

st.set_page_config(page_title="Toxidrome CDS", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR ENTERPRISE UI (High Visibility Cyan) ---
st.markdown("""
    <style>
    .critical-alert { background-color: #721c24; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #dc3545; }
    .urgent-alert { background-color: #856404; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #ffc107; }
    .stable-alert { background-color: #155724; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #28a745; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #00BFFF; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 1.5rem; margin-bottom: 0.5rem; border-bottom: 1px solid #444; padding-bottom: 4px; }
    .diagnostic-card { border: 1px solid #dee2e6; border-radius: 6px; padding: 16px; background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

# --- 1. THE CLINICAL DATABASE ---
TOXICOLOGY_DB = {
    "Opioid": {
        "hallmarks": ["Pinpoint pupils", "Respiratory depression", "CNS depression", "Bradycardia"],
        "alternatives": ["Sedative-hypnotic exposure", "Hypoglycemia", "Primary intracranial event"],
        "antidote": "Naloxone",
        "dose": "0.04 - 0.4 mg IV (titrate to effect).",
        "goal": "Adequate spontaneous ventilation (not full arousal).",
        "warnings": "Observe for re-sedation (naloxone half-life is ~30-81 mins)."
    },
    "Anticholinergic": {
        "hallmarks": ["Dilated pupils", "Dry / Flushed skin", "Tachycardia", "Agitation / Delirium", "Decreased / Absent bowel sounds"],
        "alternatives": ["Sepsis / Infection", "Thyroid storm", "Alcohol withdrawal"],
        "antidote": "Supportive Care & Physostigmine",
        "dose": "Physostigmine 0.5 - 2 mg IV over 5 mins (for severe delirium).",
        "goal": "Control severe central nervous system agitation.",
        "warnings": "ABSOLUTE CONTRAINDICATION: Do NOT administer physostigmine if QRS > 100ms or TCA overdose is suspected."
    },
    "Sympathomimetic": {
        "hallmarks": ["Dilated pupils", "Diaphoresis (Sweaty)", "Tachycardia", "Agitation / Delirium", "Hyperthermia (>39C)"],
        "alternatives": ["Serotonin Syndrome", "Thyroid storm", "Alcohol/Benzo withdrawal"],
        "antidote": "Benzodiazepines",
        "dose": "Diazepam 5-10 mg IV or Lorazepam 1-2 mg IV.",
        "goal": "Reduce sympathetic outflow and prevent seizures/hyperthermia.",
        "warnings": "ABSOLUTE CONTRAINDICATION: Beta-blockers (risk of unopposed alpha stimulation)."
    },
    "Cholinergic": {
        "hallmarks": ["Pinpoint pupils", "Diaphoresis (Sweaty)", "Hyperactive bowel sounds", "Tachypnea (>20)"],
        "alternatives": ["Pontine hemorrhage", "Opiate co-ingestion"],
        "antidote": "Atropine & Pralidoxime (2-PAM)",
        "dose": "Atropine 2 - 5 mg IV. Double every 5 minutes.",
        "goal": "Titrate Atropine specifically to the clearing of respiratory secretions.",
        "warnings": "Do not stop atropine based on heart rate or pupil size."
    },
    "Serotonin Syndrome": {
        "hallmarks": ["Agitation / Delirium", "Tachycardia", "Diaphoresis (Sweaty)", "Hyperactive bowel sounds", "Hyperthermia (>39C)"],
        "alternatives": ["Sympathomimetic toxicity", "Neuroleptic Malignant Syndrome (NMS)"],
        "antidote": "Cyproheptadine & Benzodiazepines",
        "dose": "Cyproheptadine 12 mg PO/NG initially, then 2 mg q2h if symptomatic.",
        "goal": "Control agitation, hyperthermia, and reduce muscle rigidity.",
        "warnings": "Do NOT use physical restraints. Avoid antipyretics."
    },
    "Tricyclic Antidepressant (TCA)": {
        "hallmarks": ["Agitation / Delirium", "Tachycardia", "Dilated pupils", "Dry / Flushed skin", "Widened QRS (>100ms)"],
        "alternatives": ["Anticholinergic toxicity", "Cocaine/Amphetamine overdose"],
        "antidote": "Sodium Bicarbonate",
        "dose": "1-2 mEq/kg IV bolus, followed by continuous IV infusion.",
        "goal": "Narrow QRS interval to <100ms and correct hypotension.",
        "warnings": "Avoid physostigmine. Monitor closely for refractory ventricular dysrhythmias."
    },
    "Sedative-Hypnotic": {
        "hallmarks": ["Depressed / Coma", "Normal pupils"],
        "alternatives": ["Opioid toxicity", "Ethanol intoxication", "Hypoglycemia"],
        "antidote": "Supportive Care",
        "dose": "Airway management and ventilatory support.",
        "goal": "Maintain adequate oxygenation and ventilation.",
        "warnings": "Flumazenil is generally contraindicated in undifferentiated overdoses due to risk of intractable seizures."
    }
}

# --- 2. LEFT PANEL: TRIAGE ASSESSMENT ---
with st.sidebar:
    st.markdown("<div style='font-size: 1.5rem; font-weight: bold; color: #00BFFF;'>Triage Assessment</div>", unsafe_allow_html=True)
    st.caption("Input real-time patient findings.")
    
    st.markdown("<div class='section-header'>CNS Findings</div>", unsafe_allow_html=True)
    pupils = st.selectbox("Pupil Examination", ["Normal", "Pinpoint", "Dilated"])
    mental_status = st.selectbox("Mental Status", ["Normal", "Depressed / Coma", "Agitated / Delirium"])
    
    st.markdown("<div class='section-header'>Hemodynamics & Airway</div>", unsafe_allow_html=True)
    respirations = st.selectbox("Respiratory Rate", ["Normal", "Depressed (<12)", "Tachypnea (>20)"])
    heart_rate = st.selectbox("Heart Rate", ["Normal", "Bradycardia (<60)", "Tachycardia (>100)"])
    
    st.markdown("<div class='section-header'>Autonomic Signs</div>", unsafe_allow_html=True)
    skin = st.selectbox("Skin / Mucous Membranes", ["Normal", "Dry / Flushed", "Diaphoretic (Sweaty)"])
    bowel_sounds = st.selectbox("Bowel Sounds", ["Normal", "Decreased / Absent", "Hyperactive"])
    
    st.markdown("<div class='section-header'>Ancillary Data</div>", unsafe_allow_html=True)
    ecg_qrs = st.selectbox("ECG QRS Interval", ["Normal (<100ms)", "Widened (>100ms)"])
    temperature = st.selectbox("Core Temperature", ["Normal", "Hyperthermia (>39C)"])
    
    if st.button("Clear Patient Data", use_container_width=True):
        st.rerun()

# --- 3. DYNAMIC MATCHING ALGORITHM ---
patient_findings = []
if pupils == "Normal": patient_findings.append("Normal pupils")
if pupils == "Pinpoint": patient_findings.append("Pinpoint pupils")
if pupils == "Dilated": patient_findings.append("Dilated pupils")
if respirations == "Depressed (<12)": patient_findings.append("Respiratory depression")
if respirations == "Tachypnea (>20)": patient_findings.append("Tachypnea (>20)")
if mental_status == "Depressed / Coma": 
    patient_findings.append("CNS depression")
    patient_findings.append("Depressed / Coma")
if mental_status == "Agitated / Delirium": patient_findings.append("Agitation / Delirium")
if heart_rate == "Bradycardia (<60)": patient_findings.append("Bradycardia")
if heart_rate == "Tachycardia (>100)": patient_findings.append("Tachycardia")
if skin == "Dry / Flushed": patient_findings.append("Dry / Flushed skin")
if skin == "Diaphoretic (Sweaty)": patient_findings.append("Diaphoresis (Sweaty)")
if bowel_sounds == "Decreased / Absent": patient_findings.append("Decreased / Absent bowel sounds")
if bowel_sounds == "Hyperactive": patient_findings.append("Hyperactive bowel sounds")
if ecg_qrs == "Widened (>100ms)": patient_findings.append("Widened QRS (>100ms)")
if temperature == "Hyperthermia (>39C)": patient_findings.append("Hyperthermia (>39C)")

results = []
for tox_name, tox_data in TOXICOLOGY_DB.items():
    matches = [f for f in patient_findings if f in tox_data["hallmarks"]]
    missing = [h for h in tox_data["hallmarks"] if h not in patient_findings]
    
    score = len(matches)
    if score > 0:
        results.append({
            "tox": tox_name, 
            "match_count": score, 
            "score": score, 
            "matches": matches, 
            "missing": missing,
            "db_data": tox_data 
        })

results = sorted(results, key=lambda x: x["score"], reverse=True)

is_critical = respirations == "Depressed (<12)" or mental_status == "Depressed / Coma" or ecg_qrs == "Widened (>100ms)"
is_high_risk = mental_status == "Agitated / Delirium" or temperature == "Hyperthermia (>39C)"

# --- 4. MAIN DASHBOARD ---
st.markdown("<div style='font-size: 2.2rem; font-weight: 800; color: #00BFFF; border-bottom: 3px solid #00BFFF; padding-bottom: 10px; margin-bottom: 20px;'>Clinical Decision Support: Toxicology</div>", unsafe_allow_html=True)

if is_critical:
    st.markdown("<div class='critical-alert'>STATUS: CRITICAL PRESENTATION - Immediate Stabilization Required</div>", unsafe_allow_html=True)
elif is_high_risk:
    st.markdown("<div class='urgent-alert'>STATUS: HIGH RISK - Monitor for Rapid Decompensation</div>", unsafe_allow_html=True)
elif len(results) > 0:
    st.markdown("<div class='urgent-alert'>STATUS: OBSERVATION - Toxidrome Evaluation In Progress</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='stable-alert'>STATUS: STABLE - Awaiting Clinical Inputs</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if len(results) > 0:
    top = results[0]
    
    st.markdown("<div class='section-header'>Diagnostic Engine</div>", unsafe_allow_html=True)
    
    if top["match_count"] < 2:
        st.markdown("<div class='diagnostic-card'><strong>Indeterminate Pattern:</strong> Presentation lacks sufficient hallmarks for definitive classification. Maintain broad differentials.</div>", unsafe_allow_html=True)
    else:
        col_res1, col_res2 = st.columns([1, 1.5])
        
        with col_res1:
            st.markdown(f"<div class='diagnostic-card'>", unsafe_allow_html=True)
            st.markdown(f"**Primary Consideration:** {top['tox']}")
            
            st.markdown("\n**Matched Indicators:**")
            for m in top["matches"]: st.markdown(f"- {m}")
            
            if len(top["missing"]) > 0:
                st.markdown("\n**Missing Hallmarks:**")
                for m in top["missing"]: st.markdown(f"- {m}")
                
            st.markdown("\n**Alternative Considerations:**")
            for alt in top["db_data"]["alternatives"]: st.markdown(f"- {alt}")
            
            st.markdown("</div>", unsafe_allow_html=True)

        with col_res2:
            st.markdown("<div class='diagnostic-card'>", unsafe_allow_html=True)
            st.markdown("**Structured Intervention Plan**")
            
            st.markdown(f"- **Primary Antidote:** {top['db_data']['antidote']}")
            st.markdown(f"- **Recommended Dose:** {top['db_data']['dose']}")
            st.markdown(f"- **Clinical Goal:** {top['db_data']['goal']}")
            st.markdown(f"- **Warnings/Contraindications:** {top['db_data']['warnings']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
