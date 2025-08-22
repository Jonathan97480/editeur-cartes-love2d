@echo off
echo 🧪 TESTS COMPLETS
echo ================
echo 1️⃣ Validation syntaxe...
python validate_tests_auto.py
echo.
echo 2️⃣ Test d'intégration...
python run_tests.py test_integration_simple
echo.
echo 3️⃣ Tests spécifiques...
python run_tests.py test_simple
python run_tests.py test_lua_integrity
echo.
echo 🏁 Tests terminés !
pause
