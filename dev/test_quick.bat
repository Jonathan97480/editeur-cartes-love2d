@echo off
echo 🧪 TESTS RAPIDES
echo ===============
python validate_tests_auto.py
if %errorlevel% equ 0 (
    echo ✅ Tests rapides OK
) else (
    echo ❌ Tests rapides échoués
)
pause
