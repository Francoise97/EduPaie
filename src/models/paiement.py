"""Modèle métier : Paiement."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Paiement:
    """Représente un versement effectué par un élève."""
    id: Optional[int] = None
    eleve_id: int = 0
    recu_id: int = 0
    montant: float = 0.0
    date_paiement: str = ""
    mode_paiement: str = "Espèces"
    reference: Optional[str] = None
    observation: Optional[str] = None
    date_creation: Optional[str] = None

    # Champs joints (remplis par le repository)
    numero_recu: Optional[str] = None
    eleve_nom: Optional[str] = None
    eleve_prenom: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Paiement":
        keys = row.keys()
        return cls(
            id=row["id"],
            eleve_id=row["eleve_id"],
            recu_id=row["recu_id"],
            montant=row["montant"],
            date_paiement=row["date_paiement"],
            mode_paiement=row["mode_paiement"],
            reference=row["reference"] if "reference" in keys else None,
            observation=row["observation"] if "observation" in keys else None,
            date_creation=row["date_creation"] if "date_creation" in keys else None,
            numero_recu=row["numero_recu"] if "numero_recu" in keys else None,
            eleve_nom=row["eleve_nom"] if "eleve_nom" in keys else None,
            eleve_prenom=row["eleve_prenom"] if "eleve_prenom" in keys else None,
        )
