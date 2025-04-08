import streamlit as st
import tempfile
import os
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play, VoiceSettings
from st_audiorec import st_audiorec
import speech_recognition as sr

# 🔐 API Keys
OPENAI_API_KEY = "your-openai-api-key"
ELEVENLABS_API_KEY = "your-elevenlabs-api-key"

# 🔧 Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# 🎤 Recognize audio from .wav file
def recognize_audio_file(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

# 💬 Send prompt to ChatGPT
def ask_chatgpt(prompt):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# 🔊 Speak response with ElevenLabs
def speak(text):
    audio = eleven_client.generate(
        text=text,
        voice="Rachel",  # Default voice
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.7, similarity_boost=0.75)
    )
    play(audio)

# 🚀 Streamlit UI
st.set_page_config(page_title="Voice Assistant", page_icon="🧠")
st.title("🎙️ Personal Voice Assistant")

st.markdown("""
This assistant lets you speak a question and receive a GPT-powered response in a cloned voice. Speak clearly for best results.
""")

user_audio = st_audiorec()

if user_audio is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(user_audio)
        temp_audio_path = temp_audio_file.name

    st.info("🕡 Processing your voice...")
    query = recognize_audio_file(temp_audio_path).strip()
    os.remove(temp_audio_path)

    if query:
        st.success(f"🗣️ You said: {query}")
        response = ask_chatgpt(query)
        st.success(f"🤖 GPT says: {response}")
        speak(response)
    else:
        st.error("No recognizable speech detected. Please try again.")
