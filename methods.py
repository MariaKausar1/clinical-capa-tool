# methods.py

def get_methodology(field, study_type):
    # Field-specific templates
    templates = {
        "Oncology": {
            "methodology": "This study utilizes RECIST 1.1 criteria to evaluate tumor response, with primary endpoints focused on Progression-Free Survival (PFS).",
            "ethics": "Strict adherence to safety monitoring and adverse event reporting is mandated given the high-risk nature of chemotherapeutic interventions."
        },
        "Pediatrics": {
            "methodology": "The study employs age-stratified recruitment and physiological growth monitoring as primary outcome measures.",
            "ethics": "Informed consent is obtained from legal guardians, with documented assent from pediatric participants where developmentally appropriate."
        },
        "Pharmacology": {
            "methodology": "A pharmacokinetic (PK) model will be utilized to assess drug plasma concentration-time profiles and bioavailability parameters.",
            "ethics": "Standardized monitoring of drug-drug interactions and patient compliance protocols will be strictly enforced."
        }
    }
    
    # Default return if field is not in templates
    default = {
        "methodology": f"A {study_type.lower()} design will be employed to ensure robust data collection and objective analysis of study endpoints.",
        "ethics": "All study procedures will be conducted in accordance with GCP guidelines and institutional review board (IRB) approval."
    }
    
    return templates.get(field, default)
