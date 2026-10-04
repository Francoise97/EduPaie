"""Fiche eleve avec historique des paiements."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QFormLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from src.services.eleve_service import EleveService
from src.services.paiement_service import PaiementService
from src.utils.formatters import formater_montant, formater_date, libelle_statut
from src.ui.dialogs.paiement_dialog import PaiementDialog


class FicheEleveWidget(QWidget):
    retour_demande = Signal()
    paiement_enregistre = Signal()

    def __init__(self):
        super().__init__()
        self.eleve_service = EleveService()
        self.paiement_service = PaiementService()
        self.eleve = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        haut = QHBoxLayout()

        btn_retour = QPushButton("<  Retour a la liste")
        btn_retour.setObjectName("Secondary")
        btn_retour.clicked.connect(self.retour_demande.emit)
        haut.addWidget(btn_retour)

        haut.addStretch()

        self.btn_paiement = QPushButton("Enregistrer un paiement")
        self.btn_paiement.setObjectName("Success")
        self.btn_paiement.setMinimumWidth(220)
        self.btn_paiement.setMinimumHeight(38)
        self.btn_paiement.clicked.connect(self._nouveau_paiement)
        haut.addWidget(self.btn_paiement)

        layout.addLayout(haut)

        self.titre = QLabel("Fiche eleve")
        self.titre.setObjectName("Title")
        layout.addWidget(self.titre)

        self.frame_infos = QFrame()
        self.frame_infos.setObjectName("Card")
        self.infos_layout = QFormLayout(self.frame_infos)
        self.infos_layout.setContentsMargins(16, 12, 16, 12)
        layout.addWidget(self.frame_infos)

        self.frame_situation = QFrame()
        self.frame_situation.setObjectName("Card")
        sit_layout = QVBoxLayout(self.frame_situation)
        sit_layout.setContentsMargins(16, 12, 16, 12)

        self.lbl_situation = QLabel("")
        self.lbl_situation.setStyleSheet("font-size: 14px;")
        sit_layout.addWidget(self.lbl_situation)
        layout.addWidget(self.frame_situation)

        titre2 = QLabel("Historique des paiements")
        titre2.setObjectName("Title")
        titre2.setStyleSheet("font-size: 16px;")
        layout.addWidget(titre2)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Recu N", "Date", "Montant", "Mode", "Solde apres",
            "Reference", "Observation"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(200)

        h = self.table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(6, QHeaderView.Stretch)

        layout.addWidget(self.table, 1)

        self.lbl_vide = QLabel("Aucun paiement enregistre pour cet eleve.")
        self.lbl_vide.setAlignment(Qt.AlignCenter)
        self.lbl_vide.setStyleSheet(
            "color: #94A3B8; padding: 20px; font-style: italic;"
        )
        layout.addWidget(self.lbl_vide)
        self.lbl_vide.setVisible(False)

    def charger_eleve(self, eleve_id):
        self.eleve = self.eleve_service.obtenir(eleve_id)
        if not self.eleve:
            QMessageBox.warning(self, "Erreur", "Eleve introuvable.")
            return

        self.titre.setText("Fiche de " + self.eleve.nom_complet)

        while self.infos_layout.rowCount() > 0:
            self.infos_layout.removeRow(0)

        self.infos_layout.addRow("Nom :", QLabel(self.eleve.nom))
        self.infos_layout.addRow("Prenom :", QLabel(self.eleve.prenom))
        self.infos_layout.addRow("Classe :", QLabel(self.eleve.classe))
        self.infos_layout.addRow("Annee scolaire :", QLabel(self.eleve.annee_scolaire))
        self.infos_layout.addRow("Telephone :", QLabel(self.eleve.telephone or "-"))
        self.infos_layout.addRow("Parent :", QLabel(self.eleve.nom_parent or "-"))

        self.lbl_situation.setText(
            "<b>Total du :</b> " + formater_montant(self.eleve.frais_totaux) + "<br>"
            "<b>Total paye :</b> " + formater_montant(self.eleve.total_paye) + "<br>"
            "<b>Solde restant :</b> "
            "<span style='color:#EF4444;font-size:16px;'>"
            + formater_montant(self.eleve.solde_restant) + "</span><br>"
            "<b>Statut :</b> " + libelle_statut(self.eleve.statut)
        )

        if self.eleve.est_solde:
            self.btn_paiement.setEnabled(False)
            self.btn_paiement.setText("Deja solde")
        else:
            self.btn_paiement.setEnabled(True)
            self.btn_paiement.setText("Enregistrer un paiement")

        paiements = self.paiement_service.lister_par_eleve(self.eleve.id)
        self.table.setRowCount(len(paiements))

        if len(paiements) == 0:
            self.lbl_vide.setVisible(True)
            self.table.setVisible(False)
        else:
            self.lbl_vide.setVisible(False)
            self.table.setVisible(True)

        for row, p in enumerate(paiements):
            valeurs = [
                p.numero_recu or "-",
                formater_date(p.date_paiement),
                formater_montant(p.montant),
                p.mode_paiement,
                formater_montant(p.solde_apres or 0),
                p.reference or "-",
                p.observation or "-",
            ]
            for col, val in enumerate(valeurs):
                item = QTableWidgetItem(val)
                if col not in (5, 6):
                    item.setTextAlignment(Qt.AlignCenter)
                if col == 2:
                    item.setForeground(QColor("#10B981"))
                if col == 0:
                    item.setForeground(QColor("#1E3A8A"))
                if col == 0:
                    item.setData(Qt.UserRole, p.recu_id)
                self.table.setItem(row, col, item)

    def _nouveau_paiement(self):
        if not self.eleve:
            return
        dialog = PaiementDialog(self, eleve=self.eleve)
        if dialog.exec():
            self.charger_eleve(self.eleve.id)
            self.paiement_enregistre.emit()
            QMessageBox.information(
                self, "Succes",
                "Paiement enregistre et recu genere."
            )
