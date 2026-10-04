# EduPaie - Gestion des paiements scolaires

Application desktop Python / PySide6 / SQLite pour gerer les eleves,
enregistrer les paiements et generer des recus numerotes en PDF.

## Fonctionnalites

- Gestion des eleves (ajout / modification / suppression)
- Liste recherchable et filtrable par classe et statut
- Enregistrement des paiements (especes, cheque, virement, mobile money)
- Calcul automatique du solde restant du
- Statut derive : Solde / Partiellement paye / Non paye
- Historique des paiements par eleve
- Generation de recus numerotes uniques (REC-AAAA-NNN)
- Export PDF des recus (reportlab)
- Tableau de bord avec statistiques en temps reel

## Prerequis

- Python 3.10 ou superieur
- pip

## Installation

    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt

## Initialiser la base de test

    python -m src.database.seed_runner

## Lancer l'application

    python main.py

## Structure du projet

    edupaie/
    |-- main.py                    Point d'entree
    |-- requirements.txt
    |-- README.md
    |-- data/
    |   |-- edupaie.db             Base SQLite
    |-- recus/                     PDF des recus generes
    |-- docs/
    |   |-- manuel_utilisateur.md
    |   |-- documentation.md
    |-- src/
        |-- database/              Connexion + schema SQL
        |-- models/                Entites metier
        |-- repositories/          Acces donnees (SQL)
        |-- services/              Logique metier
        |-- utils/                 Validation + formatage
        |-- ui/                    Interface PySide6

## Architecture

Le projet suit une architecture en couches :

1. Acces aux donnees (src/repositories/) : encapsule tout le SQL
2. Logique metier (src/services/) : validation, calcul solde, numerotation
3. Interface (src/ui/) : fenetres PySide6, widgets, dialogs

Aucun widget n'execute de SQL directement.

## Base de donnees

Tables principales :

- eleve (id, nom, prenom, classe, annee_scolaire, frais_totaux, ...)
- recu (id, numero_unique, annee, sequence, eleve_id, montant_paye, solde_apres)
- paiement (id, eleve_id, recu_id, montant, date_paiement, mode_paiement)

Vue SQL vue_solde_eleve : calcule automatiquement solde et statut.

## Packaging

    pyinstaller --onefile --windowed --name EduPaie main.py

Executable dans dist/EduPaie.exe.

## Auteur

Projet realise dans le cadre de la certification Developpeur web et web mobile (2026).

