# Guide de contribution - EduPaie

Merci de votre interet pour EduPaie !

## Comment contribuer

### 1. Signaler un bug

Ouvrir une issue avec :
- Description du probleme
- Etapes pour reproduire
- Comportement attendu vs observe
- Version de l'application

### 2. Proposer une fonctionnalite

Ouvrir une issue avec le label "enhancement" :
- Description de la fonctionnalite
- Cas d'usage
- Benefices attendus

### 3. Soumettre du code

#### Fork et clone

    git clone https://github.com/VOTRE_USERNAME/EduPaie.git
    cd EduPaie
    git remote add upstream https://github.com/Francoise97/EduPaie.git

#### Creer une branche

    git checkout -b feature/ma-fonctionnalite

#### Developper

- Suivre les conventions de code (docs/CONVENTIONS.md)
- Tester les modifications
- Mettre a jour la documentation

#### Commiter

Convention de messages :

| Prefixe | Usage |
|---------|-------|
| feat: | Nouvelle fonctionnalite |
| fix: | Correction de bug |
| docs: | Documentation |
| style: | Formatage |
| refactor: | Refactorisation |
| test: | Tests |
| chore: | Maintenance |

#### Pousser et Pull Request

    git push origin feature/ma-fonctionnalite

Puis ouvrir une Pull Request sur GitHub.

## Standards de code

- PEP 8 pour Python
- 4 espaces d'indentation
- Lignes < 100 caracteres
- Noms explicites
- Commentaires en francais

## Tests

Avant de soumettre :

    python -m pytest tests/ -v

## Code de conduite

Voir CODE_OF_CONDUCT.md

## Questions

Contact : contact@mavictoire.tg
