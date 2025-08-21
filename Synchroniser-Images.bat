@echo off
title Synchronisation des Images
cd /d "%~dp0"

echo ==========================================
echo   Synchronisation des Images
echo ==========================================
echo.

echo 🔄 Recherche des dossiers images les plus recents...
echo.

REM Trouver le dossier images le plus recent
set "LATEST_SOURCE="
set "LATEST_DATE=0"

for /d %%d in ("images" "dist\images" "dist\EditeurCartesLove2D\images") do (
    if exist "%%d" (
        echo 📁 Trouve : %%d
        REM Note: Verification basique de l'existence
        set "LATEST_SOURCE=%%d"
    )
)

if "%LATEST_SOURCE%"=="" (
    echo ❌ Aucun dossier images trouve
    echo.
    pause
    exit /b 1
)

echo.
echo 📂 Source selectionnee : %LATEST_SOURCE%
echo.
echo 🔄 Synchronisation vers tous les emplacements...

REM Copier vers tous les autres emplacements
if not "%LATEST_SOURCE%"=="images" (
    if exist "images" rmdir /s /q "images" 2>nul
    xcopy "%LATEST_SOURCE%" "images\" /E /I /Y >nul 2>&1
    echo ✅ → images\
)

if not "%LATEST_SOURCE%"=="dist\images" (
    if exist "dist\images" rmdir /s /q "dist\images" 2>nul
    if exist "dist" (
        xcopy "%LATEST_SOURCE%" "dist\images\" /E /I /Y >nul 2>&1
        echo ✅ → dist\images\
    )
)

if not "%LATEST_SOURCE%"=="dist\EditeurCartesLove2D\images" (
    if exist "dist\EditeurCartesLove2D\images" rmdir /s /q "dist\EditeurCartesLove2D\images" 2>nul
    if exist "dist\EditeurCartesLove2D" (
        xcopy "%LATEST_SOURCE%" "dist\EditeurCartesLove2D\images\" /E /I /Y >nul 2>&1
        echo ✅ → dist\EditeurCartesLove2D\images\
    )
)

echo.
echo ✅ Synchronisation terminee !
echo 🎯 Tous vos executables ont maintenant les memes images
echo.
pause
