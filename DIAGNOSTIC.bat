@echo off
setlocal enabledelayedexpansion
title Diagnostic système - Éditeur de cartes Love2D
color 0B
cls

echo ================================================================
echo             DIAGNOSTIC SYSTÈME - ÉDITEUR LOVE2D
echo ================================================================
echo.

echo 🔍 Vérification de l'environnement système...
echo.

set ERROR_FOUND=0

REM Vérification du répertoire
echo [1/6] 📁 Vérification des fichiers du projet...
if exist "app_final.py" (
    echo     ✅ app_final.py trouvé
) else (
    echo     ❌ app_final.py manquant !
    set ERROR_FOUND=1
)

if exist "data\cartes.db" (
    echo     ✅ Base de données trouvée
) else (
    echo     ❌ Base de données manquante !
    set ERROR_FOUND=1
)

if exist "lib\" (
    echo     ✅ Dossier lib/ trouvé
) else (
    echo     ❌ Dossier lib/ manquant !
    set ERROR_FOUND=1
)

echo.

REM Vérification de Python
echo [2/6] 🐍 Vérification de Python...
where python >nul 2>&1
if %errorlevel%==0 (
    echo     ✅ Python trouvé dans le PATH
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo     📋 Version: !PYTHON_VERSION!
) else (
    echo     ❌ Python non trouvé dans le PATH
    set ERROR_FOUND=1
    
    REM Recherche manuelle
    echo     🔍 Recherche dans les emplacements standards...
    set PYTHON_MANUAL=0
    for %%P in (
        "C:\Python3\python.exe"
        "C:\Python39\python.exe" 
        "C:\Python310\python.exe"
        "C:\Python311\python.exe"
        "C:\Python312\python.exe"
    ) do (
        if exist %%P (
            echo     ⚠️  Python trouvé manuellement: %%P
            set PYTHON_MANUAL=1
        )
    )
    
    if !PYTHON_MANUAL!==0 (
        echo     ❌ Aucune installation Python détectée
    )
)

echo.

REM Vérification des modules Python
echo [3/6] 📦 Vérification des modules Python...
if %errorlevel%==0 (
    python -c "import tkinter; print('     ✅ tkinter disponible')" 2>nul || echo      ❌ tkinter manquant
    python -c "import sqlite3; print('     ✅ sqlite3 disponible')" 2>nul || echo      ❌ sqlite3 manquant
    python -c "import sys; print('     📋 Python path:', sys.executable)" 2>nul
) else (
    echo     ⚠️  Tests ignorés (Python non accessible)
)

echo.

REM Vérification de la configuration système
echo [4/6] ⚙️ Configuration système...
echo     💻 OS: %OS%
echo     🏷️  Utilisateur: %USERNAME%
echo     📍 Répertoire: %CD%
if defined PYTHONPATH (
    echo     🐍 PYTHONPATH: %PYTHONPATH%
) else (
    echo     🐍 PYTHONPATH: Non défini
)

echo.

REM Test de lancement
echo [5/6] 🚀 Test de lancement...
if exist "app_final.py" (
    if %errorlevel%==0 (
        echo     🔄 Test d'import des modules...
    python -c "
import sys
sys.path.insert(0, 'lib')
try:
    from config import DB_FILE
    print('     ✅ Configuration chargée')
    from database import CardRepo
    print('     ✅ Base de données accessible')
    from ui_components import CardListApp
    print('     ✅ Interface utilisateur prête')
    print('     🎯 Application prête au lancement')
except ImportError as e:
    print('     ❌ Module manquant:', str(e))
except Exception as e:
    print('     ❌ Erreur:', str(e))
" 2>nul
    ) else (
        echo     ⚠️  Test ignoré (Python non accessible)
    )
) else (
    echo     ❌ Impossible de tester (app_final.py manquant)
)

echo.

REM Résumé et recommandations
echo [6/6] 📊 Résumé et recommandations...
if defined ERROR_FOUND (
    echo     ⚠️  PROBLÈMES DÉTECTÉS
    echo.
    echo     💡 SOLUTIONS RECOMMANDÉES:
    echo        1. Installez Python depuis https://python.org
    echo        2. Cochez "Add Python to PATH" lors de l'installation
    echo        3. Redémarrez votre ordinateur
    echo        4. Utilisez LAUNCH_PORTABLE.bat pour lancer
    echo.
) else (
    echo     ✅ SYSTÈME PRÊT
    echo        Vous pouvez lancer l'éditeur avec START.bat ou LAUNCH_PORTABLE.bat
    echo.
)

echo ================================================================
echo                        DIAGNOSTIC TERMINÉ
echo ================================================================
echo.
echo 📝 Pour plus d'aide, consultez INSTALLATION_GUIDE.md
echo.
pause
