@echo off
title Sauvegarde de la Base de Donnees
cd /d "%~dp0"

echo ==========================================
echo   Sauvegarde de la Base de Donnees
echo ==========================================
echo.

set "BACKUP_DIR=backup_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%"
set "BACKUP_DIR=%BACKUP_DIR: =0%"
set "BACKUP_DIR=%BACKUP_DIR::=%"

echo 📁 Creation du dossier de sauvegarde : %BACKUP_DIR%
mkdir "%BACKUP_DIR%" 2>nul

set FOUND=0

REM Chercher et sauvegarder toutes les bases de donnees
if exist "cartes.db" (
    copy "cartes.db" "%BACKUP_DIR%\cartes_racine.db" 2>nul
    echo ✅ cartes.db → %BACKUP_DIR%\cartes_racine.db
    set FOUND=1
)

if exist "dist\cartes.db" (
    copy "dist\cartes.db" "%BACKUP_DIR%\cartes_dist.db" 2>nul
    echo ✅ dist\cartes.db → %BACKUP_DIR%\cartes_dist.db
    set FOUND=1
)

if exist "dist\_internal\cartes.db" (
    copy "dist\_internal\cartes.db" "%BACKUP_DIR%\cartes_internal.db" 2>nul
    echo ✅ dist\_internal\cartes.db → %BACKUP_DIR%\cartes_internal.db
    set FOUND=1
)

if exist "dist\EditeurCartesLove2D\cartes.db" (
    copy "dist\EditeurCartesLove2D\cartes.db" "%BACKUP_DIR%\cartes_dossier.db" 2>nul
    echo ✅ dist\EditeurCartesLove2D\cartes.db → %BACKUP_DIR%\cartes_dossier.db
    set FOUND=1
)

if %FOUND%==0 (
    echo ❌ Aucune base de donnees trouvee
    rmdir "%BACKUP_DIR%" 2>nul
) else (
    echo.
    echo ✅ Sauvegarde terminee dans le dossier : %BACKUP_DIR%
)

echo.
pause
