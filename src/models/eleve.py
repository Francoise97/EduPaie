"""Modèle métier : Eleve."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Eleve:
    """Représente un élève inscrit dans l'établissement."""
    id: Optional[int] = None
    nom: str = ""
    prenom: str = ""
    classe: str = ""
    annee_scolaire: str = ""
    frais_totaux: float = 0.0
    telephone: Optional[str] = None
    nom_parent: Optional[str] = None
    date_creation: Optional[str] = None

    # Champs calculés (remplis par le repository depuis la vue SQL)
    total_paye: float = 0.0
    solde_restant: float = 0.0
    statut: str = "Non payé"

    @property
    def nom_complet(self) -> str:
        return f"{self.nom} {self.prenom}".strip()

    @property
    def est_solde(self) -> bool:
        return self.statut == "Soldé"

    def __str__(self) -> str:
        return f"{self.nom_complet} ({self.classe})"

    @classmethod
    def from_row(cls, row) -> "Eleve":
        """Construit un Eleve depuis une ligne sqlite3.Row."""
        keys = row.keys()
        return cls(
            id=row["id"],
            nom=row["nom"],
            prenom=row["prenom"],
            classe=row["classe"],
            annee_scolaire=row["annee_scolaire"],
            frais_totaux=row["frais_totaux"],
            telephone=row["telephone"] if "telephone" in keys else None,
            nom_parent=row["nom_parent"] if "nom_parent" in keys else None,
            date_creation=row["date_creation"] if "date_creation" in keys else None,
            total_paye=row["total_paye"] if "total_paye" in keys else 0.0,
            solde_restant=row["solde_restant"] if "solde_restant" in keys else 0.0,
            statut=row["statut"] if "statut" in keys else "Non payé",
        )
