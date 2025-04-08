import streamlit as st
import threading
import time
import speech_recognition as sr
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play, VoiceSettings

# 🔐 API Keys
OPENAI_API_KEY = "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"
ELEVENLABS_API_KEY = "sk_0e9b252b7b351ddb48968db5fff74eb79591e18f15e3c34f"

# 🔧 Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# 🎤 Voice recognition
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {query}")
        return query
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

# 💬 Send prompt to ChatGPT
def ask_chatgpt(prompt):
    print("🤖 Thinking...")
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content
    print(f"🤖 GPT says: {answer}")
    return answer

# 🔊 Speak response with ElevenLabs
def speak(text):
    audio = eleven_client.generate(
        text=text,
        voice="RM_A1",  # You can change this to any voice you have access to
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.7, similarity_boost=0.75)
    )
    play(audio)

# 🚀 Main assistant loop
def run_assistant(stop_flag):
    while not stop_flag.is_set():
        query = listen().strip()
        if query.lower() in ["exit", "quit", "stop"]:
            print("👋 Exiting. Have a nice day!")
            break
        if query:
            response = ask_chatgpt(query)
            speak(response)

# STREAMLIT UI
st.set_page_config(page_title="Voice Assistant", page_icon="🧠")
st.title("🎙️ Personal Voice Assistant")

if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "stop_event" not in st.session_state:
    st.session_state.stop_event = threading.Event()
if "thread" not in st.session_state:
    st.session_state.thread = None

if not st.session_state.is_running:
    if st.button("▶️ Start Assistant"):
        st.session_state.stop_event.clear()
        st.session_state.thread = threading.Thread(target=run_assistant, args=(st.session_state.stop_event,))
        st.session_state.thread.start()
        st.session_state.is_running = True
else:
    if st.button("⏹️ Stop Assistant"):
        st.session_state.stop_event.set()
        st.session_state.is_running = False
        st.success("🛑 Assistant stopped.")

st.markdown(f"**Status:** {'🟢 Running' if st.session_state.is_running else '🔴 Idle'}")
