@echo off
title Editeur de cartes Love2D - Guide de lancement
color 0A
cls

echo ================================================================
echo               EDITEUR DE CARTES LOVE2D
echo                 Guide de lancement
echo ================================================================
echo.
echo Fichiers de lancement disponibles :
echo.
echo   launch.bat         Menu complet avec tous les modes
echo   launch_simple.bat  Menu simplifié pour usage rapide
echo   run_final.bat      Lancement direct mode stable
echo   run.bat            Lancement auto avec environnement
echo.
echo ================================================================
echo.
echo Quel fichier voulez-vous exécuter ?
echo.
echo   [1] launch.bat (menu complet)
echo   [2] launch_simple.bat (menu simple) 
echo   [3] run_final.bat (direct stable)
echo   [4] run.bat (auto avec venv)
echo   [H] Ouvrir l'aide (MODES.md)
echo   [Q] Quitter
echo.

:choice
set /p choice="Votre choix [1-4, H, Q] : "

if /i "%choice%"=="1" (
    cls
    echo Lancement de launch.bat...
    echo.
    call launch.bat
    goto end
)
if /i "%choice%"=="2" (
    cls  
    echo Lancement de launch_simple.bat...
    echo.
    call launch_simple.bat
    goto end
)
if /i "%choice%"=="3" (
    cls
    echo Lancement de run_final.bat...
    echo.
    call run_final.bat
    goto end
)
if /i "%choice%"=="4" (
    cls
    echo Lancement de run.bat...
    echo.
    call run.bat
    goto end
)
if /i "%choice%"=="h" (
    echo.
    echo Ouverture du guide des modes...
    start notepad MODES.md
    goto choice
)
if /i "%choice%"=="q" goto quit

echo.
echo Choix invalide. Veuillez sélectionner 1, 2, 3, 4, H ou Q.
echo.
goto choice

:quit
echo.
echo Au revoir !
exit /b 0

:end
echo.
echo Retour au guide principal.
pause
cls
goto 0
