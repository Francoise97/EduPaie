"""Tests de performance de base."""
import time
from src.services.eleve_service import EleveService


def test_temps_chargement_eleves():
    """Verifie que le chargement des eleves est rapide."""
    service = EleveService()
    debut = time.time()
    eleves = service.lister_tous()
    duree = time.time() - debut

    assert len(eleves) > 0
    assert duree < 2.0, f"Chargement trop lent : {duree:.2f}s"


def test_temps_recherche():
    """Verifie que la recherche est rapide."""
    service = EleveService()
    debut = time.time()
    resultats = service.rechercher("Diallo")
    duree = time.time() - debut

    assert duree < 1.0, f"Recherche trop lente : {duree:.2f}s"


def test_temps_statistiques():
    """Verifie que les statistiques sont rapides."""
    service = EleveService()
    debut = time.time()
    stats = service.statistiques()
    duree = time.time() - debut

    assert "nb_eleves" in stats
    assert duree < 1.0, f"Statistiques trop lentes : {duree:.2f}s"
