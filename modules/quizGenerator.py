import streamlit as st
from sambanova import SambaNova as ai
import json
import time

client = ai(
    api_key=st.secrets["SAMBANOVA_SECRET"],
    base_url="https://api.sambanova.ai/v1",
)

def generateQuiz(topic, file, num):
    prompt = f"""
Generate {num} multiple choice question on the topic {topic}
return response strictly in following JSON format:
[{{
    "question": "question text",
    "options": ["A", "B", "C", "D"],
    "answer": "correct option"
}}]
do not include any explanation or any extra text keep it strictly json only response
"""

    MAX_RETRIES = 3
    response = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model="ALLaM-7B-Instruct-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                top_p=0.1,
            )
            break  # success

        except Exception as e:
            if "429" in str(e) and attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                st.warning(
                    "Quiz generation rate limit exceeded. Please try later."
                )
                return []

    if not response:
        return []

    content = response.choices[0].message.content.strip()

    #model wrapping JSON in ```json ````        `
    if content.startswith("```"):
        content = content.split("```")[1]
        content = content.replace("json", "", 1).strip()

    try:
        quiz = json.loads(content)
        return quiz

    except json.JSONDecodeError:
        st.error("AI response parsing failed")
        return []