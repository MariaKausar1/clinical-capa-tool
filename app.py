import streamlit as st
from datetime import datetime, timedelta
from fpdf import FPDF
from database import deviation_db

# --- PDF Generation (Same as before) ---
def create_capa_pdf(date, category, issue, description, classification, irb, gcp_ref, action, deadline):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, "Protocol Deviation & CAPA Report", ln=1, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, f"Category: {category}", ln=1)
    pdf.multi_cell(0, 8, f"Issue: {issue}")
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "Description:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, description)
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "Regulatory Justification:", ln=1)
    pdf.set_font("Arial", style="I", size=11)
    pdf.multi_cell(0, 8, gcp_ref)
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "Required Action:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, action)
    return bytes(pdf.output())

# --- Frontend ---
st.set_page_config(page_title="Smart GCP Matrix", layout="wide")
st.title("🏥 Smart GCP Deviation Assistant")

# AI-Powered Input
user_input = st.text_area("Describe the incident:", placeholder="e.g., Patient received investigational product before eligibility labs were reviewed.")

if st.button("Analyze Incident", type="primary"):
    # Simple Keyword Inference Logic
    detected_cat = "Protocol Compliance" # Default
    detected_issue = "Visit Outside Window" # Default
    
    if "consent" in user_input.lower():
        detected_cat, detected_issue = "Informed Consent (ICF)", "Unsigned consent form prior to any study procedures"
    elif "sae" in user_input.lower() or "report" in user_input.lower():
        detected_cat, detected_issue = "Safety Reporting", "Delayed SAE Reporting"
    
    data = deviation_db[detected_cat][detected_issue]
    
    st.write(f"**Detected Category:** {detected_cat}")
    st.write(f"**Detected Issue:** {detected_issue}")
    st.success(f"**Classification:** {data['classification']}")
    
    pdf_bytes = create_capa_pdf(
        datetime.today(), detected_cat, detected_issue, user_input,
        data['classification'], data['irb_type'], data['gcp_ref'], data['action'], 
        datetime.today() + timedelta(days=data['timeline_days'])
    )
    
    st.download_button("📄 Download Report", pdf_bytes, "CAPA.pdf")
