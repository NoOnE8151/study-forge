import streamlit as st
from modules.quizGenerator import generateQuiz


if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

st.title("📚 Study Forge - AI Study Assistant")
st.subheader("Create AI Powered Quiz Questions In Seconds")

topic = st.text_input(label="Topic", placeholder="Enter study topic")
st.write("OR")
doc = st.file_uploader(label="Upload Assignment/Notes (pdf)", type=".pdf")

numberOfQuestions = st.slider(
    label="Number of questions", min_value=1, max_value=20, value=10
)

if st.button("Generate Quiz"):
    if topic.strip() == "" and doc is None:
        st.error("Please enter a study topic or upload a study document")
    else:
        st.session_state.quiz_submitted = False
        # clening previous answers
        keys_to_remove = [
            key for key in st.session_state.keys() if key.startswith("question_")
        ]
        for key in keys_to_remove:
            del st.session_state[key]

        st.session_state.quiz = generateQuiz(topic, doc, numberOfQuestions)

if "quiz" in st.session_state:
    for i, q in enumerate(st.session_state.quiz):
        with st.container():
            st.markdown(f"### 🧠 Question {i+1}")
            st.markdown(f"**{q['question']}**")

            user_answer = st.session_state.get(f"question_{i}")

            # quiz
            if not st.session_state.quiz_submitted:
                st.radio(
                    label="Select your answer:",
                    options=q["options"],
                    key=f"question_{i}",
                    index=None,
                )

            # review mode
            else:
                correct = q["answer"]

                for opt in q["options"]:
                    if opt == correct:
                        st.success(f"✓ {opt} — Correct Answer")
                    elif opt == user_answer:
                        st.error(f"✗ {opt} — Your Answer")
                    else:
                        st.write(f"○ {opt}")

st.divider()

#submission
if "quiz_submitted" not in st.session_state:
    if st.button("Submit Quiz"):
        if "quiz" not in st.session_state:
            st.error("Please generate quiz first")
        else:
            score = 0
            st.subheader("Results")

            unanswered = []
            for i in range(len(st.session_state.quiz)):
                if st.session_state.get(f"question_{i}") is None:
                    unanswered.append(i + 1)

            if unanswered:
                st.warning(f"Please answer all questions to submit the quiz: {unanswered}")
                st.stop()

            for i, q in enumerate(st.session_state.quiz):
                selectedAnswer = st.session_state.get(f"question_{i}")
                correctAnswer = q["answer"]

                if selectedAnswer == correctAnswer:
                    score += 1
                    st.success(f"Q{i+1}. Correct ✅")
                else:
                    st.error(f"Q{i+1}: Wrong ❌ | Correct Answer: {correctAnswer}")
        st.session_state.score = score
        st.session_state.quiz_submitted = True
        st.rerun()


if "score" in st.session_state and "quiz" in st.session_state:
    st.markdown("---")
    st.subheader(
        f"Final Score: {st.session_state.score} / {len(st.session_state.quiz)}"
    )
