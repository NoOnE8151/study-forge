import streamlit as st
from modules.quiz_scoring import evaluateQuiz


def submitSection():
    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:
        if st.session_state.quiz and st.session_state.quiz_submitted is not True:
            if st.button("✅ Submit Quiz"):
                if "quiz" not in st.session_state:
                    st.error("Please generate quiz first")
                    return

                score = evaluateQuiz()

                st.session_state.score = score
                st.session_state.quiz_submitted = True
                st.rerun()
