@echo off
chcp 65001 > nul
title Configuration Sécurité Git

echo 🔒 CONFIGURATION SYSTÈME SÉCURITÉ GIT
echo =====================================
echo.

REM Configuration de l'environnement Python
set PYTHON_EXE=C:\Users\berou\AppData\Local\NVIDIA\ChatWithRTX\env_nvd_rag\python.exe

REM Vérification que Python existe
if not exist "%PYTHON_EXE%" (
    echo ❌ Python introuvable à %PYTHON_EXE%
    echo Utilisation du Python système...
    set PYTHON_EXE=python
)

echo 🐍 Python: %PYTHON_EXE%
echo 📁 Configuration hooks Git sécurisés...
echo.

echo 🔧 Installation des hooks Git avec sécurité...
"%PYTHON_EXE%" setup_secure_hooks.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ CONFIGURATION TERMINÉE AVEC SUCCÈS !
    echo.
    echo 🎯 Votre dépôt Git est maintenant sécurisé :
    echo    🧪 Tests automatiques avant chaque commit
    echo    🔒 Audit de sécurité complet
    echo    📄 Rapports détaillés dans commit_reports\
    echo    🛡️ Blocage automatique si problèmes détectés
    echo.
    echo 💡 Pour tester le système : dev\test_security.bat
    echo 🚀 Pour commiter : dev\git.bat commit "votre message"
) else (
    echo.
    echo ❌ ERREUR LORS DE LA CONFIGURATION
    echo    Vérifiez que vous êtes dans un dépôt Git valide
)

echo.
pause
