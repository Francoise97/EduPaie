"""Tests de la configuration."""
from src import config


def test_config_existe():
    assert hasattr(config, "ECOLE_NOM")
    assert hasattr(config, "DEVISE")
    assert hasattr(config, "VERSION")


def test_config_valeurs():
    assert config.DEVISE == "FCFA"
    assert config.VERSION == "v1.0.0"
    assert len(config.ECOLE_NOM) > 0
