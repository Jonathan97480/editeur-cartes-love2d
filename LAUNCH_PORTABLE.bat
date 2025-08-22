@echo off
title Éditeur de cartes Love2D - Lancement Portable
color 0A
echo.
echo ================================================================
echo               ÉDITEUR DE CARTES LOVE2D
echo                    Version Portable
echo ================================================================
echo.

REM Vérifier si nous sommes dans le bon répertoire
if not exist "app_final.py" (
    echo ❌ ERREUR: Fichier app_final.py non trouvé
    echo 📍 Assurez-vous d'être dans le répertoire du projet
    echo.
    pause
    exit /b 1
)

echo 🔍 Détection de Python...
echo.

REM Méthode 1: Python dans le PATH
where python >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Python détecté dans le PATH système
    echo 🚀 Lancement de l'éditeur...
    echo.
    python app_final.py
    goto :end
)

REM Méthode 2: py launcher (Windows 10+)
where py >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Python Launcher détecté
    echo 🚀 Lancement de l'éditeur...
    echo.
    py app_final.py
    goto :end
)

REM Méthode 3: Emplacements standards Windows
echo 🔍 Recherche dans les emplacements standards...

set PYTHON_FOUND=0

for %%P in (
    "C:\Python3\python.exe"
    "C:\Python39\python.exe" 
    "C:\Python310\python.exe"
    "C:\Python311\python.exe"
    "C:\Python312\python.exe"
    "C:\Program Files\Python39\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files (x86)\Python39\python.exe"
    "C:\Program Files (x86)\Python310\python.exe"
    "C:\Program Files (x86)\Python311\python.exe"
    "C:\Program Files (x86)\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
) do (
    if exist %%P (
        echo ✅ Python trouvé: %%P
        echo 🚀 Lancement de l'éditeur...
        echo.
        %%P app_final.py
        set PYTHON_FOUND=1
        goto :end
    )
)

REM Si aucun Python trouvé
if %PYTHON_FOUND%==0 (
    echo.
    echo ❌ ERREUR: Python non trouvé sur ce système !
    echo.
    echo 💡 SOLUTIONS:
    echo    1. Téléchargez Python depuis: https://python.org/downloads/
    echo    2. Lors de l'installation, cochez "Add Python to PATH"
    echo    3. Redémarrez ce script après installation
    echo.
    echo 🔧 INSTALLATION RECOMMANDÉE:
    echo    - Python 3.9 ou plus récent
    echo    - Cocher "Add Python to PATH" pendant l'installation
    echo    - Redémarrer l'ordinateur après installation
    echo.
)

:end
echo.
echo 📝 Session terminée.
pause
