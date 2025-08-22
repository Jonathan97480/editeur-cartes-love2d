@echo off
title Editeur de cartes Love2D - Lancement rapide
color 0B

:start
cls

echo ========================================
echo     EDITEUR DE CARTES LOVE2D
echo        Lancement rapide
echo ========================================
echo.
echo [1] Mode recommandé (automatique)
echo [2] Mode stable garanti 
echo [3] Tests
echo [Q] Quitter
echo.

:choice
set /p choice="Votre choix [1-3, Q] : "

if /i "%choice%"=="1" goto auto
if /i "%choice%"=="2" goto final
if /i "%choice%"=="3" goto test
if /i "%choice%"=="q" goto quit

echo.
echo Choix invalide. Tapez 1, 2, 3 ou Q.
goto choice

:auto
echo.
echo Lancement automatique...
python test.py
goto end

:final
echo.
echo Lancement stable...
python app_final.py
goto end

:test
echo.
echo Tests...
python test.py --test
goto end

:quit
exit /b 0

:end
if errorlevel 1 (
    echo.
    echo ERREUR lors du lancement.
    pause
    goto start
) else (
    echo.
    echo Fermé normalement.
    pause
    goto start
)
