# Changelog - EduPaie

Toutes les modifications notables de ce projet sont documentees ici.

## [1.0.0] - 2026-10-04

### Ajoute
- Gestion complete des eleves (CRUD)
- Enregistrement des paiements avec validation du solde
- Calcul automatique du solde restant du
- Generation de recus numerotes uniques (REC-AAAA-NNN)
- Export PDF des recus via reportlab
- Tableau de bord avec statistiques temps reel
- Ecran Recus avec liste complete
- Ecran Parametres avec informations de l'ecole
- Personnalisation du nom d'ecole via config.py

### Technique
- Architecture en 3 couches (donnees / metier / interface)
- Base SQLite avec contraintes d'integrite
- Interface PySide6 avec charte graphique QSS
- Packaging PyInstaller (exe autonome)
