import streamlit as st

st.set_page_config(page_title="Toxidrome Diagnostic Engine", layout="wide")

st.title("☠️ Toxidrome Diagnostic & Antidote Engine")
st.markdown("A rapid clinical decision-support tool for emergency toxicology and overdose management.")
st.markdown("---")

st.subheader("1. Patient Presentation (Vitals & Exam)")
st.info("Select the predominant clinical signs presenting in the emergency department.")

col1, col2, col3 = st.columns(3)
with col1:
    pupils = st.radio("Pupils (Mydriasis/Miosis)", ["Normal", "Pinpoint (Constricted)", "Dilated"])
    heart_rate = st.radio("Heart Rate", ["Normal", "Bradycardia (<60)", "Tachycardia (>100)"])
with col2:
    skin = st.radio("Skin/Mucous Membranes", ["Normal", "Dry / Hot", "Sweaty (Diaphoretic)"])
    respirations = st.radio("Respiratory Rate", ["Normal", "Depressed (<12)", "Elevated"])
with col3:
    mental_status = st.radio("Mental Status", ["Normal", "CNS Depression / Coma", "Agitated / Delirious"])
    bowel_sounds = st.radio("Bowel Sounds", ["Normal", "Absent / Decreased", "Hyperactive"])

if st.button("Run Diagnostic Algorithm", type="primary"):
    st.markdown("---")
    st.subheader("2. Diagnostic Output & Clinical Protocol")
    
    # -----------------------------------------
    # CLINICAL LOGIC ENGINE
    # -----------------------------------------
    toxidrome = "Unknown or Mixed Presentation"
    antidote = "Supportive care. Consider calling Poison Control."
    mechanism = ""
    
    # Opioid Logic
    if pupils == "Pinpoint (Constricted)" and respirations == "Depressed (<12)" and (mental_status == "CNS Depression / Coma" or heart_rate == "Bradycardia (<60)"):
        toxidrome = "Opioid Toxicity"
        antidote = "**Naloxone (Narcan)**. Initial dose: 0.4 to 2 mg IV/IM/IN. Repeat every 2-3 minutes as needed. Goal is adequate ventilation, not necessarily a fully awake patient."
        mechanism = "Mu-opioid receptor agonism leading to profound CNS and respiratory depression."
        
    # Anticholinergic Logic
    elif pupils == "Dilated" and skin == "Dry / Hot" and heart_rate == "Tachycardia (>100)" and mental_status == "Agitated / Delirious":
        toxidrome = "Anticholinergic Toxicity"
        antidote = "**Physostigmine**. 0.5 to 2 mg IV slowly over 5 minutes. (Avoid if TCA overdose is suspected due to risk of asystole). Benzodiazepines for agitation."
        mechanism = "Competitive antagonism of acetylcholine at central and peripheral muscarinic receptors (Classic mnemonic: 'Blind as a bat, mad as a hatter, red as a beet, hot as a hare, dry as a bone')."
        
    # Cholinergic Logic
    elif pupils == "Pinpoint (Constricted)" and skin == "Sweaty (Diaphoretic)" and bowel_sounds == "Hyperactive":
        toxidrome = "Cholinergic Toxicity (e.g., Organophosphates)"
        antidote = "**Atropine** (for muscarinic symptoms) starting at 2-5 mg IV, doubling dose every 5 mins until airway secretions clear. Followed by **Pralidoxime (2-PAM)** for nicotinic symptoms."
        mechanism = "Inhibition of acetylcholinesterase, leading to massive acetylcholine accumulation at synapses (SLUDGE syndrome)."
        
    # Sympathomimetic Logic
    elif pupils == "Dilated" and skin == "Sweaty (Diaphoretic)" and heart_rate == "Tachycardia (>100)" and mental_status == "Agitated / Delirious":
        toxidrome = "Sympathomimetic Toxicity (e.g., Cocaine, Amphetamines)"
        antidote = "**Benzodiazepines** (e.g., Diazepam or Lorazepam) for agitation, seizures, and tachycardia. **Strictly avoid beta-blockers** due to the risk of unopposed alpha-receptor stimulation."
        mechanism = "Excessive catecholamine release or reuptake inhibition causing severe sympathetic overdrive."

    # -----------------------------------------
    # UI RENDERING
    # -----------------------------------------
    if toxidrome != "Unknown or Mixed Presentation":
        st.error(f"### 🚨 Most Likely Toxidrome: {toxidrome}")
        st.success(f"**💉 Antidote Protocol:**\n {antidote}")
        st.info(f"**🔬 Pharmacological Mechanism:**\n {mechanism}")
    else:
        st.warning(f"### ⚠️ {toxidrome}")
        st.write("The selected symptoms do not perfectly match a classic, isolated toxidrome. This may indicate a polypharmacy overdose or an alternate medical etiology.")
        st.write(antidote)

    st.markdown("---")
    st.caption("Disclaimer: This tool is a Proof of Concept for portfolio demonstration only. It is not a substitute for clinical judgment or official poison control guidelines.")
