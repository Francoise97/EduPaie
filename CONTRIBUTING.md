# Guide de contribution - EduPaie

## Workflow Git

1. Creer une branche depuis `dev` :
   git checkout dev
   git pull origin dev
   git checkout -b feature/ma-fonctionnalite

2. Developper et commiter :
   git add .
   git commit -m "feat: description claire"

3. Pousser vers GitHub :
   git push -u origin feature/ma-fonctionnalite

4. Creer une Pull Request sur GitHub

## Convention de commits

- `feat:` nouvelle fonctionnalite
- `fix:` correction de bug
- `docs:` documentation
- `style:` formatage
- `refactor:` refactorisation
- `test:` ajout de tests
- `chore:` taches diverses
