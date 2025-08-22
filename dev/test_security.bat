@echo off
chcp 65001 > nul
title Test Système Sécurité Pré-Commit

echo 🔒 TEST DU SYSTÈME DE SÉCURITÉ PRÉ-COMMIT
echo ============================================
echo.

REM Configuration de l'environnement Python
set PYTHON_EXE=C:\Users\berou\AppData\Local\NVIDIA\ChatWithRTX\env_nvd_rag\python.exe

REM Vérification que Python existe
if not exist "%PYTHON_EXE%" (
    echo ❌ Python introuvable à %PYTHON_EXE%
    echo Utilisation du Python système...
    set PYTHON_EXE=python
)

echo 🐍 Python: %PYTHON_EXE%
echo 📁 Dossier rapports: commit_reports\
echo.

echo 🚀 Lancement du test de sécurité...
echo.

"%PYTHON_EXE%" pre_commit_security.py

echo.
echo 📋 Test terminé. Vérifiez les rapports dans commit_reports\
echo.

if exist commit_reports\*.md (
    echo 📄 Rapports générés:
    dir commit_reports\*.md /B
    echo.
    echo 💡 Ouvrir le dernier rapport Markdown ?
    set /p open="(O/N): "
    if /i "%open%"=="O" (
        for /f %%i in ('dir commit_reports\commit_report_*.md /B /O:D') do set "LATEST=%%i"
        if defined LATEST (
            start notepad commit_reports\!LATEST!
        )
    )
)

pause
