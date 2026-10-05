"""Tests des validateurs."""
from src.utils.validators import (
    valider_montant, valider_texte_obligatoire, valider_date
)


def test_valider_montant_valide():
    ok, val = valider_montant("50000")
    assert ok is True
    assert val == 50000.0


def test_valider_montant_invalide():
    ok, msg = valider_montant("abc")
    assert ok is False


def test_valider_montant_negatif():
    ok, msg = valider_montant("-100")
    assert ok is False


def test_valider_texte_obligatoire():
    ok, val = valider_texte_obligatoire("Diallo", "nom")
    assert ok is True
    assert val == "Diallo"

    ok, msg = valider_texte_obligatoire("", "nom")
    assert ok is False


def test_valider_date():
    ok, dt = valider_date("2026-10-05")
    assert ok is True

    ok, msg = valider_date("05/10/2026")
    assert ok is False
