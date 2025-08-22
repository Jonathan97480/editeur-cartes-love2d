@echo off
REM Script Git push amélioré avec tests
echo ================================
echo PUSH GIT AVEC VALIDATION
echo ================================

REM Définir le Python correct
set PYTHON_EXE=C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe

echo 📍 Utilisation de Python: %PYTHON_EXE%
echo.

echo 🧪 Validation avant push...
"%PYTHON_EXE%" app_final.py --test

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Tests échoués - Push annulé
    echo Corrigez les tests avant de push
    pause
    exit /b 1
)

echo ✅ Tests OK - Proceeding avec le push...
echo.

echo 📤 Push vers origin...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo ✅ Push réussi !
    
    echo.
    echo 📊 Status après push:
    git status
) else (
    echo ❌ Erreur lors du push
    echo Vérifiez votre connexion et vos permissions
)

echo.
echo ================================
pause
