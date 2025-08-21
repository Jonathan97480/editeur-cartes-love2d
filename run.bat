@echo off
setlocal
SET SCRIPT=%~dp0test.py
SET VENV_DIR=%~dp0venv
SET REQUIREMENTS=%~dp0requirements.txt

echo ========================================
echo   Editeur de Cartes Love2D - Launcher
echo ========================================

REM Verification de Python
where python >nul 2>nul || where py >nul 2>nul || (
  echo [ERREUR] Python introuvable. Installez-le depuis https://www.python.org/
  echo Assurez-vous d'ajouter Python au PATH lors de l'installation.
  pause
  exit /b 1
)

REM Creation de l'environnement virtuel s'il n'existe pas
if not exist "%VENV_DIR%" (
  echo Creation de l'environnement virtuel...
  python -m venv "%VENV_DIR%" 2>nul || (
    echo Tentative avec py...
    py -m venv "%VENV_DIR%" || (
      echo [ERREUR] Impossible de creer l'environnement virtuel.
      pause
      exit /b 1
    )
  )
  echo Environnement virtuel cree avec succes.
)

REM Activation de l'environnement virtuel
echo Activation de l'environnement virtuel...
call "%VENV_DIR%\Scripts\activate.bat" || (
  echo [ERREUR] Impossible d'activer l'environnement virtuel.
  pause
  exit /b 1
)

REM Mise a jour de pip
echo Mise a jour de pip...
python -m pip install --upgrade pip >nul 2>nul

REM Installation des dependances si requirements.txt existe
if exist "%REQUIREMENTS%" (
  echo Installation des dependances...
  pip install -r "%REQUIREMENTS%" || (
    echo [ERREUR] Echec de l'installation des dependances.
    pause
    exit /b 1
  )
  echo Dependances installees avec succes.
) else (
  echo Installation manuelle de Pillow...
  pip install Pillow || (
    echo [ERREUR] Echec de l'installation de Pillow.
    pause
    exit /b 1
  )
)

REM Lancement de l'application
echo Lancement de l'application...
echo.
python "%SCRIPT%" %*

REM En cas d'erreur, afficher un message et attendre
if errorlevel 1 (
  echo.
  echo [ERREUR] L'application s'est fermee de maniere inattendue.
  echo Tentative de lancement en mode compatibilite...
  echo.
  python "%~dp0test_compat.py" --compat
  if errorlevel 1 (
    echo.
    echo [ERREUR] Echec du mode compatibilite.
    echo Verifiez que tous les modules sont presents dans le dossier lib/
    pause
  )
)

REM Desactivation de l'environnement virtuel
deactivate 2>nul
