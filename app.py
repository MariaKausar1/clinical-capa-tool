import streamlit as st
import pandas as pd

# Page Config must be the first Streamlit command
st.set_page_config(page_title="ED Triage: Toxidrome Engine", layout="wide", initial_sidebar_state="collapsed")

# --- UI Styling & Header ---
st.title("⚡ ED Toxidrome Decision Support")
st.markdown("Rapid clinical pattern recognition and antidote protocols.")
st.markdown("---")

# --- Initialize State for "Smart Defaults" & "Clear All" ---
if 'reset' not in st.session_state:
    st.session_state.reset = False

def clear_all():
    st.session_state.reset = not st.session_state.reset

st.button("🔄 Clear All to Normal", on_click=clear_all)

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

# --- 2. LIVE DANGER ALERTS (Instant Pattern Recognition) ---
st.markdown("### 🚨 Live Clinical Alerts")
alert_triggered = False

if pupils == "Pinpoint" and respirations == "Depressed (<12)":
    st.error("**⚠ CRITICAL:** High concern for Opioid Toxicity. Prepare Airway & Naloxone.")
    alert_triggered = True
if pupils == "Dilated" and skin == "Dry, Flushed" and mental_status == "Agitated / Delirium":
    st.warning("**⚠ WARNING:** Anticholinergic syndrome likely. Monitor for hyperthermia and seizures.")
    alert_triggered = True
if skin == "Diaphoretic (Sweaty)" and bowel_sounds == "Hyperactive" and pupils == "Pinpoint":
    st.warning("**⚠ WARNING:** Cholinergic crisis possible (SLUDGE syndrome). Isolate patient if organophosphate exposure suspected.")
    alert_triggered = True

if not alert_triggered:
    st.success("No critical toxidrome combinations instantly detected. Review probability engine below.")

st.markdown("---")

# --- 3. PROBABILITY ENGINE (Weighted Scoring) ---
# We calculate a score for each toxidrome based on clinical weight of symptoms
scores = {"Opioid": 0, "Anticholinergic": 0, "Sympathomimetic": 0, "Cholinergic": 0}

# Opioid (Max Score ~ 10)
if pupils == "Pinpoint": scores["Opioid"] += 3
if respirations == "Depressed (<12)": scores["Opioid"] += 4
if mental_status == "Depressed / Coma": scores["Opioid"] += 2
if heart_rate == "Bradycardia (<60)": scores["Opioid"] += 1

# Anticholinergic (Max Score ~ 10)
if pupils == "Dilated": scores["Anticholinergic"] += 2
if skin == "Dry, Flushed": scores["Anticholinergic"] += 3
if heart_rate == "Tachycardia (>100)": scores["Anticholinergic"] += 2
if mental_status == "Agitated / Delirium": scores["Anticholinergic"] += 2
if bowel_sounds == "Decreased / Absent": scores["Anticholinergic"] += 1

# Sympathomimetic (Max Score ~ 10)
if pupils == "Dilated": scores["Sympathomimetic"] += 2
if skin == "Diaphoretic (Sweaty)": scores["Sympathomimetic"] += 3
if heart_rate == "Tachycardia (>100)": scores["Sympathomimetic"] += 3
if mental_status == "Agitated / Delirium": scores["Sympathomimetic"] += 2

# Cholinergic (Max Score ~ 10)
if pupils == "Pinpoint": scores["Cholinergic"] += 2
if skin == "Diaphoretic (Sweaty)": scores["Cholinergic"] += 3
if bowel_sounds == "Hyperactive": scores["Cholinergic"] += 3
if respirations == "Tachypnea (>20)": scores["Cholinergic"] += 1
if heart_rate == "Bradycardia (<60)": scores["Cholinergic"] += 1

# Convert scores to rough percentages (Max score roughly equals 100%)
probabilities = {k: min(v * 10, 99) for k, v in scores.items()}
sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

# --- 4. CLINICAL INTELLIGENCE OUTPUT ---
st.subheader("📊 Live Toxidrome Matching")

out_col1, out_col2 = st.columns([1, 2])

with out_col1:
    st.write("**Top Differential Diagnoses:**")
    for tox, prob in sorted_probs[:2]: # Show top 2
        if prob > 0:
            st.metric(label=tox, value=f"{prob}% Match")
        else:
            st.write("Awaiting clinical inputs...")
            break

with out_col2:
    top_toxidrome = sorted_probs[0][0]
    top_prob = sorted_probs[0][1]
    
    if top_prob >= 50:
        st.info(f"**AI Interpretation:** Presentation is most consistent with **{top_toxidrome}** toxidrome.")
        
        # Pull the specific protocol based on the top match
        if top_toxidrome == "Opioid":
            st.write("💉 **Antidote Protocol:** Administer **Naloxone (Narcan)** 0.4 - 2 mg IV/IM/IN. Goal is adequate ventilation.")
        elif top_toxidrome == "Anticholinergic":
            st.write("💉 **Antidote Protocol:** Consider **Physostigmine** for severe central symptoms. Benzodiazepines for agitation. Avoid beta-blockers.")
        elif top_toxidrome == "Sympathomimetic":
            st.write("💉 **Antidote Protocol:** **Benzodiazepines** (Diazepam/Lorazepam) are first-line for agitation and cardiovascular toxicity. STRICTLY AVOID BETA-BLOCKERS.")
        elif top_toxidrome == "Cholinergic":
            st.write("💉 **Antidote Protocol:** **Atropine** escalating doses until airway secretions clear. Follow with **Pralidoxime (2-PAM)**.")
