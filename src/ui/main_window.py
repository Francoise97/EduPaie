"""Fenêtre principale de l'application."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
    QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt

from src.ui.widgets.eleves_widget import ElevesWidget
from src.ui.widgets.dashboard_widget import DashboardWidget
from src.ui.widgets.fiche_eleve_widget import FicheEleveWidget
from src.ui.widgets.paiements_widget import PaiementsWidget


class MainWindow(QMainWindow):
    """Fenêtre principale avec barre latérale de navigation."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduPaie — Gestion des paiements scolaires")
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

        self.stack.addWidget(self.dashboard)        # index 0
        self.stack.addWidget(self.eleves_widget)    # index 1
        self.stack.addWidget(self.fiche_widget)     # index 2
        self.stack.addWidget(self.paiements_widget) # index 3

        layout.addWidget(self.stack, 1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")

    def _creer_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("SideBar")
        sidebar.setFixedWidth(220)

        vbox = QVBoxLayout(sidebar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        logo = QLabel("🎓 EduPaie")
        logo.setObjectName("Logo")
        vbox.addWidget(logo)

        self.btn_dashboard = QPushButton("📊  Tableau de bord")
        self.btn_eleves    = QPushButton("👥  Élèves")
        self.btn_paiement  = QPushButton("💰  Paiements")
        self.btn_recus     = QPushButton("📄  Reçus")
        self.btn_param     = QPushButton("⚙️  Paramètres")

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
        self.btn_recus.clicked.connect(self._afficher_recus)
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

    def _afficher_page(self, index: int, bouton: QPushButton):
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

    def _afficher_fiche(self, eleve_id: int):
        self.fiche_widget.charger_eleve(eleve_id)
        self.stack.setCurrentIndex(2)
        for b in [self.btn_dashboard, self.btn_eleves, self.btn_paiement,
                  self.btn_recus, self.btn_param]:
            b.setChecked(False)

    def _afficher_recus(self):
        QMessageBox.information(
            self, "Reçus",
            "La gestion des reçus arrive à l'étape 5."
        )

    def _afficher_parametres(self):
        QMessageBox.information(
            self, "Paramètres",
            "Les paramètres arrivent plus tard."
        )
