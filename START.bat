@echo off
:: Éditeur de Cartes Love2D - Lancement Principal
:: Version 2.4.0 - Réorganisé et optimisé

title Éditeur de Cartes Love2D v2.4.0

echo ===============================================
echo    Éditeur de Cartes Love2D v2.4.0
echo    Projet réorganisé et optimisé
echo ===============================================
echo.

:: Vérifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou accessible
    echo    Veuillez installer Python 3.8+ et redémarrer
    pause
    exit /b 1
)

:: Vérifier que le fichier principal existe
if not exist "app_final.py" (
    echo ❌ Fichier app_final.py introuvable
    echo    Assurez-vous d'être dans le bon répertoire
    pause
    exit /b 1
)

:: Lancer l'application
echo 🚀 Démarrage de l'éditeur de cartes...
python app_final.py

:: Gérer la sortie
if errorlevel 1 (
    echo.
    echo ❌ L'application s'est fermée avec une erreur
    echo    Consultez les logs ou essayez tools/DIAGNOSTIC.bat
    pause
) else (
    echo.
    echo ✅ Application fermée normalement
)

exit /b 0
