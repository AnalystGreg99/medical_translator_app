import sys
import os
from pathlib import Path
import shutil
from faster_whisper import WhisperModel
import streamlit as st
from typing import Optional

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

# Define the cache directory
CACHE_DIR = os.path.expanduser("~/.cache/huggingface/hub")

# Function to ensure the model is copied to the cache for deployment
def ensure_model_cache():
    model_dir = "models/Systran--faster-whisper-small"  # Adjust this path to where your model files are located locally

    # Create the cache directory if it doesn't exist
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Copy model files to the cache if not already present
    if not os.path.exists(os.path.join(CACHE_DIR, "models--Systran--faster-whisper-small")):
        shutil.copytree(model_dir, os.path.join(CACHE_DIR, "models--Systran--faster-whisper-small"))

# Ensure the model cache is prepared before loading the model
ensure_model_cache()

@st.cache_resource
def load_model():
    try:
        # Load the Faster-Whisper model
        return WhisperModel(
            "Systran/faster-whisper-small",  # Model identifier matching your cache
            device="cpu",  # Use "cuda" for GPU acceleration if available
            download_root=CACHE_DIR,  # Parent directory of all cached models
            local_files_only=False  # Force usage of local files only
        )
    except Exception as e:
        st.error(f"Failed to load model: {e}\n\n"
                 f"Cache location: {CACHE_DIR}\n"
                 f"Try checking if the model is correctly placed in the cache.")
        st.stop()

# Transcription function
def transcribe_audio(audio_file: str) -> Optional[str]:
    if not audio_file:
        st.warning("No audio file provided.")
        return None
    try:
        # Load the model and transcribe the audio
        model = load_model()
        segments, _ = model.transcribe(audio_file)
        return " ".join(segment.text for segment in segments)
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return None
