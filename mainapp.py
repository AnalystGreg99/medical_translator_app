import streamlit as st
from audio_recorder_streamlit import audio_recorder
from transcription import transcribe_audio
from groq_translation import groq_translate
from text_to_speech import generate_speech
import tempfile
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# Set page config
st.set_page_config(page_title="Healthcare Translator", page_icon="🎤", layout="centered")

# Title and introduction
st.title("Healthcare Translator")
st.write("A real-time translation app for healthcare communication. Speak, translate, and listen!")

# Language selection
languages = {
    "English": "en",
    "Portuguese": "pt",
    "Spanish": "es",
    "German": "de",
    "French": "fr",
    "Italian": "it",
    "Dutch": "nl",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese": "zh",
    "Korean": "ko"
}

# Dropdowns for input and target languages
input_language = st.selectbox(
    "Language to transcribe from:",
    options=list(languages.keys()),
    index=0,  # Default to English
    help="Select the language you will speak in."
)

target_language = st.selectbox(
    "Language to translate to:",
    options=list(languages.keys()),
    index=1,  # Default to Spanish
    help="Select the language to translate the text into."
)

# Record audio
st.write("Click the microphone to record your voice:")
audio_bytes = audio_recorder()

if audio_bytes and target_language:
    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    # Display audio player
    st.audio(temp_audio_path, format="audio/wav")

    try:
        # Step 1: Transcribe audio
        st.divider()
        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio(temp_audio_path)
        if transcript:
            st.subheader(f"Transcribed Text ({input_language})")
            st.write(transcript)

            # Step 2: Translate the transcribed text
            st.divider()
            with st.spinner("Translating text..."):
                translation = groq_translate(
                    query=transcript,
                    from_language=languages[input_language],
                    to_language=languages[target_language]
                )
            if translation:
                st.subheader(f"Translated Text ({target_language})")
                st.write(translation.translated_text)

                # Step 3: Play back the translated text
                st.divider()
                if st.button("Play Translation"):
                    with st.spinner("Generating audio for translation..."):
                        audio_data = generate_speech(translation.translated_text, language=languages[target_language])
                        if audio_data:
                            st.audio(audio_data, format="audio/mp3")
            else:
                st.error("Translation failed. Please try again.")
        else:
            st.error("Transcription failed. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # Clean up temporary files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
