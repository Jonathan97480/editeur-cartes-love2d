@echo off
color 0A
echo.
echo    ╔══════════════════════════════════════════════════════════╗
echo    ║              SYSTÈME D'ANALYSE AUTOMATIQUE              ║
echo    ║                    EXPORT LUA LOVE2D                    ║
echo    ╚══════════════════════════════════════════════════════════╝
echo.
echo  🎯 CE SYSTÈME VA :
echo.
echo     1. Ouvrir automatiquement votre application
echo     2. Vous permettre d'exporter vos cartes  
echo     3. Détecter quand vous fermez l'application
echo     4. Analyser automatiquement le fichier exporté
echo     5. Créer une version corrigée avec formatage Love2D
echo.
echo  📁 RÉSULTATS DANS : result_export_lua/
echo.
echo     - cards_joueur_exported.lua   (original de l'app)
echo     - cards_joueur_CORRECTED.lua  (version avec formatage)
echo     - GUIDE_UTILISATION.md        (documentation)
echo.
echo  ⚠️  IMPORTANT : Mettez le fichier exporté dans result_export_lua/
echo     quand l'application vous le demande !
echo.
echo.
set /p choice="Voulez-vous continuer ? (O/N) : "
if /i "%choice%"=="O" goto start
if /i "%choice%"=="Y" goto start
goto end

:start
echo.
echo  🚀 Lancement du système d'analyse...
echo.
python auto_export_analyzer.py
goto end

:end
echo.
echo  Appuyez sur une touche pour fermer...
pause > nul
