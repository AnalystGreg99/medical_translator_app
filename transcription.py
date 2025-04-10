from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download
import streamlit as st
import os

# Configuration
MODEL_REPO = "analystgreg99/faster-whisper-small"  # Hugging Face model repo
CACHE_DIR = os.path.expanduser("~/.cache/huggingface/hub")  # Standard cache location

@st.cache_resource
def load_model():
    """Load model with automatic download from Hugging Face Hub"""
    try:
        # Download model if not cached (will use cached version if available)
        model_dir = snapshot_download(
            repo_id=MODEL_REPO,
            cache_dir=CACHE_DIR,
            local_files_only=False  # Allow download if not cached
        )
        
        return WhisperModel(
            model_size_or_path=model_dir,
            device="cpu",  # or "cuda" if GPU available
            compute_type="int8"
        )
    except Exception as e:
        st.error(f"""Failed to load model: {e}
                 Please check:
                 1. Internet connection
                 2. Model repository access: {MODEL_REPO}
                 3. Available disk space""")
        st.stop()

def transcribe_audio(audio_path):
    model = load_model()
    segments, _ = model.transcribe(audio_path)
    return " ".join(segment.text for segment in segments)
