@echo off
title Editeur de cartes Love2D - Lancement

echo ======================================
echo   EDITEUR DE CARTES LOVE2D
echo   Version finale stable
echo ======================================
echo.

cd /d "%~dp0"

REM Vérifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou accessible dans le PATH.
    echo Veuillez installer Python 3.7+ depuis https://python.org
    pause
    exit /b 1
)

echo [INFO] Lancement de l'application finale...
echo.

REM Installer les dépendances si nécessaire
if not exist lib\ (
    echo [ERREUR] Le dossier lib/ est manquant !
    echo Assurez-vous d'avoir tous les fichiers de l'application.
    pause
    exit /b 1
)

REM Lancer l'application finale
python app_final.py
if errorlevel 1 (
    echo.
    echo [ERREUR] L'application s'est terminée avec une erreur.
    echo Consultez les messages ci-dessus pour plus d'informations.
    pause
    exit /b 1
)

echo.
echo [INFO] Application fermée normalement.
pause
