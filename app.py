# app.py
import streamlit as st
from database import master_taxonomy

# Agent 1: Classifier (Identifies the Category)
def agent_classify(text):
    text = text.lower()
    for cat in master_taxonomy:
        if cat.lower() in text or any(word in text for word in cat.lower().split()):
            return cat
    return "Protocol Deviation"

# Agent 2: Analyst (Extracts Risk & Root Cause)
def agent_analyze(cat, text):
    category_data = master_taxonomy.get(cat, {})
    # Fallback to the first issue if specific mapping isn't found
    issue_key = list(category_data.keys())[0] if category_data else "General Deviation"
    return category_data.get(issue_key, {
        "root_cause": "Undetermined", 
        "risk": "Medium", 
        "action": "Document and notify monitor.", 
        "gcp_ref": "N/A"
    })

# --- UI Setup ---
st.set_page_config(page_title="QMS Agent", layout="wide")
st.title("🏥 Enterprise QMS Agent Framework")
st.markdown("Automated clinical compliance assessment powered by modular agents.")

user_input = st.text_area("Enter incident details:", placeholder="e.g., Patient randomized despite failed screening labs...")

if st.button("Run Multi-Agent Workflow", type="primary"):
    with st.status("Agents processing compliance data...", expanded=True) as status:
        st.write("Agent 1: Classifying Category...")
        cat = agent_classify(user_input)
        
        st.write("Agent 2: Analyzing Risk & Root Cause...")
        analysis = agent_analyze(cat, user_input)
        
        status.update(label="Analysis Complete", state="complete")

    # Display Results
    st.subheader(f"Classification: {cat}")
    col1, col2 = st.columns(2)
    col1.metric("Risk Level", analysis['risk'])
    col2.write(f"**Root Cause Analysis:** {analysis['root_cause']}")
    
    st.info(f"**Recommended CAPA Action:** {analysis['action']}")
    st.caption(f"Regulatory Justification: {analysis['gcp_ref']}")
