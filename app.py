# app.py
import streamlit as st
from database import master_taxonomy

def get_risk_level(score):
    if score >= 81: return "Critical"
    if score >= 51: return "High"
    if score >= 21: return "Medium"
    return "Low"

st.set_page_config(page_title="Enterprise Compliance Engine", layout="wide")
st.title("🏥 Enterprise Compliance Engine")

user_input = st.text_area("Enter incident details:", height=200)

if st.button("Run Enterprise Assessment"):
    detected = []
    total_score = 0
    
    # Hierarchical detection
    for issue, details in master_taxonomy.items():
        if issue.lower() in user_input.lower() or any(w in user_input.lower() for w in issue.split()):
            detected.append((issue, details))
            total_score += details['score']

    if detected:
        risk_level = get_risk_level(total_score)
        st.subheader(f"Classification: Protocol Deviation")
        st.metric("Risk Level", risk_level, delta=f"Score: {total_score}")
        
        for issue_name, data in detected:
            with st.expander(f"Detected: {issue_name}"):
                st.write(f"**Root Cause:** {data['root_causes']}")
                col1, col2 = st.columns(2)
                col1.write(f"**Corrective:** {', '.join(data['corrective'])}")
                col2.write(f"**Preventive:** {', '.join(data['preventive'])}")
                st.info(f"**Regulatory Justification:** {data['gcp_ref']}")
    else:
        st.warning("No compliance markers identified. Please refine incident description.")
