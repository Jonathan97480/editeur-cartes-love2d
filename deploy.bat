@echo off
echo 🚀 DÉPLOIEMENT AVEC TESTS
echo ========================
echo 1️⃣ Tests pré-déploiement...
python validate_tests_auto.py
if %errorlevel% neq 0 (
    echo ❌ Tests échoués - Déploiement annulé
    pause
    exit /b 1
)
echo ✅ Tests OK - Déploiement autorisé
echo.
echo 2️⃣ Créer un commit ?
set /p commit_msg="Message de commit (ou ENTER pour annuler) : "
if "%commit_msg%"=="" (
    echo Déploiement annulé
    pause
    exit /b 0
)
echo.
echo 3️⃣ Commit en cours...
git add .
git commit -m "%commit_msg%"
echo ✅ Commit terminé !
pause
