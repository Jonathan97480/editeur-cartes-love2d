@echo off
REM Script Git status amélioré
echo ================================
echo STATUS GIT AVEC ENVIRONNEMENT
echo ================================

REM Définir le Python correct
set PYTHON_EXE=C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe

echo 📍 Repository: %CD%
echo 📍 Python: %PYTHON_EXE%
echo.

echo 📊 Statut du repository:
git status

echo.
echo 📋 Derniers commits:
git log --oneline -5

echo.
echo 🏷️  Branches:
git branch -a

echo.
echo 📦 Fichiers modifiés récemment:
git diff --name-only HEAD~1 HEAD

echo.
echo ================================
pause
