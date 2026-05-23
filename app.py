# Robust Keyword Inference Logic
    detected_cat = "Protocol Compliance" # Default catch-all
    detected_issue = "Patient visit occurred outside the protocol-allowed window" # Default
    
    # Analyze text with multiple priority keywords
    text = user_input.lower()
    
    if "consent" in text:
        detected_cat, detected_issue = "Informed Consent (ICF)", "Unsigned consent form prior to any study procedures"
    elif "sae" in text or "adverse event" in text or "report" in text:
        detected_cat, detected_issue = "Safety Reporting", "Failure to report a Serious Adverse Event (SAE) within 24 hours"
    elif "eligibility" in text or "criteria" in text or "glucose" in text:
        detected_cat, detected_issue = "Eligibility & Enrollment", "Subject randomized who failed Inclusion/Exclusion criteria"
    elif "temperature" in text or "fridge" in text:
        detected_cat, detected_issue = "Investigational Product (IP) Management", "Temperature excursion in storage fridge/freezer not reported"

    # Ensure the database actually has these keys before accessing
    if detected_cat in deviation_db and detected_issue in deviation_db[detected_cat]:
        data = deviation_db[detected_cat][detected_issue]
    else:
        # Fallback to a safe entry if no match is found
        detected_cat = "Protocol Compliance"
        detected_issue = "Patient visit occurred outside the protocol-allowed window"
        data = deviation_db[detected_cat][detected_issue]
