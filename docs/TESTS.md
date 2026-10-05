# Guide des tests - EduPaie

## Strategie de test

### Pyramide des tests

1. Tests unitaires (base)
2. Tests d'integration (milieu)
3. Tests fonctionnels (sommet)

## Tests unitaires

### Formatters (test_formatters.py)

- test_formater_montant
- test_formater_date
- test_libelle_statut

### Validators (test_validators.py)

- test_valider_montant_valide
- test_valider_montant_invalide
- test_valider_montant_negatif
- test_valider_texte_obligatoire
- test_valider_date

### Config (test_config.py)

- test_config_existe
- test_config_valeurs

## Tests d'integration

### Services (test_services.py)

- test_lister_eleves
- test_statistiques

### Repositories (test_repositories.py)

- test_compter_eleves

## Lancement

### Tous les tests

    python -m pytest tests/ -v

### Un fichier specifique

    python -m pytest tests/test_formatters.py -v

### Avec couverture

    python -m pytest tests/ --cov=src

## Bonnes pratiques

- Un test = une assertion principale
- Nommer les tests de facon explicite
- Isoler les tests (pas de dependance)
- Nettoyer apres chaque test

## Resultats attendus

Tous les tests doivent passer :
    ===== 15 passed in 0.5s =====
