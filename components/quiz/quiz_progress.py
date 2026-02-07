import streamlit as st

def quizProgress(quiz):
    answered = 0
    total = len(quiz)

    for i in range(total):
        if st.session_state.get(f"question_{i}") is not None:
            answered += 1

    progress = answered / total if total > 0 else 0

    st.progress(progress, text=f"Progress: {answered}/{total} answered")