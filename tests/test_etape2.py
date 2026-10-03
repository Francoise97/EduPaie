"""Test de la couche métier (étape 2)."""
import sys
from pathlib import Path

# Ajoute la racine du projet au PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.services.eleve_service import EleveService
from src.services.paiement_service import PaiementService
from src.utils.formatters import formater_montant, formater_date, libelle_statut

# ... (le reste du code est identique, tu peux laisser tel quel)
