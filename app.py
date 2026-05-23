import streamlit as st
from datetime import datetime, timedelta
from fpdf import FPDF

# IMPORT the database from the new file we just created
from database import deviation_db

# --- PDF Generation Engine ---
def create_capa_pdf(date, category, issue, classification, irb, gcp_ref, action, deadline):
    """Generates a formatted PDF report and returns it as bytes."""
    pdf = FPDF()
    pdf.add_page()
    
    # Document Header
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, "Protocol Deviation & CAPA Initial Report", ln=1, align="C")
    pdf.line(10, 22, 200, 22)
    pdf.ln(10)
    
    # Body Content
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "Date of Discovery:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, date.strftime('%d %b %Y'), ln=1)
    pdf.ln(4)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "Primary Category:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, category)
    pdf.ln(4)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "Specific Incident:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, issue)
    pdf.ln(8)
    
    # Assessment Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Regulatory Assessment", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "Severity Level:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, classification, ln=1)
    pdf.ln(4)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "IRB Reporting:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, irb, ln=1)
    pdf.ln(8)

    # GCP Reference Section
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, "Regulatory Justification:", ln=1)
    pdf.set_font("Arial", style="I", size=11)
    pdf.multi_cell(0, 8, f'"{gcp_ref}"')
    pdf.ln(8)
    
    # Action Plan
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Required Immediate Action", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, action)
    
    return bytes(pdf.output())

# --- Frontend Layout ---
st.set_page_config(page_title="GCP Deviation Matrix", page_icon="🏥", layout="wide")

with st.sidebar:
    st.title("⚙️ System Info")
    st.info("This tool cross-references trial incidents against FDA, EMA, and MHRA inspection standards to determine compliance severity.")
    st.divider()
    st.write("**Capabilities:**")
    st.write("✔️ Severity Classification")
    st.write("✔️ 21 CFR & ICH GCP E6(R2) Citations")
    st.write("✔️ CAPA PDF Generation")

st.title("🏥 GCP Protocol Deviation Matrix")
st.markdown("Determine severity classifications, pull exact regulatory citations, and instantly generate initial CAPA reports based on global inspection findings.")
st.divider()

st.subheader("📝 Incident Details")
col1, col2 = st.columns([2, 1])

with col1:
    primary_category = st.selectbox("Select Primary Category", options=list(deviation_db.keys()))
    specific_issues = list(deviation_db[primary_category].keys())
    selected_issue = st.selectbox("Select Specific Issue", options=specific_issues)

with col2:
    discovery_date = st.date_input("Date of Discovery", value=datetime.today())
    st.markdown("<br>", unsafe_allow_html=True)
    assess_button = st.button("Assess Deviation", type="primary", use_container_width=True)

# --- Assessment & Export Logic ---
if assess_button:
    st.divider()
    st.subheader("📊 Assessment Results")
    
    incident_data = deviation_db[primary_category][selected_issue]
    classification = incident_data["classification"]
    timeline_days = incident_data["timeline_days"]
    irb_type = incident_data["irb_type"]
    gcp_ref = incident_data["gcp_ref"]
    action = incident_data["action"]
    due_date = discovery_date + timedelta(days=timeline_days)
    
    res_col1, res_col2 = st.columns(2)
    res_col1.metric(label="Severity Classification", value=classification)
    res_col2.metric(label="IRB Reporting Category", value=irb_type)
    
    st.markdown("### 🏛️ Regulatory Justification")
    st.info(f"**{gcp_ref}**")
        
    st.markdown("### ⚡ Required Immediate Action")
    st.write(action)
    
    st.divider()
    
    pdf_bytes = create_capa_pdf(
        discovery_date, 
        primary_category, 
        selected_issue, 
        classification, 
        irb_type,
        gcp_ref,
        action, 
        due_date
    )
    
    st.download_button(
        label="📄 Download Official CAPA Report",
        data=pdf_bytes,
        file_name=f"CAPA_Report_{discovery_date.strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        type="primary"
    )
