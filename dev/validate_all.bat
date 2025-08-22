@echo off
echo ================================
echo VALIDATION COMPLETE DU PROJET
echo ================================
echo.

echo 1. Test de l'environnement Python...
"C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe" configure_python_env.py
echo.

echo 2. Lancement des tests du projet...
"C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe" app_final.py --test
echo.

echo 3. Verification de l'organisation...
echo Structure des dossiers:
if exist "data" echo   ✓ data/
if exist "logs" echo   ✓ logs/  
if exist "tests" echo   ✓ tests/
if exist "docs" echo   ✓ docs/
if exist "guides" echo   ✓ guides/
echo.

echo 4. Verification des scripts de lancement...
if exist "run_app.bat" echo   ✓ run_app.bat
if exist "run_tests.bat" echo   ✓ run_tests.bat  
if exist "run_organize.bat" echo   ✓ run_organize.bat
echo.

echo ================================
echo VALIDATION TERMINEE
echo ================================
echo.
echo Le projet est pret a l'utilisation !
echo.
pause
