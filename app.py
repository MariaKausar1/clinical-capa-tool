import streamlit as st
from datetime import datetime, timedelta
from fpdf import FPDF

# --- 1. Comprehensive GCP Database ---
# (Keep your entire deviation_db dictionary here exactly as it was)
deviation_db = {
    "Informed Consent": {
        "Unsigned consent form prior to procedures": {
            "classification": "Major Violation",
            "timeline_days": 1,
            "irb_type": "Expedited",
            "action": "Halt procedures immediately until valid consent is obtained. Notify the sponsor."
        }
    }
    # ... (include the rest of the database we built previously) ...
}

# --- 2. PDF Generation Engine ---
def create_capa_pdf(date, category, issue, classification, irb, action, deadline):
    """Generates a formatted PDF report and returns it as bytes."""
    pdf = FPDF()
    pdf.add_page()
    
    # Document Header
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, txt="Protocol Deviation & CAPA Initial Report", ln=True, align="C")
    pdf.line(10, 22, 200, 22)
    pdf.ln(10)
    
    # Body Content
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, txt="Date of Discovery:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=date.strftime('%d %b %Y'), ln=True)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, txt="Primary Category:")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=category)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, txt="Specific Incident:")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=issue)
    
    pdf.ln(5)
    
    # Assessment Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, txt="Regulatory Assessment", ln=True)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, txt="Severity Level:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=classification, ln=True)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, txt="IRB Reporting:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=irb, ln=True)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, txt="Action Deadline:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=deadline.strftime('%d %b %Y'), ln=True)
    
    pdf.ln(5)
    
    # Action Plan
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, txt="Required Immediate Action", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=action)
    
    # Return the generated PDF as a byte string for the download button
    return bytes(pdf.output())

# --- 3. Frontend Layout ---
st.set_page_config(page_title="GCP Deviation Matrix", layout="centered")

st.title("GCP Protocol Deviation Matrix")
st.write("Determine severity classifications and instantly generate initial CAPA reports.")

st.divider()

st.header("Incident Details")

primary_category = st.selectbox("Select Primary Category", options=list(deviation_db.keys()))
specific_issues = list(deviation_db[primary_category].keys())
selected_issue = st.selectbox("Select Specific Issue", options=specific_issues)
discovery_date = st.date_input("Date of Discovery", value=datetime.today())

# --- 4. Assessment & Export Logic ---
if st.button("Assess Deviation", type="primary"):
    st.divider()
    
    incident_data = deviation_db[primary_category][selected_issue]
    classification = incident_data["classification"]
    timeline_days = incident_data["timeline_days"]
    irb_type = incident_data["irb_type"]
    action = incident_data["action"]
    due_date = discovery_date + timedelta(days=timeline_days)
    
    st.header("Assessment Results")
    
    col1, col2 = st.columns(2)
    col1.metric(label="Severity Classification", value=classification)
    col2.metric(label="IRB Reporting Category", value=irb_type)
    
    if classification == "Major Violation":
        st.error(f"Deadline for IRB/Sponsor Notification: {due_date.strftime('%d %b %Y')}")
    else:
        st.info(f"Include in next Continuing Review. Estimated Logging Date: {due_date.strftime('%d %b %Y')}")
        
    st.subheader("Required Immediate Action")
    st.write(action)
    
    st.divider()
    
    # Generate the PDF bytes quietly in the background
    pdf_bytes = create_capa_pdf(
        discovery_date, 
        primary_category, 
        selected_issue, 
        classification, 
        irb_type, 
        action, 
        due_date
    )
    
    # Display the download button
    st.download_button(
        label="📄 Download Official CAPA Report",
        data=pdf_bytes,
        file_name=f"CAPA_Report_{discovery_date.strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
    )