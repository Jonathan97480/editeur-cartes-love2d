@echo off
echo ===========================================
echo    ANALYSEUR AUTOMATIQUE D'EXPORT LUA
echo ===========================================
echo.
echo Ce script va:
echo   1. Ouvrir automatiquement l'application
echo   2. Vous permettre d'exporter vos cartes  
echo   3. Analyser le fichier automatiquement
echo.
echo Appuyez sur une touche pour continuer...
pause > nul
echo.

python auto_export_analyzer.py

echo.
echo ===========================================
echo Appuyez sur une touche pour fermer...
pause > nul
