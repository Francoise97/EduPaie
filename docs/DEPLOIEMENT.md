# Guide de deploiement - EduPaie

## 1. Deploiement developpeur

    git clone https://github.com/Francoise97/EduPaie.git
    cd EduPaie
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    python -m src.database.seed_runner
    python main.py

## 2. Deploiement utilisateur (exe)

1. Copier le dossier distribution/
2. Double-cliquer sur EduPaie.exe

## 3. Generation de l'executable

Windows : build.bat

## 4. Sauvegarde

La base de donnees est dans data/edupaie.db.
