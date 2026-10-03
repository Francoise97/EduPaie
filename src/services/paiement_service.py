"""Service métier : enregistrement des paiements."""
from datetime import datetime
from typing import List, Optional, Tuple
from src.models.paiement import Paiement
from src.models.eleve import Eleve
from src.repositories.paiement_repository import PaiementRepository
from src.repositories.eleve_repository import EleveRepository
from src.services.recu_service import RecuService
from src.utils.validators import (
    valider_paiement, valider_date, valider_mode_paiement
)


class PaiementService:
    """Logique métier : enregistrer un paiement + générer le reçu associé."""

    def __init__(self):
        self.paiement_repo = PaiementRepository()
        self.eleve_repo    = EleveRepository()
        self.recu_service  = RecuService()

    # ---------- Lecture ----------
    def lister_par_eleve(self, eleve_id: int) -> List[Paiement]:
        return self.paiement_repo.lister_par_eleve(eleve_id)

    def lister_tous(self) -> List[Paiement]:
        return self.paiement_repo.lister_tous()

    def derniers(self, limite: int = 5) -> List[Paiement]:
        return self.paiement_repo.derniers(limite)

    # ---------- Création ----------
    def enregistrer(self,
                    eleve_id: int,
                    montant,
                    date_paiement: str,
                    mode_paiement: str,
                    reference: str | None = None,
                    observation: str | None = None
                    ) -> Tuple[bool, str | Paiement]:
        """Enregistre un paiement complet.

        Retourne (True, Paiement) ou (False, message_erreur).
        """
        # 1) Vérifier l'élève
        eleve = self.eleve_repo.obtenir(eleve_id)
        if not eleve:
            return False, "Élève introuvable."

        if eleve.solde_restant <= 0:
            return False, f"{eleve.nom_complet} a déjà soldé ses frais."

        # 2) Valider le montant par rapport au solde
        ok, result = valider_paiement(montant, eleve.solde_restant)
        if not ok:
            return False, result
        montant_float = result

        # 3) Valider la date
        ok, result = valider_date(date_paiement)
        if not ok:
            return False, result

        # 4) Valider le mode
        ok, result = valider_mode_paiement(mode_paiement)
        if not ok:
            return False, result

        # 5) Calculer le nouveau solde
        nouveau_solde = eleve.solde_restant - montant_float

        try:
            conn = self.eleve_repo.conn
            conn.execute("BEGIN")

            # a) Créer le reçu
            recu = self.recu_service.creer_recu(
                eleve_id=eleve_id,
                montant_paye=montant_float,
                solde_apres=nouveau_solde,
                date_paiement=date_paiement,
            )

            # b) Créer le paiement
            paiement = Paiement(
                eleve_id=eleve_id,
                recu_id=recu.id,
                montant=montant_float,
                date_paiement=date_paiement,
                mode_paiement=mode_paiement,
                reference=reference,
                observation=observation,
            )
            paiement.id = self.paiement_repo.ajouter(paiement)
            paiement.numero_recu = recu.numero_unique

            conn.commit()
            return True, paiement

        except Exception as e:
            conn.rollback()
            return False, f"Erreur lors de l'enregistrement : {e}"

    def supprimer(self, paiement_id: int) -> tuple[bool, str]:
        try:
            self.paiement_repo.supprimer(paiement_id)
            return True, "Paiement supprimé."
        except Exception as e:
            return False, f"Erreur : {e}"
