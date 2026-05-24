import streamlit as st

st.set_page_config(page_title="Research Proposal Builder", layout="wide")
st.title("🔬 AI Clinical Research Proposal Builder")

# Step 1: Selection
field = st.selectbox("Select Research Field", ["Oncology", "Cardiology", "Pediatrics", "Pharmacology"])
study_type = st.radio("Study Type", ["Prospective", "Retrospective", "Observational"])

# Step 2: Input Details
if st.button("Generate Proposal Structure"):
    st.subheader("Drafting your Proposal...")
    
    # This is the "Brain" of your app
    with st.spinner("Analyzing research parameters..."):
        # Here you can later connect to an AI API, 
        # but for now, we structure the output
        st.success("Proposal Structure Generated:")
        
        st.write(f"**Title:** A {study_type} analysis of [Disease] in {field}")
        st.write("**Objective:** To evaluate the clinical efficacy and safety outcomes.")
        st.write("**Hypothesis:** Implementation of [Intervention] will improve patient outcomes.")
        
        st.info("💡 Tip: You can now export this as a Word document or PDF.")
