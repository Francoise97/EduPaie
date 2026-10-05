"""Service metier : enregistrement des paiements."""
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
    """Logique metier : enregistrer un paiement + generer le recu associe."""

    def __init__(self):
        self.paiement_repo = PaiementRepository()
        self.eleve_repo    = EleveRepository()
        self.recu_service  = RecuService()

    # ---------- Lecture ----------
    def lister_par_eleve(self, eleve_id: int) -> List[Paiement]:
        """Retourne TOUS les paiements d'un eleve (actifs + annules)."""
        return self.paiement_repo.lister_par_eleve(eleve_id)

    def lister_actifs_par_eleve(self, eleve_id: int) -> List[Paiement]:
        """Retourne uniquement les paiements ACTIFS d'un eleve."""
        return self.paiement_repo.lister_actifs_par_eleve(eleve_id)

    def lister_tous(self) -> List[Paiement]:
        """Retourne tous les paiements (actifs + annules)."""
        return self.paiement_repo.lister_tous()

    def derniers(self, limite: int = 5) -> List[Paiement]:
        """Retourne les N derniers paiements ACTIFS."""
        return self.paiement_repo.derniers(limite)

    def obtenir(self, paiement_id: int) -> Optional[Paiement]:
        return self.paiement_repo.obtenir(paiement_id)

    # ---------- Creation ----------
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
        # 1) Verifier l'eleve
        eleve = self.eleve_repo.obtenir(eleve_id)
        if not eleve:
            return False, "Eleve introuvable."

        if eleve.solde_restant <= 0:
            return False, f"{eleve.nom_complet} a deja solde ses frais."

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

            # --- Transaction : recu + paiement ---
            conn.execute("BEGIN")

            # a) Creer le recu
            recu = self.recu_service.creer_recu(
                eleve_id=eleve_id,
                montant_paye=montant_float,
                solde_apres=nouveau_solde,
                date_paiement=date_paiement,
            )

            # b) Creer le paiement
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

    # ---------- Annulation ----------
    def annuler(self, paiement_id: int, raison: str) -> Tuple[bool, str]:
        """Annule un paiement (soft delete - conserve l'historique).

        Retourne (True, message) ou (False, message_erreur).
        """
        # 1) Verifier que le paiement existe
        paiement = self.paiement_repo.obtenir(paiement_id)
        if not paiement:
            return False, "Paiement introuvable."

        # 2) Verifier qu'il n'est pas deja annule
        if paiement.annule == 1:
            return False, "Ce paiement est deja annule."

        # 3) Annuler (soft delete)
        try:
            self.paiement_repo.annuler(paiement_id, raison)
            return True, "Paiement annule avec succes."
        except Exception as e:
            return False, "Erreur lors de l'annulation : " + str(e)

    # ---------- Suppression definitive (a eviter) ----------
    def supprimer(self, paiement_id: int) -> Tuple[bool, str]:
        """Suppression DEFINITIVE - a utiliser avec precaution."""
        try:
            self.paiement_repo.supprimer(paiement_id)
            return True, "Paiement supprime."
        except Exception as e:
            return False, f"Erreur : {e}"