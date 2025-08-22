@echo off
REM Script Git amélioré avec environnement Python configuré
echo ================================
echo COMMIT AVEC ENVIRONNEMENT PYTHON
echo ================================

REM Définir le Python correct
set PYTHON_EXE=C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe

REM Vérifier que Python est disponible
if not exist "%PYTHON_EXE%" (
    echo ERREUR: Python non trouvé à %PYTHON_EXE%
    echo Utilisation du Python par défaut...
    set PYTHON_EXE=python
)

echo 📍 Utilisation de Python: %PYTHON_EXE%
echo.

REM Ajouter tous les fichiers modifiés
echo 📝 Ajout des fichiers modifiés...
git add .

REM Vérifier le statut
echo 📊 Statut du repository:
git status --short

echo.
REM Demander le message de commit
set /p commit_msg="💬 Message de commit: "

if "%commit_msg%"=="" (
    echo ❌ Message de commit requis
    pause
    exit /b 1
)

REM Faire le commit avec gestion d'erreur
echo.
echo 🚀 Création du commit...
git commit -m "%commit_msg%"

if %ERRORLEVEL% EQU 0 (
    echo ✅ Commit créé avec succès !
    
    REM Lancer les tests post-commit avec le bon Python
    echo.
    echo 🧪 Validation post-commit...
    "%PYTHON_EXE%" app_final.py --test
    
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Tous les tests passent !
    ) else (
        echo ⚠️  Certains tests ont des problèmes
    )
) else (
    echo ❌ Erreur lors du commit
)

echo.
echo ================================
pause
