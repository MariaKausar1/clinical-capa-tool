import streamlit as st
from methods import get_methodology

st.set_page_config(page_title="Research Proposal Builder", layout="wide")
st.title("🔬 AI Clinical Research Proposal Builder")

field = st.selectbox("Select Research Field", ["Oncology", "Pediatrics", "Other"])
study_type = st.radio("Study Type", ["Prospective", "Retrospective"])

if st.button("Generate Professional Proposal"):
    data = get_methodology(field, study_type)
    
    proposal_text = f"""
    ==================================================
    CLINICAL RESEARCH PROPOSAL: {field.upper()}
    ==================================================
    
    1. STUDY OVERVIEW
    Type: {study_type}
    Field: {field}
    
    2. METHODOLOGY
    {data['methodology']}
    
    3. DATA COLLECTION PLAN
    {data['data_collection']}
    
    4. ETHICAL CONSIDERATIONS
    {data['ethics']}
    
    ==================================================
    """
    
    st.success("Proposal Generated Successfully!")
    st.text_area("Final Draft Preview:", value=proposal_text, height=400)
    
    st.download_button("📥 Download Formal Proposal (.txt)", proposal_text, "Clinical_Proposal.txt")
