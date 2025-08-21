@echo off
title Copie du Dossier Images
cd /d "%~dp0"

echo ==========================================
echo   Copie du Dossier Images
echo ==========================================
echo.

if not exist "images" (
    echo ❌ Aucun dossier images trouve
    echo.
    echo Pour utiliser vos images existantes :
    echo 1. Creez un dossier "images" dans ce repertoire
    echo 2. Placez vos images dedans (originals/, cards/, templates/)
    echo 3. Relancez ce script
    echo.
    pause
    exit /b 1
)

echo 🖼️ Dossier images trouve
echo.
echo 📋 Copie vers les executables...

REM Copier vers les differents emplacements
if exist "dist" (
    if exist "dist\images" (
        echo 🗑️ Suppression ancien dossier dist\images...
        rmdir /s /q "dist\images" 2>nul
    )
    
    xcopy "images" "dist\images\" /E /I /Y >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ dist\images\
    ) else (
        echo ❌ Erreur copie vers dist\images\
    )
    
    if exist "dist\EditeurCartesLove2D" (
        if exist "dist\EditeurCartesLove2D\images" (
            echo 🗑️ Suppression ancien dossier dist\EditeurCartesLove2D\images...
            rmdir /s /q "dist\EditeurCartesLove2D\images" 2>nul
        )
        
        xcopy "images" "dist\EditeurCartesLove2D\images\" /E /I /Y >nul 2>&1
        if !errorlevel! equ 0 (
            echo ✅ dist\EditeurCartesLove2D\images\
        ) else (
            echo ❌ Erreur copie vers dist\EditeurCartesLove2D\images\
        )
    )
)

echo.
echo ✅ Copie terminee !
echo.
echo 🎯 Vos executables utilisent maintenant vos images
echo    Templates, cartes et images sources incluses !
echo.
pause
