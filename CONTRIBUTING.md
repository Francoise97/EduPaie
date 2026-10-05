# Guide de contribution - EduPaie

Merci de votre interet pour EduPaie ! Ce document explique comment
contribuer au projet.

## Types de contributions

- Rapports de bugs
- Suggestions de fonctionnalites
- Corrections de code
- Amelioration de la documentation
- Tests

## Workflow Git

1. Fork le projet
2. Creer une branche :
   git checkout -b feature/ma-fonctionnalite

3. Faire les modifications
4. Commiter avec un message clair :
   git commit -m "feat: description"

5. Pousser :
   git push origin feature/ma-fonctionnalite

6. Ouvrir une Pull Request

## Convention de commits

| Prefixe | Usage |
|---------|-------|
| feat: | Nouvelle fonctionnalite |
| fix: | Correction de bug |
| docs: | Documentation |
| style: | Formatage |
| refactor: | Refactorisation |
| test: | Ajout de tests |
| chore: | Taches diverses |

## Style de code

- Python : PEP 8
- Indentation : 4 espaces
- Longueur de ligne : 100 caracteres max
- Langue des commentaires : francais

## Tests

Avant de soumettre, lancer :
python -m pytest tests/

## Contact

Francoise97 - github.com/Francoise97
