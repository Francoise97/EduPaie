"""Ecran listant tous les recus emis."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox,
    QDialog, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from src.services.recu_service import RecuService
from src.services.eleve_service import EleveService
from src.services.paiement_service import PaiementService
from src.services.pdf_service import PDFService
from src.utils.formatters import formater_montant, formater_date
from src.ui.dialogs.recu_dialog import RecuDialog


class RecusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.recu_service = RecuService()
        self.eleve_service = EleveService()
        self.paiement_service = PaiementService()
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

        sous_titre = QLabel("Clique sur une ligne puis sur le bouton pour voir le recu")
        sous_titre.setObjectName("Subtitle")
        layout.addWidget(sous_titre)

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText(
            "Rechercher par numero de recu ou nom d'eleve..."
        )
        self.recherche.setObjectName("SearchBar")
        layout.addWidget(self.recherche)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Recu N", "Date", "Eleve", "Montant", "Solde apres", "PDF", "Statut"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
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
        h.setSectionResizeMode(6, QHeaderView.ResizeToContents)

        layout.addWidget(self.table, 1)

        pied = QHBoxLayout()
        pied.addStretch()

        self.btn_voir = QPushButton("Voir le recu selectionne")
        self.btn_voir.setObjectName("Secondary")
        self.btn_voir.clicked.connect(self._voir_recu)
        pied.addWidget(self.btn_voir)

        self.btn_annuler = QPushButton("Annuler le paiement")
        self.btn_annuler.setObjectName("Danger")
        self.btn_annuler.setMinimumWidth(200)
        self.btn_annuler.clicked.connect(self._annuler_paiement)
        pied.addWidget(self.btn_annuler)

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

            # Verifier si le paiement associe est annule
            paiement = None
            for p in self.paiement_service.lister_par_eleve(r.eleve_id):
                if p.recu_id == r.id:
                    paiement = p
                    break

            annule = paiement.annule if paiement else 0
            statut_txt = "Annule" if annule == 1 else "Actif"

            valeurs = [
                r.numero_unique,
                formater_date(r.date_emission),
                eleve_nom,
                formater_montant(r.montant_paye),
                formater_montant(r.solde_apres),
                a_pdf,
                statut_txt,
            ]

            # Police barree pour les annules
            font = QFont()
            if annule == 1:
                font.setStrikeOut(True)

            for col, val in enumerate(valeurs):
                item = QTableWidgetItem(val)
                if col != 2:
                    item.setTextAlignment(Qt.AlignCenter)

                # Couleurs
                if col == 0:
                    item.setForeground(QColor("#1E3A8A") if annule == 0 else QColor("#94A3B8"))
                    item.setData(Qt.UserRole, r.id)
                if col == 3:
                    item.setForeground(QColor("#10B981") if annule == 0 else QColor("#94A3B8"))
                if col == 4:
                    item.setForeground(QColor("#EF4444") if annule == 0 else QColor("#94A3B8"))
                if col == 5:
                    if a_pdf == "Oui":
                        item.setForeground(QColor("#10B981"))
                    else:
                        item.setForeground(QColor("#94A3B8"))
                if col == 6:
                    item.setForeground(QColor("#EF4444") if annule == 1 else QColor("#10B981"))

                # Barrer les annules
                if annule == 1:
                    item.setFont(font)

                self.table.setItem(row, col, item)

        # Auto-selectionner la 1ere ligne si possible
        if len(resultats) > 0:
            self.table.selectRow(0)

        self.label_total.setText("Total : " + str(len(resultats)) + " recus")

    def _double_click(self, index):
        if index.isValid():
            self._voir_recu()

    def _voir_recu(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne un recu dans la liste.")
            return

        item = self.table.item(row, 0)
        if not item:
            return

        recu_id = item.data(Qt.UserRole)
        if recu_id:
            dialog = RecuDialog(self, recu_id=recu_id)
            dialog.exec()
            self.rafraichir()

    def _annuler_paiement(self):
        """Annule un paiement (soft delete) avec raison."""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aucune selection",
                                "Selectionne un recu dans la liste.")
            return

        item = self.table.item(row, 0)
        if not item:
            return
        recu_id = item.data(Qt.UserRole)
        if not recu_id:
            return

        # Verifier que le paiement n'est pas deja annule
        statut_item = self.table.item(row, 6)
        if statut_item and statut_item.text() == "Annule":
            QMessageBox.information(self, "Deja annule",
                                    "Ce paiement est deja annule.")
            return

        # Recuperer les infos
        recu = self.recu_service.obtenir(recu_id)
        if not recu:
            QMessageBox.warning(self, "Erreur", "Recu introuvable.")
            return

        eleve = self.eleve_service.obtenir(recu.eleve_id)
        eleve_nom = eleve.nom_complet if eleve else "-"

        numero_recu = item.text()
        montant = formater_montant(recu.montant_paye)
        date_p = formater_date(recu.date_emission)

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
            "<b>Eleve :</b> " + eleve_nom + "<br>"
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
        for p in self.paiement_service.lister_par_eleve(recu.eleve_id):
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
            self.rafraichir()
        else:
            QMessageBox.critical(self, "Erreur", msg)