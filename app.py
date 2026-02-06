import streamlit as st
from modules.quizGenerator import generateQuiz

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Study Forge",
    page_icon="📚",
    layout="wide",
)

# -------------------- CUSTOM UI STYLING --------------------
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(135deg, #0f172a, #020617);
        }

        h1, h2, h3, h4 {
            color: #f8fafc !important;
        }

        .stMarkdown, label, p {
            color: #cbd5f5 !important;
        }

        div[data-testid="stContainer"] {
            background: rgba(255,255,255,0.03);
            border-radius: 16px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(6px);
        }

        .stButton button {
            background: linear-gradient(90deg, #6366f1, #22d3ee);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            transition: 0.3s;
        }

        .stButton button:hover {
            transform: scale(1.03);
            box-shadow: 0px 6px 18px rgba(99,102,241,0.4);
        }

        div[role="radiogroup"] > label {
            background: rgba(255,255,255,0.04);
            padding: 8px;
            border-radius: 10px;
            margin-bottom: 6px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        hr {
            border-color: rgba(255,255,255,0.1);
        }

        /* Loading Animation Styles */
        .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 3rem 2rem;
            background: rgba(99, 102, 241, 0.05);
            border-radius: 20px;
            border: 2px solid rgba(99, 102, 241, 0.2);
            backdrop-filter: blur(10px);
            margin: 2rem 0;
        }

        .loader {
            position: relative;
            width: 120px;
            height: 120px;
            margin-bottom: 2rem;
        }

        .loader-ring {
            position: absolute;
            width: 100%;
            height: 100%;
            border: 4px solid transparent;
            border-top-color: #6366f1;
            border-right-color: #22d3ee;
            border-radius: 50%;
            animation: rotate 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
        }

        .loader-ring:nth-child(2) {
            width: 80%;
            height: 80%;
            top: 10%;
            left: 10%;
            border-top-color: #22d3ee;
            border-right-color: #8b5cf6;
            animation-delay: -0.3s;
        }

        .loader-ring:nth-child(3) {
            width: 60%;
            height: 60%;
            top: 20%;
            left: 20%;
            border-top-color: #8b5cf6;
            border-right-color: #6366f1;
            animation-delay: -0.6s;
        }

        .loader-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2rem;
            animation: pulse 1.5s ease-in-out infinite;
        }

        @keyframes rotate {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
            50% {
                opacity: 0.6;
                transform: translate(-50%, -50%) scale(1.1);
            }
        }

        .loading-text {
            font-size: 1.4rem;
            font-weight: 600;
            background: linear-gradient(90deg, #6366f1, #22d3ee, #8b5cf6);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient 2s linear infinite;
            margin-bottom: 0.5rem;
        }

        .loading-subtext {
            color: #94a3b8;
            font-size: 0.95rem;
            animation: fadeInOut 2s ease-in-out infinite;
        }

        @keyframes gradient {
            0% {
                background-position: 0% center;
            }
            100% {
                background-position: 200% center;
            }
        }

        @keyframes fadeInOut {
            0%, 100% {
                opacity: 0.5;
            }
            50% {
                opacity: 1;
            }
        }

        .dots {
            display: inline-flex;
            gap: 4px;
            margin-left: 4px;
        }

        .dots span {
            width: 6px;
            height: 6px;
            background: #22d3ee;
            border-radius: 50%;
            animation: bounce 1.4s ease-in-out infinite;
        }

        .dots span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .dots span:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes bounce {
            0%, 60%, 100% {
                transform: translateY(0);
                opacity: 1;
            }
            30% {
                transform: translateY(-10px);
                opacity: 0.7;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- SESSION STATE --------------------
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# -------------------- HEADER --------------------
st.title("📚 Study Forge")
st.subheader("⚡ Generate AI Powered Quiz Questions in Seconds")

st.markdown("---")

# -------------------- INPUT SECTION --------------------
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
                st.error(
                    "Please enter a study topic or upload a study document"
                )
            else:
                st.session_state.is_generating = True
                st.rerun()

# -------------------- LOADING ANIMATION --------------------
if st.session_state.is_generating:
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
    
    # Generate quiz
    st.session_state.quiz_submitted = False

    keys_to_remove = [
        key
        for key in st.session_state.keys()
        if key.startswith("question_")
    ]
    for key in keys_to_remove:
        del st.session_state[key]

    st.session_state.quiz = generateQuiz(
        topic, doc, numberOfQuestions
    )
    
    st.session_state.is_generating = False
    st.rerun()

# -------------------- QUIZ DISPLAY --------------------
if "quiz" in st.session_state:
    st.markdown("## 📝 Quiz")

    progress = 0
    answered = 0
    total = len(st.session_state.quiz)

    for i in range(total):
        if st.session_state.get(f"question_{i}") is not None:
            answered += 1

    progress = answered / total if total > 0 else 0
    st.progress(progress, text=f"Progress: {answered}/{total} answered")

    for i, q in enumerate(st.session_state.quiz):
        with st.container():
            st.markdown(f"### 🧠 Question {i+1}")
            st.markdown(f"**{q['question']}**")

            user_answer = st.session_state.get(f"question_{i}")

            if not st.session_state.quiz_submitted:
                st.radio(
                    label="Select your answer:",
                    options=q["options"],
                    key=f"question_{i}",
                    index=None,
                )
            else:
                correct = q["answer"]

                for opt in q["options"]:
                    if opt == correct:
                        st.success(f"✓ {opt} — Correct Answer")
                    elif opt == user_answer:
                        st.error(f"✗ {opt} — Your Answer")
                    else:
                        st.write(f"○ {opt}")

# -------------------- SUBMIT SECTION --------------------
st.divider()

if "quiz" in st.session_state and not st.session_state.quiz_submitted:
    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:
        if st.button("✅ Submit Quiz"):
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
                    st.warning(
                        f"Please answer all questions to submit the quiz: {unanswered}"
                    )
                    st.stop()

                for i, q in enumerate(st.session_state.quiz):
                    selectedAnswer = st.session_state.get(f"question_{i}")
                    correctAnswer = q["answer"]

                    if selectedAnswer == correctAnswer:
                        score += 1
                        st.success(f"Q{i+1}. Correct ✅")
                    else:
                        st.error(
                            f"Q{i+1}: Wrong ❌ | Correct Answer: {correctAnswer}"
                        )

            st.session_state.score = score
            st.session_state.quiz_submitted = True
            st.rerun()

# -------------------- RESET SECTION --------------------
if st.session_state.quiz_submitted:
    st.markdown("---")
    if st.button("🔄 Reset Quiz"):
        st.session_state.pop("quiz", None)
        st.session_state.pop("score", None)

        keys_to_remove = [
            key
            for key in st.session_state.keys()
            if key.startswith("question_")
        ]
        for key in keys_to_remove:
            del st.session_state[key]

        st.session_state.quiz_submitted = False
        st.rerun()

# -------------------- SCORE DISPLAY --------------------
if "score" in st.session_state and "quiz" in st.session_state:
    st.markdown("---")
    st.subheader(
        f"🏆 Final Score: {st.session_state.score} / {len(st.session_state.quiz)}"
    )

st.sidebar.text("hello")