import os
import sys
from pathlib import Path
from typing import Optional
import streamlit as st
from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download

# Constants
MODEL_REPO = "AnalystGreg99/faster-whisper-small"  # Updated model repository
CACHE_DIR = os.path.expanduser("~/.cache/huggingface/hub")

def set_cuda_paths():
    """Configure CUDA paths if GPU is available."""
    if st.secrets.get("USE_GPU", "false").lower() == "true":
        try:
            venv_base = Path(sys.executable).parent.parent
            nvidia_base_path = venv_base / 'Lib' / 'site-packages' / 'nvidia'
            paths_to_add = [
                str(nvidia_base_path / 'cuda_runtime' / 'bin'),
                str(nvidia_base_path / 'cublas' / 'bin'),
                str(nvidia_base_path / 'cudnn' / 'bin')
            ]
            
            for env_var in ['CUDA_PATH', 'CUDA_PATH_V12_4', 'PATH']:
                current = os.environ.get(env_var, '')
                os.environ[env_var] = os.pathsep.join(paths_to_add + [current] if current else paths_to_add)
        except Exception as e:
            st.warning(f"CUDA path configuration failed: {e}")

# Initialize CUDA paths early
set_cuda_paths()

@st.cache_resource
def load_model():
    """Load Whisper model with automatic download from Hugging Face Hub."""
    try:
        # Ensure model is downloaded
        model_dir = snapshot_download(
            repo_id=MODEL_REPO,
            cache_dir=CACHE_DIR,
            local_files_only=False,
            resume_download=True
        )
        
        device = "cuda" if st.secrets.get("USE_GPU", "false").lower() == "true" else "cpu"
        
        return WhisperModel(
            model_size_or_path=model_dir,
            device=device,
            compute_type="int8",
            download_root=CACHE_DIR
        )
    except Exception as e:
        st.error(f"""Model loading failed: {e}
                 Cache location: {CACHE_DIR}
                 Please check:
                 1. Internet connection
                 2. Model repository access
                 3. Available disk space""")
        st.stop()

def transcribe_audio(audio_file: str) -> Optional[str]:
    """Transcribe audio file using Whisper model."""
    if not audio_file or not os.path.exists(audio_file):
        st.warning("Invalid audio file path")
        return None
        
    try:
        model = load_model()
        segments, _ = model.transcribe(
            audio_file,
            beam_size=5,
            vad_filter=True
        )
        return " ".join(segment.text for segment in segments)
    except Exception as e:
        st.error(f"""Transcription failed: {e}
                 Possible issues:
                 1. Corrupted audio file
                 2. Unsupported format
                 3. Insufficient resources""")
        return None