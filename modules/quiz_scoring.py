import streamlit as st

def evaluateQuiz():
    quiz = st.session_state.quiz
    score = 0
    unanswered = []

    for i in range(len(quiz)):
        if st.session_state.get(f"question_{i}") is None:
            unanswered.append(i + 1)

    if unanswered:
        st.warning(
            f"Please answer all questions to submit the quiz: {unanswered}"
        )
        st.stop()

    st.subheader("Results")

    for i, q in enumerate(quiz):
        selected = st.session_state.get(f"question_{i}")
        correct = q["answer"]

        if selected == correct:
            score += 1
            st.success(f"Q{i+1}. Correct ✅")
        else:
            st.error(
                f"Q{i+1}: Wrong ❌ | Correct Answer: {correct}"
            )

    return score