@echo off
chcp 65001 > nul
title Validation Complète avec Test Application

echo 🔍 VALIDATION COMPLÈTE DU PROJET
echo =================================
echo 📋 Tests de sécurité + Test complet application
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
echo.

echo 🚀 ÉTAPE 1 : Test de sécurité système
echo =======================================
call test_quick_security.bat
set SECURITY_RESULT=%ERRORLEVEL%

echo.
echo 🧪 ÉTAPE 2 : Test complet application
echo ====================================
call test_application_complet.bat
set APP_RESULT=%ERRORLEVEL%

echo.
echo 🎯 RÉSULTATS FINAUX
echo ==================

if %SECURITY_RESULT% == 0 (
    echo ✅ Tests de sécurité : RÉUSSIS
) else (
    echo ❌ Tests de sécurité : ÉCHOUÉS
)

if %APP_RESULT% == 0 (
    echo ✅ Test complet application : RÉUSSI
) else (
    echo ❌ Test complet application : ÉCHOUÉ
)

echo.
echo 📊 BILAN GLOBAL
echo ==============

if %SECURITY_RESULT% == 0 if %APP_RESULT% == 0 (
    echo 🎉 ✅ ✅ ✅ VALIDATION COMPLÈTE RÉUSSIE ! ✅ ✅ ✅
    echo.
    echo 🚀 Le projet est prêt pour :
    echo    📝 Commit sécurisé
    echo    🚀 Déploiement
    echo    👥 Partage avec les utilisateurs
    echo    🎮 Utilisation en production
    echo.
    echo 💯 Tous les composants sont validés :
    echo    🔒 Sécurité système : OK
    echo    🧪 Tests fonctionnels : OK  
    echo    📱 Interface utilisateur : OK
    echo    🗄️  Base de données : OK
    echo    🎨 Éditeur de formatage : OK
    echo    🚀 Export Lua : OK
) else (
    echo ❌ ❌ ❌ VALIDATION ÉCHOUÉE ❌ ❌ ❌
    echo.
    echo 🚨 Problèmes détectés - Actions requises :
    
    if not %SECURITY_RESULT% == 0 (
        echo    🔒 Corriger les problèmes de sécurité
        echo    📋 Vérifier la structure du projet
        echo    🐍 Valider l'environnement Python
    )
    
    if not %APP_RESULT% == 0 (
        echo    🧪 Réparer les fonctionnalités de l'application
        echo    🗄️  Vérifier la base de données
        echo    🎨 Contrôler l'éditeur de formatage
    )
    
    echo.
    echo 💡 Exécutez les tests individuellement pour plus de détails
)

echo.
echo 📋 Informations :
echo    ⏰ Date : %DATE% %TIME%
echo    📁 Dossier : %CD%
echo    🐍 Python : %PYTHON_EXE%

echo.
pause
