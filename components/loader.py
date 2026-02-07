import streamlit as st

def loader():
    st.markdown(
        """
        <div class="loading-container">
            <div class="loader">
                <div class="loader-ring"></div>
                <div class="loader-ring"></div>
                <div class="loader-ring"></div>
                <div class="loader-center">🧠</div>
            </div>
            <div class="loading-text">Generating Your Quiz</div>
            <div class="loading-subtext">
                AI is crafting questions
                <span class="dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )