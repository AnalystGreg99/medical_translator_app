from gtts import gTTS
import streamlit as st

# Text-to-speech function
def generate_speech(text: str, language: str = "en") -> bytes:
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        audio_file = "translated_audio.mp3"
        tts.save(audio_file)
        with open(audio_file, "rb") as f:
            audio_data = f.read()
        return audio_data
    except Exception as e:
        st.error(f"Text-to-speech generation failed: {e}")
        return None
