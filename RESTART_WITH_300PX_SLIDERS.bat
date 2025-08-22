@echo off
echo.
echo 🔄 REDÉMARRAGE AVEC SLIDERS 300PX
echo =====================================
echo.

echo 🛑 Arrêt de tous les processus Python...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

echo ⏱️  Attente de 2 secondes...
timeout /t 2 /nobreak >nul

echo 🧹 Nettoyage du cache Python...
if exist "__pycache__" rmdir /s /q "__pycache__" >nul 2>&1
if exist "lib\__pycache__" rmdir /s /q "lib\__pycache__" >nul 2>&1

echo 🚀 Lancement de l'application avec les nouveaux sliders...
echo.
echo ✅ Les sliders sont maintenant limités à 300px de longueur visuelle
echo ✅ La plage fonctionnelle reste complète (0-470px pour Y)
echo.

python app_final.py

echo.
echo 🏁 Application fermée
pause
