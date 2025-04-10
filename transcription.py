import sys
import os
from pathlib import Path
import shutil
from faster_whisper import WhisperModel
import streamlit as st
from typing import Optional

# --- CUDA Configuration ---
def set_cuda_paths():
    """
    Configure CUDA paths for GPU support if available.
    Adjusts environment variables to include NVIDIA library paths.
    """
    venv_base = Path(sys.executable).parent.parent
    nvidia_base_path = venv_base / 'Lib' / 'site-packages' / 'nvidia'
    paths_to_add = [
        str(nvidia_base_path / 'cuda_runtime' / 'bin'),
        str(nvidia_base_path / 'cublas' / 'bin'),
        str(nvidia_base_path / 'cudnn' / 'bin')
    ]

    for env_var in ['CUDA_PATH', 'CUDA_PATH_V12_4', 'PATH']:
        current_value = os.environ.get(env_var, '')
        new_value = os.pathsep.join(paths_to_add + [current_value] if current_value else paths_to_add)
        os.environ[env_var] = new_value

set_cuda_paths()  # Execute before loading the model

# --- Cache Directory Configuration ---
CACHE_DIR = os.path.expanduser("~/.cache/huggingface/hub")

# --- Ensure Model Cache ---
def ensure_model_cache():
    """
    Ensures the model directory is prepared for deployment.
    If the model files are missing, raises an error.
    """
    model_dir = "models/Systran--faster-whisper-small"  # Adjust this path to match your local directory structure
    cache_target = os.path.join(CACHE_DIR, "models--Systran--faster-whisper-small")

    # Verify the source model directory exists
    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"Source model directory not found: {model_dir}")

    # Ensure the target cache directory exists
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Copy model files to the cache directory if not already present
    if not os.path.exists(cache_target):
        try:
            shutil.copytree(model_dir, cache_target)
            print(f"Model successfully cached at: {cache_target}")
        except Exception as e:
            raise RuntimeError(f"Failed to copy model files to cache: {e}")
    else:
        print(f"Model already cached at: {cache_target}")

ensure_model_cache()  # Ensure cache is prepared before using the model

# --- Load Model ---
@st.cache_resource
def load_model():
    """
    Loads the Faster-Whisper model from the cache directory.
    Returns:
        WhisperModel: Loaded model instance.
    """
    try:
        return WhisperModel(
            "Systran/faster-whisper-small",  # Model identifier matching your cache
            device="cpu",  # Use "cuda" for GPU acceleration if available
            download_root=CACHE_DIR,  # Parent directory of all cached models
            local_files_only=True  # Ensure only local files are used
        )
    except Exception as e:
        st.error(f"""
        Failed to load the Whisper model: {e}
        Cache location: {CACHE_DIR}
        Ensure the model files are correctly placed in the cache directory.
        """)
        st.stop()

# --- Audio Transcription Function ---
def transcribe_audio(audio_file: str) -> Optional[str]:
    """
    Transcribes an audio file using the loaded Whisper model.
    Args:
        audio_file (str): Path to the audio file.
    Returns:
        Optional[str]: Transcribed text if successful, else None.
    """
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
