@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo 🔒 TEST RAPIDE DU SYSTÈME DE SÉCURITÉ
echo ======================================

REM Détecter l'environnement Python
set "PYTHON_EXE="
if exist "C:\Users\berou\AppData\Local\NVIDIA\ChatWithRTX\env_nvd_rag\python.exe" (
    set "PYTHON_EXE=C:\Users\berou\AppData\Local\NVIDIA\ChatWithRTX\env_nvd_rag\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo 🐍 Python: !PYTHON_EXE!

REM S'assurer que le dossier reports existe
if not exist "commit_reports" mkdir "commit_reports"

echo 📁 Test rapide des composants critiques...

echo.
echo ✅ Test syntaxe Python...
"%PYTHON_EXE%" -m py_compile app_final.py >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur syntaxe Python
    set "TEST_FAILED=1"
) else (
    echo ✅ Syntaxe Python OK
)

echo.
echo ✅ Test application principale...
"%PYTHON_EXE%" app_final.py --test >nul 2>&1
if errorlevel 1 (
    echo ❌ Application principale échoue
    set "TEST_FAILED=1"
) else (
    echo ✅ Application principale OK
)

echo.
echo ✅ Test base de données...
if exist "cartes.db" (
    echo ✅ Base de données présente
) else (
    echo ❌ Base de données manquante
    set "TEST_FAILED=1"
)

echo.
echo ✅ Test structure projet...
if exist "lib" if exist "lang" if exist "config" (
    echo ✅ Structure projet OK
) else (
    echo ❌ Structure projet incomplète
    set "TEST_FAILED=1"
)

echo.
echo 🧪 Test complet application (simulation utilisateur)...
"%PYTHON_EXE%" dev\test_application_complete.py >nul 2>&1
if errorlevel 1 (
    echo ❌ Test complet application échoué
    set "TEST_FAILED=1"
) else (
    echo ✅ Test complet application OK
)

echo.
echo 🎯 RÉSULTAT FINAL
echo ================
if "%TEST_FAILED%"=="1" (
    echo ❌ DES PROBLÈMES DÉTECTÉS
    echo ⚠️  Corrigez les erreurs avant de commiter
    exit /b 1
) else (
    echo ✅ TOUS LES TESTS PASSENT
    echo 🚀 Système prêt pour commit sécurisé
    exit /b 0
)
