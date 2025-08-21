@echo off
echo ========================================
echo     SCRIPT DE COMMIT RAPIDE
echo ========================================
echo.

REM Vérifier si on est dans un dépôt Git
git status >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Ce n'est pas un dépôt Git valide!
    pause
    exit /b 1
)

echo État actuel du dépôt:
echo ----------------------
git status --short

echo.
echo Fichiers modifiés:
echo ------------------
git diff --name-only

echo.
set /p "message=Entrez votre message de commit: "

if "%message%"=="" (
    echo ERREUR: Message de commit requis!
    pause
    exit /b 1
)

echo.
echo Ajout de tous les fichiers modifiés...
git add .

echo.
echo Création du commit...
git commit -m "%message%"

echo.
echo Historique récent:
echo ------------------
git log --oneline -5

echo.
echo ✅ Commit créé avec succès!
echo.
echo Voulez-vous voir les détails du dernier commit? (O/N)
set /p "details="
if /i "%details%"=="O" (
    echo.
    echo Détails du commit:
    echo ==================
    git show --stat HEAD
)

echo.
pause
