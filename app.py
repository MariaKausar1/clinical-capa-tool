import streamlit as st
from datetime import datetime, timedelta
from fpdf import FPDF

# --- 1. Comprehensive GCP Database (FDA/EMA/MHRA Backed) ---
deviation_db = {
    "Informed Consent (ICF)": {
        "Unsigned consent form prior to any study procedures": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Halt all study procedures immediately. Obtain valid consent. Notify sponsor and IRB."
        },
        "Used expired, obsolete, or unapproved version of consent form": {
            "classification": "Major Violation", "timeline_days": 2, "irb_type": "Expedited",
            "action": "Re-consent the subject with the correct IRB-approved version at the next earliest contact."
        },
        "Consent obtained by staff not listed on the Delegation of Authority (DOA) log": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "action": "PI must review the consent. Update DOA log immediately. Re-train staff on delegation rules."
        },
        "Subject did not personally date the consent form (dated by coordinator)": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "action": "Write a Note to File (NTF). Re-train staff that subjects must personally date the ICF."
        },
        "Missing checkmarks in optional study sections (e.g., pharmacogenomics)": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "action": "Clarify subject's intent at next visit. Do not perform optional procedures until clarified."
        }
    },
    "Eligibility & Enrollment": {
        "Subject randomized who failed Inclusion/Exclusion criteria": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Notify Medical Monitor immediately. Assess if subject needs to be withdrawn for safety."
        },
        "Subject randomized before all screening lab results were received/reviewed": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "PI must review labs immediately. If labs violate eligibility, halt IP and notify sponsor."
        },
        "Enrolled a vulnerable subject (e.g., prisoner, minor) without prior IRB approval": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Immediately suspend subject participation. Report to IRB and Sponsor as a critical compliance breach."
        }
    },
    "Investigational Product (IP) Management": {
        "Incorrect dose of IP administered to patient": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Monitor patient for AEs. Alert Medical Monitor within 24 hours. Document exact dose given."
        },
        "Dispensed IP to the wrong subject": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Contact both subjects immediately to retrieve wrong IP. Assess safety and alert sponsor."
        },
        "IP administered after its expiration date": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Notify Medical Monitor. Document in source. Check all site inventory for other expired IP."
        },
        "Temperature excursion in storage fridge/freezer": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Quarantine affected IP. Do not dispense until sponsor reviews data and approves stability."
        },
        "Subject lost IP or spilled liquid IP at home": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "action": "Document in accountability log. Dispense replacement IP per protocol guidelines."
        }
    },
    "Blinding & Randomization": {
        "Accidental unblinding of study staff or subject": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Notify sponsor immediately. Unblinded staff must be removed from subsequent subject assessments."
        },
        "Subject randomized out of sequence (wrong IRT kit dispensed)": {
            "classification": "Major Violation", "timeline_days": 2, "irb_type": "Expedited",
            "action": "Notify sponsor's IRT/IWRS team to correct the system assignment. Do not alter physical kits."
        }
    },
    "Safety Reporting & Pharmacovigilance": {
        "Failure to report a Serious Adverse Event (SAE) within 24 hours of site awareness": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Submit SAE report immediately. Draft a CAPA detailing the root cause of the delay."
        },
        "Missed reporting of a patient pregnancy": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Report to sponsor immediately. Halt IP administration immediately per protocol."
        },
        "Adverse event (AE) noted in progress notes but not entered into EDC": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "action": "Enter the AE into the EDC. Re-train staff on timely data entry requirements."
        }
    },
    "Protocol Compliance & Study Procedures": {
        "Subject took prohibited concomitant medication": {
            "classification": "Major Violation", "timeline_days": 2, "irb_type": "Expedited",
            "action": "Consult Medical Monitor regarding potential drug interactions and subject withdrawal criteria."
        },
        "Patient visit occurred outside the protocol-allowed window": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "action": "Document the out-of-window visit in source and deviation log. No immediate alert required."
        },
        "Missed primary endpoint assessment (e.g., missed MRI or tumor scan)": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "action": "Notify sponsor immediately. Attempt to reschedule scan as close to the window as clinically valid."
        },
        "Missed non-critical safety lab draw or vital signs": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "action": "Document the missed assessment in source notes. Ensure it is captured at the next visit."
        }
    },
    "Biological Samples & Laboratory": {
        "PK/PD blood sample drawn at the wrong time interval": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "action": "Document the exact time drawn in the lab requisition and EDC so statisticians can adjust models."
        },
        "Samples processed or centrifuged incorrectly (e.g., wrong RPM)": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "action": "Notify central lab. The sample may be unviable. Re-train phlebotomy/lab staff on lab manual."
        },
        "Samples shipped at ambient temperature instead of on dry ice": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "action": "Notify central lab to flag the shipment. Document the temperature deviation."
        }
    },
    "Equipment & Calibration": {
        "Used uncalibrated or expired equipment (e.g., expired ECG machine or scale)": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "action": "Take equipment out of service immediately. Schedule recalibration. Assess impact on collected data."
        }
    },
    "Source Documentation & Data Integrity (ALCOA+)": {
        "Unauthorized correction of source data (e.g., use of white-out or scribbling)": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "action": "Draft CAPA. Retrain staff on GCP corrections (single line through, initial, date, reason)."
        },
        "Source documents missing, lost, or destroyed": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Notify sponsor and IRB immediately. Attempt to reconstruct data from EMR if legally permissible."
        },
        "Data entered in EDC by staff without system access rights (sharing passwords)": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Revoke access. Notify sponsor Data Management immediately. This is a severe 21 CFR Part 11 breach."
        }
    },
    "Regulatory & IRB": {
        "Implemented protocol change without prior IRB approval": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Unless done to eliminate an immediate hazard, halt the unapproved procedure and notify IRB."
        },
        "Principal Investigator (PI) failed to sign FDA Form 1572 before trial start": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "action": "Halt enrollment. Obtain signature immediately. Notify sponsor regulatory team."
        }
    }
}

# --- 2. PDF Generation Engine ---
def create_capa_pdf(date, category, issue, classification, irb, action, deadline):
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
    pdf.cell(50, 10, "Date of Discovery:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, date.strftime('%d %b %Y'), ln=1)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, "Primary Category:")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, category)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, "Specific Incident:")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, issue)
    
    pdf.ln(5)
    
    # Assessment Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Regulatory Assessment", ln=1)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, "Severity Level:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, classification, ln=1)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, "IRB Reporting:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, irb, ln=1)
    
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, "Action Deadline:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, deadline.strftime('%d %b %Y'), ln=1)
    
    pdf.ln(5)
    
    # Action Plan
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Required Immediate Action", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, action)
    
    return bytes(pdf.output())

# --- 3. Frontend Layout ---
st.set_page_config(page_title="GCP Deviation Matrix", layout="centered")

st.title("GCP Protocol Deviation Matrix")
st.write("Determine severity classifications and instantly generate initial CAPA reports based on FDA, EMA, and MHRA inspection findings.")

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