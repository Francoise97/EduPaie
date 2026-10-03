"""Ecran liste des eleves."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from src.services.eleve_service import EleveService
from src.utils.formatters import formater_montant, libelle_statut
from src.ui.dialogs.eleve_dialog import EleveDialog
from src.ui.dialogs.paiement_dialog import PaiementDialog


class ElevesWidget(QWidget):
    eleve_selectionne = Signal(int)
    donnees_modifiees = Signal()

    def __init__(self):
        super().__init__()
        self.service = EleveService()
        self._build_ui()
        self.rafraichir()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        titre = QLabel("Liste des eleves")
        titre.setObjectName("Title")
        header.addWidget(titre)
        header.addStretch()

        self.btn_nouveau = QPushButton("+  Nouvel eleve")
        self.btn_nouveau.setObjectName("Success")
        header.addWidget(self.btn_nouveau)
        layout.addLayout(header)

        filtres = QHBoxLayout()

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Rechercher un eleve...")
        self.recherche.setObjectName("SearchBar")
        filtres.addWidget(self.recherche, 1)

        self.filtre_classe = QComboBox()
        self.filtre_classe.addItem("Toutes les classes")
        for c in self.service.lister_classes():
            self.filtre_classe.addItem(c)
        filtres.addWidget(self.filtre_classe)

        self.filtre_statut = QComboBox()
        self.filtre_statut.addItems([
            "Tous les statuts", "Solde", "Partiellement paye", "Non paye"
        ])
        filtres.addWidget(self.filtre_statut)

        layout.addLayout(filtres)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom", "Prenom", "Classe", "Total du", "Paye", "Statut"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header_view.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header_view.setSectionResizeMode(6, QHeaderView.ResizeToContents)

        layout.addWidget(self.table, 1)

        actions = QHBoxLayout()
        actions.addStretch()

        self.btn_fiche = QPushButton("Voir la fiche et historique")
        self.btn_fiche.setObjectName("Secondary")

        self.btn_paiement = QPushButton("Enregistrer un paiement")
        self.btn_paiement.setObjectName("Success")

        self.btn_modifier = QPushButton("Modifier")
        self.btn_modifier.setObjectName("Secondary")

        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_supprimer.setObjectName("Danger")

        for b in [self.btn_fiche, self.btn_paiement,
                  self.btn_modifier, self.btn_supprimer]:
            actions.addWidget(b)

        layout.addLayout(actions)

        self.recherche.textChanged.connect(self.rafraichir)
        self.filtre_classe.currentTextChanged.connect(self.rafraichir)
        self.filtre_statut.currentTextChanged.connect(self.rafraichir)
        self.btn_nouveau.clicked.connect(self._nouvel_eleve)
        self.btn_modifier.clicked.connect(self._modifier_eleve)
        self.btn_supprimer.clicked.connect(self._supprimer_eleve)
        self.btn_fiche.clicked.connect(self._voir_fiche)
        self.btn_paiement.clicked.connect(self._enregistrer_paiement)
        self.table.doubleClicked.connect(lambda _idx: self._voir_fiche())

    def rafraichir(self):
        terme = self.recherche.text().strip()
        classe = self.filtre_classe.currentText()
        statut = self.filtre_statut.currentText()

        if terme:
            eleves = self.service.rechercher(terme)
        else:
            eleves = self.service.lister_tous()

        if classe != "Toutes les classes":
            eleves = [e for e in eleves if e.classe == classe]

        if statut != "Tous les statuts":
            eleves = [e for e in eleves if e.statut == statut]

        self.table.setRowCount(len(eleves))
        for row, e in enumerate(eleves):
            self._remplir_ligne(row, e)

    def _remplir_ligne(self, row, eleve):
        valeurs = [
            str(eleve.id),
            eleve.nom,
            eleve.prenom,
            eleve.classe,
            formater_montant(eleve.frais_totaux),
            formater_montant(eleve.total_paye),
            libelle_statut(eleve.statut),
        ]
        couleurs = {
            "Solde": QColor("#10B981"),
            "Partiellement paye": QColor("#F59E0B"),
            "Non paye": QColor("#EF4444"),
        }

        for col, val in enumerate(valeurs):
            item = QTableWidgetItem(val)
            if col in (0, 4, 5):
                item.setTextAlignment(Qt.AlignCenter)
            if col == 6:
                item.setForeground(couleurs.get(eleve.statut, QColor("#1E293B")))
            self.table.setItem(row, col, item)

    def _get_selection_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        if not item:
            return None
        return int(item.text())

    def _nouvel_eleve(self):
        dialog = EleveDialog(self)
        if dialog.exec():
            self.rafraichir()
            self.donnees_modifiees.emit()

    def _modifier_eleve(self):
        eid = self._get_selection_id()
        if eid is None:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne un eleve dans la liste.")
            return
        eleve = self.service.obtenir(eid)
        dialog = EleveDialog(self, eleve=eleve)
        if dialog.exec():
            self.rafraichir()
            self.donnees_modifiees.emit()

    def _supprimer_eleve(self):
        eid = self._get_selection_id()
        if eid is None:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne un eleve dans la liste.")
            return
        eleve = self.service.obtenir(eid)
        reponse = QMessageBox.question(
            self, "Confirmer la suppression",
            "Supprimer " + eleve.nom_complet + " (" + eleve.classe + ") ?\n\n"
            "Tous ses paiements et recus seront aussi supprimes.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reponse == QMessageBox.Yes:
            ok, msg = self.service.supprimer(eid)
            if ok:
                QMessageBox.information(self, "Succes", msg)
                self.rafraichir()
                self.donnees_modifiees.emit()
            else:
                QMessageBox.critical(self, "Erreur", msg)

    def _voir_fiche(self):
        eid = self._get_selection_id()
        if eid is None:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne un eleve dans la liste.")
            return
        self.eleve_selectionne.emit(eid)

    def _enregistrer_paiement(self):
        eid = self._get_selection_id()
        if eid is None:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne un eleve dans la liste.")
            return

        eleve = self.service.obtenir(eid)
        if eleve.est_solde:
            QMessageBox.information(
                self, "Deja solde",
                eleve.nom_complet + " a deja paye la totalite de ses frais."
            )
            return

        dialog = PaiementDialog(self, eleve=eleve)
        if dialog.exec():
            self.rafraichir()
            self.donnees_modifiees.emit()
