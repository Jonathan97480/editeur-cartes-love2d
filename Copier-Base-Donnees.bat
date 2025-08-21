@echo off
title Copie de la Base de Donnees
cd /d "%~dp0"

echo ==========================================
echo   Copie de la Base de Donnees
echo ==========================================
echo.

if not exist "cartes.db" (
    echo ❌ Aucune base de donnees cartes.db trouvee
    echo.
    echo Pour utiliser vos donnees existantes :
    echo 1. Copiez votre fichier cartes.db dans ce dossier
    echo 2. Relancez ce script
    echo.
    pause
    exit /b 1
)

echo 📊 Base de donnees trouvee : cartes.db
echo.
echo 📋 Copie vers les executables...

REM Copier vers les differents emplacements
if exist "dist" (
    copy "cartes.db" "dist\" 2>nul
    echo ✅ dist\cartes.db
    
    if exist "dist\_internal" (
        copy "cartes.db" "dist\_internal\" 2>nul
        echo ✅ dist\_internal\cartes.db
    )
    
    if exist "dist\EditeurCartesLove2D" (
        copy "cartes.db" "dist\EditeurCartesLove2D\" 2>nul
        echo ✅ dist\EditeurCartesLove2D\cartes.db
        
        if exist "dist\EditeurCartesLove2D\_internal" (
            copy "cartes.db" "dist\EditeurCartesLove2D\_internal\" 2>nul
            echo ✅ dist\EditeurCartesLove2D\_internal\cartes.db
        )
    )
)

echo.
echo ✅ Copie terminee !
echo.
echo 🎯 Vos executables utiliseront maintenant votre base existante
echo    avec toutes vos cartes personnalisees !
echo.
pause
