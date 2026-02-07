import streamlit as st

def loadCSS(file_path="styles/main.css"):
    with open(file_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )