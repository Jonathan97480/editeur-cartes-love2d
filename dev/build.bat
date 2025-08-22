@echo off
setlocal
set NAME=EditeurCartesLove2D
set SCRIPT=test.py
set ICON=icon.ico
set VENV_DIR=%~dp0venv
set REQUIREMENTS=%~dp0requirements.txt

echo ========================================
echo   Build Editeur de Cartes Love2D
echo ========================================

REM Verification de Python
where python >nul 2>nul || where py >nul 2>nul || (
  echo [ERREUR] Python introuvable. Installez-le depuis https://www.python.org/
  pause
  exit /b 1
)

REM Creation de l'environnement virtuel s'il n'existe pas
if not exist "%VENV_DIR%" (
  echo Creation de l'environnement virtuel pour le build...
  python -m venv "%VENV_DIR%" 2>nul || py -m venv "%VENV_DIR%" || (
    echo [ERREUR] Impossible de creer l'environnement virtuel.
    pause
    exit /b 1
  )
)

REM Activation de l'environnement virtuel
call "%VENV_DIR%\Scripts\activate.bat" || (
  echo [ERREUR] Impossible d'activer l'environnement virtuel.
  pause
  exit /b 1
)

REM Mise a jour de pip
python -m pip install --upgrade pip >nul 2>nul

REM Installation des dependances
if exist "%REQUIREMENTS%" (
  echo Installation des dependances...
  pip install -r "%REQUIREMENTS%"
) else (
  echo Installation manuelle de Pillow...
  pip install Pillow
)

REM Installation de PyInstaller
echo Installation de PyInstaller...
pip install --upgrade pyinstaller || (
  echo [ERREUR] Echec de l'installation de PyInstaller.
  pause
  exit /b 1
)

REM Nettoyage des builds precedents
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Configuration de l'icone
if exist "%ICON%" (
  set ICON_ARG=--icon "%ICON%"
) else (
  set ICON_ARG=
)

REM Build interface graphique
echo Build de l'executable avec interface graphique...
pyinstaller --noconfirm --windowed --name "%NAME%" %ICON_ARG% --add-data "lib;lib" "%SCRIPT%" || (
  echo [ERREUR] Echec du build GUI.
  pause
  exit /b 1
)

REM Build console
echo Build de l'executable console...
pyinstaller --noconfirm --onefile --name "%NAME%_console" --add-data "lib;lib" "%SCRIPT%" || (
  echo [ERREUR] Echec du build console.
  pause
  exit /b 1
)

echo.
echo ========================================
echo   Build termine avec succes !
echo ========================================
echo Executables disponibles dans le dossier 'dist':
echo - %NAME%.exe (interface graphique)
echo - %NAME%_console.exe (console)
echo.

REM Desactivation de l'environnement virtuel
deactivate 2>nul

pause
