@echo off
title Editeur de cartes Love2D - Lancement Rapide
cls

echo ===============================================
echo          EDITEUR DE CARTES LOVE2D
echo               Lancement Rapide
echo ===============================================
echo.

echo Demarrage de l'application...
echo.

REM Vérifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python non trouve!
    echo.
    echo Installez Python depuis: https://python.org
    echo.
    pause
    exit /b 1
)

REM Vérifier que le fichier principal existe
if not exist "app_final.py" (
    echo ERREUR: Fichier app_final.py non trouve!
    echo.
    echo Verifiez que vous etes dans le bon dossier.
    echo.
    pause
    exit /b 1
)

REM Lancer l'application
echo Lancement en cours...
python app_final.py

REM Gestion des erreurs
if errorlevel 1 (
    echo.
    echo ERREUR: L'application a rencontre un probleme.
    echo.
    echo Conseils de depannage:
    echo - Verifiez les dependances Python (requirements.txt)
    echo - Consultez les messages d'erreur ci-dessus
    echo.
) else (
    echo.
    echo Application fermee normalement.
)

pause
