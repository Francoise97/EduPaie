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
        self.label_titre = QLabel(titre.upper())
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
            "font-size: 13px; padding: 15px; "
            "background-color: #FFFFFF; border: 1px solid #E2E8F0; "
            "border-radius: 10px; color: #475569;"
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

        # ============ REPARTITION STYLISEE ============
        nb_eleves = stats.get("nb_eleves", 0) or 1
        soldes = stats.get("nb_soldes", 0) or 0
        partiels = stats.get("nb_partiels", 0) or 0
        non_payes = stats.get("nb_non_payes", 0) or 0

        # Construire le HTML avec style
        html = "<div style='font-family: Segoe UI Variable Display, Segoe UI, Arial;'>"
        html += "<p style='font-size: 14px; font-weight: 700; color: #1E3A8A; "
        html += "letter-spacing: 1px; margin-bottom: 10px;'>"
        html += "REPARTITION PAR STATUT</p>"

        # Ligne 1 - Soldes (vert)
        pct_soldes = int(soldes * 100 / nb_eleves)
        blocs_soldes = int(round(pct_soldes / 5))
        barre_soldes = "X" * blocs_soldes + "." * (20 - blocs_soldes)
        html += "<p style='font-size: 13px; margin: 6px 0;'>"
        html += "<span style='color: #10B981; font-weight: 700;'>"
        html += "Soldes</span>"
        html += "<span style='color: #10B981; margin-left: 20px;'>"
        html += barre_soldes + "</span>"
        html += "<span style='color: #10B981; font-weight: 700; margin-left: 15px;'>"
        html += str(soldes) + " (" + str(pct_soldes) + "%)</span>"
        html += "</p>"

        # Ligne 2 - Partiels (orange)
        pct_partiels = int(partiels * 100 / nb_eleves)
        blocs_partiels = int(round(pct_partiels / 5))
        barre_partiels = "X" * blocs_partiels + "." * (20 - blocs_partiels)
        html += "<p style='font-size: 13px; margin: 6px 0;'>"
        html += "<span style='color: #F59E0B; font-weight: 700;'>"
        html += "Partiels</span>"
        html += "<span style='color: #F59E0B; margin-left: 10px;'>"
        html += barre_partiels + "</span>"
        html += "<span style='color: #F59E0B; font-weight: 700; margin-left: 15px;'>"
        html += str(partiels) + " (" + str(pct_partiels) + "%)</span>"
        html += "</p>"

        # Ligne 3 - Non payes (rouge)
        pct_non_payes = int(non_payes * 100 / nb_eleves)
        blocs_non_payes = int(round(pct_non_payes / 5))
        barre_non_payes = "X" * blocs_non_payes + "." * (20 - blocs_non_payes)
        html += "<p style='font-size: 13px; margin: 6px 0;'>"
        html += "<span style='color: #EF4444; font-weight: 700;'>"
        html += "Non payes</span>"
        html += "<span style='color: #EF4444; margin-left: 5px;'>"
        html += barre_non_payes + "</span>"
        html += "<span style='color: #EF4444; font-weight: 700; margin-left: 15px;'>"
        html += str(non_payes) + " (" + str(pct_non_payes) + "%)</span>"
        html += "</p>"

        html += "</div>"

        self.label_repartition.setText(html)
        self.label_repartition.setTextFormat(Qt.TextFormat.RichText)

        # ============ DERNIERS PAIEMENTS ============
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