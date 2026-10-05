# Bonnes pratiques - EduPaie

## Developpement

### Nommage

- Classes : PascalCase (PaiementService)
- Fonctions : snake_case (calculer_solde)
- Variables : snake_case (montant_total)
- Constantes : UPPER_SNAKE (ECOLE_NOM)

### Structure

    """Docstring du module."""

    # Imports standard
    import sys

    # Imports tiers
    from PySide6 import QtWidgets

    # Imports locaux
    from src.services import EleveService

### Indentation

- 4 espaces
- Pas de tabulations
- Lignes < 100 caracteres

### Commentaires

- Langue : francais
- Docstrings : triple quotes
- Commentaires : #

## Git

### Messages de commit

Format : type: description

Types :
- feat: nouvelle fonctionnalite
- fix: correction de bug
- docs: documentation
- style: formatage
- refactor: refactorisation
- test: tests
- chore: maintenance

### Branches

- main : version stable
- dev : developpement
- feature/xxx : fonctionnalite specifique

### Commits

- Un commit = une modification logique
- Message clair et concis
- Pas de "WIP" ou "fix"

## Base de donnees

- Toujours utiliser des transactions
- Valider avant d'inserer
- Utiliser les contraintes SQL
- Indexer les colonnes filtrees

## Tests

- Tester avant de commiter
- Test unitaire par fonction
- Test d'integration pour les flux
