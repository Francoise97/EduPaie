#!/bin/bash
# Preparation de la distribution - EduPaie

echo "=== Preparation de la distribution ==="
echo ""

if [ ! -f "dist/EduPaie.exe" ]; then
    echo "ERREUR : dist/EduPaie.exe introuvable"
    echo "Lancez d'abord : pyinstaller --onefile --windowed main.py"
    exit 1
fi

echo "[1/3] Nettoyage de l'ancienne distribution..."
rm -rf distribution

echo ""
echo "[2/3] Creation de la structure..."
mkdir -p distribution/data
mkdir -p distribution/recus
mkdir -p distribution/docs

echo ""
echo "[3/3] Copie des fichiers..."
cp dist/EduPaie.exe distribution/
cp data/edupaie.db distribution/data/
cp README.md distribution/
cp docs/installation.md distribution/docs/
cp docs/manuel_utilisateur.md distribution/docs/

echo ""
echo "=== Distribution prete ==="
echo ""
echo "Contenu :"
ls -la distribution/
