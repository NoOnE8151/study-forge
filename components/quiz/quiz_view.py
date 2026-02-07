import streamlit as st
from components.quiz.quiz_progress import quizProgress
from components.quiz.question_block import questionBlock

def quizView():
    quiz = st.session_state.quiz

    st.markdown("## 📝 Quiz")
    quizProgress(quiz)

    for i, q in enumerate(quiz):
        questionBlock(i, q)