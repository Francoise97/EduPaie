"""Service métier : gestion des reçus (numérotation unique)."""
from datetime import datetime
from typing import List, Optional
from src.models.recu import Recu
from src.repositories.recu_repository import RecuRepository


class RecuService:
    """Logique métier autour des reçus."""

    def __init__(self):
        self.repo = RecuRepository()

    def obtenir(self, recu_id: int) -> Optional[Recu]:
        return self.repo.obtenir(recu_id)

    def obtenir_par_numero(self, numero: str) -> Optional[Recu]:
        return self.repo.obtenir_par_numero(numero)

    def lister_par_eleve(self, eleve_id: int) -> List[Recu]:
        return self.repo.lister_par_eleve(eleve_id)

    def lister_tous(self) -> List[Recu]:
        return self.repo.lister_tous()

    def creer_recu(self, eleve_id: int, montant_paye: float,
                   solde_apres: float,
                   date_paiement: str | None = None) -> Recu:
        """Crée un nouveau reçu avec un numéro unique.

        Ne commit PAS -- c'est le service paiement qui orchestre.
        """
        annee = datetime.now().year
        numero, sequence = self.repo.prochain_numero(annee)

        recu = Recu(
            numero_unique=numero,
            annee=annee,
            sequence=sequence,
            eleve_id=eleve_id,
            date_emission=date_paiement or datetime.now().strftime("%Y-%m-%d"),
            montant_paye=montant_paye,
            solde_apres=solde_apres,
            chemin_pdf=None,
        )
        recu_id = self.repo.ajouter(recu)
        recu.id = recu_id
        return recu

    def mettre_a_jour_pdf(self, recu_id: int, chemin_pdf: str) -> None:
        self.repo.mettre_a_jour_pdf(recu_id, chemin_pdf)
