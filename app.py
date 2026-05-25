import streamlit as st

st.set_page_config(page_title="Toxidrome CDS", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR ENTERPRISE UI (High Visibility Cyan) ---
st.markdown("""
    <style>
    .critical-alert { background-color: #721c24; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #dc3545; }
    .urgent-alert { background-color: #856404; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #ffc107; }
    .stable-alert { background-color: #155724; color: white; padding: 12px; border-radius: 4px; font-weight: bold; border-left: 6px solid #28a745; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #00BFFF; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 1.5rem; margin-bottom: 0.5rem; border-bottom: 1px solid #444; padding-bottom: 4px; }
    .diagnostic-card { border: 1px solid #dee2e6; border-radius: 6px; padding: 16px; background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

# --- 1. LEFT PANEL: TRIAGE ASSESSMENT ---
with st.sidebar:
    st.markdown("<div style='font-size: 1.5rem; font-weight: bold; color: #00BFFF;'>Triage Assessment</div>", unsafe_allow_html=True)
    st.caption("Input real-time patient findings.")
    
    st.markdown("<div class='section-header'>CNS Findings</div>", unsafe_allow_html=True)
    pupils = st.selectbox("Pupil Examination", ["Normal", "Pinpoint", "Dilated"])
    mental_status = st.selectbox("Mental Status", ["Normal", "Depressed / Coma", "Agitated / Delirium"])
    
    st.markdown("<div class='section-header'>Hemodynamics & Airway</div>", unsafe_allow_html=True)
    respirations = st.selectbox("Respiratory Rate", ["Normal", "Depressed (<12)", "Tachypnea (>20)"])
    heart_rate = st.selectbox("Heart Rate", ["Normal", "Bradycardia (<60)", "Tachycardia (>100)"])
    
    st.markdown("<div class='section-header'>Autonomic Signs</div>", unsafe_allow_html=True)
    skin = st.selectbox("Skin / Mucous Membranes", ["Normal", "Dry / Flushed", "Diaphoretic (Sweaty)"])
    bowel_sounds = st.selectbox("Bowel Sounds", ["Normal", "Decreased / Absent", "Hyperactive"])
    
    st.markdown("<div class='section-header'>Ancillary Data</div>", unsafe_allow_html=True)
    ecg_qrs = st.selectbox("ECG QRS Interval", ["Normal (<100ms)", "Widened (>100ms)"])
    temperature = st.selectbox("Core Temperature", ["Normal", "Hyperthermia (>39C)"])
    
    if st.button("Clear Patient Data", use_container_width=True):
        st.rerun()

# --- 2. LOGIC & PHYSIOLOGY ENGINE ---
hallmarks = {
    "Opioid": ["Pinpoint pupils", "Respiratory depression", "CNS depression", "Bradycardia"],
    "Antichol
