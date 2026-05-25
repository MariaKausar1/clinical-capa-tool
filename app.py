import streamlit as st

st.set_page_config(page_title="Toxidrome CDS", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR ENTERPRISE UI (No Emojis) ---
st.markdown("""
    <style>
    .critical-alert { background-color: #721c24; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #dc3545; }
    .urgent-alert { background-color: #856404; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #ffc107; }
    .stable-alert { background-color: #155724; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #28a745; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #495057; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 1.5rem; margin-bottom: 0.5rem; border-bottom: 1px solid #dee2e6; padding-bottom: 4px; }
    .diagnostic-card { border: 1px solid #dee2e6; border-radius: 6px; padding: 16px; background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

# --- 1. LEFT PANEL: CLINICAL DATA ENTRY ---
with st.sidebar:
    st.markdown("<div style='font-size: 1.5rem; font-weight: bold; color: #212529;'>Clinical Data Entry</div>", unsafe_allow_html=True)
    st.caption("Update findings to calculate live diagnostics.")
    
    st.markdown("<div class='section-header'>Neurologic</div>", unsafe_allow_html=True)
    pupils = st.selectbox("Pupil Examination", ["Normal", "Pinpoint", "Dilated"])
    mental_status = st.selectbox("Mental Status", ["Normal", "Depressed / Coma", "Agitated / Delirium"])
    
    st.markdown("<div class='section-header'>Cardiopulmonary</div>", unsafe_allow_html=True)
    respirations = st.selectbox("Respiratory Rate", ["Normal", "Depressed (<12)", "Tachypnea (>20)"])
    heart_rate = st.selectbox("Heart Rate", ["Normal", "Bradycardia (<60)", "Tachycardia (>100)"])
    
    st.markdown("<div class='section-header'>Autonomic</div>", unsafe_allow_html=True)
    skin = st.selectbox("Skin / Mucous Membranes", ["Normal", "Dry / Flushed", "Diaphoretic (Sweaty)"])
    bowel_sounds = st.selectbox("Bowel Sounds", ["Normal", "Decreased / Absent", "Hyperactive"])
    
    st.markdown("<div class='section-header'>Adjunct Diagnostics</div>", unsafe_allow_html=True)
    ecg_qrs = st.selectbox("ECG QRS Interval", ["Normal (<100ms)", "Widened (>100ms)"])
    temperature = st.selectbox("Core Temperature", ["Normal", "Hyperthermia (>39C)"])
    
    if st.button("Clear Patient Data", use_container_width=True):
        st.rerun()

# --- 2. LOGIC & PHYSIOLOGY ENGINE ---
hallmarks = {
    "Opioid": ["Pinpoint pupils", "Respiratory depression", "CNS depression", "Bradycardia"],
    "Anticholinergic": ["Dilated pupils", "Dry/Flushed skin", "Tachycardia", "Agitation/Delirium"],
    "Sympathomimetic": ["Dilated pupils", "Diaphoresis", "Tachycardia", "Agitation/Delirium", "Hyperthermia (>39C)"],
    "Cholinergic": ["Pinpoint pupils", "Diaphoresis", "Hyperactive bowel sounds", "Tachypnea"]
}

matched_findings = {"Opioid": [], "Anticholinergic": [], "Sympathomimetic": [], "Cholinergic": []}
contradictory_findings = {"Opioid": [], "Anticholinergic": [], "Sympathomimetic": [], "Cholinergic": []}

# Advanced Physiology: TCA Overdose Detection
tca_warning = (ecg_qrs == "Widened (>100ms)" and (heart_rate == "Tachycardia (>100)" or mental_status == "Agitated / Delirium"))

if pupils == "Pinpoint":
    matched_findings["Opioid"].append("Pinpoint pupils")
    matched_findings["Cholinergic"].append("Pinpoint pupils")
    contradictory_findings["Anticholinergic"].append("Pinpoint pupils")
    contradictory_findings["Sympathomimetic"].append("Pinpoint pupils")
if pupils == "Dilated":
    matched_findings["Anticholinergic"].append("Dilated pupils")
    matched_findings["Sympathomimetic"].append("Dilated pupils")
    contradictory_findings["Opioid"].append("Dilated pupils")
    contradictory_findings["Cholinergic"].append("Dilated pupils")
if respirations == "Depressed (<12)": matched_findings["Opioid"].append("Respiratory depression")
if respirations == "Tachypnea (>20)": matched_findings["Cholinergic"].append("Tachypnea")
if mental_status == "Depressed / Coma": matched_findings["Opioid"].append("CNS depression")
if mental_status == "Agitated / Delirium":
    matched_findings["Anticholinergic"].append("Agitation/Delirium")
    matched_findings["Sympathomimetic"].append("Agitation/Delirium")
    contradictory_findings["Opioid"].append("Agitation")
if heart_rate == "Bradycardia (<60)": matched_findings["Opioid"].append("Bradycardia")
if heart_rate == "Tachycardia (>100)":
    matched_findings["Anticholinergic"].append("Tachycardia")
    matched_findings["Sympathomimetic"].append("Tachycardia")
if skin == "Dry / Flushed":
    matched_findings["Anticholinergic"].append("Dry/Flushed skin")
    contradictory_findings["Sympathomimetic"].append("Dry skin")
    contradictory_findings["Cholinergic"].append("Dry skin")
if skin == "Diaphoretic (Sweaty)":
    matched_findings["Sympathomimetic"].append("Diaphoresis")
    matched_findings["Cholinergic"].append("Diaphoresis")
    contradictory_findings["Anticholinergic"].append("Diaphoresis")
if bowel_sounds == "Decreased / Absent": matched_findings["Anticholinergic"].append("Decreased bowel sounds")
if bowel_sounds == "Hyperactive": matched_findings["Cholinergic"].append("Hyperactive bowel sounds")
if temperature == "Hyperthermia (>39C)":
    matched_findings["Sympathomimetic"].append("Hyperthermia (>39C)")
    matched_findings["Anticholinergic"].append("Hyperthermia (>39C)")

results = []
for tox, matches in matched_findings.items():
    score = len(matches) - (len(contradictory_findings[tox]) * 1.5)
    missing = [h for h in hallmarks[tox] if h not in matches]
    if len(matches) > 0:
        results.append({"tox": tox, "match_count": len(matches), "score": score, "matches": matches, "contradictions": contradictory_findings[tox], "missing": missing})

results = sorted(results, key=lambda x: x["score"], reverse=True)

# Severity Engine
is_critical = respirations == "Depressed (<12)" or mental_status == "Depressed / Coma" or tca_warning
is_high_risk = mental_status == "Agitated / Delirium" or temperature == "Hyperthermia (>39C)"

# --- 3. MAIN DASHBOARD ---
st.markdown("<div style='font-size: 2.2rem; font-weight: 800; color: #0A3161; border-bottom: 3px solid #0A3161; padding-bottom: 10px; margin-bottom: 20px;'>Clinical Decision Support: Toxicology</div>", unsafe_allow_html=True)

# Status Bar
if is_critical:
    st.markdown("<div class='critical-alert'>STATUS: CRITICAL PRESENTATION - Immediate Stabilization Required</div>", unsafe_allow_html=True)
elif is_high_risk:
    st.markdown("<div class='urgent-alert'>STATUS: HIGH RISK - Monitor for Rapid Decompensation</div>", unsafe_allow_html=True)
elif len(results) > 0:
    st.markdown("<div class='urgent-alert'>STATUS: OBSERVATION - Toxidrome Evaluation In Progress</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='stable-alert'>STATUS: STABLE - Awaiting Clinical Inputs</div>", unsafe_allow_html=True)

# TCA Warning Override
if tca_warning:
    st.markdown("<br><div class='critical-alert'>ECG WARNING: Widened QRS + Anticholinergic/Tachycardic features detected. High suspicion for Tricyclic Antidepressant (TCA) toxicity. Prepare Sodium Bicarbonate.</div>", unsafe_allow_html=True)

if len(results) > 0:
    top = results[0]
    
    st.markdown("<div class='section-header'>Diagnostic Engine</div>", unsafe_allow_html=True)
    
    if top["match_count"] < 2 or top["score"] < 1:
        st.markdown("<div class='diagnostic-card'><strong>Indeterminate Pattern:</strong> Presentation lacks sufficient hallmarks for definitive classification. Maintain broad differentials.</div>", unsafe_allow_html=True)
    else:
        col_res1, col_res2 = st.columns([1, 1.5])
        
        with col_res1:
            st.markdown(f"<div class='diagnostic-card'>", unsafe_allow_html=True)
            st.markdown(f"**Primary Consideration:** {top['tox']} Toxidrome")
            
            st.markdown("\n**Matched Indicators:**")
            for m in top["matches"]: st.markdown(f"- {m}")
            
            if len(top["missing"]) > 0:
                st.markdown("\n**Missing Hallmarks:**")
                for m in top["missing"]: st.markdown(f"- {m}")
                
            if len(top["contradictions"]) > 0:
                st.markdown("\n**Conflicting Data:**")
                for c in top["contradictions"]: st.markdown(f"- {c}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_res2:
            st.markdown("<div class='diagnostic-card'>", unsafe_allow_html=True)
            st.markdown("**Structured Intervention Plan**")
            
            if top["tox"] == "Opioid":
                st.markdown("- **Antidote:** Naloxone 0.04 - 0.4 mg IV.")
                st.markdown("- **Goal:** Spontaneous ventilation (not full arousal).")
                st.markdown("- **Monitoring:** Continuous SpO2 and ETCO2 capnography.")
            elif top["tox"] == "Anticholinergic":
                st.markdown("- **Antidote:** Physostigmine 0.5 - 2 mg IV (Administer only if QRS is normal).")
                st.markdown("- **Contraindication:** Do NOT administer physostigmine if QRS > 100ms or TCA overdose suspected.")
                st.markdown("- **Monitoring:** Continuous ECG and core temperature monitoring.")
            elif top["tox"] == "Sympathomimetic":
                st.markdown("- **Intervention:** Benzodiazepines (Diazepam 5-10 mg IV) for agitation.")
                st.markdown("- **Contraindication:** Absolute contraindication for beta-blockers (risk of unopposed alpha stimulation).")
                st.markdown("- **Monitoring:** Active cooling required if hyperthermic.")
            elif top["tox"] == "Cholinergic":
                st.markdown("- **Antidote:** Atropine 2 - 5 mg IV (titrate to drying of respiratory secretions).")
                st.markdown("- **Secondary:** Follow with Pralidoxime (2-PAM) for neuromuscular weakness.")
                st.markdown("- **Monitoring:** Assess frequently for impending respiratory failure.")
            st.markdown("</div>", unsafe_allow_html=True)
