@echo off
chcp 65001 > nul
title Éditeur de cartes Love2D - Lancement automatique

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                  LANCEMENT AUTOMATIQUE                       ║
echo ║              Éditeur de cartes Love2D                        ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Configuration
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%venv"
set "PYTHON_EXE=python"

echo 🔍 Vérification de l'environnement...

REM Vérifier si Python est installé
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python n'est pas installé ou non accessible
    echo.
    echo 💡 Veuillez installer Python depuis : https://python.org/
    echo    Assurez-vous de cocher "Add Python to PATH" lors de l'installation
    pause
    exit /b 1
)

echo ✅ Python détecté

echo.
echo 📦 PRÉPARATION DE L'ENVIRONNEMENT
echo ================================

REM Créer l'environnement virtuel s'il n'existe pas
if not exist "%VENV_DIR%" (
    echo 🔧 Création de l'environnement virtuel...
    python -m venv "%VENV_DIR%"
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Échec de création de l'environnement virtuel
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé
) else (
    echo ✅ Environnement virtuel déjà présent
)

REM Activer l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call "%VENV_DIR%\Scripts\activate.bat"
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Problème d'activation, utilisation de Python système
    set "PYTHON_EXE=python"
) else (
    echo ✅ Environnement virtuel activé
    set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"
)

REM Installer/Mettre à jour les dépendances
echo 🔧 Vérification des dépendances...
if exist "requirements.txt" (
    echo 📋 Installation des dépendances depuis requirements.txt...
    "%PYTHON_EXE%" -m pip install --upgrade pip >nul 2>&1
    "%PYTHON_EXE%" -m pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo ⚠️  Certaines dépendances ont échoué, continuons...
    ) else (
        echo ✅ Dépendances installées
    )
) else (
    echo 📋 Installation des dépendances essentielles...
    "%PYTHON_EXE%" -m pip install --upgrade pip >nul 2>&1
    "%PYTHON_EXE%" -m pip install pillow
    if %ERRORLEVEL% NEQ 0 (
        echo ⚠️  Installation de Pillow échouée, fonctionnalités d'images limitées
    ) else (
        echo ✅ Pillow installé (traitement d'images)
    )
)

REM Vérifier les modules critiques
echo 🧪 Vérification des modules...
"%PYTHON_EXE%" -c "import tkinter; print('✅ Tkinter disponible')" 2>nul || echo "⚠️  Tkinter non disponible"
"%PYTHON_EXE%" -c "import PIL; print('✅ PIL/Pillow disponible')" 2>nul || echo "⚠️  PIL/Pillow non disponible"
"%PYTHON_EXE%" -c "import sqlite3; print('✅ SQLite3 disponible')" 2>nul || echo "⚠️  SQLite3 non disponible"

echo.
echo 🚀 LANCEMENT DE L'APPLICATION
echo =============================

REM Chercher le point d'entrée principal
if exist "app_final.py" (
    echo 🎮 Lancement de l'éditeur de cartes...
    "%PYTHON_EXE%" app_final.py
) else if exist "test.py" (
    echo 🎮 Lancement de l'éditeur de cartes...
    "%PYTHON_EXE%" test.py
) else if exist "main.py" (
    echo 🎮 Lancement de l'éditeur de cartes...
    "%PYTHON_EXE%" main.py
) else (
    echo ❌ Aucun point d'entrée trouvé
    echo.
    echo 💡 Fichiers recherchés :
    echo    - app_final.py
    echo    - test.py
    echo    - main.py
    echo.
    echo Veuillez vérifier l'installation du projet
    pause
    exit /b 1
)

REM Gérer la fermeture
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ L'application s'est fermée avec une erreur
    echo.
    echo 💡 Conseils de dépannage :
    echo    • Vérifiez que toutes les dépendances sont installées
    echo    • Consultez les messages d'erreur ci-dessus
    echo    • Essayez de relancer en tant qu'administrateur
    echo.
    pause
) else (
    echo.
    echo ✅ Application fermée normalement
)

echo.
echo 🎯 Pour plus d'aide, consultez le README.md
echo.
pause
