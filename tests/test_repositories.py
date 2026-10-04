"""Tests basiques des repositories."""
from src.repositories.eleve_repository import EleveRepository


def test_compter_eleves():
    """Verifie que le comptage fonctionne."""
    repo = EleveRepository()
    assert repo.compter() == 15
