"""Tests basiques des services."""
from src.services.eleve_service import EleveService
from src.services.paiement_service import PaiementService


def test_lister_eleves():
    """Verifie que la liste des eleves n'est pas vide."""
    service = EleveService()
    eleves = service.lister_tous()
    assert len(eleves) > 0


def test_statistiques():
    """Verifie les statistiques."""
    service = EleveService()
    stats = service.statistiques()
    assert "nb_eleves" in stats
    assert stats["nb_eleves"] > 0
