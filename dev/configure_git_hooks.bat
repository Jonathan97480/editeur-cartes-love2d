@echo off
chcp 65001 > nul
title Configuration Git - Hooks

echo 🔧 CONFIGURATION DES HOOKS GIT
echo ================================

echo.
echo Que voulez-vous faire ?
echo 1. Désactiver les hooks (renomme en .bak)
echo 2. Réactiver les hooks (restaure depuis .bak)
echo 3. Voir l'état des hooks
echo 0. Quitter

set /p choice="Votre choix: "

if "%choice%"=="1" goto disable_hooks
if "%choice%"=="2" goto enable_hooks
if "%choice%"=="3" goto show_hooks
if "%choice%"=="0" goto end
goto invalid

:disable_hooks
echo.
echo 📴 Désactivation des hooks...
cd .git\hooks
if exist pre-commit (
    ren pre-commit pre-commit.bak
    echo ✅ pre-commit → pre-commit.bak
)
if exist post-commit (
    ren post-commit post-commit.bak
    echo ✅ post-commit → post-commit.bak
)
if exist pre-push (
    ren pre-push pre-push.bak
    echo ✅ pre-push → pre-push.bak
)
echo.
echo ✅ Hooks désactivés. Vous pouvez maintenant faire des commits sans validation.
goto end

:enable_hooks
echo.
echo 📳 Réactivation des hooks...
cd .git\hooks
if exist pre-commit.bak (
    ren pre-commit.bak pre-commit
    echo ✅ pre-commit.bak → pre-commit
)
if exist post-commit.bak (
    ren post-commit.bak post-commit
    echo ✅ post-commit.bak → post-commit
)
if exist pre-push.bak (
    ren pre-push.bak pre-push
    echo ✅ pre-push.bak → pre-push
)
echo.
echo ✅ Hooks réactivés. Les validations automatiques sont actives.
goto end

:show_hooks
echo.
echo 📋 État des hooks:
cd .git\hooks
echo.
if exist pre-commit (
    echo ✅ pre-commit: ACTIF
) else if exist pre-commit.bak (
    echo 📴 pre-commit: DÉSACTIVÉ (.bak)
) else (
    echo ❌ pre-commit: ABSENT
)

if exist post-commit (
    echo ✅ post-commit: ACTIF
) else if exist post-commit.bak (
    echo 📴 post-commit: DÉSACTIVÉ (.bak)
) else (
    echo ❌ post-commit: ABSENT
)

if exist pre-push (
    echo ✅ pre-push: ACTIF
) else if exist pre-push.bak (
    echo 📴 pre-push: DÉSACTIVÉ (.bak)
) else (
    echo ❌ pre-push: ABSENT
)
goto end

:invalid
echo ❌ Choix invalide
goto end

:end
echo.
pause
