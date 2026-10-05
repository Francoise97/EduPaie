@echo off
REM Script de lancement des tests - EduPaie

echo ============================================
echo   Tests EduPaie
echo ============================================
echo.

cd /d "%~dp0\.."

echo [1/2] Tests unitaires...
python -m pytest tests/ -v
if errorlevel 1 (
    echo.
    echo ERREUR : Tests echoues
    pause
    exit /b 1
)

echo.
echo [2/2] Verification de la base...
python -c "import sqlite3; c=sqlite3.connect('data/edupaie.db'); n=c.execute('SELECT COUNT(*) FROM eleve').fetchone()[0]; print(f'Eleves en base : {n}'); c.close()"

echo.
echo ============================================
echo   Tests termines avec succes
echo ============================================
pause
