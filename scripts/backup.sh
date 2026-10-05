#!/bin/bash
# Sauvegarde de la base - EduPaie

DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p backups

if [ -f "data/edupaie.db" ]; then
    cp "data/edupaie.db" "backups/edupaie_${DATE}.db"
    echo "Sauvegarde creee"
else
    echo "Erreur : base introuvable"
    exit 1
fi
