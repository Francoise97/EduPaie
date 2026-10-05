#!/bin/bash
# Analyse de code - EduPaie

echo "=== Analyse de code ==="
echo ""

# 1. Syntaxe Python
echo "[1/3] Verification de la syntaxe Python..."
find src -name "*.py" -exec python -m py_compile {} \;
if [ $? -eq 0 ]; then
    echo "  OK Syntaxe valide"
else
    echo "  ERREUR de syntaxe"
    exit 1
fi

# 2. Imports
echo ""
echo "[2/3] Verification des imports..."
python -c "from src.ui.main_window import MainWindow; print('  OK Imports valides')"

# 3. Statistiques
echo ""
echo "[3/3] Statistiques du projet..."
echo "  Nombre de fichiers Python : $(find src -name '*.py' | wc -l)"
echo "  Nombre de lignes : $(find src -name '*.py' -exec cat {} \; | wc -l)"

echo ""
echo "=== Analyse terminee ==="
