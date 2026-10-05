#!/bin/bash
# Installation complete - EduPaie

echo "=== Installation EduPaie ==="
echo ""

echo "[1/4] Verification de Python..."
python --version
if [ $? -ne 0 ]; then
    echo "ERREUR : Python n'est pas installe"
    exit 1
fi

echo ""
echo "[2/4] Creation de l'environnement virtuel..."
python -m venv venv
source venv/Scripts/activate

echo ""
echo "[3/4] Installation des dependances..."
pip install -r requirements.txt

echo ""
echo "[4/4] Initialisation de la base de donnees..."
python -m src.database.seed_runner

echo ""
echo "=== Installation terminee ==="
echo ""
echo "Pour lancer l'application :"
echo "  source venv/Scripts/activate"
echo "  python main.py"
