# database.py
master_taxonomy = {
    "Temperature Excursion": {
        "Storage out of range": {
            "root_cause": "Equipment failure or human oversight.",
            "risk": "High - Integrity of the investigational product is compromised.",
            "action": "Quarantine IP, notify sponsor, conduct stability assessment.",
            "gcp_ref": "ICH GCP E6(R2) 4.6.3"
        }
    },
    "Data Integrity": {
        "Unauthorized correction": {
            "root_cause": "Lack of training on ALCOA+ principles.",
            "risk": "Critical - Audit trail obfuscation.",
            "action": "Retrain staff, update SOPs, submit CAPA.",
            "gcp_ref": "FDA 21 CFR Part 11"
        }
    },
    "Safety Reporting": {
        "Delayed SAE Reporting": {
            "root_cause": "Communication breakdown between site and sponsor.",
            "risk": "High - Regulatory reporting non-compliance.",
            "action": "Submit SAE report, conduct root cause analysis, update training.",
            "gcp_ref": "ICH GCP E6(R2) 4.11.1"
        }
    },
    "Eligibility/Enrollment": {
        "Failed inclusion criteria": {
            "root_cause": "Inadequate review of medical history or lab data.",
            "risk": "High - Violation of study design and data validity.",
            "action": "Notify Medical Monitor, withdraw subject if required, log deviation.",
            "gcp_ref": "ICH GCP E6(R2) 4.5.1"
        }
    }
}
