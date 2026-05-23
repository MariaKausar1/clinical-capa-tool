# --- Comprehensive Regulatory Database (FDA, EMA, MHRA, ICH GCP) ---
deviation_db = {
    "Informed Consent (ICF)": {
        "Unsigned consent form prior to any study procedures": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "FDA 21 CFR 50.27 & ICH GCP E6(R2) 4.8.8: Prior to clinical trial participation, the subject must sign and personally date the written informed consent form.",
            "action": "Halt all study procedures immediately. Obtain valid consent. Notify sponsor and IRB."
        },
        "Used expired, obsolete, or unapproved version of consent form": {
            "classification": "Major Violation", "timeline_days": 2, "irb_type": "Expedited",
            "gcp_ref": "ICH GCP E6(R2) 4.8.1: The investigator should not involve a subject in a trial before receiving IRB/IEC approval of the consent form.",
            "action": "Re-consent the subject with the correct IRB-approved version at the next earliest contact."
        },
        "Consent obtained by staff not listed on the Delegation of Authority (DOA) log": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "gcp_ref": "MHRA GCP Guide & ICH GCP E6(R2) 4.1.5: The investigator should maintain a list of appropriately qualified persons to whom trial-related duties have been delegated.",
            "action": "PI must review the consent. Update DOA log immediately. Re-train staff on delegation rules."
        },
        "Subject did not personally date the consent form (dated by coordinator)": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "gcp_ref": "FDA 21 CFR 50.27(a): A written consent document that embodies the elements of informed consent must be signed and dated by the subject.",
            "action": "Write a Note to File (NTF). Re-train staff that subjects must personally date the ICF."
        }
    },
    "Eligibility & Enrollment": {
        "Subject randomized who failed Inclusion/Exclusion criteria": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "FDA 21 CFR 312.60: An investigator is responsible for ensuring that an investigation is conducted according to the signed investigator statement and the investigational plan.",
            "action": "Notify Medical Monitor immediately. Assess if subject needs to be withdrawn for safety."
        },
        "Subject randomized before all screening lab results were received/reviewed": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "ICH GCP E6(R2) 4.5.1: The investigator should conduct the trial in compliance with the protocol agreed to by the sponsor and approved by the IRB/IEC.",
            "action": "PI must review labs immediately. If labs violate eligibility, halt IP and notify sponsor."
        },
        "Enrolled a vulnerable subject (e.g., prisoner, minor) without prior IRB approval": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "FDA 21 CFR 56.111(b): When some or all of the subjects are likely to be vulnerable, additional safeguards must be included in the study.",
            "action": "Immediately suspend subject participation. Report to IRB and Sponsor as a critical compliance breach."
        }
    },
    "Investigational Product (IP) Management": {
        "Incorrect dose of IP administered to patient": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "ICH GCP E6(R2) 4.6.4: The investigational product(s) should be used in accordance with the approved protocol.",
            "action": "Monitor patient for AEs. Alert Medical Monitor within 24 hours. Document exact dose given."
        },
        "Dispensed IP to the wrong subject": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "EMA Annex 13 (Manufacture of Investigational Medicinal Products): Systems must ensure blinding is maintained and the correct product is dispensed.",
            "action": "Contact both subjects immediately to retrieve wrong IP. Assess safety and alert sponsor."
        },
        "Temperature excursion in storage fridge/freezer not reported": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "ICH GCP E6(R2) 4.6.3: The investigator/institution should maintain records of the product's delivery, inventory at the site, and use.",
            "action": "Quarantine affected IP. Do not dispense until sponsor reviews data and approves stability."
        },
        "Missing daily temperature log entries": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "gcp_ref": "ICH GCP E6(R2) 4.6.3: Records should include dates, quantities, batch/serial numbers, and expiration dates.",
            "action": "Write a note to file. Check min/max thermometer to ensure no excursion occurred during gap."
        }
    },
    "Safety Reporting & Pharmacovigilance": {
        "Failure to report a Serious Adverse Event (SAE) within 24 hours": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "FDA 21 CFR 312.64(b) & ICH GCP 4.11.1: The investigator must immediately report to the sponsor any serious adverse event.",
            "action": "Submit SAE report immediately. Draft a CAPA detailing the root cause of the delay."
        },
        "Missed reporting of a patient pregnancy": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "ICH GCP E6(R2) 4.11.1: Immediate reports should be followed promptly by detailed, written reports.",
            "action": "Report to sponsor immediately. Halt IP administration immediately per protocol guidelines."
        }
    },
    "Protocol Compliance & Study Procedures": {
        "Subject took prohibited concomitant medication": {
            "classification": "Major Violation", "timeline_days": 2, "irb_type": "Expedited",
            "gcp_ref": "ICH GCP E6(R2) 4.5.1: The investigator should not implement any deviation from the protocol without prior review and documented approval.",
            "action": "Consult Medical Monitor regarding potential drug interactions and subject withdrawal criteria."
        },
        "Missed primary endpoint assessment (e.g., missed MRI or tumor scan)": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "gcp_ref": "FDA BIMO Compliance Program 7348.811: Investigators must adhere to protocol requirements for efficacy and safety endpoint capture.",
            "action": "Notify sponsor immediately. Attempt to reschedule scan as close to the window as clinically valid."
        },
        "Patient visit occurred outside the protocol-allowed window": {
            "classification": "Minor Deviation", "timeline_days": 365, "irb_type": "Routine (Annual)",
            "gcp_ref": "ICH GCP E6(R2) 4.5.3: The investigator should document and explain any deviation from the approved protocol.",
            "action": "Document the out-of-window visit in source and deviation log. No immediate alert required."
        }
    },
    "Source Documentation & Data Integrity (ALCOA+)": {
        "Unauthorized correction of source data (e.g., use of white-out or scribbling)": {
            "classification": "Major Violation", "timeline_days": 5, "irb_type": "Expedited",
            "gcp_ref": "ICH GCP E6(R2) 4.9.3: Any change to a CRF should be dated, initialed, and explained, and should not obscure the original entry (ALCOA+).",
            "action": "Draft CAPA. Retrain staff on GCP corrections (single line through, initial, date, reason)."
        },
        "Source documents missing, lost, or destroyed": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "FDA 21 CFR 312.62(b): An investigator is required to prepare and maintain adequate and accurate case histories.",
            "action": "Notify sponsor and IRB immediately. Attempt to reconstruct data from EMR if legally permissible."
        },
        "Data entered in EDC by staff without system access rights (sharing passwords)": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "FDA 21 CFR Part 11.30: Controls must be in place to ensure that only authorized individuals can use the system and electronically sign records.",
            "action": "Revoke access. Notify sponsor Data Management immediately. This is a severe Part 11 breach."
        }
    },
    "Regulatory & IRB": {
        "Implemented protocol change without prior IRB approval": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "FDA 21 CFR 56.108(a)(4): Ensure that changes in approved research are not initiated without IRB review and approval, except when necessary to eliminate apparent immediate hazards.",
            "action": "Unless done to eliminate an immediate hazard, halt the unapproved procedure and notify IRB."
        },
        "Principal Investigator (PI) failed to sign FDA Form 1572 before trial start": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "FDA 21 CFR 312.53(c): A sponsor shall obtain a signed investigator statement (Form FDA 1572) before permitting an investigator to begin participation.",
            "action": "Halt enrollment. Obtain signature immediately. Notify sponsor regulatory team."
        }
    },
    "Blinding & Randomization": {
        "Accidental unblinding of study staff or subject": {
            "classification": "Major Violation", "timeline_days": 1, "irb_type": "Expedited",
            "gcp_ref": "ICH GCP E6(R2) 4.7: The investigator should follow the trial's randomization procedures, if any, and should ensure that the code is broken only in accordance with the protocol.",
            "action": "Notify sponsor immediately. Unblinded staff must be removed from subsequent subject assessments."
        }
    }
}
