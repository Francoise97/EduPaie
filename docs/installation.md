# Guide d'installation - EduPaie

> Guide pour installer et lancer l'application sur une machine Windows.

---

## 1. Prerequis

| Element | Requis |
|---|---|
| Systeme | Windows 10 ou 11 (64 bits) |
| Python | NON requis (l'exe est autonome) |
| Espace disque | ~100 Mo |
| Droits | Utilisateur standard (pas admin) |

**ATTENTION** : Le fichier `edupaie.db` doit **OBLIGATOIREMENT** etre dans le sous-dossier `data/`, a cote de `EduPaie.exe`.

---
---

## 3. Installation

### Etape 1 : Creer un dossier

Creer un dossier sur le Bureau par exemple :

    C:\Users\[VotreNom]\Desktop\EduPaie\

### Etape 2 : Copier les fichiers

Copier **TOUT le contenu** du dossier de distribution dans ce dossier :
- EduPaie.exe
- Le dossier data/ (avec edupaie.db dedans)
- Le dossier recus/

### Etape 3 : Verifier la structure

Apres copie, votre dossier doit ressembler a :


## 4. Lancement

### Methode 1 : Double-clic

**Double-cliquez** sur `EduPaie.exe`.

La fenetre de l'application s'ouvre apres quelques secondes.

### Methode 2 : Raccourci sur le Bureau

1. Clic droit sur `EduPaie.exe`
2. **Envoyer vers** -> **Bureau (creer un raccourci)**
3. Renommer le raccourci en **EduPaie**
4. Double-clic sur le raccourci

---

## 5. Utilisation

Voir le **manuel utilisateur** : docs/manuel_utilisateur.md

Resume rapide :
1. **Eleves** : ajouter / modifier / supprimer les eleves
2. **Paiements** : enregistrer un versement
3. **Recus** : voir / generer les recus PDF
4. **Tableau de bord** : vue d'ensemble des statistiques
5. **Parametres** : informations de l'ecole

---

## 6. Sauvegarde des donnees

**Toutes les donnees sont dans le fichier data/edupaie.db.**

Pour sauvegarder :
1. Fermer l'application
2. Copier le fichier data/edupaie.db sur une cle USB ou dans le cloud
3. En cas de probleme, remplacer le fichier par la sauvegarde

**Frequence recommandee** : 1 fois par semaine.

---

## 7. Desinstallation

1. Fermer l'application
2. Supprimer le dossier EduPaie/ en entier
3. Vider la corbeille

**Aucune entree dans le registre Windows, aucun fichier cache.**

---

## 8. Problemes courants

### L'application ne s'ouvre pas

**Cause** : Windows Defender bloque l'exe (car non signe).

**Solution** :
1. Clic droit sur EduPaie.exe -> Proprietes
2. Onglet Compatibilite
3. Cocher "Executer ce programme en tant qu'administrateur"
4. Appliquer

Ou :
1. Cliquer sur "Informations complementaires" dans l'alerte Windows
2. "Executer quand meme"

### Message "Base de donnees introuvable"

**Cause** : edupaie.db n'est pas au bon endroit.

**Solution** :
- Verifier que data/edupaie.db existe
- Verifier l'orthographe des noms de fichiers

### L'application met du temps a s'ouvrir

**Cause** : PyInstaller decompresse les ressources au premier lancement.

**Solution** : Patienter 5-10 secondes.

### Les recus PDF ne se generent pas

**Cause** : Pas de lecteur PDF installe.

**Solution** : Installer Adobe Reader ou Microsoft Edge.

---

## 9. Configuration minimale

| Composant | Recommande |
|---|---|
| Processeur | Intel i3 ou equivalent |
| RAM | 4 Go |
| Ecran | 1280 x 720 |
| Systeme | Windows 10 64 bits |

---

## 10. Contact

Pour toute question :
- Email : contact@mavictoire.tg
- Auteur : Francoise97
- Depot GitHub : https://github.com/Francoise97/EduPaie

---

**EduPaie v1.0.0 - Octobre 2026**
**Aucune installation Python n'est necessaire.** L'executable est autonome et contient tout ce qu'il faut (PySide6, reportlab, SQLite).

---

## 2. Contenu du dossier de distribution

Apres telechargement, vous devez avoir :# EduPaie - Gestion des paiements scolaires

Application desktop pour gerer les paiements des eleves dans un
etablissement scolaire : enregistrement des eleves, calcul du solde
restant du et generation de recus PDF numerotes.

## Fonctionnalites

- Gestion complete des eleves (ajout / modification / suppression)
- Liste recherchable et filtrable par classe et statut
- Enregistrement des paiements (especes, cheque, virement, mobile money)
- Calcul automatique du solde restant du avec validation
- Statut derive : Solde / Partiellement paye / Non paye
- Historique des paiements par eleve
- Generation de recus PDF numerotes uniques (REC-AAAA-NNN)
- Tableau de bord avec statistiques en temps reel
- Interface moderne (charte graphique QSS)

## Captures d'ecran

- Tableau de bord : docs/screenshots/01-dashboard.png
- Liste des eleves : docs/screenshots/02-eleves.png
- Fiche eleve : docs/screenshots/03-fiche.png
- Dialogue paiement : docs/screenshots/04-paiement.png
- Recus : docs/screenshots/05-recus.png
- Parametres : docs/screenshots/06-parametres.png

## Installation

### Prerequis

- Python 3.10 ou superieur (pour la version developpeur)
- Windows 10/11 64 bits

### Version developpeur

Ouvrir un terminal et executer :

git clone https://github.com/Francoise97/EduPaie.git
cd EduPaie
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python -m src.database.seed_runner
python main.py

### Version executable

Voir le guide d'installation : docs/installation.md

## Architecture

Le projet suit une architecture en 3 couches :

- database/ : Connexion SQLite + schema SQL
- models/ : Entites metier (Eleve, Paiement, Recu)
- repositories/ : Acces donnees (SQL encapsule)
- services/ : Logique metier (calcul solde, validation, PDF)
- utils/ : Validation + formatage
- ui/ : Interface PySide6 (widgets, dialogs, resources)
- config.py : Configuration (nom ecole, annee scolaire)

Regle : aucun widget n'execute de SQL directement.

## Base de donnees

- Table eleve : nom, prenom, classe, annee_scolaire, frais_totaux
- Table recu : numero_unique, montant_paye, solde_apres
- Table paiement : montant, date, mode, reference, observation
- Vue vue_solde_eleve : calcule automatiquement le solde et statut

Voir le schema complet : docs/MCD_MLD.md

## Documentation

- docs/documentation.md : Architecture, choix techniques, limites
- docs/manuel_utilisateur.md : Guide pas a pas pour l'utilisation
- docs/installation.md : Installation de l'executable
- docs/MCD_MLD.md : Modele de donnees
- docs/guide_soutenance.md : Preparation de la soutenance
- docs/FAQ.md : Questions frequentes
- CHANGELOG.md : Historique des versions
- CONTRIBUTING.md : Guide de contribution

## Tests

python -m pytest tests/

## Packaging

Windows : double-clic sur build.bat

OU

pyinstaller --onefile --windowed --name EduPaie --add-data "src/database/schema.sql;src/database" --add-data "src/ui/resources/styles.qss;src/ui/resources" main.py

L'executable est genere dans dist/EduPaie.exe.

## Technologies

- Python 3.10+ - Langage principal
- PySide6 - Interface graphique (Qt 6)
- SQLite - Base de donnees locale
- reportlab - Generation PDF
- PyInstaller - Packaging executable

## Auteur

Francoise97

Projet realise dans le cadre de la certification
Developpeur web et web mobile (2018).

## Licence

MIT - voir LICENSE
