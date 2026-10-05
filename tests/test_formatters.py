"""Tests des fonctions de formatage."""
from src.utils.formatters import (
    formater_montant, formater_date, libelle_statut
)


def test_formater_montant():
    assert formater_montant(250000) == "250 000 FCFA"
    assert formater_montant(0) == "0 FCFA"
    assert formater_montant(None) == "0 FCFA"


def test_formater_date():
    assert formater_date("2026-10-05") == "05/10/2026"
    assert formater_date("") == ""


def test_libelle_statut():
    assert libelle_statut("Solde") == "Solde"
    assert libelle_statut("inconnu") == "inconnu"
