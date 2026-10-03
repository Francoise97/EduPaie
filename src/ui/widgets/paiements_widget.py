"""Écran listant tous les paiements de l'établissement."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from src.services.paiement_service import PaiementService
from src.services.eleve_service import EleveService
from src.utils.formatters import formater_montant, formater_date


class PaiementsWidget(QWidget):
    """Écran listant tous les paiements."""

    def __init__(self):
        super().__init__()
        self.paiement_service = PaiementService()
        self.eleve_service = EleveService()
        self._build_ui()
        self.rafraichir()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # En-tête
        header = QHBoxLayout()
        titre = QLabel("💰  Tous les paiements")
        titre.setObjectName("Title")
        header.addWidget(titre)
        header.addStretch()
        layout.addLayout(header)

        sous_titre = QLabel("Historique complet des versements enregistrés")
        sous_titre.setObjectName("Subtitle")
        layout.addWidget(sous_titre)

        # Filtres
        filtres = QHBoxLayout()

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText(
            "🔍  Rechercher par nom d'élève ou N° de reçu..."
        )
        self.recherche.setObjectName("SearchBar")
        filtres.addWidget(self.recherche, 1)

        self.filtre_mode = QComboBox()
        self.filtre_mode.addItems([
            "Tous les modes", "Espèces", "Chèque", "Virement", "Mobile Money"
        ])
        filtres.addWidget(self.filtre_mode)

        layout.addLayout(filtres)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Reçu N°", "Date", "Élève", "Classe", "Montant", "Mode"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        h = self.table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        layout.addWidget(self.table, 1)

        # Pied : total
        pied = QHBoxLayout()
        pied.addStretch()
        self.label_total = QLabel("Total affiché : 0 FCFA")
        self.label_total.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1E3A8A; padding: 8px;"
        )
        pied.addWidget(self.label_total)
        layout.addLayout(pied)

        # Connexions
        self.recherche.textChanged.connect(self.rafraichir)
        self.filtre_mode.currentTextChanged.connect(self.rafraichir)

    def rafraichir(self):
        paiements = self.paiement_service.lister_tous()

        terme = self.recherche.text().strip().lower()
        mode = self.filtre_mode.currentText()

        resultats = []
        for p in paiements:
            eleve_nom = f"{p.eleve_nom or ''} {p.eleve_prenom or ''}".lower()
            if terme and terme not in eleve_nom and \
               terme not in (p.numero_recu or "").lower():
                continue
            if mode != "Tous les modes" and p.mode_paiement != mode:
                continue
            resultats.append(p)

        # Remplir le tableau
        self.table.setRowCount(len(resultats))
        total = 0.0

        for row, p in enumerate(resultats):
            eleve = self.eleve_service.obtenir(p.eleve_id)
            classe = eleve.classe if eleve else "—"
            eleve_nom = f"{p.eleve_nom or ''} {p.eleve_prenom or ''}".strip()

            valeurs = [
                p.numero_recu or "-",
                formater_date(p.date_paiement),
                eleve_nom,
                classe,
                formater_montant(p.montant),
                p.mode_paiement,
            ]
            for col, val in enumerate(valeurs):
                item = QTableWidgetItem(val)
                if col in (0, 1, 3, 4, 5):
                    item.setTextAlignment(Qt.AlignCenter)
                if col == 0:
                    item.setForeground(QColor("#1E3A8A"))
                if col == 4:
                    item.setForeground(QColor("#10B981"))
                self.table.setItem(row, col, item)

            total += p.montant

        self.label_total.setText(
            f"Total affiché : {formater_montant(total)}  "
            f"({len(resultats)} paiement(s))"
        )
