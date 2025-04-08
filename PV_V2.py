import streamlit as st
import threading
import time
import speech_recognition as sr
from openai import OpenAI
from ele]
        st.session_state.is_running = True
else:
    if st.button("⏹️ Stop Assistant"):
        st.session_state.stop_event.set()
        st.session_state.is_running = False
        st.success("🛑 Assistant stopped.")

st.markdown(f"**Status:** {'🟢 Running' if st.session_state.is_running else '🔴 Idle'}")
