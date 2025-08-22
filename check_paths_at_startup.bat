@echo off
echo 🔍 Vérification des chemins dans la base de données...

python check_database_paths.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️  Des chemins absolus ont été détectés dans la base de données
    echo    Cela peut causer des problèmes de portabilité entre ordinateurs.
    echo.
    echo 🔧 Correction automatique en cours...
    python fix_database_paths.py
    
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Chemins corrigés avec succès!
    ) else (
        echo ❌ Erreur lors de la correction des chemins
        pause
        exit /b 1
    )
) else (
    echo ✅ Tous les chemins sont corrects
)

echo.
