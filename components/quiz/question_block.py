import streamlit as st

def questionBlock(i, q):
    with st.container():
        st.markdown(f"### 🧠 Question {i+1}")
        st.markdown(f"**{q['question']}**")

        user_answer = st.session_state.get(f"question_{i}")

        if not st.session_state.quiz_submitted:
            st.radio(
                "Select your answer:",
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