"""Project settings and paths shared by the application modules."""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "chess.db"
IDS_PATH = DATA_DIR / "id.txt"
BRACKET_PATH = DATA_DIR / "array.txt"
COMPETITORS_PATH = DATA_DIR / "competitorlist.txt"
ADMIN_PASSWORD = os.environ.get("CHESS_ADMIN_PASSWORD", "HysIct2024!")
