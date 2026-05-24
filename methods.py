# methods.py

def get_methodology(field, study_type):
    # Expanded professional templates
    templates = {
        "Oncology": {
            "methodology": "This study employs a prospective design to evaluate clinical efficacy. Assessment is based on RECIST 1.1 criteria, with primary endpoints defined as Progression-Free Survival (PFS) and Objective Response Rate (ORR).",
            "data_collection": "Electronic Case Report Forms (eCRF) will capture patient demographics, tumor assessment logs, and adverse event profiles.",
            "ethics": "Given the high-risk nature of oncology interventions, strict adherence to GCP safety monitoring, continuous benefit-risk assessment, and rapid SAE reporting is mandatory."
        },
        "Pediatrics": {
            "methodology": "The study utilizes an age-stratified, prospective recruitment strategy, focusing on physiological growth trajectories and pharmacokinetic developmental milestones.",
            "data_collection": "Data collection includes longitudinal growth tracking, weight-based dosage adjustments, and age-appropriate quality-of-life assessments.",
            "ethics": "Informed consent is obtained from legal guardians, with documented participant assent and strict adherence to the Declaration of Helsinki regarding vulnerable populations."
        }
    }
    
    # Default template
    default = {
        "methodology": f"A {study_type.lower()} design will be employed to ensure robust data collection and objective analysis of study endpoints.",
        "data_collection": "Clinical data will be documented via source-verified electronic systems.",
        "ethics": "All procedures will be conducted in accordance with ICH-GCP guidelines and institutional IRB approval."
    }
    
    return templates.get(field, default)
