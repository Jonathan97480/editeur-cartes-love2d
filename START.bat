@echo off
title Editeur de cartes Love2D - Lancement
color 0A
cls

echo ================================================================
echo               EDITEUR DE CARTES LOVE2D
echo                    Version GitHub
echo ================================================================
echo.
echo 🎮 MODES DE LANCEMENT
echo.
echo   [1] Lancer éditeur Python (Mode Edition)
echo   [2] Menu développeur (Scripts dev/)
echo   [U] Mise à jour automatique (UPDATE.bat)
echo   [H] Aide et documentation
echo   [Q] Quitter
echo.

:choice
set /p choice="Votre choix : "

if /i "%choice%"=="1" (
    cls  
    echo 🐍 Lancement de l'éditeur Python...
    echo.
    if exist "dev\run_app.bat" (
        call dev\run_app.bat
    ) else (
        python app_final.py
    )
    goto end
)
if /i "%choice%"=="2" (
    cls
    echo 🛠️ Menu développeur...
    echo.
    if exist "dev\git.bat" (
        call dev\git.bat
    ) else (
        echo ❌ Scripts de développement non trouvés dans dev/
        pause
    )
    goto end
)
if /i "%choice%"=="u" (
    cls
    echo 🔄 Mise à jour automatique...
    echo.
    if exist "UPDATE.bat" (
        call UPDATE.bat
    ) else (
        echo ❌ Script UPDATE.bat non trouvé
        pause
    )
    goto end
)
if /i "%choice%"=="h" (
    echo.
    echo 📖 Ouverture de la documentation...
    if exist "README_GITHUB.md" (
        start notepad README_GITHUB.md
    ) else if exist "README.md" (
        start notepad README.md
    ) else (
        echo ❌ Documentation non trouvée
    )
    goto choice
)
if /i "%choice%"=="q" goto quit

echo.
echo ❌ Choix invalide. Veuillez sélectionner 1, 2, U, H ou Q.
echo.
goto choice

:quit
echo.
echo 👋 Au revoir !
exit /b 0

:end
echo.
echo ✅ Terminé. Retour au menu principal.
pause
cls
goto choice
