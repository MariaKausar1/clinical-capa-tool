# database.py
master_taxonomy = {
    "Eligibility Violation": {
        "score": 40,
        "root_causes": "Failure to verify eligibility before dosing; Lack of pre-dose verification workflow.",
        "corrective": ["Notify sponsor and IRB/IEC", "Medical assessment of subject safety", "Document protocol deviation"],
        "preventive": ["Implement mandatory eligibility verification checklist", "Add electronic protocol workflow lock"],
        "gcp_ref": "ICH-GCP E6(R2) 4.5.1: Compliance with approved protocol and subject safety."
    },
    "Investigational Product Dosing Error": {
        "score": 30,
        "root_causes": "Inadequate staff training; Failure to follow administration guidelines.",
        "corrective": ["Report to medical monitor", "Assess subject for adverse effects"],
        "preventive": ["Conduct periodic compliance monitoring", "Retrain study coordinator and PI"],
        "gcp_ref": "ICH-GCP E6(R2) 4.6.1: Investigational product shall be used in accordance with the protocol."
    },
    "Late Sponsor Notification": {
        "score": 15,
        "root_causes": "Inadequate deviation escalation process.",
        "corrective": ["Immediate notification to sponsor", "Root cause analysis"],
        "preventive": ["Add deviation reporting timeline alerts"],
        "gcp_ref": "ICH-GCP E6(R2) 5.20.1: Non-compliance reporting requirements."
    },
    "Documentation Control Issue": {
        "score": 10,
        "root_causes": "Poor document version control.",
        "corrective": ["Quarantine outdated eligibility checklist"],
        "preventive": ["Introduce document version control audit"],
        "gcp_ref": "ALCOA+ Principles for Data Integrity."
    }
}
