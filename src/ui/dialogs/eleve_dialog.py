"""Formulaire d'ajout / modification d'un élève."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QLabel,
    QMessageBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from src.models.eleve import Eleve
from src.services.eleve_service import EleveService


class EleveDialog(QDialog):
    """Dialogue modal pour créer ou modifier un élève."""

    def __init__(self, parent=None, eleve: Eleve | None = None):
        super().__init__(parent)
        self.service = EleveService()
        self.eleve = eleve
        self.mode_edition = eleve is not None

        titre = "✏️  Modifier un élève" if self.mode_edition else "➕  Nouvel élève"
        self.setWindowTitle(titre)
        self.setMinimumWidth(480)

        self._build_ui()
        if self.mode_edition:
            self._remplir(eleve)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Titre
        titre = QLabel("✏️  Modifier un élève" if self.mode_edition else "➕  Nouvel élève")
        titre.setObjectName("Title")
        layout.addWidget(titre)

        # Champs
        form = QFormLayout()
        form.setSpacing(10)

        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Obligatoire")
        form.addRow("Nom *", self.input_nom)

        self.input_prenom = QLineEdit()
        self.input_prenom.setPlaceholderText("Obligatoire")
        form.addRow("Prénom *", self.input_prenom)

        self.input_classe = QComboBox()
        self.input_classe.setEditable(True)
        classes = self.service.lister_classes()
        if classes:
            self.input_classe.addItems(classes)
        form.addRow("Classe *", self.input_classe)

        self.input_annee = QComboBox()
        self.input_annee.setEditable(True)
        self.input_annee.addItems(["2026-2027", "2027-2028", "2028-2029"])
        form.addRow("Année scolaire *", self.input_annee)

        self.input_frais = QDoubleSpinBox()
        self.input_frais.setMaximum(10_000_000)
        self.input_frais.setDecimals(0)
        self.input_frais.setSingleStep(5000)
        self.input_frais.setSuffix(" FCFA")
        form.addRow("Frais totaux *", self.input_frais)

        self.input_telephone = QLineEdit()
        self.input_telephone.setPlaceholderText("Optionnel")
        form.addRow("Téléphone", self.input_telephone)

        self.input_parent = QLineEdit()
        self.input_parent.setPlaceholderText("Optionnel")
        form.addRow("Nom du parent", self.input_parent)

        layout.addLayout(form)
        layout.addStretch()

        # Boutons
        boutons = QHBoxLayout()
        boutons.addStretch()

        btn_annuler = QPushButton("Annuler")
        btn_annuler.setObjectName("Secondary")
        btn_annuler.clicked.connect(self.reject)
        boutons.addWidget(btn_annuler)

        btn_valider = QPushButton("💾  Enregistrer")
        btn_valider.clicked.connect(self._valider)
        boutons.addWidget(btn_valider)

        layout.addLayout(boutons)

    def _remplir(self, eleve: Eleve):
        self.input_nom.setText(eleve.nom)
        self.input_prenom.setText(eleve.prenom)
        self.input_classe.setCurrentText(eleve.classe)
        self.input_annee.setCurrentText(eleve.annee_scolaire)
        self.input_frais.setValue(eleve.frais_totaux)
        self.input_telephone.setText(eleve.telephone or "")
        self.input_parent.setText(eleve.nom_parent or "")

    def _valider(self):
        eleve = Eleve(
            id=self.eleve.id if self.mode_edition else None,
            nom=self.input_nom.text().strip(),
            prenom=self.input_prenom.text().strip(),
            classe=self.input_classe.currentText().strip(),
            annee_scolaire=self.input_annee.currentText().strip(),
            frais_totaux=self.input_frais.value(),
            telephone=self.input_telephone.text().strip() or None,
            nom_parent=self.input_parent.text().strip() or None,
        )

        if self.mode_edition:
            ok, msg = self.service.modifier(eleve)
        else:
            ok, msg = self.service.creer(eleve)

        if ok:
            QMessageBox.information(self, "Succès",
                                    "Élève enregistré avec succès.")
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur de validation", str(msg))
