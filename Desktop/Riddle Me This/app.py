import streamlit as st # type: ignore
import requests # type: ignore
import random

# -------------------------------
# Riddles Dataset (Static)
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
# Hugging Face API Function (Cached for Performance)
# -------------------------------
@st.cache_data
def ask_hugging_face(prompt, model="meta-llama/Llama-3.2-3B-Instruct"):
    # Securely access the API key from Streamlit secrets
    if "huggingface_api_key" not in st.secrets:
        st.error("Hugging Face API key not found. Please add it to your Streamlit secrets.")
        return "⚠️ AI features are disabled. Please configure the API key."

    try:
        api_key = st.secrets["huggingface_api_key"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200, "temperature": 0.7}
        }
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()[0]["generated_text"].strip()
    except requests.exceptions.RequestException as e:
        return f"⚠️ Could not connect to Hugging Face AI: {str(e)}. Please check your network connection."
    except Exception as e:
        return f"⚠️ An error occurred with the Hugging Face AI: {str(e)}. Please try again."

# -------------------------------
# Conversational AI Function
# -------------------------------
def chat_with_ai(user_input, conversation_history):
    prompt = f"""
    You are a friendly AI assistant for a kids' riddle game called 'Avery's Riddle Me This?'. Respond in a fun, simple, and child-friendly way. Use emojis and keep answers short. The current riddle is: '{st.session_state.riddle['question'] if st.session_state.riddle else 'No riddle selected'}'. The conversation so far: {conversation_history}
    User: {user_input}
    AI: """
    response = ask_hugging_face(prompt)
    return response

# -------------------------------
# Dynamic Riddle Generation
# -------------------------------
def generate_riddle(level):
    prompt = f"Generate a {level.lower()}-difficulty riddle for kids. Provide the riddle as a question and the answer separately, formatted as: Question: [riddle] Answer: [answer]. Keep it short and fun."
    response = ask_hugging_face(prompt)
    try:
        question = response.split("Answer:")[0].replace("Question:", "").strip()
        answer = response.split("Answer:")[1].strip()
        return {"question": question, "answer": answer}
    except IndexError:
        return None  # Fallback to static riddles if parsing fails

# -------------------------------
# Translate Riddle (Multilingual Support)
# -------------------------------
def translate_riddle(riddle, language="es"):
    model = "Helsinki-NLP/opus-mt-en-es" if language == "es" else "Helsinki-NLP/opus-mt-en-fr"
    prompt = f"Translate this riddle to {language}: {riddle['question']}"
    translated_question = ask_hugging_face(prompt, model=model)
    return {"question": translated_question, "answer": riddle["answer"]}

# -------------------------------
# AI Answer Evaluator
# -------------------------------
def evaluate_answer(user_input, correct_answer):
    prompt = f"""
    The correct answer to the riddle is: '{correct_answer}'.
    A child answered: '{user_input}'.

    Is the child's answer essentially correct? Respond only with 'Yes' or 'No'.
    """
    reply = ask_hugging_face(prompt).strip().lower()
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
if 'language' not in st.session_state:
    st.session_state.language = "en"
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.image("logo.jpg", width=150)  # Compressed for faster loading
    st.title("📜 Game Info")

    st.subheader("🎯 Rules")
    st.markdown("""
    - Solve riddles or chat with the AI.
    - One answer per try.
    - Ask for hints or talk to the AI if stuck.
    """)

    st.subheader("🕹️ How to Play")
    st.markdown("""
    1. Choose a level  
    2. Select a language (optional)  
    3. Solve the riddle or chat with the AI  
    4. Submit answers or ask questions  
    5. Score points for correct answers!
    """)

    st.subheader("💡 Hints")
    st.markdown("""
    - Think about keywords.  
    - Break it down.  
    - Ask the AI for help! 😊
    """)

    st.subheader("📈 Progress")
    st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.attempts}")

    if st.button("🔄 Reset Progress"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.conversation_history = []
        st.success("Progress reset!")

    st.subheader("🌐 Language")
    language = st.selectbox("Choose language:", ["English", "Spanish", "French"], index=["en", "es", "fr"].index(st.session_state.language))
    st.session_state.language = "en" if language == "English" else "es" if language == "Spanish" else "fr"

# -------------------------------
# Main App Content
# -------------------------------
st.title("🧠 Avery's Riddle Me This?")
st.image("logo.jpg", width=150)
st.markdown("Welcome to Avery's Riddle Me This? where you can solve riddles, chat with the AI, and have fun! 🎉")
level = st.selectbox("Choose your difficulty level:", ["Easy", "Medium", "Hard"])

if st.button("🎲 New Riddle"):
    if random.random() < 0.5:
        st.session_state.riddle = random.choice(riddles[level])
    else:
        st.session_state.riddle = generate_riddle(level)
        if not st.session_state.riddle:
            st.session_state.riddle = random.choice(riddles[level])
    if st.session_state.language != "en":
        st.session_state.riddle = translate_riddle(st.session_state.riddle, st.session_state.language)
    st.session_state.last_result = None
    st.session_state.conversation_history = []

mode = st.radio("Choose a mode:", ["Solve a riddle", "Stump the AI with your own riddle", "Chat with AI"])
if mode == "Solve a riddle":
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
                hint_level = "simple" if st.session_state.attempts < 3 else "detailed"
                prompt = f"Provide a {hint_level} hint for this riddle: {st.session_state.riddle['question']}. Keep it short and child-friendly."
                hint = ask_hugging_face(prompt)
                st.info(f"🧠 Hint: {hint}")

        with col3:
            if st.button("🤖 Ask the AI for help"):
                prompt = f"Help a child solve this riddle:\n\nRiddle: {st.session_state.riddle['question']}\n\nThey guessed: '{user_input}'. How should I help them?"
                ai_help = ask_hugging_face(prompt)
                st.markdown(f"**AI says:** {ai_help}")

elif mode == "Stump the AI with your own riddle":
    st.subheader("🧙 Challenge the AI")
    custom_riddle = st.text_area("✍️ Type your own riddle for the AI:")
    if st.button("🤔 What’s your answer, AI?"):
        if custom_riddle.strip():
            prompt = f"A kid gave you this riddle. Try to solve it simply:\n\n{custom_riddle}"
            ai_answer = ask_hugging_face(prompt)
            st.markdown(f"**AI thinks:** {ai_answer}")
        else:
            st.warning("Please type a riddle first!")

elif mode == "Chat with AI":
    st.subheader("💬 Chat with the AI")
    st.markdown("Ask questions about the riddle, the game, or anything fun! 😄")
    user_chat = st.text_input("Type your message to the AI:")
    if st.button("📨 Send Message"):
        if user_chat.strip():
            # Update conversation history
            st.session_state.conversation_history.append(f"User: {user_chat}")
            response = chat_with_ai(user_chat, "\n".join(st.session_state.conversation_history))
            st.session_state.conversation_history.append(f"AI: {response}")
            # Display conversation
            for message in st.session_state.conversation_history:
                st.markdown(message)
        else:
            st.warning("Please type a message first!")

st.markdown("---")
st.markdown("🗣️ Solve riddles, stump the AI, or chat for fun in the modes above!")
