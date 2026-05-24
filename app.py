import streamlit as st

st.set_page_config(page_title="ED Triage: Toxidrome Engine", layout="wide", initial_sidebar_state="collapsed")

# --- UI Styling & Header ---
st.title("⚡ ED Toxidrome Decision Support (V3)")
st.markdown("Rapid clinical pattern recognition with transparent reasoning and structured interventions.")
st.markdown("---")

if 'reset' not in st.session_state:
    st.session_state.reset = False

def clear_all():
    st.session_state.reset = not st.session_state.reset

st.button("🔄 Reset to Normal", on_click=clear_all)

# --- 1. BODY-SYSTEM CARDS (Clinical UI) ---
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

# --- 2. ADVANCED PROBABILITY ENGINE (Weighted + Contradictory Logic) ---
scores = {"Opioid": 0, "Anticholinergic": 0, "Sympathomimetic": 0, "Cholinergic": 0}
matched_findings = {"Opioid": [], "Anticholinergic": [], "Sympathomimetic": [], "Cholinergic": []}
contradictory_findings = {"Opioid": [], "Anticholinergic": [], "Sympathomimetic": [], "Cholinergic": []}

# OPIOID
if pupils == "Pinpoint": scores["Opioid"] += 3; matched_findings["Opioid"].append("Pinpoint pupils")
if respirations == "Depressed (<12)": scores["Opioid"] += 4; matched_findings["Opioid"].append("Respiratory depression")
if mental_status == "Depressed / Coma": scores["Opioid"] += 3; matched_findings["Opioid"].append("CNS depression")
if heart_rate == "Bradycardia (<60)": scores["Opioid"] += 1; matched_findings["Opioid"].append("Bradycardia")
# Contradictory for Opioid
if mental_status == "Agitated / Delirium": scores["Opioid"] -= 3; contradictory_findings["Opioid"].append("Agitation")
if pupils == "Dilated": scores["Opioid"] -= 3; contradictory_findings["Opioid"].append("Dilated pupils")

# ANTICHOLINERGIC
if pupils == "Dilated": scores["Anticholinergic"] += 2; matched_findings["Anticholinergic"].append("Dilated pupils")
if skin == "Dry, Flushed": scores["Anticholinergic"] += 3; matched_findings["Anticholinergic"].append("Dry/Flushed skin")
if heart_rate == "Tachycardia (>100)": scores["Anticholinergic"] += 2; matched_findings["Anticholinergic"].append("Tachycardia")
if mental_status == "Agitated / Delirium": scores["Anticholinergic"] += 2; matched_findings["Anticholinergic"].append("Delirium/Agitation")
if bowel_sounds == "Decreased / Absent": scores["Anticholinergic"] += 1; matched_findings["Anticholinergic"].append("Decreased bowel sounds")
# Contradictory for Anticholinergic
if skin == "Diaphoretic (Sweaty)": scores["Anticholinergic"] -= 3; contradictory_findings["Anticholinergic"].append("Diaphoresis")
if pupils == "Pinpoint": scores["Anticholinergic"] -= 2; contradictory_findings["Anticholinergic"].append("Pinpoint pupils")

# SYMPATHOMIMETIC
if pupils == "Dilated": scores["Sympathomimetic"] += 2; matched_findings["Sympathomimetic"].append("Dilated pupils")
if skin == "Diaphoretic (Sweaty)": scores["Sympathomimetic"] += 3; matched_findings["Sympathomimetic"].append("Diaphoresis")
if heart_rate == "Tachycardia (>100)": scores["Sympathomimetic"] += 3; matched_findings["Sympathomimetic"].append("Tachycardia")
if mental_status == "Agitated / Delirium": scores["Sympathomimetic"] += 2; matched_findings["Sympathomimetic"].append("Agitation")
# Contradictory for Sympathomimetic
if pupils == "Pinpoint": scores["Sympathomimetic"] -= 3; contradictory_findings["Sympathomimetic"].append("Pinpoint pupils")
if skin == "Dry, Flushed": scores["Sympathomimetic"] -= 3; contradictory_findings["Sympathomimetic"].append("Dry skin")

# CHOLINERGIC
if pupils == "Pinpoint": scores["Cholinergic"] += 2; matched_findings["Cholinergic"].append("Pinpoint pupils")
if skin == "Diaphoretic (Sweaty)": scores["Cholinergic"] += 3; matched_findings["Cholinergic"].append("Diaphoresis")
if bowel_sounds == "Hyperactive": scores["Cholinergic"] += 3; matched_findings["Cholinergic"].append("Hyperactive bowel sounds")
if respirations == "Tachypnea (>20)": scores["Cholinergic"] += 1; matched_findings["Cholinergic"].append("Tachypnea")
# Contradictory for Cholinergic
if pupils == "Dilated": scores["Cholinergic"] -= 3; contradictory_findings["Cholinergic"].append("Dilated pupils")
if skin == "Dry, Flushed": scores["Cholinergic"] -= 3; contradictory_findings["Cholinergic"].append("Dry skin")

# Determine Likelihood Categories (Max score is roughly 10-11)
def get_likelihood(score):
    if score >= 7: return "HIGH Likelihood", "🔴"
    if score >= 4: return "MODERATE Likelihood", "🟠"
    if score > 0: return "LOW Likelihood", "🟡"
    return "Unlikely", "⚪"

results = []
for tox, score in scores.items():
    likelihood, icon = get_likelihood(score)
    if score > 0:
        results.append({"tox": tox, "score": score, "likelihood": likelihood, "icon": icon})

results = sorted(results, key=lambda x: x["score"], reverse=True)

# --- 3. TIERED SEVERITY ALERTS & ABCs ---
st.markdown("### 🚑 Immediate Priorities & Alerts")

alert_triggered = False
if respirations == "Depressed (<12)" or mental_status == "Depressed / Coma":
    st.error("#### 🔴 CRITICAL: Airway Threat Detected\n* **A/B:** Evaluate airway patency and ventilatory effort immediately.\n* **Action:** Prepare for bag-valve-mask (BVM) ventilation or intubation. Continuous SpO2 and ETCO2 monitoring required.")
    alert_triggered = True
elif mental_status == "Agitated / Delirium" and heart_rate == "Tachycardia (>100)":
    st.warning("#### 🟠 URGENT: Severe Agitation / Autonomic Instability\n* **C:** Continuous cardiac monitoring. Secure IV access.\n* **Action:** Monitor for hyperthermia and prepare benzodiazepines for chemical restraint / seizure prophylaxis.")
    alert_triggered = True
else:
    st.info("#### 🟡 STANDARD MONITORING\n* Assess ABCs. Secure IV access. Obtain baseline ECG and point-of-care glucose.")

st.markdown("---")

# --- 4. EXPLAINABLE CLINICAL INTELLIGENCE ---
if len(results) > 0:
    top_result = results[0]
    
    # Check for Co-Ingestion (Two High/Moderate scores)
    if len(results) > 1 and results[0]["score"] >= 4 and results[1]["score"] >= 4:
        st.warning(f"**⚠ MIXED TOXIDROME POSSIBLE:** High indices of suspicion for both **{results[0]['tox']}** and **{results[1]['tox']}**. Consider polypharmacy overdose.")

    st.subheader(f"Diagnostic Engine: {top_result['icon']} {top_result['tox']} ({top_result['likelihood']})")
    
    col_exp1, col_exp2 = st.columns([1, 1.5])
    
    with col_exp1:
        with st.container(border=True):
            st.markdown("**🔍 Diagnostic Reasoning**")
            for f in matched_findings[top_result["tox"]]:
                st.write(f"✅ {f}")
            if len(contradictory_findings[top_result["tox"]]) > 0:
                st.markdown("**Conflicting Data:**")
                for c in contradictory_findings[top_result["tox"]]:
                    st.write(f"❌ {c} (Reduces confidence)")

    with col_exp2:
        with st.container(border=True):
            st.markdown("**💉 Structured Intervention Plan**")
            if top_result["tox"] == "Opioid":
                st.markdown("""
                **Intervention:** Naloxone (Narcan)
                * **Initial Dose:** 0.4 mg IV/IM (Use 0.04 mg if chronic user to avoid acute withdrawal).
                * **Titration:** Repeat every 2-3 minutes.
                * **Clinical Goal:** Adequate ventilation (RR > 12), *not* full arousal.
                * **Monitoring:** Continuous SpO2. Observe for re-sedation (half-life of naloxone is shorter than many opioids).
                """)
            elif top_result["tox"] == "Anticholinergic":
                st.markdown("""
                **Intervention:** Supportive Care & Physostigmine
                * **Initial Dose:** Physostigmine 0.5 - 2 mg IV pushed slowly over 5 minutes.
                * **Indications:** Severe central delirium or hyperthermia unresponsive to benzodiazepines.
                * **Warnings:** Obtain screening ECG first. STRICTLY CONTRAINDICATED if QRS > 100ms or suspected TCA overdose.
                """)
            elif top_result["tox"] == "Sympathomimetic":
                st.markdown("""
                **Intervention:** Benzodiazepines & Cooling
                * **First-line:** Diazepam or Lorazepam IV for agitation, tachycardia, and hypertension.
                * **Cooling:** Active cooling measures for hyperthermia.
                * **Warnings:** STRICTLY AVOID BETA-BLOCKERS (risk of unopposed alpha-adrenergic stimulation leading to severe hypertension/ischemia).
                """)
            elif top_result["tox"] == "Cholinergic":
                st.markdown("""
                **Intervention:** Atropine & Pralidoxime
                * **Initial Dose:** Atropine 2 - 5 mg IV. Double the dose every 5 minutes.
                * **Clinical Goal:** Titrate until airway secretions clear and bronchospasm resolves. Heart rate and pupil size are *not* endpoints for titration.
                * **Secondary:** Follow with Pralidoxime (2-PAM) 1-2 grams IV for nicotinic receptor regeneration.
                """)
else:
    st.write("Awaiting clinical findings to generate differential diagnosis...")
