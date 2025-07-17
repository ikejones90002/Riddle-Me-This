import streamlit as st  # type: ignore
import requests  # type: ignore
import random
import os

# -------------------------------
# Riddles Dataset
# -------------------------------
riddles = {
    "Easy": [
        {"question": "What has hands but can’t clap?", "answer": "a clock"},
        {"question": "What has to be broken before you can use it?", "answer": "an egg"}
    ],
    "Medium": [
        {"question": "What gets wetter the more it dries?", "answer": "a towel"},
        {"question": "What has one eye but can’t see?", "answer": "a needle"}
    ],
    "Hard": [
        {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
        {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "the letter m"}
    ]
}

# -------------------------------
# Local AI Function (Ollama)
# -------------------------------
def ask_local_ai(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi4-mini-reasoning", "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
    except Exception:
        return "⚠️ Can't connect to local AI. Is Ollama running?"

# -------------------------------
# AI Answer Evaluator
# -------------------------------
def evaluate_answer(user_input, correct_answer):
    prompt = f"""
    The correct answer to the riddle is: '{correct_answer}'.
    A child answered: '{user_input}'.

    Is the child's answer essentially correct? Respond only with 'Yes' or 'No'.
    """
    reply = ask_local_ai(prompt).strip().lower()
    return "yes" in reply

# -------------------------------
# Streamlit App Config
# -------------------------------
st.set_page_config(page_title="Avery's Riddle Me This?", page_icon="🧠")

# -------------------------------
# Session State Initialization
# -------------------------------
if 'riddle' not in st.session_state:
    st.session_state.riddle = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# -------------------------------
# Safe Image Loader
# -------------------------------
def safe_image(path, width=200):
    if os.path.exists(path):
        st.image(path, width=width)
    else:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png", width=width, caption="Missing logo")

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    safe_image("logo.jpg", width=200)
    st.title("📜 Game Info")

    st.subheader("🎯 Rules")
    st.markdown("""
    - Solve the riddle to move on.
    - One answer per try.
    - Ask for help or hints if stuck.
    """)

    st.subheader("🕹️ How to Play")
    st.markdown("""
    1. Choose a level  
    2. Solve the riddle  
    3. Submit your answer  
    4. Score points for correct answers!
    """)

    st.subheader("💡 Hints")
    st.markdown("""
    - Think about keywords.  
    - Break it down.  
    - Ask the AI!
    """)

    st.subheader("📈 Progress")
    st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.attempts}")

    if st.button("🔄 Reset Progress"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.success("Progress reset!")

# -------------------------------
# Main App Content
# -------------------------------
st.title("🧠 Avery's Riddle Me This?")
safe_image("logo.jpg", width=200)
st.markdown("Welcome to Avery's Riddle Me This? where you can solve riddles, learn, and have fun! 🎉")

level = st.selectbox("Choose your difficulty level:", ["Easy", "Medium", "Hard"])
mode = st.radio("Choose a mode:", ["Solve a riddle", "Stump the AI with your own riddle"])

if mode == "Solve a riddle":
    if st.button("🎲 New Riddle"):
        st.session_state.riddle = random.choice(riddles[level])
        st.session_state.last_result = None

    if st.session_state.riddle:
        st.subheader("🧩 Riddle:")
        st.write(st.session_state.riddle["question"])

        user_input = st.text_input("🔤 Type your answer:")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Submit Answer"):
                st.session_state.attempts += 1
                is_correct = evaluate_answer(user_input.strip().lower(), st.session_state.riddle["answer"])

                if is_correct:
                    st.session_state.score += 1
                    st.success("🎉 That's correct! Great job!")
                    st.audio("https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg")
                    st.balloons()
                    st.snow()
                else:
                    st.error("❌ Hmm... that's not quite right. Want a hint?")
                    st.audio("https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg")

        with col2:
            if st.button("💡 Hint"):
                st.info("🧠 Hint: Think about the keywords. Break it down.")

        with col3:
            if st.button("🤖 Ask the AI for help"):
                prompt = f"Help a child solve this riddle:\n\nRiddle: {st.session_state.riddle['question']}\n\nThey guessed: '{user_input}'. How should I help them?"
                ai_help = ask_local_ai(prompt)
                st.markdown(f"**AI says:** {ai_help}")

elif mode == "Stump the AI with your own riddle":
    st.subheader("🧙 Challenge the AI")
    custom_riddle = st.text_area("✍️ Type your own riddle for the AI:")
    if st.button("🤔 What’s your answer, AI?"):
        if custom_riddle.strip():
            prompt = f"A kid gave you this riddle. Try to solve it simply:\n\n{custom_riddle}"
            ai_answer = ask_local_ai(prompt)
            st.markdown(f"**AI thinks:** {ai_answer}")
        else:
            st.warning("Please type a riddle first!")

st.markdown("---")
st.markdown("🗣️ You can even stump the AI with your own riddle in the input box above!")

