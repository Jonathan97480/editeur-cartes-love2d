@echo off
chcp 65001 > nul
title Mise à jour automatique - Éditeur de cartes Love2D

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                  MISE À JOUR AUTOMATIQUE                     ║
echo ║              Éditeur de cartes Love2D                        ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Configuration
set "PROJECT_DIR=%~dp0"
set "BACKUP_DIR=%PROJECT_DIR%backup_%date:~6,4%_%date:~3,2%_%date:~0,2%_%time:~0,2%_%time:~3,2%"
set "BACKUP_DIR=%BACKUP_DIR: =0%"

echo 🔍 Vérification de l'environnement...

REM Vérifier si Git est installé
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git n'est pas installé ou non accessible
    echo.
    echo 💡 Veuillez installer Git depuis : https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Git détecté

REM Vérifier si on est dans un dépôt Git
if not exist ".git" (
    echo ❌ Ce dossier n'est pas un dépôt Git
    echo.
    echo 💡 Clonez d'abord le projet avec :
    echo    git clone https://github.com/jonathan97480/editeur-cartes-love2d.git
    pause
    exit /b 1
)

echo ✅ Dépôt Git détecté

echo.
echo 📦 MISE À JOUR DU PROJET
echo ========================

echo.
echo 1️⃣  Sauvegarde des modifications locales...

REM Créer un dossier de sauvegarde
if not exist "backups" mkdir backups
set "BACKUP_DIR=backups\backup_%date:~6,4%_%date:~3,2%_%date:~0,2%_%time:~0,2%_%time:~3,2%"
set "BACKUP_DIR=%BACKUP_DIR: =0%"
mkdir "%BACKUP_DIR%" 2>nul

REM Sauvegarder les fichiers modifiés
echo 💾 Sauvegarde en cours dans %BACKUP_DIR%...

REM Sauvegarder la base de données si elle existe
if exist "cartes.db" (
    copy "cartes.db" "%BACKUP_DIR%\cartes.db" >nul
    echo ✅ Base de donnees sauvegardee
)

if exist "data\cartes.db" (
    copy "data\cartes.db" "%BACKUP_DIR%\cartes_data.db" >nul
    echo ✅ Base de donnees ^(data/^) sauvegardee
)

REM Sauvegarder les images personnalisées
if exist "images" (
    xcopy "images" "%BACKUP_DIR%\images" /E /I /Q >nul 2>&1
    echo ✅ Images sauvegardees
)

if exist "assets\images" (
    xcopy "assets\images" "%BACKUP_DIR%\assets_images" /E /I /Q >nul 2>&1
    echo ✅ Images ^(assets/^) sauvegardees
)

REM Sauvegarder les configurations personnalisées
if exist "config.lua" (
    copy "config.lua" "%BACKUP_DIR%\config.lua" >nul
    echo ✅ Configuration sauvegardee
)

echo.
echo 2️⃣  Récupération des dernières modifications...

REM Sauvegarder l'état local au cas où
git stash push -m "Sauvegarde automatique avant mise à jour" >nul 2>&1

REM Récupérer les dernières modifications
echo 🔄 Téléchargement des mises à jour...
git fetch origin

echo 🔄 Application des mises à jour...
git pull origin main

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erreur lors de la mise à jour
    echo.
    echo 💡 Essayez de résoudre les conflits manuellement avec :
    echo    git status
    echo    git pull origin main
    pause
    exit /b 1
)

echo ✅ Mise à jour terminée

echo.
echo 3️⃣  Restauration des données personnelles...

REM Restaurer la base de données si elle n'existe plus
if not exist "cartes.db" if exist "%BACKUP_DIR%\cartes.db" (
    copy "%BACKUP_DIR%\cartes.db" "cartes.db" >nul
    echo ✅ Base de données restaurée
)

if not exist "data\cartes.db" if exist "%BACKUP_DIR%\cartes_data.db" (
    if not exist "data" mkdir data
    copy "%BACKUP_DIR%\cartes_data.db" "data\cartes.db" >nul
    echo ✅ Base de données (data/) restaurée
)

REM Restaurer les images personnalisées si le dossier n'existe plus
if not exist "images" if exist "%BACKUP_DIR%\images" (
    xcopy "%BACKUP_DIR%\images" "images" /E /I /Q >nul 2>&1
    echo ✅ Images restaurées
)

echo.
echo 4️⃣  Vérification de l'installation...

REM Vérifier que Love2D est accessible
echo 🔍 Vérification de Love2D...

REM Chercher Love2D dans les emplacements courants
set "LOVE2D_FOUND=0"

if exist "C:\Program Files\LOVE\love.exe" (
    set "LOVE2D_FOUND=1"
    echo ✅ Love2D trouvé dans Program Files
)

if exist "C:\Program Files (x86)\LOVE\love.exe" (
    set "LOVE2D_FOUND=1"
    echo ✅ Love2D trouvé dans Program Files (x86)
)

if "%LOVE2D_FOUND%"=="0" (
    echo ⚠️  Love2D non détecté automatiquement
    echo.
    echo 💡 Si Love2D n'est pas installé, téléchargez-le depuis :
    echo    https://love2d.org/
    echo.
    echo    Après installation, vous pourrez lancer le projet avec START.bat
)

echo.
echo 5️⃣  Configuration de l'environnement de développement...

REM Configurer l'environnement Python si le script existe
if exist "dev\configure_python_env.py" (
    echo 🐍 Configuration de l'environnement Python...
    
    REM Chercher Python
    python --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        python dev\configure_python_env.py
        echo ✅ Environnement Python configuré
    ) else (
        echo ⚠️  Python non trouvé - configuration manuelle requise
    )
) else (
    echo ℹ️  Configuration Python non disponible (version simplifiée)
)

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    MISE À JOUR TERMINÉE !                    ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo ✅ Projet mis à jour avec succès
echo 💾 Vos données sont sauvegardées dans : %BACKUP_DIR%
echo.
echo 🚀 Pour lancer le projet :
echo    • Double-cliquez sur START.bat
echo    • Ou lancez Love2D avec le dossier du projet
echo.
echo 🛠️  Pour le développement :
echo    • Scripts disponibles dans le dossier dev/
echo    • Documentation dans GUIDE_ENVIRONNEMENT_PYTHON.md
echo.

echo Appuyez sur une touche pour fermer...
pause >nul
