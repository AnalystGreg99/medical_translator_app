import sys
import os
from pathlib import Path
import streamlit as st
from typing import Optional
from faster_whisper import WhisperModel

# Function to dynamically configure CUDA paths (if needed for GPUs)
def set_cuda_paths():
    venv_base = Path(sys.executable).parent.parent
    nvidia_base_path = venv_base / 'Lib' / 'site-packages' / 'nvidia'
    cuda_path = nvidia_base_path / 'cuda_runtime' / 'bin'
    cublas_path = nvidia_base_path / 'cublas' / 'bin'
    cudnn_path = nvidia_base_path / 'cudnn' / 'bin'
    paths_to_add = [str(cuda_path), str(cublas_path), str(cudnn_path)]
    env_vars = ['CUDA_PATH', 'CUDA_PATH_V12_4', 'PATH']

    for env_var in env_vars:
        current_value = os.environ.get(env_var, '')
        new_value = os.pathsep.join(paths_to_add + [current_value] if current_value else paths_to_add)
        os.environ[env_var] = new_value

# Set CUDA paths before importing any other library
set_cuda_paths()

# Define the cache directory for Hugging Face models
CACHE_DIR = os.path.expanduser("~/.cache/huggingface/hub")

# Load the Whisper model from Hugging Face (or local cache)
@st.cache_resource
def load_model():
    try:
        return WhisperModel(
            "AnalystGreg99/faster-whisper-small",  # Hugging Face repo ID
            device="cpu",                          # Use "cuda" if you want GPU
            download_root=CACHE_DIR,
        )
    except Exception as e:
        st.error(f"Failed to load the Whisper model: {e}\nCache location: {CACHE_DIR}\nEnsure the model is accessible.")
        st.stop()

# Transcription function: takes an audio file and returns the transcribed text.
def transcribe_audio(audio_file: str) -> Optional[str]:
    if not audio_file:
        st.warning("No audio file provided.")
        return None
    try:
        model = load_model()
        segments, _ = model.transcribe(audio_file)
        return " ".join(segment.text for segment in segments)
    except Exception as e:
        st.error(f"Transcription failed: {e}\nEnsure the audio file is compatible and accessible.")
        return None