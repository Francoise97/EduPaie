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

Apres telechargement, vous devez avoir :
