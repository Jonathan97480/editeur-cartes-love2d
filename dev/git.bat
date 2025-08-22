@echo off
chcp 65001 > nul
title Gestionnaire Git

REM Configuration de l'environnement Python
set PYTHON_EXE=C:\Users\berou\AppData\Local\NVIDIA\ChatWithRTX\env_nvd_rag\python.exe

REM Vérification que Python existe
if not exist "%PYTHON_EXE%" (
    echo ❌ Python introuvable à %PYTHON_EXE%
    echo Utilisation du Python système...
    set PYTHON_EXE=python
)

echo 🔧 Lancement du gestionnaire Git...
echo 🐍 Python: %PYTHON_EXE%
echo.

REM Lancement du gestionnaire Git
"%PYTHON_EXE%" git_manager.py %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erreur lors de l'exécution
    pause
)
