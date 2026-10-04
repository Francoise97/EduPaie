"""Connexion SQLite centralisee pour EduPaie."""
import sqlite3
import sys
from pathlib import Path


def _resource_path(relative_path):
    """Retourne le chemin absolu vers une ressource.

    Fonctionne en mode developpement ET en mode PyInstaller (exe).
    """
    if hasattr(sys, "_MEIPASS"):
        # Mode PyInstaller : les ressources sont dans un dossier temporaire
        return Path(sys._MEIPASS) / relative_path
    # Mode developpement : racine du projet
    return Path(__file__).resolve().parents[2] / relative_path


# Chemin de la base de donnees (TOUJOURS a cote de l'exe ou du projet)
if hasattr(sys, "_MEIPASS"):
    # En mode exe : le .exe est dans dist/, la base doit etre dans dist/data/
    DB_PATH = Path(sys.executable).parent / "data" / "edupaie.db"
else:
    DB_PATH = Path(__file__).resolve().parents[2] / "data" / "edupaie.db"

# Chemin du schema SQL (ressource embarquee dans l'exe)
SCHEMA_PATH = _resource_path("src/database/schema.sql")


class DatabaseManager:
    """Gere UNE connexion partagee a SQLite."""

    _conn = None

    @classmethod
    def get_connection(cls):
        if cls._conn is None:
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            cls._conn = sqlite3.connect(DB_PATH)
            cls._conn.row_factory = sqlite3.Row
            cls._conn.execute("PRAGMA foreign_keys = ON")
        return cls._conn

    @classmethod
    def initialize(cls):
        conn = cls.get_connection()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()

    @classmethod
    def close(cls):
        if cls._conn is not None:
            cls._conn.close()
            cls._conn = None
