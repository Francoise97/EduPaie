#!/bin/bash
# Diagnostic du projet - EduPaie

echo "=== DIAGNOSTIC EduPaie ==="
echo ""

echo "1. SYSTEME"
echo "   OS : $(uname -s)"
echo "   Python : $(python --version 2>&1)"
echo ""

echo "2. PROJET"
echo "   Dossier : $(pwd)"
echo "   Fichiers Python : $(find src -name '*.py' 2>/dev/null | wc -l)"
echo "   Lignes de code : $(find src -name '*.py' -exec cat {} \; 2>/dev/null | wc -l)"
echo ""

echo "3. BASE DE DONNEES"
if [ -f "data/edupaie.db" ]; then
    echo "   Fichier : data/edupaie.db"
    echo "   Taille : $(ls -lh data/edupaie.db | awk '{print $5}')"
    python -c "
import sqlite3
c = sqlite3.connect('data/edupaie.db')
print(f'   Eleves : {c.execute(\"SELECT COUNT(*) FROM eleve\").fetchone()[0]}')
print(f'   Paiements : {c.execute(\"SELECT COUNT(*) FROM paiement\").fetchone()[0]}')
print(f'   Recus : {c.execute(\"SELECT COUNT(*) FROM recu\").fetchone()[0]}')
c.close()
"
else
    echo "   ERREUR : fichier introuvable"
fi
echo ""

echo "4. GIT"
echo "   Branche : $(git branch --show-current 2>/dev/null)"
echo "   Commits : $(git log --oneline 2>/dev/null | wc -l)"
echo "   Statut : $(git status --short 2>/dev/null | wc -l) fichiers modifies"
echo ""

echo "5. DISTRIBUTION"
if [ -f "distribution/EduPaie.exe" ]; then
    echo "   Exe : $(ls -lh distribution/EduPaie.exe | awk '{print $5}')"
else
    echo "   Exe : non genere"
fi
echo ""

echo "=== FIN DIAGNOSTIC ==="
