"""Service metier : gestion des eleves."""
from typing import List, Optional
from src.models.eleve import Eleve
from src.repositories.eleve_repository import EleveRepository
from src.utils.validators import (
    valider_texte_obligatoire, valider_montant, valider_telephone
)


class EleveService:
    def __init__(self):
        self.repo = EleveRepository()

    def lister_tous(self):
        return self.repo.lister_tous()

    def rechercher(self, terme):
        if not terme or not terme.strip():
            return self.repo.lister_tous()
        return self.repo.rechercher(terme.strip())

    def lister_par_classe(self, classe):
        return self.repo.lister_par_classe(classe)

    def lister_par_statut(self, statut):
        return [e for e in self.repo.lister_tous() if e.statut == statut]

    def obtenir(self, eleve_id):
        return self.repo.obtenir(eleve_id)

    def lister_classes(self):
        return self.repo.lister_classes()

    def lister_annees(self):
        return self.repo.lister_annees()

    def statistiques(self):
        return self.repo.statistiques()

    def _valider(self, eleve):
        for champ, valeur in [
            ("nom", eleve.nom),
            ("prenom", eleve.prenom),
            ("classe", eleve.classe),
            ("annee scolaire", eleve.annee_scolaire),
        ]:
            ok, msg = valider_texte_obligatoire(valeur, champ)
            if not ok:
                return msg

        ok, result = valider_montant(eleve.frais_totaux, "frais totaux",
                                     strictement_positif=False)
        if not ok:
            return result
        if result == 0:
            return "Les frais totaux doivent etre superieurs a 0."

        if eleve.telephone:
            ok, msg = valider_telephone(eleve.telephone)
            if not ok:
                return msg

        return None

    def creer(self, eleve):
        erreur = self._valider(eleve)
        if erreur:
            return False, erreur

        try:
            new_id = self.repo.ajouter(eleve)
            return True, new_id
        except Exception as e:
            return False, "Erreur lors de la creation : " + str(e)

    def modifier(self, eleve):
        if eleve.id is None:
            return False, "Eleve sans identifiant."

        erreur = self._valider(eleve)
        if erreur:
            return False, erreur

        try:
            self.repo.modifier(eleve)
            return True, "Eleve modifie avec succes."
        except Exception as e:
            return False, "Erreur lors de la modification : " + str(e)

    def supprimer(self, eleve_id):
        try:
            self.repo.supprimer(eleve_id)
            return True, "Eleve supprime."
        except Exception as e:
            return False, "Erreur lors de la suppression : " + str(e)
