#!/bin/bash
# Restauration de la base - EduPaie

if [ -z "$1" ]; then
    echo "Usage : ./scripts/restore.sh <backup.db>"
    exit 1
fi

cp data/edupaie.db data/edupaie.db.old
cp "$1" data/edupaie.db
echo "Base restauree depuis : $1"
