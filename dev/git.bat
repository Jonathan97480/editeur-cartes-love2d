@echo off
chcp 65001 > nul
title Gestionnaire Git avec Sécurité

REM Configuration de l'environnement Python
set PYTHON_EXE=C:\Users\berou\AppData\Local\NVIDIA\ChatWithRTX\env_nvd_rag\python.exe

REM Vérification que Python existe
if not exist "%PYTHON_EXE%" (
    echo ❌ Python introuvable à %PYTHON_EXE%
    echo Utilisation du Python système...
    set PYTHON_EXE=python
)

echo 🔧 Lancement du gestionnaire Git avec sécurité...
echo 🐍 Python: %PYTHON_EXE%
echo 🔒 Sécurité pré-commit activée
echo.

REM Lancement du gestionnaire Git avec sécurité
"%PYTHON_EXE%" git_manager.py %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erreur lors de l'exécution
    pause
)
