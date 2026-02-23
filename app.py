import streamlit as st
from modules.quiz_generator import generateQuiz
from modules.session_init import initSessionState
from utils.styles import loadCSS
from components.loader import loader
from components.quiz.quiz_view import quizView
from components.quiz.submit_section import submitSection

st.set_page_config(
    page_title="Study Forge",
    page_icon="📚",
    layout="wide",
)

initSessionState()
loadCSS()


st.title("📚 Study Forge")
st.subheader("⚡ Generate AI Powered Quiz Questions in Seconds")

st.markdown("---")


with st.container():
    c1, c2 = st.columns([2, 1])

    with c1:
        topic = st.text_input(
            label="📘 Topic",
            placeholder="Enter study topic",
            disabled=st.session_state.is_generating,
        )
        st.write("OR")
        doc = st.file_uploader(
            label="📄 Upload Assignment/Notes (PDF)",
            type=".pdf",
            disabled=st.session_state.is_generating,
        )

    with c2:
        st.markdown("### ⚙ Quiz Settings")
        numberOfQuestions = st.slider(
            label="Number of questions",
            min_value=1,
            max_value=20,
            value=10,
            disabled=st.session_state.is_generating,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Generate Quiz", disabled=st.session_state.is_generating):
            if topic.strip() == "" and doc is None:
                st.error("Please enter a study topic or upload a study document")
            else:
                st.session_state.is_generating = True
                st.rerun()


if st.session_state.is_generating:
    loader()

    # Generate quiz
    st.session_state.quiz_submitted = False

    keys_to_remove = [
        key for key in st.session_state.keys() if key.startswith("question_")
    ]
    for key in keys_to_remove:
        del st.session_state[key]

    st.session_state.quiz = generateQuiz(topic, doc, numberOfQuestions)

    st.session_state.is_generating = False
    st.rerun()


if "quiz" in st.session_state:
    quizView()

st.divider()

if "quiz" in st.session_state and not st.session_state.quiz_submitted:
    submitSection()


if st.session_state.quiz_submitted:
    st.markdown("---")
    if st.button("🔄 Reset Quiz"):
        st.session_state.pop("quiz", None)
        st.session_state.pop("score", None)

        keys_to_remove = [
            key for key in st.session_state.keys() if key.startswith("question_")
        ]
        for key in keys_to_remove:
            del st.session_state[key]

        st.session_state.quiz_submitted = False
        st.rerun()

if st.session_state.quiz and st.session_state.score is not None:
    st.markdown("---")
    st.subheader(
        f"🏆 Final Score: {st.session_state.score} / {len(st.session_state.quiz)}"
    )
