#!/bin/bash
# Nettoyage des fichiers temporaires - EduPaie

echo "=== Nettoyage du projet ==="
echo ""

echo "[1/4] Suppression des __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "  OK"

echo ""
echo "[2/4] Suppression des .pyc..."
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "  OK"

echo ""
echo "[3/4] Suppression du cache pytest..."
rm -rf .pytest_cache 2>/dev/null
echo "  OK"

echo ""
echo "[4/4] Suppression de build/ et dist/ (optionnel)..."
read -p "Supprimer build/ et dist/ ? (o/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[OoYy]$ ]]; then
    rm -rf build/ dist/ *.spec 2>/dev/null
    echo "  Supprimes"
else
    echo "  Conserves"
fi

echo ""
echo "=== Nettoyage termine ==="
