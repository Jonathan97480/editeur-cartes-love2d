@echo off
echo 🚀 SCRIPT DE PUBLICATION GITHUB
echo ================================
echo.
echo Ce script va vous aider à publier votre projet sur GitHub
echo.

echo 📋 ÉTAPES À SUIVRE :
echo.
echo 1. Créez d'abord un repository sur GitHub :
echo    - Allez sur https://github.com
echo    - Cliquez sur "New repository" (bouton vert +)
echo    - Nommez-le : editeur-cartes-love2d
echo    - Description : "Éditeur moderne de cartes Love2D avec interface française"
echo    - Laissez PUBLIC
echo    - NE PAS cocher "Add a README file"
echo    - Cliquez "Create repository"
echo.

set /p username="2. Entrez votre nom d'utilisateur GitHub : "
if "%username%"=="" (
    echo ❌ Nom d'utilisateur requis !
    pause
    exit /b 1
)

echo.
echo 3. Configuration du repository local...
git remote remove origin 2>nul
git remote add origin https://github.com/%username%/editeur-cartes-love2d.git

echo.
echo 4. Préparation des branches...
git branch -M main

echo.
echo 5. Publication sur GitHub...
echo ⚠️  Vous devrez peut-être entrer vos identifiants GitHub
echo    (utilisez un Personal Access Token comme mot de passe)
echo.

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🎉 SUCCÈS ! Votre projet est maintenant sur GitHub :
    echo 🔗 https://github.com/%username%/editeur-cartes-love2d
    echo.
    echo 📝 PROCHAINES ÉTAPES :
    echo    - Personnalisez la description sur GitHub
    echo    - Ajoutez des topics : love2d, python, tkinter, card-game
    echo    - Partagez votre projet !
) else (
    echo.
    echo ❌ Erreur lors de la publication
    echo 💡 Vérifiez :
    echo    - Que le repository existe sur GitHub
    echo    - Vos identifiants GitHub
    echo    - Votre connexion internet
)

echo.
pause
