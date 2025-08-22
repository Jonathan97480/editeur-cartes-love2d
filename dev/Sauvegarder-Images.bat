@echo off
title Sauvegarde du Dossier Images
cd /d "%~dp0"

echo ==========================================
echo   Sauvegarde du Dossier Images
echo ==========================================
echo.

set "BACKUP_DIR=backup_images_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%"
set "BACKUP_DIR=%BACKUP_DIR: =0%"
set "BACKUP_DIR=%BACKUP_DIR::=%"

echo 📁 Creation du dossier de sauvegarde : %BACKUP_DIR%
mkdir "%BACKUP_DIR%" 2>nul

set FOUND=0

REM Chercher et sauvegarder tous les dossiers images
if exist "images" (
    xcopy "images" "%BACKUP_DIR%\images_racine\" /E /I /Y >nul 2>&1
    echo ✅ images\ → %BACKUP_DIR%\images_racine\
    set FOUND=1
)

if exist "dist\images" (
    xcopy "dist\images" "%BACKUP_DIR%\images_dist\" /E /I /Y >nul 2>&1
    echo ✅ dist\images\ → %BACKUP_DIR%\images_dist\
    set FOUND=1
)

if exist "dist\EditeurCartesLove2D\images" (
    xcopy "dist\EditeurCartesLove2D\images" "%BACKUP_DIR%\images_dossier\" /E /I /Y >nul 2>&1
    echo ✅ dist\EditeurCartesLove2D\images\ → %BACKUP_DIR%\images_dossier\
    set FOUND=1
)

if %FOUND%==0 (
    echo ❌ Aucun dossier images trouve
    rmdir "%BACKUP_DIR%" 2>nul
) else (
    echo.
    echo ✅ Sauvegarde terminee dans le dossier : %BACKUP_DIR%
    echo 📊 Verifiez le contenu pour vous assurer que tout est sauve
)

echo.
pause
