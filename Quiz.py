import streamlit as st
import random
import time

# ------------------ Config ------------------
st.set_page_config(page_title="Python Quiz App", page_icon="🐍")
st.title("🐍 Python Quiz for Beginners")
st.markdown("You have **60 seconds** to complete the quiz. You need at least **80%** to pass.")

# ------------------ Initialize Session State ------------------
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}

# ------------------ Quiz Data ------------------
original_questions = [
    {
        "question": "What is the correct file extension for Python files?",
        "options": [".pyth", ".pt", ".py", ".pyt"],
        "answer": ".py"
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "def", "define", "fun"],
        "answer": "def"
    },
    {
        "question": "What is the output of print(2 ** 3)?",
        "options": ["6", "8", "9", "5"],
        "answer": "8"
    },
    {
        "question": "Which data type is used to store True/False values?",
        "options": ["int", "str", "bool", "float"],
        "answer": "bool"
    },
    {
        "question": "Which of the following is a loop in Python?",
        "options": ["for", "foreach", "loop", "iterate"],
        "answer": "for"
    }
]

# ------------------ Start Quiz ------------------
def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.start_time = time.time()
    st.session_state.submitted = False
    st.session_state.answers = {}
    # Shuffle questions and options
    questions = original_questions.copy()
    random.shuffle(questions)
    for q in questions:
        random.shuffle(q["options"])
    st.session_state.shuffled_questions = questions

# ------------------ Restart Quiz ------------------
def restart_quiz():
    st.session_state.quiz_started = False
    st.session_state.start_time = None
    st.session_state.submitted = False
    st.session_state.shuffled_questions = []
    st.session_state.answers = {}

# ------------------ Start Button ------------------
if not st.session_state.quiz_started:
    st.button("Start Quiz", on_click=start_quiz)

# ------------------ Quiz UI ------------------
if st.session_state.quiz_started:
    st.markdown("### Answer the following questions:")
    for i, q in enumerate(st.session_state.shuffled_questions):
        key = f"q{i}"
        default = st.session_state.answers.get(key, "Select an answer")
        answer = st.radio(
            f"Q{i+1}: {q['question']}",
            ["Select an answer"] + q["options"],
            index=(["Select an answer"] + q["options"]).index(default) if default in q["options"] else 0,
            key=key
        )
        st.session_state.answers[key] = answer

    all_answered = all(ans != "Select an answer" for ans in st.session_state.answers.values())

    if not st.session_state.submitted:
        st.button("Submit Quiz", on_click=lambda: setattr(st.session_state, 'submitted', True), disabled=not all_answered)

# ------------------ Results ------------------
if st.session_state.submitted:
    correct_count = 0
    st.markdown("---")
    st.subheader("📊 Result Summary")

    for i, q in enumerate(st.session_state.shuffled_questions):
        user_answer = st.session_state.answers.get(f"q{i}", "Select an answer")
        if user_answer == "Select an answer":
            st.warning(f"⚠️ Q{i+1}: No answer selected. Correct answer is **{q['answer']}**")
            continue
        if user_answer == q["answer"]:
            correct_count += 1
            st.success(f"✅ Q{i+1}: Correct")
        else:
            st.error(f"❌ Q{i+1}: Incorrect. Correct answer is **{q['answer']}**")

    percentage = (correct_count / len(st.session_state.shuffled_questions)) * 100
    st.markdown(f"**Your Score: {percentage:.2f}% ({correct_count}/5)**")

    if percentage >= 80:
        st.success("🎉 Congratulations! You passed the quiz.")
    else:
        st.error("😥 You failed the quiz. Please try again.")

    st.button("🔁 Retry Quiz", on_click=restart_quiz)

# ------------------ Timer ------------------
if st.session_state.quiz_started and not st.session_state.submitted:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 60 - elapsed)

    timer_placeholder = st.empty()
    timer_placeholder.info(f"⏰ Time remaining: {remaining} seconds")

    if remaining <= 0:
        st.session_state.submitted = True
        st.warning("⏱ Time is up! Submitting automatically...")
        st.rerun()
    else:
        time.sleep(1)
        st.rerun()
