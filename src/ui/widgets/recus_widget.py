
"""Ecran listant tous les recus emis."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from src.services.recu_service import RecuService
from src.services.eleve_service import EleveService
from src.services.pdf_service import PDFService
from src.utils.formatters import formater_montant, formater_date
from src.ui.dialogs.recu_dialog import RecuDialog


class RecusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.recu_service = RecuService()
        self.eleve_service = EleveService()
        self.pdf_service = PDFService()
        self._build_ui()
        self.rafraichir()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        titre = QLabel("Tous les recus emis")
        titre.setObjectName("Title")
        header.addWidget(titre)
        header.addStretch()
        layout.addLayout(header)

        sous_titre = QLabel("Liste de tous les recus numerotes")
        sous_titre.setObjectName("Subtitle")
        layout.addWidget(sous_titre)

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText(
            "Rechercher par numero de recu ou nom d'eleve..."
        )
        self.recherche.setObjectName("SearchBar")
        layout.addWidget(self.recherche)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Recu N", "Date", "Eleve", "Montant", "Solde apres", "PDF"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(lambda _idx: self._voir_recu())

        h = self.table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        layout.addWidget(self.table, 1)

        pied = QHBoxLayout()
        pied.addStretch()

        self.btn_voir = QPushButton("Voir le recu selectionne")
        self.btn_voir.setObjectName("Secondary")
        self.btn_voir.clicked.connect(self._voir_recu)
        pied.addWidget(self.btn_voir)

        self.label_total = QLabel("Total : 0 recus")
        self.label_total.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1E3A8A; padding: 8px;"
        )
        pied.addWidget(self.label_total)
        layout.addLayout(pied)

        self.recherche.textChanged.connect(self.rafraichir)

    def rafraichir(self):
        recus = self.recu_service.lister_tous()
        terme = self.recherche.text().strip().lower()

        resultats = []
        for r in recus:
            eleve = self.eleve_service.obtenir(r.eleve_id)
            eleve_nom = eleve.nom_complet.lower() if eleve else ""
            if terme and terme not in eleve_nom and \
               terme not in (r.numero_unique or "").lower():
                continue
            resultats.append((r, eleve))

        self.table.setRowCount(len(resultats))

        for row, (r, eleve) in enumerate(resultats):
            eleve_nom = eleve.nom_complet if eleve else "-"
            a_pdf = "Oui" if r.chemin_pdf else "Non"
            valeurs = [
                r.numero_unique,
                formater_date(r.date_emission),
                eleve_nom,
                formater_montant(r.montant_paye),
                formater_montant(r.solde_apres),
                a_pdf,
            ]
            for col, val in enumerate(valeurs):
                item = QTableWidgetItem(val)
                if col != 2:
                    item.setTextAlignment(Qt.AlignCenter)
                if col == 0:
                    item.setForeground(QColor("#1E3A8A"))
                    item.setData(Qt.UserRole, r.id)
                if col == 3:
                    item.setForeground(QColor("#10B981"))
                if col == 4:
                    item.setForeground(QColor("#EF4444"))
                if col == 5:
                    if a_pdf == "Oui":
                        item.setForeground(QColor("#10B981"))
                    else:
                        item.setForeground(QColor("#94A3B8"))
                self.table.setItem(row, col, item)

        self.label_total.setText("Total : " + str(len(resultats)) + " recus")

    def _voir_recu(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne un recu dans la liste.")
            return
        item = self.table.item(row, 0)
        recu_id = item.data(Qt.UserRole)
        if recu_id:
            dialog = RecuDialog(self, recu_id=recu_id)
            self.rafraichir()
