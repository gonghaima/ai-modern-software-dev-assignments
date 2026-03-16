from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral-nemo:12b")
