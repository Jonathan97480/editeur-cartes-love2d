@echo off
echo.
echo 🔧 LANCEMENT AVEC PANNEAU REDIMENSIONNABLE
echo ==========================================
echo.

echo 🛑 Arrêt de tous les processus Python...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

echo ⏱️  Attente de 2 secondes...
timeout /t 2 /nobreak >nul

echo 🧹 Nettoyage du cache Python...
if exist "__pycache__" rmdir /s /q "__pycache__" >nul 2>&1
if exist "lib\__pycache__" rmdir /s /q "lib\__pycache__" >nul 2>&1

echo 🎯 Lancement de l'application avec panneau redimensionnable...
echo.
echo ✅ NOUVELLES FONCTIONNALITÉS:
echo    • Panneau de contrôles redimensionnable
echo    • Sliders adaptatifs (150-300px)
echo    • Séparateur glissant entre panneaux
echo    • Interface plus flexible
echo.

python app_final.py

echo.
echo 🏁 Application fermée
pause
