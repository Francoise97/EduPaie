"""Fenetre principale."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
    QStatusBar, QMessageBox, QDialog, QFormLayout
)
from PySide6.QtCore import Qt

from src.ui.widgets.eleves_widget import ElevesWidget
from src.ui.widgets.dashboard_widget import DashboardWidget
from src.ui.widgets.fiche_eleve_widget import FicheEleveWidget
from src.ui.widgets.paiements_widget import PaiementsWidget
from src.ui.widgets.recus_widget import RecusWidget
from src.services.eleve_service import EleveService
from src.config import (
    ECOLE_NOM, ECOLE_ADRESSE, ECOLE_TELEPHONE, ECOLE_EMAIL,
    DEVISE, ANNEE_SCOLAIRE_PAR_DEFAUT, VERSION
)


class ParametresDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parametres")
        self.setMinimumWidth(400)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        titre = QLabel("Parametres de l'application")
        titre.setObjectName("Title")
        layout.addWidget(titre)

        frame = QFrame()
        frame.setObjectName("Card")
        form = QFormLayout(frame)
        form.setContentsMargins(16, 12, 16, 12)

        stats = EleveService().statistiques()

        form.addRow("Nom de l'ecole :", QLabel(ECOLE_NOM))
        form.addRow("Adresse :", QLabel(ECOLE_ADRESSE))
        form.addRow("Telephone :", QLabel(ECOLE_TELEPHONE))
        form.addRow("Email :", QLabel(ECOLE_EMAIL))
        form.addRow("", QLabel(""))
        form.addRow("Annee scolaire :", QLabel(ANNEE_SCOLAIRE_PAR_DEFAUT))
        form.addRow("Devise :", QLabel(DEVISE))
        form.addRow("Nombre d'eleves :", QLabel(str(stats.get("nb_eleves", 0))))
        form.addRow("Version :", QLabel(VERSION))
        form.addRow("Technologie :", QLabel("Python + PySide6 + SQLite"))

        layout.addWidget(frame)

        btn = QPushButton("Fermer")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduPaie - Gestion des paiements scolaires")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = self._creer_sidebar()
        layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.dashboard = DashboardWidget()
        self.eleves_widget = ElevesWidget()
        self.fiche_widget = FicheEleveWidget()
        self.paiements_widget = PaiementsWidget()
        self.recus_widget = RecusWidget()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.eleves_widget)
        self.stack.addWidget(self.fiche_widget)
        self.stack.addWidget(self.paiements_widget)
        self.stack.addWidget(self.recus_widget)

        layout.addWidget(self.stack, 1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pret")

    def _creer_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("SideBar")
        sidebar.setFixedWidth(220)

        vbox = QVBoxLayout(sidebar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        logo = QLabel("EDUPAIE")
        logo.setObjectName("Logo")
        vbox.addWidget(logo)

        sous_titre = QLabel("GESTION SCOLAIRE")
        sous_titre.setObjectName("Subtitle")
        vbox.addWidget(sous_titre)

        self.btn_dashboard = QPushButton("Tableau de bord")
        self.btn_eleves    = QPushButton("Eleves")
        self.btn_paiement  = QPushButton("Paiements")
        self.btn_recus     = QPushButton("Recus")
        self.btn_param     = QPushButton("Parametres")

        for b in [self.btn_dashboard, self.btn_eleves, self.btn_paiement,
                  self.btn_recus, self.btn_param]:
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
            vbox.addWidget(b)

        vbox.addStretch()

        version = QLabel("  v1.0.0")
        version.setStyleSheet("color: #93C5FD; padding: 12px; font-size: 11px;")
        vbox.addWidget(version)

        self.btn_dashboard.setChecked(True)
        return sidebar

    def _connect_signals(self):
        self.btn_dashboard.clicked.connect(
            lambda: self._afficher_page(0, self.btn_dashboard)
        )
        self.btn_eleves.clicked.connect(
            lambda: self._afficher_page(1, self.btn_eleves)
        )
        self.btn_paiement.clicked.connect(
            lambda: self._afficher_page(3, self.btn_paiement)
        )
        self.btn_recus.clicked.connect(
            lambda: self._afficher_page(4, self.btn_recus)
        )
        self.btn_param.clicked.connect(self._afficher_parametres)

        self.eleves_widget.eleve_selectionne.connect(self._afficher_fiche)

        self.fiche_widget.retour_demande.connect(
            lambda: self._afficher_page(1, self.btn_eleves)
        )

        self.eleves_widget.donnees_modifiees.connect(self.dashboard.rafraichir)
        self.fiche_widget.paiement_enregistre.connect(self.dashboard.rafraichir)
        self.fiche_widget.paiement_enregistre.connect(
            self.paiements_widget.rafraichir
        )
        self.fiche_widget.paiement_enregistre.connect(
            self.recus_widget.rafraichir
        )

    def _afficher_page(self, index, bouton):
        self.stack.setCurrentIndex(index)
        for b in [self.btn_dashboard, self.btn_eleves, self.btn_paiement,
                  self.btn_recus, self.btn_param]:
            b.setChecked(b is bouton)
        if index == 0:
            self.dashboard.rafraichir()
        elif index == 1:
            self.eleves_widget.rafraichir()
        elif index == 3:
            self.paiements_widget.rafraichir()
        elif index == 4:
            self.recus_widget.rafraichir()

    def _afficher_fiche(self, eleve_id):
        self.fiche_widget.charger_eleve(eleve_id)
        self.stack.setCurrentIndex(2)
        for b in [self.btn_dashboard, self.btn_eleves, self.btn_paiement,
                  self.btn_recus, self.btn_param]:
            b.setChecked(False)

    def _afficher_parametres(self):
        dialog = ParametresDialog(self)
        dialog.exec()
