# Tests - EduPaie

Tests unitaires de l'application.

## Structure

| Fichier | Description |
|---------|-------------|
| conftest.py | Configuration pytest |
| test_formatters.py | Tests des formateurs |
| test_validators.py | Tests des validateurs |
| test_config.py | Tests de la configuration |
| test_services.py | Tests des services |
| test_repositories.py | Tests des repositories |

## Lancement

python -m pytest tests/ -v

## Ajouter un test

    def test_mon_calcul():
        resultat = ma_fonction(2, 3)
        assert resultat == 5

## Regles

- Un test = une fonction test_xxx()
- Pas de dependance entre les tests
- Nettoyer la base apres chaque test
