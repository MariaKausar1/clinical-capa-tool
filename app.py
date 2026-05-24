import streamlit as st

st.set_page_config(page_title="ED Triage: Toxidrome Engine", layout="wide", initial_sidebar_state="collapsed")

st.title("⚡ ED Toxidrome Decision Support (V4)")
st.markdown("Pattern recognition, threshold diagnostics, and structured stabilization protocols.")
st.markdown("---")

if 'reset' not in st.session_state:
    st.session_state.reset = False

def clear_all():
    st.session_state.reset = not st.session_state.reset

st.button("🔄 Reset to Normal", on_click=clear_all)

# --- 1. BODY-SYSTEM CARDS ---
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("🧠 Neurologic")
        pupils = st.radio("Pupils", ["Normal", "Pinpoint", "Dilated"], horizontal=True, key=f"pupils_{st.session_state.reset}")
        mental_status = st.radio("Mental Status", ["Normal", "Depressed / Coma", "Agitated / Delirium"], horizontal=True, key=f"ms_{st.session_state.reset}")

    with st.container(border=True):
        st.subheader("🫁 Respiratory")
        respirations = st.radio("Respiratory Rate", ["Normal", "Depressed (<12)", "Tachypnea (>20)"], horizontal=True, key=f"resp_{st.session_state.reset}")

with col2:
    with st.container(border=True):
        st.subheader("🫀 Cardiovascular")
        heart_rate = st.radio("Heart Rate", ["Normal", "Bradycardia (<60)", "Tachycardia (>100)"], horizontal=True, key=f"hr_{st.session_state.reset}")

    with st.container(border=True):
        st.subheader("🧬 GI / Autonomic")
        skin = st.radio("Skin Exam", ["Normal", "Dry, Flushed", "Diaphoretic (Sweaty)"], horizontal=True, key=f"skin_{st.session_state.reset}")
        bowel_sounds = st.radio("Bowel Sounds", ["Normal", "Decreased / Absent", "Hyperactive"], horizontal=True, key=f"bs_{st.session_state.reset}")

st.markdown("---")

# --- 2. CRITICAL ALERTS & STABILIZATION ---
st.subheader("🚨 Clinical Severity & Stabilization")

# Determine Severity Status
is_critical = respirations == "Depressed (<12)" or mental_status == "Depressed / Coma"
is_high_risk = mental_status == "Agitated / Delirium" or heart_rate == "Tachycardia (>100)" or skin != "Normal"

if is_critical:
    st.error("#### 🔴 CRITICAL PRESENTATION\nImmediate airway threat or profound CNS depression detected.")
elif is_high_risk:
    st.warning("#### 🟠 HIGH-RISK FEATURES PRESENT\nAutonomic instability or severe agitation detected. High risk for decompensation.")
else:
    if pupils != "Normal" or bowel_sounds != "Normal":
        st.info("#### 🟡 REQUIRES OBSERVATION\nIsolated abnormal findings detected. Monitor for toxidrome evolution.")
    else:
        st.success("#### 🟢 CURRENTLY STABLE\nNo immediately life-threatening toxidrome pattern identified.")

with st.expander("🚑 Immediate Stabilization Protocols", expanded=True):
    col_stab1, col_stab2 = st.columns(2)
    with col_stab1:
        st.markdown("**Core ED Management:**")
        st.markdown("- **A/B:** Assess airway patency & respiratory effort.")
        st.markdown("- **C:** Secure large-bore IV access.")
        st.markdown("- **D:** Check point-of-care glucose (rule out hypoglycemia).")
    with col_stab2:
        st.markdown("**Monitoring Required:**")
        st.markdown("- Continuous pulse oximetry.")
        st.markdown("- Continuous cardiac telemetry (obtain baseline 12-lead ECG).")
        if is_critical:
            st.markdown("- **ETCO2 (Capnography)** required for ventilatory monitoring.")

st.markdown("---")

# --- 3. DIAGNOSTIC ENGINE (Threshold Logic) ---
matched_findings = {"Opioid": [], "Anticholinergic": [], "Sympathomimetic": [], "Cholinergic": []}
contradictory_findings = {"Opioid": [], "Anticholinergic": [], "Sympathomimetic": [], "Cholinergic": []}

# OPIOID
if pupils == "Pinpoint": matched_findings["Opioid"].append("Pinpoint pupils")
if respirations == "Depressed (<12)": matched_findings["Opioid"].append("Respiratory depression")
if mental_status == "Depressed / Coma": matched_findings["Opioid"].append("CNS depression")
if heart_rate == "Bradycardia (<60)": matched_findings["Opioid"].append("Bradycardia")
if mental_status == "Agitated / Delirium": contradictory_findings["Opioid"].append("Agitation")
if pupils == "Dilated": contradictory_findings["Opioid"].append("Dilated pupils")

# ANTICHOLINERGIC
if pupils == "Dilated": matched_findings["Anticholinergic"].append("Dilated pupils")
if skin == "Dry, Flushed": matched_findings["Anticholinergic"].append("Dry/Flushed skin")
if heart_rate == "Tachycardia (>100)": matched_findings["Anticholinergic"].append("Tachycardia")
if mental_status == "Agitated / Delirium": matched_findings["Anticholinergic"].append("Delirium/Agitation")
if bowel_sounds == "Decreased / Absent": matched_findings["Anticholinergic"].append("Decreased bowel sounds")
if skin == "Diaphoretic (Sweaty)": contradictory_findings["Anticholinergic"].append("Diaphoresis")
if pupils == "Pinpoint": contradictory_findings["Anticholinergic"].append("Pinpoint pupils")

# SYMPATHOMIMETIC
if pupils == "Dilated": matched_findings["Sympathomimetic"].append("Dilated pupils")
if skin == "Diaphoretic (Sweaty)": matched_findings["Sympathomimetic"].append("Diaphoresis")
if heart_rate == "Tachycardia (>100)": matched_findings["Sympathomimetic"].append("Tachycardia")
if mental_status == "Agitated / Delirium": matched_findings["Sympathomimetic"].append("Agitation")
if pupils == "Pinpoint": contradictory_findings["Sympathomimetic"].append("Pinpoint pupils")
if skin == "Dry, Flushed": contradictory_findings["Sympathomimetic"].append("Dry skin")

# CHOLINERGIC
if pupils == "Pinpoint": matched_findings["Cholinergic"].append("Pinpoint pupils")
if skin == "Diaphoretic (Sweaty)": matched_findings["Cholinergic"].append("Diaphoresis")
if bowel_sounds == "Hyperactive": matched_findings["Cholinergic"].append("Hyperactive bowel sounds")
if respirations == "Tachypnea (>20)": matched_findings["Cholinergic"].append("Tachypnea")
if pupils == "Dilated": contradictory_findings["Cholinergic"].append("Dilated pupils")
if skin == "Dry, Flushed": contradictory_findings["Cholinergic"].append("Dry skin")

# Determine max match length to find primary candidate
results = []
for tox, matches in matched_findings.items():
    score = len(matches) - (len(contradictory_findings[tox]) * 0.5) # Penalize for contradictions
    if len(matches) > 0:
        results.append({"tox": tox, "match_count": len(matches), "score": score, "matches": matches, "contradictions": contradictory_findings[tox]})

results = sorted(results, key=lambda x: x["score"], reverse=True)

st.subheader("🧠 Diagnostic Engine")

if len(results) == 0:
    st.write("Awaiting clinical findings...")
else:
    top_result = results[0]
    
    # Confidence Thresholds
    if top_result["match_count"] >= 4:
        confidence = "STRONG PATTERN MATCH"
        icon = "🟩"
    elif top_result["match_count"] >= 2:
        confidence = "MODERATE CONCERN"
        icon = "🟨"
    else:
        confidence = "WEAK SIGNAL"
        icon = "⬜"

    if top_result["match_count"] < 2:
        st.info("**Insufficient findings for reliable toxidrome classification.**\nSingle isolated finding detected. Pattern insufficient for definitive toxidrome identification. Continue monitoring and reassessment.")
    else:
        st.markdown(f"### {icon} {top_result['tox']} ({confidence})")
        
        col_exp1, col_exp2 = st.columns([1, 1.5])
        
        with col_exp1:
            with st.container(border=True):
                st.markdown("**🔍 Diagnostic Reasoning**")
                st.write(f"{top_result['match_count']} hallmark findings identified:")
                for f in top_result["matches"]:
                    st.write(f"✅ {f}")
                if len(top_result["contradictions"]) > 0:
                    st.markdown("**Conflicting Data:**")
                    for c in top_result["contradictions"]:
                        st.write(f"❌ {c}")

        with col_exp2:
            with st.container(border=True):
                st.markdown("**💉 Treatment Recommendations**")
                
                if top_result["tox"] == "Opioid":
                    st.markdown("""
                    **Intervention:** Naloxone
                    * **Initial dose:** 0.4 mg IV (Use 0.04 mg if chronic user to avoid acute withdrawal).
                    * **Goal:** Adequate ventilation, not full arousal.
                    
                    **Contraindications / Warnings:**
                    * Avoid aggressive dosing in suspected poly-substance overdose involving stimulants.
                    
                    **Escalate Care If:**
                    * Refractory hypoxia despite BVM and naloxone.
                    * Re-sedation occurs (naloxone half-life < opioid half-life).
                    """)
                elif top_result["tox"] == "Anticholinergic":
                    st.markdown("""
                    **Intervention:** Supportive Care & Physostigmine
                    * **Initial dose:** Physostigmine 0.5 - 2 mg IV over 5 mins.
                    
                    **Contraindications / Warnings:**
                    * **ABSOLUTE:** QRS > 100ms or suspected TCA overdose.
                    * Have atropine at bedside before administering physostigmine.
                    
                    **Escalate Care If:**
                    * Hyperthermia >40°C.
                    * Refractory seizures.
                    """)
                elif top_result["tox"] == "Sympathomimetic":
                    st.markdown("""
                    **Intervention:** Benzodiazepines
                    * **Initial dose:** Diazepam 5-10 mg IV or Lorazepam 1-2 mg IV.
                    
                    **Contraindications / Warnings:**
                    * **ABSOLUTE:** Beta-blockers (risk of unopposed alpha stimulation leading to severe ischemia/hypertension).
                    
                    **Escalate Care If:**
                    * Chest pain / ECG ischemic changes.
                    * Hyperthermia >40°C.
                    * Severe hypertension refractory to benzos (consider phentolamine or nitroprusside).
                    """)
                elif top_result["tox"] == "Cholinergic":
                    st.markdown("""
                    **Intervention:** Atropine & Pralidoxime (2-PAM)
                    * **Initial dose:** Atropine 2 - 5 mg IV. Double the dose every 5 minutes.
                    * **Goal:** Titrate until airway secretions clear and bronchospasm resolves.
                    
                    **Contraindications / Warnings:**
                    * Do not stop atropine based on heart rate or pupil size. Focus solely on clearing respiratory secretions.
                    
                    **Escalate Care If:**
                    * Impending respiratory failure due to profound neuromuscular weakness (nicotinic effect).
                    * Seizures.
                    """)
