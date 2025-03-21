import sys
import os
from pathlib import Path

# Function to dynamically configure CUDA paths
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

# Continue with regular imports
from faster_whisper import WhisperModel
import streamlit as st
from typing import Optional
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# Load Faster-Whisper model
@st.cache_resource
def load_model():
    try:
        return WhisperModel("small", device="cpu")  # Use "cuda" for GPU or "cpu" otherwise
    except Exception as e:
        st.error(f"Failed to load Faster-Whisper model: {e}")
        st.stop()

# Transcription function
def transcribe_audio(audio_file: str) -> Optional[str]:
    if not audio_file:
        st.warning("No audio file provided.")
        return None
    try:
        model = load_model()
        segments, _ = model.transcribe(audio_file)
        return " ".join(segment.text for segment in segments)
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return None
