import unittest
from transcription import transcribe_audio
from groq_translation import groq_translate
from text_to_speech import generate_speech

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class TestHealthcareTranslator(unittest.TestCase):
    def test_transcribe_audio(self):
        # Test with a sample audio file (ensure the file exists)
        audio_file = "sample.wav"
        transcript = transcribe_audio(audio_file)
        self.assertIsNotNone(transcript)
        self.assertIsInstance(transcript, str)

    def test_translate_text(self):
        # Test translation function
        text = "Hello, how are you?"
        translated = groq_translate(query=text, from_language="en", to_language="es")
        self.assertIsNotNone(translated)
        self.assertIsInstance(translated.translated_text, str)

    def test_generate_speech(self):
        # Test text-to-speech conversion
        text = "Hola, ¿cómo estás?"
        audio_data = generate_speech(text=text, language="es")
        self.assertIsNotNone(audio_data)
        self.assertIsInstance(audio_data, bytes)

if __name__ == "__main__":
    unittest.main()
