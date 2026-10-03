"""Connexion SQLite centralisée pour EduPaie."""
import sqlite3
from pathlib import Path

# Racine du projet (remonte depuis src/database/)
ROOT_DIR    = Path(__file__).resolve().parents[2]
DB_PATH     = ROOT_DIR / "data" / "edupaie.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


class DatabaseManager:
    """Gère UNE connexion partagée à SQLite."""

    _conn: sqlite3.Connection | None = None

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._conn is None:
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            cls._conn = sqlite3.connect(DB_PATH)
            cls._conn.row_factory = sqlite3.Row
            cls._conn.execute("PRAGMA foreign_keys = ON")
        return cls._conn

    @classmethod
    def initialize(cls) -> None:
        """Crée les tables si elles n'existent pas."""
        conn = cls.get_connection()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()

    @classmethod
    def close(cls) -> None:
        if cls._conn is not None:
            cls._conn.close()
            cls._conn = None
