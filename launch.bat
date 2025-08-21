@echo off
title Editeur de cartes Love2D - Sélection du mode
color 0F

:start
cls

echo ================================================================
echo                EDITEUR DE CARTES LOVE2D
echo                    Selection du mode
echo ================================================================
echo.
echo Choisissez le mode de lancement :
echo.
echo   [1] Mode Automatique (recommandé)
echo       - Détection automatique du meilleur mode
echo       - Fallback en cas de problème
echo.
echo   [2] Mode Final Stable
echo       - Interface complète et moderne
echo       - Garantie de fonctionnement
echo.
echo   [3] Mode Compatibilité
echo       - Interface basique mais robuste
echo       - Pour les environnements restreints
echo.
echo   [4] Mode Avancé (force)
echo       - Interface avec thèmes Windows 11
echo       - Peut échouer selon l'environnement
echo.
echo   [T] Lancer les tests
echo   [Q] Quitter
echo.
echo ================================================================
echo.

:choice
set /p choice="Votre choix [1-4, T, Q] : "

if /i "%choice%"=="1" goto auto
if /i "%choice%"=="2" goto final
if /i "%choice%"=="3" goto compat
if /i "%choice%"=="4" goto advanced
if /i "%choice%"=="t" goto test
if /i "%choice%"=="q" goto quit

echo.
echo Choix invalide. Veuillez sélectionner 1, 2, 3, 4, T ou Q.
echo.
goto choice

:auto
echo.
echo [INFO] Lancement en mode automatique...
echo.
python test.py
goto end

:final
echo.
echo [INFO] Lancement en mode final stable...
echo.
python app_final.py
goto end

:compat
echo.
echo [INFO] Lancement en mode compatibilité...
echo.
python test_compat.py --compat
goto end

:advanced
echo.
echo [INFO] Lancement en mode avancé (forcé)...
echo.
python test.py --force-advanced
goto end

:test
echo.
echo [INFO] Exécution des tests...
echo.
python test.py --test
goto end

:quit
echo.
echo Au revoir !
exit /b 0

:end
if errorlevel 1 (
    echo.
    echo [ERREUR] L'application s'est terminée avec une erreur.
    echo.
    echo Appuyez sur une touche pour revenir au menu...
    pause >nul
    cls
    goto start
) else (
    echo.
    echo [INFO] Application fermée normalement.
    echo.
    echo Appuyez sur une touche pour revenir au menu...
    pause >nul
    cls
    goto start
)

:start
