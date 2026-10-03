"""Dialogue d'enregistrement d'un paiement."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QLabel,
    QMessageBox, QDateEdit, QDoubleSpinBox, QFrame
)
from PySide6.QtCore import Qt, QDate
from src.models.eleve import Eleve
from src.services.paiement_service import PaiementService
from src.utils.formatters import formater_montant


class PaiementDialog(QDialog):
    def __init__(self, parent=None, eleve=None):
        super().__init__(parent)
        self.eleve = eleve
        self.service = PaiementService()
        self.paiement_cree = None

        self.setWindowTitle("Enregistrer un paiement")
        self.setMinimumWidth(520)

        self._build_ui()
        self._maj_solde_preview()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        titre = QLabel("Enregistrer un paiement")
        titre.setObjectName("Title")
        layout.addWidget(titre)

        info_frame = QFrame()
        info_frame.setObjectName("Card")
        info_layout = QFormLayout(info_frame)
        info_layout.setContentsMargins(16, 12, 16, 12)

        info_layout.addRow("Eleve :",
            QLabel("<b>" + self.eleve.nom_complet + "</b> (" + self.eleve.classe + ")"))
        info_layout.addRow("Total du :",
            QLabel(formater_montant(self.eleve.frais_totaux)))
        info_layout.addRow("Deja paye :",
            QLabel(formater_montant(self.eleve.total_paye)))
        info_layout.addRow("Solde restant :",
            QLabel("<b style='color:#EF4444;'>"
                   + formater_montant(self.eleve.solde_restant) + "</b>"))
        layout.addWidget(info_frame)

        form = QFormLayout()
        form.setSpacing(10)

        self.input_montant = QDoubleSpinBox()
        self.input_montant.setMaximum(10000000)
        self.input_montant.setDecimals(0)
        self.input_montant.setSingleStep(5000)
        self.input_montant.setSuffix(" FCFA")
        self.input_montant.setValue(min(50000, self.eleve.solde_restant))
        self.input_montant.valueChanged.connect(self._maj_solde_preview)
        form.addRow("Montant *", self.input_montant)

        self.input_date = QDateEdit()
        self.input_date.setDate(QDate.currentDate())
        self.input_date.setCalendarPopup(True)
        self.input_date.setDisplayFormat("dd/MM/yyyy")
        form.addRow("Date *", self.input_date)

        self.input_mode = QComboBox()
        self.input_mode.addItems(["Especes", "Cheque", "Virement", "Mobile Money"])
        form.addRow("Mode de paiement *", self.input_mode)

        self.input_reference = QLineEdit()
        self.input_reference.setPlaceholderText("N cheque, transaction... (optionnel)")
        form.addRow("Reference", self.input_reference)

        self.input_observation = QLineEdit()
        self.input_observation.setPlaceholderText("Optionnel")
        form.addRow("Observation", self.input_observation)

        layout.addLayout(form)

        self.label_apercu = QLabel("")
        self.label_apercu.setStyleSheet(
            "background:#FEF3C7; padding:10px; border-radius:6px; "
            "color:#92400E; font-weight:bold;"
        )
        self.label_apercu.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_apercu)

        boutons = QHBoxLayout()
        boutons.addStretch()

        btn_annuler = QPushButton("Annuler")
        btn_annuler.setObjectName("Secondary")
        btn_annuler.clicked.connect(self.reject)
        boutons.addWidget(btn_annuler)

        btn_valider = QPushButton("Enregistrer + Recu")
        btn_valider.setObjectName("Success")
        btn_valider.clicked.connect(self._valider)
        boutons.addWidget(btn_valider)

        layout.addLayout(boutons)

    def _maj_solde_preview(self):
        montant = self.input_montant.value()
        nouveau_solde = self.eleve.solde_restant - montant
        if nouveau_solde < 0:
            self.label_apercu.setText(
                "Montant trop eleve ! Solde deviendrait "
                + formater_montant(nouveau_solde)
            )
            self.label_apercu.setStyleSheet(
                "background:#FEE2E2; padding:10px; border-radius:6px; "
                "color:#991B1B; font-weight:bold;"
            )
        else:
            self.label_apercu.setText(
                "Nouveau solde apres paiement : "
                + formater_montant(nouveau_solde)
            )
            self.label_apercu.setStyleSheet(
                "background:#FEF3C7; padding:10px; border-radius:6px; "
                "color:#92400E; font-weight:bold;"
            )

    def _valider(self):
        montant = self.input_montant.value()
        date_str = self.input_date.date().toString("yyyy-MM-dd")
        mode = self.input_mode.currentText()
        reference = self.input_reference.text().strip() or None
        observation = self.input_observation.text().strip() or None

        ok, result = self.service.enregistrer(
            eleve_id=self.eleve.id,
            montant=montant,
            date_paiement=date_str,
            mode_paiement=mode,
            reference=reference,
            observation=observation,
        )

        if ok:
            self.paiement_cree = result
            QMessageBox.information(
                self, "Paiement enregistre",
                "Paiement de " + formater_montant(montant) + " enregistre.\n\n"
                "Recu N : " + result.numero_recu + "\n"
                "Nouveau solde : "
                + formater_montant(self.eleve.solde_restant - montant)
            )
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", str(result))
