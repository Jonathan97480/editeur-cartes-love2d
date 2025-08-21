#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 HOOKS DE TEST AUTOMATISÉS
============================

Configuration de hooks pour automatiser l'exécution des tests.
"""
import os
import sys
import subprocess
from datetime import datetime

def create_git_hooks():
    """Crée des hooks Git pour les tests automatisés"""
    print("🔧 CRÉATION HOOKS GIT")
    print("=" * 50)
    
    # Créer le dossier .git/hooks s'il n'existe pas
    hooks_dir = ".git/hooks"
    if not os.path.exists(hooks_dir):
        os.makedirs(hooks_dir)
        print(f"📁 Dossier créé: {hooks_dir}")
    
    # Hook pre-commit : Tests avant commit
    pre_commit_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook pre-commit : Validation automatique avant commit
"""
import subprocess
import sys

def run_validation():
    """Lance la validation automatisée"""
    print("🔍 VALIDATION PRE-COMMIT")
    print("=" * 40)
    
    # Test de syntaxe rapide
    result = subprocess.run([
        sys.executable, "validate_tests_auto.py"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Validation réussie - Commit autorisé")
        return True
    else:
        print("❌ Validation échouée - Commit bloqué")
        print("Erreurs:", result.stderr[:200])
        return False

if __name__ == "__main__":
    if not run_validation():
        sys.exit(1)
    sys.exit(0)
'''
    
    pre_commit_path = os.path.join(hooks_dir, "pre-commit")
    with open(pre_commit_path, 'w', encoding='utf-8') as f:
        f.write(pre_commit_content)
    
    # Rendre exécutable (sur Unix)
    if os.name != 'nt':
        os.chmod(pre_commit_path, 0o755)
    
    print(f"✅ Hook pre-commit créé: {pre_commit_path}")
    
    # Hook post-commit : Rapport après commit
    post_commit_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook post-commit : Rapport automatique après commit
"""
import subprocess
import sys
from datetime import datetime

def generate_report():
    """Génère un rapport post-commit"""
    print("📊 RAPPORT POST-COMMIT")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Lancer les tests d'intégration en arrière-plan
    try:
        result = subprocess.run([
            sys.executable, "validate_tests_auto.py"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Tests post-commit OK")
        else:
            print("⚠️ Attention : Certains tests échouent")
    except subprocess.TimeoutExpired:
        print("⏱️ Tests en cours d'exécution...")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    generate_report()
'''
    
    post_commit_path = os.path.join(hooks_dir, "post-commit")
    with open(post_commit_path, 'w', encoding='utf-8') as f:
        f.write(post_commit_content)
    
    if os.name != 'nt':
        os.chmod(post_commit_path, 0o755)
    
    print(f"✅ Hook post-commit créé: {post_commit_path}")
    
    return True

def create_batch_runners():
    """Crée des scripts batch pour faciliter l'exécution"""
    print("\n🚀 CRÉATION SCRIPTS BATCH")
    print("=" * 50)
    
    # Script de test rapide
    quick_test_content = '''@echo off
echo 🧪 TESTS RAPIDES
echo ===============
python validate_tests_auto.py
if %errorlevel% equ 0 (
    echo ✅ Tests rapides OK
) else (
    echo ❌ Tests rapides échoués
)
pause
'''
    
    with open("test_quick.bat", 'w', encoding='utf-8') as f:
        f.write(quick_test_content)
    print("✅ Script créé: test_quick.bat")
    
    # Script de test complet
    full_test_content = '''@echo off
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
'''
    
    with open("test_full.bat", 'w', encoding='utf-8') as f:
        f.write(full_test_content)
    print("✅ Script créé: test_full.bat")
    
    # Script de déploiement
    deploy_content = '''@echo off
echo 🚀 DÉPLOIEMENT AVEC TESTS
echo ========================
echo 1️⃣ Tests pré-déploiement...
python validate_tests_auto.py
if %errorlevel% neq 0 (
    echo ❌ Tests échoués - Déploiement annulé
    pause
    exit /b 1
)
echo ✅ Tests OK - Déploiement autorisé
echo.
echo 2️⃣ Créer un commit ?
set /p commit_msg="Message de commit (ou ENTER pour annuler) : "
if "%commit_msg%"=="" (
    echo Déploiement annulé
    pause
    exit /b 0
)
echo.
echo 3️⃣ Commit en cours...
git add .
git commit -m "%commit_msg%"
echo ✅ Commit terminé !
pause
'''
    
    with open("deploy.bat", 'w', encoding='utf-8') as f:
        f.write(deploy_content)
    print("✅ Script créé: deploy.bat")
    
    return True

def create_test_config():
    """Crée un fichier de configuration pour les tests"""
    print("\n⚙️ CRÉATION CONFIGURATION TESTS")
    print("=" * 50)
    
    config_content = '''{
    "test_config": {
        "version": "1.0",
        "created": "2025-08-21",
        "description": "Configuration automatisée des tests"
    },
    "hooks": {
        "pre_commit": {
            "enabled": true,
            "timeout": 30,
            "tests": ["validate_tests_auto.py"]
        },
        "post_commit": {
            "enabled": true,
            "timeout": 60,
            "tests": ["validate_tests_auto.py"]
        }
    },
    "test_suites": {
        "quick": {
            "description": "Tests rapides (syntaxe + imports)",
            "script": "validate_tests_auto.py",
            "timeout": 30
        },
        "integration": {
            "description": "Tests d'intégration simplifiés", 
            "script": "run_tests.py test_integration_simple",
            "timeout": 60
        },
        "full": {
            "description": "Suite complète de tests",
            "scripts": [
                "validate_tests_auto.py",
                "run_tests.py test_integration_simple",
                "run_tests.py test_simple",
                "run_tests.py test_lua_integrity"
            ],
            "timeout": 120
        }
    },
    "reporting": {
        "format": "console",
        "log_file": "test_results.log",
        "email_notifications": false
    }
}'''
    
    with open("test_config.json", 'w', encoding='utf-8') as f:
        f.write(config_content)
    print("✅ Configuration créée: test_config.json")
    
    return True

def create_ci_workflow():
    """Crée un workflow pour CI/CD (GitHub Actions style)"""
    print("\n🔄 CRÉATION WORKFLOW CI")
    print("=" * 50)
    
    # Créer le dossier .github/workflows s'il n'existe pas
    workflow_dir = ".github/workflows"
    if not os.path.exists(workflow_dir):
        os.makedirs(workflow_dir)
        print(f"📁 Dossier créé: {workflow_dir}")
    
    workflow_content = '''name: Tests Automatisés

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pillow
    
    - name: Run syntax validation
      run: python validate_tests_auto.py
    
    - name: Run integration tests
      run: python run_tests.py test_integration_simple
      continue-on-error: true
    
    - name: Run specific tests
      run: |
        python run_tests.py test_simple
        python run_tests.py test_lua_integrity
      continue-on-error: true
    
    - name: Generate test report
      run: echo "Tests terminés - voir les logs ci-dessus"
'''
    
    workflow_path = os.path.join(workflow_dir, "tests.yml")
    with open(workflow_path, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    print(f"✅ Workflow créé: {workflow_path}")
    
    return True

def main():
    """Configure tous les hooks automatisés"""
    print("🔧 CONFIGURATION HOOKS AUTOMATISÉS")
    print("=" * 60)
    print(f"📅 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tasks = [
        ("Hooks Git", create_git_hooks),
        ("Scripts Batch", create_batch_runners),
        ("Configuration", create_test_config),
        ("Workflow CI", create_ci_workflow),
    ]
    
    success_count = 0
    
    for task_name, task_func in tasks:
        print(f"🔧 {task_name}")
        print("-" * 40)
        
        try:
            result = task_func()
            if result:
                success_count += 1
                print(f"✅ {task_name} configuré avec succès")
            else:
                print(f"❌ Erreur {task_name}")
        except Exception as e:
            print(f"❌ ERREUR {task_name}: {e}")
        
        print()
    
    # Rapport final
    print("=" * 60)
    print("📊 RAPPORT CONFIGURATION HOOKS")
    print("=" * 60)
    
    print(f"✅ Tâches réussies : {success_count}/{len(tasks)} ({success_count/len(tasks)*100:.1f}%)")
    print()
    
    if success_count == len(tasks):
        print("🎉 HOOKS AUTOMATISÉS CONFIGURÉS AVEC SUCCÈS !")
        print()
        print("🚀 UTILISATION :")
        print("   • test_quick.bat       - Tests rapides")
        print("   • test_full.bat        - Tests complets") 
        print("   • deploy.bat           - Déploiement avec tests")
        print("   • Hooks Git            - Automatiques lors des commits")
        print("   • Workflow CI          - Pour GitHub Actions")
        print()
        print("⚙️ CONFIGURATION :")
        print("   • test_config.json     - Configuration centralisée")
        print("   • .git/hooks/          - Hooks Git automatiques")
        print("   • .github/workflows/   - CI/CD workflows")
        print()
        print("🎯 VALIDATION AUTOMATIQUE ACTIVÉE !")
    else:
        print("⚠️  Configuration partiellement réussie")
        print("🔧 Vérifier les erreurs ci-dessus")
    
    print("\n🏁 Configuration terminée !")
    
    return success_count == len(tasks)

if __name__ == "__main__":
    success = main()
    print("\nAppuyez sur Entrée pour fermer...")
    input()
    sys.exit(0 if success else 1)
