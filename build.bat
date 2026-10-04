@echo off
REM ============================================================
REM Script de build - EduPaie
REM Genere un executable Windows autonome avec PyInstaller
REM ============================================================

echo.
echo ============================================================
echo   BUILD EduPaie - Generation de l'executable
echo ============================================================
echo.

REM Etape 1 : Nettoyage
echo [1/4] Nettoyage des anciens builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist EduPaie.spec del /q EduPaie.spec

REM Etape 2 : Generation de l'exe avec PyInstaller
echo.
echo [2/4] Generation de l'executable avec PyInstaller...
pyinstaller --onefile --windowed --name EduPaie ^
    --add-data "src/database/schema.sql;src/database" ^
    --add-data "src/ui/resources/styles.qss;src/ui/resources" ^
    main.py

if errorlevel 1 (
    echo.
    echo ERREUR : PyInstaller a echoue.
    pause
    exit /b 1
)

REM Etape 3 : Preparation du dossier de distribution
echo.
echo [3/4] Preparation du dossier dist/...
if not exist dist\data mkdir dist\data
if not exist dist\recus mkdir dist\recus
copy data\edupaie.db dist\data\edupaie.db > nul

REM Etape 4 : Verification
echo.
echo [4/4] Verification...
if exist dist\EduPaie.exe (
    echo.
    echo ============================================================
    echo   BUILD REUSSI !
    echo ============================================================
    echo.
    echo   Executable : dist\EduPaie.exe
    echo   Base de donnees : dist\data\edupaie.db
    echo   Dossier recus : dist\recus\
    echo.
    echo   Pour tester : dist\EduPaie.exe
    echo.
) else (
    echo.
    echo ERREUR : L'executable n'a pas ete genere.
)

pause
