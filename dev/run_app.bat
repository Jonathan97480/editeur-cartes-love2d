@echo off
title Éditeur de cartes Love2D - Lancement
echo 🐍 Lancement de l'éditeur de cartes Love2D...
echo.

REM Détecter Python automatiquement
where python >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Python détecté dans le PATH
    python app_final.py %*
) else (
    echo ❌ Python non trouvé dans le PATH
    echo 🔍 Recherche de Python dans les emplacements courants...
    
    REM Essayer quelques emplacements courants
    if exist "C:\Python3\python.exe" (
        echo ✅ Python trouvé: C:\Python3\python.exe
        "C:\Python3\python.exe" app_final.py %*
    ) else if exist "C:\Python39\python.exe" (
        echo ✅ Python trouvé: C:\Python39\python.exe
        "C:\Python39\python.exe" app_final.py %*
    ) else if exist "C:\Python310\python.exe" (
        echo ✅ Python trouvé: C:\Python310\python.exe
        "C:\Python310\python.exe" app_final.py %*
    ) else if exist "C:\Python311\python.exe" (
        echo ✅ Python trouvé: C:\Python311\python.exe
        "C:\Python311\python.exe" app_final.py %*
    ) else if exist "C:\Python312\python.exe" (
        echo ✅ Python trouvé: C:\Python312\python.exe
        "C:\Python312\python.exe" app_final.py %*
    ) else (
        echo.
        echo ❌ ERREUR: Python non trouvé !
        echo.
        echo 💡 SOLUTIONS:
        echo    1. Installez Python depuis https://python.org
        echo    2. Ajoutez Python au PATH de Windows
        echo    3. Ou modifiez ce script avec votre chemin Python
        echo.
        echo 📍 Votre script: %~dp0%~nx0
        echo.
    )
)

echo.
pause
