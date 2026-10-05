"""Fiche detaillee d'un eleve avec historique des paiements."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QFormLayout, QComboBox,
    QDialog, QLineEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

from src.services.eleve_service import EleveService
from src.services.paiement_service import PaiementService
from src.utils.formatters import formater_montant, formater_date, libelle_statut
from src.ui.dialogs.paiement_dialog import PaiementDialog
from src.ui.dialogs.recu_dialog import RecuDialog


class FicheEleveWidget(QWidget):
    """Fiche complete d'un eleve : infos, situation, historique."""

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

        # --- Ligne du haut : retour + bouton paiement ---
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

        # --- Titre ---
        self.titre = QLabel("Fiche eleve")
        self.titre.setObjectName("Title")
        layout.addWidget(self.titre)

        # --- Bloc infos ---
        self.frame_infos = QFrame()
        self.frame_infos.setObjectName("Card")
        self.infos_layout = QFormLayout(self.frame_infos)
        self.infos_layout.setContentsMargins(16, 12, 16, 12)
        layout.addWidget(self.frame_infos)

        # --- Situation financiere ---
        self.frame_situation = QFrame()
        self.frame_situation.setObjectName("Card")
        sit_layout = QVBoxLayout(self.frame_situation)
        sit_layout.setContentsMargins(16, 12, 16, 12)

        self.lbl_situation = QLabel("")
        self.lbl_situation.setStyleSheet("font-size: 14px;")
        sit_layout.addWidget(self.lbl_situation)
        layout.addWidget(self.frame_situation)

        # --- Titre historique ---
        titre2 = QLabel("Historique des paiements")
        titre2.setObjectName("Title")
        titre2.setStyleSheet("font-size: 16px;")
        layout.addWidget(titre2)

        # --- Tableau historique (8 colonnes : ajout Statut) ---
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Recu N", "Date", "Montant", "Mode",
            "Solde apres", "Reference", "Observation", "Statut"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(250)
        self.table.doubleClicked.connect(lambda _idx: self._voir_recu_selectionne())

        h = self.table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(6, QHeaderView.Stretch)
        h.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        layout.addWidget(self.table, 1)

        # --- Message si vide ---
        self.lbl_vide = QLabel("Aucun paiement enregistre pour cet eleve.")
        self.lbl_vide.setAlignment(Qt.AlignCenter)
        self.lbl_vide.setStyleSheet(
            "color: #94A3B8; padding: 20px; font-style: italic;"
        )
        layout.addWidget(self.lbl_vide)
        self.lbl_vide.setVisible(False)

        # --- Boutons bas ---
        actions = QHBoxLayout()
        actions.addStretch()

        self.btn_voir_recu = QPushButton("Voir le recu selectionne")
        self.btn_voir_recu.setObjectName("Secondary")
        self.btn_voir_recu.clicked.connect(self._voir_recu_selectionne)
        actions.addWidget(self.btn_voir_recu)

        self.btn_annuler = QPushButton("Annuler le paiement")
        self.btn_annuler.setObjectName("Danger")
        self.btn_annuler.setMinimumWidth(200)
        self.btn_annuler.clicked.connect(self._annuler_paiement)
        actions.addWidget(self.btn_annuler)

        layout.addLayout(actions)

    def charger_eleve(self, eleve_id):
        self.eleve = self.eleve_service.obtenir(eleve_id)
        if not self.eleve:
            QMessageBox.warning(self, "Erreur", "Eleve introuvable.")
            return

        self.titre.setText("Fiche de " + self.eleve.nom_complet)

        # Infos
        while self.infos_layout.rowCount() > 0:
            self.infos_layout.removeRow(0)

        self.infos_layout.addRow("Nom :", QLabel(self.eleve.nom))
        self.infos_layout.addRow("Prenom :", QLabel(self.eleve.prenom))
        self.infos_layout.addRow("Classe :", QLabel(self.eleve.classe))
        self.infos_layout.addRow("Annee scolaire :", QLabel(self.eleve.annee_scolaire))
        self.infos_layout.addRow("Telephone :", QLabel(self.eleve.telephone or "-"))
        self.infos_layout.addRow("Parent :", QLabel(self.eleve.nom_parent or "-"))

        # Situation financiere
        self.lbl_situation.setText(
            "<b>Total du :</b> " + formater_montant(self.eleve.frais_totaux) + "<br>"
            "<b>Total paye :</b> " + formater_montant(self.eleve.total_paye) + "<br>"
            "<b>Solde restant :</b> "
            "<span style='color:#EF4444;font-size:16px;'>"
            + formater_montant(self.eleve.solde_restant) + "</span><br>"
            "<b>Statut :</b> " + libelle_statut(self.eleve.statut)
        )

        # Bouton paiement
        if self.eleve.est_solde:
            self.btn_paiement.setEnabled(False)
            self.btn_paiement.setText("Deja solde")
        else:
            self.btn_paiement.setEnabled(True)
            self.btn_paiement.setText("Enregistrer un paiement")

        # Historique (TOUS les paiements : actifs + annules)
        paiements = self.paiement_service.lister_par_eleve(self.eleve.id)
        self.table.setRowCount(len(paiements))

        if len(paiements) == 0:
            self.lbl_vide.setVisible(True)
            self.table.setVisible(False)
            self.btn_voir_recu.setEnabled(False)
            self.btn_annuler.setEnabled(False)
        else:
            self.lbl_vide.setVisible(False)
            self.table.setVisible(True)
            self.btn_voir_recu.setEnabled(True)
            self.btn_annuler.setEnabled(True)

        for row, p in enumerate(paiements):
            # Statut
            if p.annule == 1:
                statut_txt = "Annule"
                statut_color = QColor("#EF4444")
                # Prix barre
                font = QFont()
                font.setStrikeOut(True)
            else:
                statut_txt = "Actif"
                statut_color = QColor("#10B981")
                font = QFont()

            valeurs = [
                p.numero_recu or "-",
                formater_date(p.date_paiement),
                formater_montant(p.montant),
                p.mode_paiement,
                formater_montant(p.solde_apres or 0),
                p.reference or "-",
                p.observation or "-",
                statut_txt,
            ]
            for col, val in enumerate(valeurs):
                item = QTableWidgetItem(val)

                # Alignement
                if col != 6:
                    item.setTextAlignment(Qt.AlignCenter)

                # Couleurs
                if col == 2:
                    item.setForeground(QColor("#10B981") if p.annule == 0
                                       else QColor("#94A3B8"))
                if col == 0:
                    item.setForeground(QColor("#1E3A8A") if p.annule == 0
                                       else QColor("#94A3B8"))
                    item.setData(Qt.UserRole, p.recu_id)
                if col == 7:
                    item.setForeground(statut_color)

                # Barre les paiements annules
                if p.annule == 1:
                    item.setFont(font)

                self.table.setItem(row, col, item)

    def _voir_recu_selectionne(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne un paiement dans l'historique.")
            return
        item = self.table.item(row, 0)
        if not item:
            return
        recu_id = item.data(Qt.UserRole)
        if recu_id:
            dialog = RecuDialog(self, recu_id=recu_id)
            dialog.exec()

    def _annuler_paiement(self):
        """Annule un paiement (soft delete) avec raison."""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne d'abord un paiement dans l'historique.")
            return

        item = self.table.item(row, 0)
        if not item:
            return
        recu_id = item.data(Qt.UserRole)
        if not recu_id:
            return

        # Verifier que le paiement n'est pas deja annule
        statut_item = self.table.item(row, 7)
        if statut_item and statut_item.text() == "Annule":
            QMessageBox.information(self, "Deja annule",
                                    "Ce paiement est deja annule.")
            return

        # Recuperer les infos
        numero_recu = item.text()
        montant_item = self.table.item(row, 2)
        montant = montant_item.text() if montant_item else ""
        date_item = self.table.item(row, 1)
        date_p = date_item.text() if date_item else ""

        # --- Dialogue personnalise ---
        dialog = QDialog(self)
        dialog.setWindowTitle("Annuler un paiement")
        dialog.setMinimumWidth(480)

        vbox = QVBoxLayout(dialog)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(12)

        # Titre
        titre = QLabel("Confirmer l'annulation")
        titre.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #EF4444;"
        )
        vbox.addWidget(titre)

        # Details
        details = QLabel(
            "<b>Eleve :</b> " + self.eleve.nom_complet + "<br>"
            "<b>Recu N :</b> " + numero_recu + "<br>"
            "<b>Date :</b> " + date_p + "<br>"
            "<b>Montant :</b> " + montant
        )
        details.setStyleSheet(
            "background-color: #F1F5F9; padding: 12px; "
            "border-radius: 6px; font-size: 13px;"
        )
        vbox.addWidget(details)

        # Raison
        label_raison = QLabel("Raison de l'annulation :")
        label_raison.setStyleSheet("font-weight: bold; margin-top: 8px;")
        vbox.addWidget(label_raison)

        combo = QComboBox()
        combo.addItems([
            "Faute de saisie",
            "Erreur de montant",
            "Doublon de paiement",
            "Paiement non recu",
            "Autre (preciser ci-dessous)"
        ])
        vbox.addWidget(combo)

        # Commentaire
        label_comm = QLabel("Commentaire (optionnel) :")
        label_comm.setStyleSheet("font-weight: bold; margin-top: 8px;")
        vbox.addWidget(label_comm)

        commentaire = QLineEdit()
        commentaire.setPlaceholderText("Details supplementaires...")
        vbox.addWidget(commentaire)

        # Avertissement
        warn = QLabel(
            "ATTENTION : Cette action est irreversible.\n"
            "Le paiement sera marque comme annule (visible dans l'historique)."
        )
        warn.setStyleSheet(
            "color: #991B1B; font-size: 12px; "
            "background-color: #FEE2E2; padding: 10px; "
            "border-radius: 6px; margin-top: 8px;"
        )
        vbox.addWidget(warn)

        # Boutons
        boutons = QHBoxLayout()
        boutons.addStretch()

        btn_non = QPushButton("Non, annuler")
        btn_non.setObjectName("Secondary")
        btn_non.clicked.connect(dialog.reject)
        boutons.addWidget(btn_non)

        btn_oui = QPushButton("Oui, confirmer")
        btn_oui.setObjectName("Danger")
        btn_oui.clicked.connect(dialog.accept)
        boutons.addWidget(btn_oui)

        vbox.addLayout(boutons)

        # Afficher
        if dialog.exec() != QDialog.Accepted:
            return

        # Recuperer la raison
        raison = combo.currentText()
        comm = commentaire.text().strip()
        if comm:
            raison = raison + " - " + comm

        # Trouver le paiement_id
        paiement_id = None
        for p in self.paiement_service.lister_par_eleve(self.eleve.id):
            if p.recu_id == recu_id:
                paiement_id = p.id
                break

        if not paiement_id:
            QMessageBox.warning(self, "Erreur", "Paiement introuvable.")
            return

        # Annuler (soft delete)
        ok, msg = self.paiement_service.annuler(paiement_id, raison)
        if ok:
            QMessageBox.information(
                self, "Succes",
                "Paiement annule avec succes.\n\n"
                "Raison : " + raison
            )
            self.charger_eleve(self.eleve.id)
            self.paiement_enregistre.emit()
        else:
            QMessageBox.critical(self, "Erreur", msg)

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