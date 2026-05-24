import streamlit as st

st.set_page_config(page_title="ED Triage: Toxidrome Engine", layout="wide", initial_sidebar_state="collapsed")

st.title("⚡ ED Toxidrome Decision Support (V5)")
st.markdown("Advanced pattern recognition, threshold diagnostics, and dynamic severity modeling.")
st.markdown("---")

if 'reset' not in st.session_state:
    st.session_state.reset = False

def clear_all():
    st.session_state.reset = not st.session_state.reset

st.button("🔄 Reset Patient Data", on_click=clear_all)

# --- 1. CLINICAL INPUTS (Body-System Cards) ---
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

# --- 2. DYNAMIC SEVERITY ENGINE ---
severity_score = 0
if respirations == "Depressed (<12)": severity_score += 5
if mental_status == "Depressed / Coma": severity_score += 4
if mental_status == "Agitated / Delirium": severity_score += 4
if heart_rate in ["Bradycardia (<60)", "Tachycardia (>100)"]: severity_score += 3
if skin != "Normal": severity_score += 2
if pupils != "Normal": severity_score += 1

st.subheader("🚨 Clinical Severity & Stabilization")
col_sev1, col_sev2 = st.columns([1, 2])

with col_sev1:
    if severity_score >= 8:
        st.error("### 🔴 CRITICAL\nImmediate stabilization required.")
    elif severity_score >= 4:
        st.warning("### 🟠 HIGH RISK\nMonitor for rapid decompensation.")
    elif severity_score > 0:
        st.info("### 🟡 OBSERVATION\nStable, but requires monitoring.")
    else:
        st.success("### 🟢 STABLE\nNo acute toxidrome severity features.")

with col_sev2:
    with st.expander("🚑 Immediate Stabilization & Monitoring", expanded=(severity_score >= 4)):
        st.markdown("**Core ED Management:**")
        st.markdown("- **A/B:** Assess airway patency & respiratory effort. Consider ETCO₂ monitoring if CNS depression is present.")
        st.markdown("- **C:** Secure large-bore IV access. Obtain baseline 12-lead ECG.")
        st.markdown("- **D:** Check point-of-care glucose immediately to rule out hypoglycemia.")
        st.markdown("- **Reassessment:** Repeat vitals and mental status check q15 min.")

st.markdown("---")

# --- 3. DIAGNOSTIC ENGINE & RESTRAINT LOGIC ---
hallmarks = {
    "Opioid": ["Pinpoint pupils", "Respiratory depression", "CNS depression", "Bradycardia"],
    "Anticholinergic": ["Dilated pupils", "Dry/Flushed skin", "Tachycardia", "Delirium/Agitation"],
    "Sympathomimetic": ["Dilated pupils", "Diaphoresis", "Tachycardia", "Agitation"],
    "Cholinergic": ["Pinpoint pupils", "Diaphoresis", "Hyperactive bowel sounds", "Tachypnea"]
}

matched_findings = {"Opioid": [], "Anticholinergic": [], "Sympathomimetic": [], "Cholinergic": []}
contradictory_findings = {"Opioid": [], "Anticholinergic": [], "Sympathomimetic": [], "Cholinergic": []}

# Pattern Matching
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
if respirations == "Depressed (<12)":
    matched_findings["Opioid"].append("Respiratory depression")
if respirations == "Tachypnea (>20)":
    matched_findings["Cholinergic"].append("Tachypnea")
if mental_status == "Depressed / Coma":
    matched_findings["Opioid"].append("CNS depression")
if mental_status == "Agitated / Delirium":
    matched_findings["Anticholinergic"].append("Delirium/Agitation")
    matched_findings["Sympathomimetic"].append("Agitation")
    contradictory_findings["Opioid"].append("Agitation")
if heart_rate == "Bradycardia (<60)":
    matched_findings["Opioid"].append("Bradycardia")
if heart_rate == "Tachycardia (>100)":
    matched_findings["Anticholinergic"].append("Tachycardia")
    matched_findings["Sympathomimetic"].append("Tachycardia")
if skin == "Dry, Flushed":
    matched_findings["Anticholinergic"].append("Dry/Flushed skin")
    contradictory_findings["Sympathomimetic"].append("Dry skin")
    contradictory_findings["Cholinergic"].append("Dry skin")
if skin == "Diaphoretic (Sweaty)":
    matched_findings["Sympathomimetic"].append("Diaphoresis")
    matched_findings["Cholinergic"].append("Diaphoresis")
    contradictory_findings["Anticholinergic"].append("Diaphoresis")
if bowel_sounds == "Decreased / Absent":
    matched_findings["Anticholinergic"].append("Decreased bowel sounds")
if bowel_sounds == "Hyperactive":
    matched_findings["Cholinergic"].append("Hyperactive bowel sounds")

# Calculate Scores
results = []
for tox, matches in matched_findings.items():
    score = len(matches) - (len(contradictory_findings[tox]) * 1.5) # Heavy penalty for contradictions
    missing = [h for h in hallmarks[tox] if h not in matches]
    if len(matches) > 0:
        results.append({"tox": tox, "match_count": len(matches), "score": score, "matches": matches, "contradictions": contradictory_findings[tox], "missing": missing})

results = sorted(results, key=lambda x: x["score"], reverse=True)

st.subheader("🧠 Diagnostic Engine & Interventions")

if len(results) == 0:
    st.write("Awaiting clinical findings...")
else:
    top_result = results[0]
    
    if top_result["match_count"] < 2 or top_result["score"] < 1:
        st.info("**Weak Signal Detected:** Single isolated finding or heavily contradictory presentation.\nPattern incomplete for definitive toxidrome identification. Continue observation and maintain broad differentials.")
    else:
        st.markdown(f"### Possible {top_result['tox']} Toxidrome Detected")
        
        col_diag1, col_diag2 = st.columns([1.2, 1.5])
        
        with col_diag1:
            with st.container(border=True):
                st.markdown("**🔍 Supporting Findings**")
                for f in top_result["matches"]: st.write(f"✅ {f}")
                
                st.markdown("**❌ Missing Hallmarks**")
                if len(top_result["missing"]) == 0:
                    st.write("None. Classic presentation.")
                else:
                    for m in top_result["missing"]: st.write(f"• {m} (Pattern incomplete)")
                
                if len(top_result["contradictions"]) > 0:
                    st.markdown("**⚠️ Contradictory Data**")
                    for c in top_result["contradictions"]: st.write(f"• {c} (Reduces confidence)")
            
            with st.container(border=True):
                st.markdown("**🔄 Alternative Considerations**")
                if top_result["tox"] == "Opioid":
                    st.write("- Sedative-hypnotic exposure\n- Hypoglycemia\n- Primary intracranial event")
                elif top_result["tox"] == "Anticholinergic" or top_result["tox"] == "Sympathomimetic":
                    st.write("- Sepsis / Infection\n- Thyroid storm\n- Alcohol/Benzo withdrawal\n- Serotonin Syndrome")
                elif top_result["tox"] == "Cholinergic":
                    st.write("- Pontine hemorrhage\n- Opiate co-ingestion (if pinpoint pupils present)")

        with col_diag2:
            with st.container(border=True):
                st.markdown("**💉 Recommended Intervention Plan**")
                
                if top_result["tox"] == "Opioid":
                    st.markdown("""
                    **Primary Antidote:** Naloxone
                    * **Dose:** 0.04 – 0.4 mg IV (titrate to effect).
                    * **Goal:** Adequate spontaneous ventilation.
                    
                    **Escalation / Monitoring:**
                    * Observe for re-sedation (naloxone half-life is ~30-81 mins).
                    * If refractory hypoxia persists despite BVM and naloxone, escalate airway management.
                    """)
                elif top_result["tox"] == "Anticholinergic":
                    st.markdown("""
                    **Primary Antidote:** Supportive Care & Physostigmine
                    * **Dose:** Physostigmine 0.5 - 2 mg IV over 5 mins (only for severe delirium).
                    
                    **Escalation / Monitoring:**
                    * **ABSOLUTE CONTRAINDICATION:** QRS > 100ms on ECG. 
                    * Obtain ECG before physostigmine administration.
                    * Monitor for hyperthermia.
                    """)
                elif top_result["tox"] == "Sympathomimetic":
                    st.markdown("""
                    **Primary Antidote:** Benzodiazepines
                    * **Dose:** Diazepam 5-10 mg IV or Lorazepam 1-2 mg IV (titrate for sedation/HR).
                    
                    **Escalation / Monitoring:**
                    * **ABSOLUTE CONTRAINDICATION:** Beta-blockers.
                    * Escalate to active cooling if temperature >40°C.
                    * Assess for ischemic chest pain / ECG changes.
                    """)
                elif top_result["tox"] == "Cholinergic":
                    st.markdown("""
                    **Primary Antidote:** Atropine & 2-PAM
                    * **Dose:** Atropine 2 - 5 mg IV. Double every 5 minutes.
                    
                    **Escalation / Monitoring:**
                    * Titrate Atropine specifically to clearing of respiratory secretions.
                    * Follow with Pralidoxime (2-PAM) for severe muscle fasciculations/weakness.
                    """)
