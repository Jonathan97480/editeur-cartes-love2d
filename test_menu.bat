@echo off
echo TEST MENU
echo [U] Option U
set /p choice="Choix: "
if /i "%choice%"=="u" (
    echo Option U choisie!
) else (
    echo Autre choix: %choice%
)
pause
