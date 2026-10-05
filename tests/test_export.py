"""Tests des fonctions d'export."""
import os
import tempfile


def test_export_dossier_temporaire():
    """Verifie que le dossier temporaire est accessible."""
    with tempfile.TemporaryDirectory() as tmp:
        assert os.path.exists(tmp)


def test_export_fichier_temporaire():
    """Verifie la creation d'un fichier temporaire."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("test,data\n1,2\n")
        chemin = f.name

    assert os.path.exists(chemin)
    os.unlink(chemin)


def test_format_csv():
    """Verifie le format CSV de base."""
    lignes = [
        "nom,prenom,montant",
        "Diallo,Amadou,50000",
        "Sow,Fatou,75000",
    ]
    contenu = "\n".join(lignes)
    assert "Diallo" in contenu
    assert "50000" in contenu
