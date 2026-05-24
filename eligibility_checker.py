import streamlit as st

def run_eligibility_checker():
    st.header("🌐 Universal Clinical Eligibility Engine")
    st.markdown("Design your own protocol criteria dynamically. Works for any therapeutic area.")
    
    # Initialize session state to remember the rules the user creates
    if 'protocol_rules' not in st.session_state:
        st.session_state.protocol_rules = []

    # -----------------------------------------
    # SECTION 1: THE PROTOCOL BUILDER
    # -----------------------------------------
    st.subheader("Step 1: Define Protocol Parameters")
    st.write("Add the specific inclusion/exclusion criteria for your trial.")
    
    with st.form("rule_builder"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            param_name = st.text_input("Parameter Name (e.g., HbA1c, Platelets, Age)")
        with col2:
            min_val = st.number_input("Minimum Value", value=0.0)
        with col3:
            max_val = st.number_input("Maximum Value", value=100.0)
            
        submitted = st.form_submit_button("Add Rule to Protocol")
        
        if submitted and param_name:
            st.session_state.protocol_rules.append({
                "parameter": param_name,
                "min": min_val,
                "max": max_val
            })
            st.success(f"Added Rule: {param_name} must be between {min_val} and {max_val}.")

    # Display current active rules
    if st.session_state.protocol_rules:
        st.info("**Active Protocol Rules:**")
        for rule in st.session_state.protocol_rules:
            st.write(f"• **{rule['parameter']}**: {rule['min']} to {rule['max']}")

    st.markdown("---")

    # -----------------------------------------
    # SECTION 2: PATIENT SCREENING
    # -----------------------------------------
    st.subheader("Step 2: Screen Patient")
    
    if len(st.session_state.protocol_rules) == 0:
        st.warning("Please add at least one protocol rule above to begin screening.")
    else:
        # Dynamically generate input fields based on the rules the user created!
        patient_data = {}
        for rule in st.session_state.protocol_rules:
            patient_data[rule['parameter']] = st.number_input(f"Enter Patient's {rule['parameter']}", value=0.0)
            
        if st.button("Run Universal Screening"):
            flags = []
            # Check the patient data against the dynamic rules
            for rule in st.session_state.protocol_rules:
                param = rule['parameter']
                val = patient_data[param]
                if not (rule['min'] <= val <= rule['max']):
                    flags.append(f"❌ {param} ({val}) is outside required range ({rule['min']} - {rule['max']}).")
            
            if flags:
                st.error("### 🚫 PATIENT EXCLUDED")
                for flag in flags:
                    st.write(flag)
            else:
                st.success("### ✅ PATIENT ELIGIBLE")
                st.write("Patient meets all custom protocol criteria.")
                
        if st.button("Clear Protocol"):
            st.session_state.protocol_rules = []
            st.rerun()
