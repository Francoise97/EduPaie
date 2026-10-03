"""Tableau de bord."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from src.services.eleve_service import EleveService
from src.services.paiement_service import PaiementService
from src.utils.formatters import formater_montant, formater_date


class CarteStat(QFrame):
    def __init__(self, icone, titre, valeur="0", couleur="#1E3A8A"):
        super().__init__()
        self.setObjectName("Card")
        self.setMinimumHeight(110)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        self.label_titre = QLabel(icone + "  " + titre.upper())
        self.label_titre.setObjectName("CardTitle")
        layout.addWidget(self.label_titre)

        self.label_valeur = QLabel(valeur)
        self.label_valeur.setObjectName("CardValue")
        self.label_valeur.setStyleSheet(
            "color: " + couleur + "; font-size: 22px; font-weight: bold;"
        )
        layout.addWidget(self.label_valeur)
        layout.addStretch()

    def set_valeur(self, valeur):
        self.label_valeur.setText(valeur)


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.eleve_service = EleveService()
        self.paiement_service = PaiementService()
        self._build_ui()
        self.rafraichir()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        titre = QLabel("Tableau de bord")
        titre.setObjectName("Title")
        layout.addWidget(titre)

        sous_titre = QLabel("Vue d'ensemble de la situation des paiements")
        sous_titre.setObjectName("Subtitle")
        layout.addWidget(sous_titre)

        cartes = QHBoxLayout()
        cartes.setSpacing(12)

        self.carte_eleves = CarteStat("ELEVES", "Eleves", "0", "#1E3A8A")
        self.carte_encaisse = CarteStat("ENCAISSE", "Total encaisse", "0 FCFA", "#10B981")
        self.carte_restant = CarteStat("RESTANT", "Restant du", "0 FCFA", "#F59E0B")
        self.carte_non_soldes = CarteStat("ALERTE", "Non soldes", "0", "#EF4444")

        for c in [self.carte_eleves, self.carte_encaisse,
                  self.carte_restant, self.carte_non_soldes]:
            cartes.addWidget(c)

        layout.addLayout(cartes)

        self.label_repartition = QLabel("")
        self.label_repartition.setStyleSheet(
            "font-size: 13px; padding: 10px 0; color: #475569;"
        )
        layout.addWidget(self.label_repartition)

        titre2 = QLabel("Derniers paiements")
        titre2.setObjectName("Title")
        titre2.setStyleSheet("font-size: 16px; margin-top: 8px;")
        layout.addWidget(titre2)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Recu N", "Eleve", "Montant", "Date", "Mode"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setMaximumHeight(240)

        h = self.table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)
        layout.addStretch()

    def rafraichir(self):
        stats = self.eleve_service.statistiques()

        self.carte_eleves.set_valeur(str(stats.get("nb_eleves", 0)))
        self.carte_encaisse.set_valeur(
            formater_montant(stats.get("total_encaisse", 0))
        )
        self.carte_restant.set_valeur(
            formater_montant(stats.get("total_restant", 0))
        )
        nb_non_soldes = (stats.get("nb_non_payes", 0) or 0) + \
                        (stats.get("nb_partiels", 0) or 0)
        self.carte_non_soldes.set_valeur(str(nb_non_soldes))

        nb_eleves = stats.get("nb_eleves", 0) or 1
        soldes = stats.get("nb_soldes", 0) or 0
        partiels = stats.get("nb_partiels", 0) or 0
        non_payes = stats.get("nb_non_payes", 0) or 0

        def barre(n):
            nb_blocs = int(round((n / nb_eleves) * 20))
            return "X" * nb_blocs + "." * (20 - nb_blocs)

        self.label_repartition.setText(
            "Soldes        : " + barre(soldes) + "  " + str(soldes) + " eleves "
            "(" + str(soldes * 100 // nb_eleves) + "%)\n"
            "Partiels      : " + barre(partiels) + "  " + str(partiels) + " eleves "
            "(" + str(partiels * 100 // nb_eleves) + "%)\n"
            "Non payes     : " + barre(non_payes) + "  " + str(non_payes) + " eleves "
            "(" + str(non_payes * 100 // nb_eleves) + "%)"
        )

        paiements = self.paiement_service.derniers(8)
        self.table.setRowCount(len(paiements))

        for row, p in enumerate(paiements):
            eleve_nom = ((p.eleve_nom or "") + " " + (p.eleve_prenom or "")).strip()
            valeurs = [
                p.numero_recu or "-",
                eleve_nom,
                formater_montant(p.montant),
                formater_date(p.date_paiement),
                p.mode_paiement,
            ]
            for col, val in enumerate(valeurs):
                item = QTableWidgetItem(val)
                if col in (2, 3, 4):
                    item.setTextAlignment(Qt.AlignCenter)
                if col == 0:
                    item.setForeground(QColor("#1E3A8A"))
                self.table.setItem(row, col, item)
