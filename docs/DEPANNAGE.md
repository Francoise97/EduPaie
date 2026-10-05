# Guide de depannage - EduPaie

## Problemes courants

### L'application ne s'ouvre pas

Cause : Windows Defender bloque l'executable.

Solution :
1. Clic droit sur EduPaie.exe
2. Proprietes > Compatibilite
3. Cocher "Executer en tant qu'administrateur"
4. Appliquer

### Base de donnees introuvable

Cause : Le fichier data/edupaie.db n'est pas au bon endroit.

Solution :
1. Verifier que data/edupaie.db existe
2. Le fichier doit etre dans le meme dossier que EduPaie.exe

### Les recus PDF ne se generent pas

Cause : Aucun lecteur PDF installe.

Solution : Installer Adobe Reader ou Microsoft Edge.

### Erreur "Module not found"

Cause : Environnement virtuel desactive.

Solution :
    source venv/Scripts/activate
    pip install -r requirements.txt

### L'application est lente

Causes possibles :
- Beaucoup d'eleves (>1000)
- Base non optimisee

Solution :
    python scripts/clean.sh

## Logs

Les logs sont dans logs/
