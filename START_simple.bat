@echo off
title Editeur de Cartes Love2D v2.4.0

echo ===============================================
echo    Editeur de Cartes Love2D v2.4.0
echo    Projet reorganise et optimise
echo ===============================================
echo.

:: Verifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou accessible
    echo    Veuillez installer Python 3.8+ et redemarrer
    pause
    exit /b 1
)

:: Verifier que le fichier principal existe
if not exist "app_final.py" (
    echo ERREUR: Fichier app_final.py introuvable
    echo    Assurez-vous d'etre dans le bon repertoire
    pause
    exit /b 1
)

echo OPTIONS DE LANCEMENT
echo.
echo   [1] Lancer l'editeur directement (par defaut)
echo   [2] Menu avance avec mise a jour GitHub
echo   [U] Mise a jour depuis GitHub
echo   [Q] Quitter
echo.

set /p choice="Votre choix (Entree pour lancer directement) : "

if /i "%choice%"=="2" (
    echo Ouverture du menu avance...
    if exist "tools\START.bat" (
        call tools\START.bat
        exit /b 0
    ) else (
        echo ERREUR: Menu avance non trouve
        pause
        goto launch_direct
    )
)

if /i "%choice%"=="u" (
    echo Lancement de la mise a jour...
    if exist "UPDATE.bat" (
        call UPDATE.bat
        exit /b 0
    ) else (
        echo ERREUR: Script de mise a jour non trouve
        pause
        goto launch_direct
    )
)

if /i "%choice%"=="q" (
    echo Au revoir !
    exit /b 0
)

:launch_direct
:: Lancer l'application
echo Demarrage de l'editeur de cartes...
python app_final.py

:: Gerer la sortie
if errorlevel 1 (
    echo.
    echo ERREUR: L'application s'est fermee avec une erreur
    echo    Consultez les logs ou essayez tools/DIAGNOSTIC.bat
    pause
) else (
    echo.
    echo Application fermee normalement
)

exit /b 0
