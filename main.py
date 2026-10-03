"""EduPaie - Point d'entrée de l'application."""
import sys
from pathlib import Path

# Ajouter la racine au PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow


def charger_styles(app: QApplication) -> None:
    """Charge la feuille de style QSS."""
    qss_path = Path(__file__).parent / "src" / "ui" / "resources" / "styles.qss"
    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def main() -> int:
    # 1) Initialiser la base (crée les tables si absentes)
    DatabaseManager.initialize()

    # 2) Créer l'application Qt
    app = QApplication(sys.argv)
    app.setApplicationName("EduPaie")
    app.setOrganizationName("EduPaie")

    # 3) Charger les styles
    charger_styles(app)

    # 4) Ouvrir la fenêtre principale
    fenetre = MainWindow()
    fenetre.show()

    # 5) Boucle d'événements
    code = app.exec()

    # 6) Nettoyage
    DatabaseManager.close()
    return code


if __name__ == "__main__":
    sys.exit(main())
