import streamlit as st

st.set_page_config(page_title="Research Proposal Builder", layout="wide")
st.title("🔬 AI Clinical Research Proposal Builder")

field = st.selectbox("Select Research Field", ["Oncology", "Cardiology", "Pediatrics", "Pharmacology"])
study_type = st.radio("Study Type", ["Prospective", "Retrospective", "Observational"])

if st.button("Generate Proposal Structure"):
    with st.spinner("Drafting your research framework..."):
        # The generated content
        proposal_text = f"""
        RESEARCH PROPOSAL
        Field: {field}
        Study Type: {study_type}
        
        Objective: To evaluate clinical outcomes and efficacy metrics.
        Hypothesis: Implementation of the study intervention will yield statistically significant improvements.
        Methodology: A {study_type.lower()} design will be employed to collect primary clinical data.
        """
        
        st.success("Proposal Structure Generated:")
        st.text_area("Draft Content:", value=proposal_text, height=300)
        
        # Export Button
        st.download_button(
            label="📥 Download Research Proposal (.txt)",
            data=proposal_text,
            file_name="Research_Proposal.txt",
            mime="text/plain"
        )
