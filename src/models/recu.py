"""Modèle métier : Recu."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Recu:
    """Représente un reçu numéroté émis pour un paiement."""
    id: Optional[int] = None
    numero_unique: str = ""
    annee: int = 0
    sequence: int = 0
    eleve_id: int = 0
    date_emission: str = ""
    montant_paye: float = 0.0
    solde_apres: float = 0.0
    chemin_pdf: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Recu":
        return cls(
            id=row["id"],
            numero_unique=row["numero_unique"],
            annee=row["annee"],
            sequence=row["sequence"],
            eleve_id=row["eleve_id"],
            date_emission=row["date_emission"],
            montant_paye=row["montant_paye"],
            solde_apres=row["solde_apres"],
            chemin_pdf=row["chemin_pdf"] if "chemin_pdf" in row.keys() else None,
        )
