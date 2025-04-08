import streaml
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
