"""Configuration pytest pour EduPaie."""
import sys
from pathlib import Path

# Ajouter la racine au PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
