"""Modele metier : Paiement."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Paiement:
    id: Optional[int] = None
    eleve_id: int = 0
    recu_id: int = 0
    montant: float = 0.0
    date_paiement: str = ""
    mode_paiement: str = "Especes"
    reference: Optional[str] = None
    observation: Optional[str] = None
    date_creation: Optional[str] = None

    # Nouveaux champs pour l'annulation
    annule: int = 0
    raison_annulation: Optional[str] = None
    date_annulation: Optional[str] = None

    # Champs joints (remplis par le repository)
    numero_recu: Optional[str] = None
    eleve_nom: Optional[str] = None
    eleve_prenom: Optional[str] = None
    solde_apres: float = 0.0

    @classmethod
    def from_row(cls, row):
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
            annule=row["annule"] if "annule" in keys else 0,
            raison_annulation=row["raison_annulation"] if "raison_annulation" in keys else None,
            date_annulation=row["date_annulation"] if "date_annulation" in keys else None,
            numero_recu=row["numero_recu"] if "numero_recu" in keys else None,
            eleve_nom=row["eleve_nom"] if "eleve_nom" in keys else None,
            eleve_prenom=row["eleve_prenom"] if "eleve_prenom" in keys else None,
            solde_apres=row["solde_apres"] if "solde_apres" in keys else 0.0,
        )

    @property
    def est_annule(self):
        """Retourne True si le paiement est annule."""
        return self.annule == 1