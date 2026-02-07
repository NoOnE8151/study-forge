import streamlit as st
from sambanova import SambaNova as ai
import json
import time
from modules.pdf_parser import pdfExtracter

client = ai(
    api_key=st.secrets["SAMBANOVA_SECRET"],
    base_url="https://api.sambanova.ai/v1",
)


def generateQuiz(topic, file, num):
    prompt = f"""
You are an exam question generator.

TASK:
Generate EXACTLY {num} high-quality multiple choice questions strictly based on the study material provided below.

STUDY MATERIAL:
----------------
{topic or pdfExtracter(file)}
----------------

QUESTION RULES:
1. Questions MUST be directly derived from or logically inferable from the given material.
2. Questions must be exam-ready, clear, and unambiguous.
3. Avoid generic questions not grounded in the provided content.
4. Difficulty should match typical academic exam style.
5. Avoid repetition or paraphrasing the same question.
6. Each question must have exactly 4 options.
7. Only one correct answer per question.

OUTPUT RULES (STRICT):
1. Output ONLY valid JSON.
2. Do NOT include explanations, markdown, comments, or extra text.
3. Do NOT wrap JSON in code blocks.
4. Response must be a JSON array containing EXACTLY {num} objects.
5. Each object must follow this structure exactly:

[
  {{
    "question": "question text",
    "options": ["option A", "option B", "option C", "option D"],
    "answer": "correct option text exactly matching one option"
  }}
]

VALIDATION BEFORE RESPONSE:
- Ensure total questions count = {num}.
- Ensure every question has 4 options.
- Ensure answer text exactly matches one option.
- Ensure output is valid JSON.
- If validation fails internally, regenerate until valid.

Return ONLY the final JSON array.
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
                wait_time = 2**attempt
                time.sleep(wait_time)
            else:
                st.warning("Quiz generation rate limit exceeded. Please try later.")
                return []

    if not response:
        return []

    content = response.choices[0].message.content.strip()

    # model wrapping JSON in ```json ````        `
    if content.startswith("```"):
        content = content.split("```")[1]
        content = content.replace("json", "", 1).strip()

    try:
        quiz = json.loads(content)
        return quiz

    except json.JSONDecodeError:
        st.error("AI response parsing failed")
        return []
