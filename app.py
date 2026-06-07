import streamlit as st

st.set_page_config(page_title="Toxicology Search Engine", layout="wide")

# --- CUSTOM CSS (Clean, Enterprise UI) ---
st.markdown("""
    <style>
    .critical-alert { background-color: #721c24; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #dc3545; margin-bottom: 15px;}
    .section-header { font-size: 1.1rem; font-weight: 600; color: #00BFFF; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 1.5rem; margin-bottom: 0.5rem; border-bottom: 1px solid #444; padding-bottom: 4px; }
    .diagnostic-card { border: 1px solid #dee2e6; border-radius: 6px; padding: 16px; background-color: #f8f9fa; }
    .search-tag { background-color: #e9ecef; padding: 4px 8px; border-radius: 4px; font-size: 0.85rem; color: #495057; margin-right: 5px; display: inline-block; margin-bottom: 5px;}
    </style>
""", unsafe_allow_html=True)

# --- 1. THE EXPANDED CLINICAL DATABASE ---
TOXICOLOGY_DB = {
    "Opioid": {
        "substances": ["Heroin", "Fentanyl", "Oxycodone", "Morphine", "Methadone", "Buprenorphine"],
        "hallmarks": ["Pinpoint pupils", "Respiratory depression (<12 bpm)", "CNS depression / Coma", "Bradycardia"],
        "antidote": "Naloxone",
        "dose": "0.04 - 0.4 mg IV (titrate to effect).",
        "goal": "Adequate spontaneous ventilation (not full arousal).",
        "warnings": "Observe for re-sedation (naloxone half-life is ~30-81 mins). Escalate airway management if refractory hypoxia persists."
    },
    "Acetaminophen (APAP)": {
        "substances": ["Tylenol", "Paracetamol", "APAP", "NyQuil", "Percocet"],
        "hallmarks": ["Nausea / Vomiting", "Right Upper Quadrant (RUQ) Pain", "Elevated AST/ALT", "Asymptomatic (Early Stage)"],
        "antidote": "N-acetylcysteine (NAC)",
        "dose": "IV Protocol: 150 mg/kg over 1 hr, then 50 mg/kg over 4 hrs, then 100 mg/kg over 16 hrs.",
        "goal": "Prevent fulminant hepatic failure by replenishing glutathione.",
        "warnings": "Plot 4-hour serum APAP level on the Rumack-Matthew Nomogram to determine if NAC is indicated."
    },
    "Anticholinergic": {
        "substances": ["Benadryl", "Diphenhydramine", "Atropine", "Scopolamine", "TCA Antidepressants"],
        "hallmarks": ["Dilated pupils", "Dry / Flushed skin", "Tachycardia", "Agitation / Delirium", "Decreased / Absent bowel sounds"],
        "antidote": "Supportive Care & Physostigmine",
        "dose": "Physostigmine 0.5 - 2 mg IV over 5 mins (for severe delirium).",
        "goal": "Control severe central nervous system agitation.",
        "warnings": "ABSOLUTE CONTRAINDICATION: Do NOT administer physostigmine if QRS > 100ms or TCA overdose is suspected."
    },
    "Sympathomimetic": {
        "substances": ["Cocaine", "Methamphetamine", "Adderall", "MDMA", "Vyvanse"],
        "hallmarks": ["Dilated pupils", "Diaphoresis (Sweaty)", "Tachycardia", "Agitation / Delirium", "Hyperthermia (>39C)", "Hypertension"],
        "antidote": "Benzodiazepines",
        "dose": "Diazepam 5-10 mg IV or Lorazepam 1-2 mg IV.",
        "goal": "Reduce sympathetic outflow and prevent seizures/hyperthermia.",
        "warnings": "ABSOLUTE CONTRAINDICATION: Beta-blockers (risk of unopposed alpha stimulation leading to severe ischemia)."
    },
    "Cholinergic": {
        "substances": ["Organophosphates", "Pesticides", "Sarin Gas", "Nerve Agents", "Donepezil"],
        "hallmarks": ["Pinpoint pupils", "Diaphoresis (Sweaty)", "Hyperactive bowel sounds", "Tachypnea (>20 bpm)", "Excessive Salivation / Secrections"],
        "antidote": "Atropine & Pralidoxime (2-PAM)",
        "dose": "Atropine 2 - 5 mg IV. Double every 5 minutes.",
        "goal": "Titrate Atropine specifically to the clearing of respiratory secretions.",
        "warnings": "Do not stop atropine based on heart rate or pupil size. Focus on clearing the airway."
    },
    "Serotonin Syndrome": {
        "substances": ["SSRI", "Lexapro", "Zoloft", "MAOI", "Linezolid", "Dextromethorphan"],
        "hallmarks": ["Agitation / Delirium", "Tachycardia", "Diaphoresis (Sweaty)", "Hyperactive bowel sounds", "Hyperthermia (>39C)", "Muscle Clonus / Rigidity"],
        "antidote": "Cyproheptadine & Benzodiazepines",
        "dose": "Cyproheptadine 12 mg PO/NG initially, then 2 mg q2h if symptomatic.",
        "goal": "Control agitation, hyperthermia, and reduce muscle rigidity.",
        "warnings": "Do NOT use physical restraints. Avoid antipyretics (fever is driven by muscle activity, not the hypothalamus)."
    }
}

# --- 2. BUILD SEARCH INDEXES ---
# Create a searchable list of all drugs and toxidromes
search_directory = []
drug_to_tox_map = {}
for tox_name, data in TOXICOLOGY_DB.items():
    search_directory.append(tox_name)
    for drug in data["substances"]:
        search_directory.append(drug)
        drug_to_tox_map[drug] = tox_name # Maps a drug back to its parent toxidrome

# Create a master list of all unique symptoms for the solver
all_symptoms = set()
for data in TOXICOLOGY_DB.values():
    for h in data["hallmarks"]:
        all_symptoms.add(h)
all_symptoms = sorted(list(all_symptoms))

# --- 3. MAIN UI HEADER ---
st.markdown("<div style='font-size: 2.2rem; font-weight: 800; color: #00BFFF; border-bottom: 3px solid #00BFFF; padding-bottom: 10px; margin-bottom: 20px;'>Universal Toxicology Search Engine</div>", unsafe_allow_html=True)

# --- 4. TABBED NAVIGATION ---
tab1, tab2 = st.tabs(["🔍 Direct Protocol Search", "🧠 Symptom Solver Engine"])

# ==========================================
# TAB 1: DIRECT PROTOCOL SEARCH
# ==========================================
with tab1:
    st.markdown("### Search by Drug, Class, or Toxidrome")
    # Universal Search Bar
    search_query = st.selectbox("Type or select a substance (e.g., Fentanyl, Tylenol, Anticholinergic):", [""] + sorted(search_directory))
    
    if search_query != "":
        st.markdown("---")
        # Figure out which toxidrome to display
        target_tox = drug_to_tox_map.get(search_query, search_query)
        data = TOXICOLOGY_DB[target_tox]
        
        # Display Results
        st.markdown(f"<div style='font-size: 1.8rem; font-weight: bold; color: #333;'>{target_tox} Protocol</div>", unsafe_allow_html=True)
        if search_query != target_tox:
            st.caption(f"↳ Triggered by search for: {search_query}")
            
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            st.markdown("<div class='section-header'>Clinical Presentation</div>", unsafe_allow_html=True)
            for h in data["hallmarks"]:
                st.markdown(f"• {h}")
                
            st.markdown("<br><div class='section-header'>Common Causative Agents</div>", unsafe_allow_html=True)
            tags_html = "".join([f"<span class='search-tag'>{drug}</span>" for drug in data["substances"]])
            st.markdown(tags_html, unsafe_allow_html=True)

        with col_b:
            st.markdown("<div class='section-header'>Treatment Protocol</div>", unsafe_allow_html=True)
            st.markdown(f"**💉 Primary Antidote:** {data['antidote']}")
            st.markdown(f"**⚖️ Dosing:** {data['dose']}")
            st.markdown(f"**🎯 Clinical Goal:** {data['goal']}")
            
            st.markdown("<br><div class='section-header'>Critical Warnings</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='critical-alert'>⚠️ {data['warnings']}</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: SYMPTOM SOLVER ENGINE
# ==========================================
with tab2:
    st.markdown("### Reverse Lookup: Enter Patient Findings")
    # Multi-select search bar for symptoms
    selected_symptoms = st.multiselect("Select all presenting signs and symptoms:", all_symptoms)
    
    if len(selected_symptoms) > 0:
        st.markdown("---")
        
        # Scoring Algorithm
        results = []
        for tox_name, data in TOXICOLOGY_DB.items():
            matches = [s for s in selected_symptoms if s in data["hallmarks"]]
            if len(matches) > 0:
                results.append({
                    "tox": tox_name,
                    "score": len(matches),
                    "matches": matches,
                    "missing": [h for h in data["hallmarks"] if h not in selected_symptoms],
                    "data": data
                })
                
        # Sort by best match
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        
        if len(results) > 0:
            top_match = results[0]
            st.markdown(f"#### 🔍 Top Differential: **{top_match['tox']}** ({top_match['score']} symptoms matched)")
            
            col_x, col_y = st.columns(2)
            with col_x:
                st.markdown("<div class='diagnostic-card'>", unsafe_allow_html=True)
                st.markdown("**Matched Findings:**")
                for m in top_match["matches"]: st.markdown(f"✅ {m}")
                st.markdown("**Missing Classic Hallmarks:**")
                if len(top_match["missing"]) == 0:
                    st.markdown("None. Classic presentation.")
                else:
                    for m in top_match["missing"]: st.markdown(f"❌ {m}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col_y:
                st.markdown("<div class='diagnostic-card'>", unsafe_allow_html=True)
                st.markdown(f"**Recommended Intervention:** {top_match['data']['antidote']}")
                st.markdown(f"**Dosing:** {top_match['data']['dose']}")
                st.markdown(f"**Warning:** {top_match['data']['warnings']}")
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Show secondary differentials if they exist
            if len(results) > 1:
                st.markdown("<br>**Secondary Considerations:**", unsafe_allow_html=True)
                for res in results[1:3]: # Show next 2 matches
                    st.caption(f"- {res['tox']} ({res['score']} matches)")
