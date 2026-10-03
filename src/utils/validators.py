"""Fonctions de validation des saisies utilisateur."""
import re
from datetime import datetime


def valider_montant(valeur, nom_champ="montant", strictement_positif=True):
    if valeur is None or str(valeur).strip() == "":
        return False, "Le " + nom_champ + " est obligatoire."

    try:
        texte = str(valeur).strip().replace(" ", "").replace(",", ".")
        nombre = float(texte)
    except (ValueError, TypeError):
        return False, "Le " + nom_champ + " doit etre un nombre valide."

    if strictement_positif and nombre <= 0:
        return False, "Le " + nom_champ + " doit etre strictement positif."

    if not strictement_positif and nombre < 0:
        return False, "Le " + nom_champ + " ne peut pas etre negatif."

    return True, nombre


def valider_texte_obligatoire(valeur, nom_champ):
    if valeur is None or str(valeur).strip() == "":
        return False, "Le champ '" + nom_champ + "' est obligatoire."
    return True, str(valeur).strip()


def valider_date(date_str, nom_champ="date"):
    if date_str is None or str(date_str).strip() == "":
        return False, "La " + nom_champ + " est obligatoire."

    texte = str(date_str).strip()
    try:
        dt = datetime.strptime(texte, "%Y-%m-%d")
        return True, dt
    except ValueError:
        return False, "La " + nom_champ + " doit etre au format AAAA-MM-JJ."


def valider_mode_paiement(mode):
    modes_valides = ["Especes", "Cheque", "Virement", "Mobile Money"]
    if mode not in modes_valides:
        return False, "Mode de paiement invalide. Choix : " + ", ".join(modes_valides) + "."
    return True, mode


def valider_telephone(tel):
    if tel is None or str(tel).strip() == "":
        return True, None
    texte = str(tel).strip()
    if not re.match(r"^[0-9+\s\-()]{6,20}$", texte):
        return False, "Le numero de telephone n'est pas valide."
    return True, texte


def valider_paiement(montant, solde_restant):
    ok, result = valider_montant(montant, "montant du paiement")
    if not ok:
        return False, result

    montant_float = result

    if montant_float > solde_restant:
        return False, (
            "Le montant saisi (" + str(int(montant_float)) + " FCFA) depasse "
            "le solde restant (" + str(int(solde_restant)) + " FCFA)."
        )

    return True, montant_float
