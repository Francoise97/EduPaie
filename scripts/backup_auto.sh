#!/bin/bash
# Sauvegarde automatique - EduPaie

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
MAX_BACKUPS=10

mkdir -p "$BACKUP_DIR"

if [ ! -f "data/edupaie.db" ]; then
    echo "ERREUR : data/edupaie.db introuvable"
    exit 1
fi

cp "data/edupaie.db" "$BACKUP_DIR/edupaie_${DATE}.db"
echo "Sauvegarde creee : $BACKUP_DIR/edupaie_${DATE}.db"

# Nettoyer les anciennes sauvegardes
cd "$BACKUP_DIR"
ls -t *.db 2>/dev/null | tail -n +$((MAX_BACKUPS + 1)) | xargs -r rm
cd ..

echo "Conservation des $MAX_BACKUPS dernieres sauvegardes"
