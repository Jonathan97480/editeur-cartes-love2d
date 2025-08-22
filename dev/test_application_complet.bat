@echo off
chcp 65001 > nul
title Test Complet Application - Simulation Utilisateur

echo 🧪 TEST COMPLET DE L'APPLICATION
echo =================================
echo 📋 Simulation complète d'un utilisateur utilisant l'application
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
echo 📁 Dossier projet: %CD%
echo.

echo 🚀 Lancement du test complet...
echo.
echo 📝 Ce test va:
echo    1. ✅ Charger les données de référence
echo    2. ✅ Créer une carte avec formatage
echo    3. ✅ Tester l'éditeur de formatage de texte
echo    4. ✅ Vérifier le chargement d'image
echo    5. ✅ Tester la sauvegarde des paramètres
echo    6. ✅ Exporter en Lua avec formatage
echo    7. ✅ Vérifier l'intégrité en base de données
echo    8. ✅ Nettoyer les données de test
echo.

REM Passer au dossier parent pour exécuter le test
cd ..

"%PYTHON_EXE%" dev\test_application_complete.py

set TEST_RESULT=%ERRORLEVEL%

echo.
echo 🎯 RÉSULTAT DU TEST
echo ==================

if %TEST_RESULT% == 0 (
    echo ✅ ✅ ✅ TEST COMPLET RÉUSSI ! ✅ ✅ ✅
    echo.
    echo 🎉 L'application fonctionne parfaitement :
    echo    📱 Interface utilisateur : OK
    echo    🗄️  Base de données : OK
    echo    🎨 Éditeur de formatage : OK
    echo    🖼️  Chargement d'images : OK
    echo    💾 Sauvegarde : OK
    echo    🚀 Export Lua : OK
    echo    🧹 Nettoyage : OK
    echo.
    echo 🚀 Application prête pour utilisation !
) else (
    echo ❌ ❌ ❌ TEST COMPLET ÉCHOUÉ ❌ ❌ ❌
    echo.
    echo 🚨 Problèmes détectés dans l'application
    echo 💡 Vérifiez les logs ci-dessus pour plus de détails
    echo.
    echo 🔧 Actions recommandées :
    echo    1. Vérifier la base de données
    echo    2. Contrôler les dépendances Python
    echo    3. Valider la structure des fichiers
    echo    4. Tester les modules individuellement
)

echo.
echo 📋 Informations système :
echo    🐍 Python : %PYTHON_EXE%
echo    📁 Dossier : %CD%
echo    ⏰ Date : %DATE% %TIME%

echo.
pause
