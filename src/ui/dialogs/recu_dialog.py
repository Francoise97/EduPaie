"""Dialogue d'apercu et d'action sur un recu."""
import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QMessageBox, QFormLayout
)
from PySide6.QtCore import Qt

from src.services.recu_service import RecuService
from src.services.eleve_service import EleveService
from src.services.paiement_service import PaiementService
from src.services.pdf_service import PDFService
from src.utils.formatters import formater_montant, formater_date


class RecuDialog(QDialog):
    def __init__(self, parent=None, recu_id=None):
        super().__init__(parent)
        self.recu_service = RecuService()
        self.eleve_service = EleveService()
        self.paiement_service = PaiementService()
        self.pdf_service = PDFService()

        self.recu = self.recu_service.obtenir(recu_id)
        if not self.recu:
            QMessageBox.warning(parent, "Erreur", "Recu introuvable.")
            self.reject()
            return

        self.eleve = self.eleve_service.obtenir(self.recu.eleve_id)
        self.paiement = None
        for p in self.paiement_service.lister_par_eleve(self.recu.eleve_id):
            if p.recu_id == self.recu.id:
                self.paiement = p
                break

        self.chemin_pdf = None

        self.setWindowTitle("Recu " + self.recu.numero_unique)
        self.setMinimumWidth(500)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        titre = QLabel("Recu de paiement")
        titre.setObjectName("Title")
        layout.addWidget(titre)

        numero = QLabel("N " + self.recu.numero_unique)
        numero.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #EF4444; padding: 6px 0;"
        )
        layout.addWidget(numero)

        info_frame = QFrame()
        info_frame.setObjectName("Card")
        form = QFormLayout(info_frame)
        form.setContentsMargins(16, 12, 16, 12)

        form.addRow("Eleve :", QLabel(self.eleve.nom_complet if self.eleve else "-"))
        form.addRow("Classe :", QLabel(self.eleve.classe if self.eleve else "-"))
        form.addRow("Montant paye :",
                    QLabel("<b style='color:#10B981;font-size:14px;'>"
                           + formater_montant(self.recu.montant_paye) + "</b>"))
        form.addRow("Date :", QLabel(formater_date(self.recu.date_emission)))
        if self.paiement:
            form.addRow("Mode :", QLabel(self.paiement.mode_paiement))
            if self.paiement.reference:
                form.addRow("Reference :", QLabel(self.paiement.reference))
            if self.paiement.observation:
                form.addRow("Observation :", QLabel(self.paiement.observation))

        form.addRow("Solde apres :",
                    QLabel("<b style='color:#EF4444;'>"
                           + formater_montant(self.recu.solde_apres) + "</b>"))

        layout.addWidget(info_frame)

        boutons = QHBoxLayout()
        boutons.addStretch()

        btn_fermer = QPushButton("Fermer")
        btn_fermer.setObjectName("Secondary")
        btn_fermer.clicked.connect(self.reject)
        boutons.addWidget(btn_fermer)

        btn_pdf = QPushButton("Generer PDF")
        btn_pdf.clicked.connect(self._generer_pdf)
        boutons.addWidget(btn_pdf)

        btn_ouvrir = QPushButton("Ouvrir le PDF")
        btn_ouvrir.setObjectName("Success")
        btn_ouvrir.clicked.connect(self._ouvrir_pdf)
        boutons.addWidget(btn_ouvrir)

        layout.addLayout(boutons)

        self.label_pdf = QLabel("")
        self.label_pdf.setStyleSheet(
            "color: #64748B; font-size: 11px; padding: 4px;"
        )
        if self.recu.chemin_pdf and Path(self.recu.chemin_pdf).exists():
            self.label_pdf.setText("PDF deja genere : " + self.recu.chemin_pdf)
            self.chemin_pdf = self.recu.chemin_pdf
        layout.addWidget(self.label_pdf)

    def _generer_pdf(self):
        try:
            chemin = self.pdf_service.generer_recu(self.recu.id)
            self.chemin_pdf = str(chemin)
            self.label_pdf.setText("PDF genere : " + str(chemin))
            QMessageBox.information(
                self, "PDF genere",
                "Le PDF a ete genere."
            )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Erreur de generation : " + str(e))

    def _ouvrir_pdf(self):
        if not self.chemin_pdf:
            self._generer_pdf()
            if not self.chemin_pdf:
                return

        try:
            if sys.platform == "win32":
                os.startfile(self.chemin_pdf)
            elif sys.platform == "darwin":
                subprocess.call(["open", self.chemin_pdf])
            else:
                subprocess.call(["xdg-open", self.chemin_pdf])
        except Exception as e:
            QMessageBox.warning(
                self, "Impossible d'ouvrir",
                "Ouvre manuellement le fichier : " + str(self.chemin_pdf)
            )
