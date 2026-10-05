# EduPaie - Gestion des paiements scolaires

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.11-green)
![SQLite](https://img.shields.io/badge/SQLite-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)


Application desktop pour gerer les paiements des eleves : enregistrement,
calcul du solde restant du et generation de recus PDF numerotes.

## Fonctionnalites

- Gestion des eleves (ajout / modification / suppression)
- Enregistrement des paiements avec validation
- Calcul automatique du solde restant du
- Statut : Solde / Partiellement paye / Non paye
- Generation de recus PDF numerotes (REC-AAAA-NNN)
- Tableau de bord avec statistiques temps reel

## Installation

Prerequis : Python 3.10+, Windows 10/11

Version developpeur :

    git clone https://github.com/Françoise/EduPaie.git
    cd EduPaie
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    python -m src.database.seed_runner
    python main.py

Version executable : voir docs/installation.md

## Architecture

Le projet suit une architecture en 3 couches :

- database/ : Connexion SQLite + schema
- models/ : Entites metier (Eleve, Paiement, Recu)
- repositories/ : Acces donnees (SQL encapsule)
- services/ : Logique metier (calcul solde, PDF)
- utils/ : Validation + formatage
- ui/ : Interface PySide6 (widgets, dialogs)
- config.py : Configuration (nom ecole, annee)

Aucun widget n'execute de SQL directement.

## Documentation

- docs/documentation.md : Documentation technique
- docs/manuel_utilisateur.md : Manuel utilisateur
- docs/installation.md : Guide d'installation
- docs/MCD_MLD.md : Modele de donnees
- docs/guide_soutenance.md : Guide de soutenance
- docs/FAQ.md : Questions frequentes

## Technologies

Python 3.10+ / PySide6 (Qt 6) / SQLite / reportlab / PyInstaller

## Auteur

Françoise - Projet Developpeur web et web mobile (2018)

## Licence

MIT
