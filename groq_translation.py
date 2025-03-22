import json
from typing import Optional
from decouple import config
from groq import Groq
from pydantic import BaseModel, Field
import streamlit as st
import os

# Fix for libiomp5md.dll conflict
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load Groq API key
try:
    GROQ_API_KEY = config("GROQ_API_KEY")
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    raise RuntimeError(f"Error loading GROQ_API_KEY: {e}")

# Define the translation model
class Translation(BaseModel):
    translated_text: str = Field(default="Translation unavailable")
    comments: Optional[str] = None

# Translation function
@st.cache_data
def groq_translate(query: str, from_language: str, to_language: str) -> Optional[Translation]:
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a medical translator. Translate the following text from {from_language} to {to_language} "
                               f"with a focus on accurately translating medical terminology. Return a JSON object with a 'translated_text' field."
                },
                {"role": "user", "content": query},
            ],
            model="llama-3.3-70b-versatile",  # Updated model
            temperature=0.2,
            max_tokens=1024,
            stream=False,
            response_format={"type": "json_object"}
        )
        response_data = response.choices[0].message.content
        return Translation.model_validate_json(response_data)
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return None