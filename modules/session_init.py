import streamlit as st

def initSessionState():
    defaults = {
        "quiz_submitted": False,
        "is_generating": False,
        "quiz": [],   
        "score": None,  
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value