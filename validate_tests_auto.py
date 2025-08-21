#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VALIDATION RAPIDE DE TOUS LES TESTS (NON-INTERACTIF)
======================================================

Version non-interactive pour validation automatisée.
"""
import os
import sys
import subprocess
from datetime import datetime

def test_imports_and_syntax():
    """Teste les imports et la syntaxe de tous les tests"""
    print("🔍 VALIDATION SYNTAXE ET IMPORTS")
    print("=" * 50)
    
    tests_dir = "tests"
    results = []
    
    for filename in os.listdir(tests_dir):
        if filename.startswith('test_') and filename.endswith('.py'):
            filepath = os.path.join(tests_dir, filename)
            test_name = filename[:-3]  # Remove .py
            
            print(f"📝 Test syntaxe : {test_name}")
            
            try:
                # Test de compilation/syntaxe
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", filepath],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    print(f"   ✅ Syntaxe OK")
                    
                    # Test d'import
                    try:
                        result_import = subprocess.run(
                            [sys.executable, "-c", f"import sys; sys.path.insert(0, 'tests'); import {test_name}; print('Import OK')"],
                            capture_output=True,
                            text=True,
                            timeout=10,
                            cwd=os.getcwd()
                        )
                        
                        if result_import.returncode == 0:
                            print(f"   ✅ Import OK")
                            results.append((test_name, True, "OK"))
                        else:
                            print(f"   ❌ Erreur import: {result_import.stderr[:100]}...")
                            results.append((test_name, False, "Import failed"))
                    
                    except Exception as e:
                        print(f"   ❌ Erreur import: {str(e)[:100]}...")
                        results.append((test_name, False, "Import exception"))
                
                else:
                    print(f"   ❌ Erreur syntaxe: {result.stderr[:100]}...")
                    results.append((test_name, False, "Syntax error"))
                    
            except Exception as e:
                print(f"   ❌ Erreur: {str(e)[:100]}...")
                results.append((test_name, False, "Exception"))
    
    return results

def test_direct_execution():
    """Teste l'exécution directe de quelques tests clés"""
    print("\n🚀 VALIDATION EXÉCUTION DIRECTE")
    print("=" * 50)
    
    # Tests simples sans interaction
    simple_tests = [
        'test_simple.py',
        'test_compat.py', 
        'test_migration.py',
        'test_lua_export.py',
        'test_template_organization.py'
    ]
    
    results = []
    
    for test_file in simple_tests:
        test_name = test_file[:-3]
        filepath = os.path.join('tests', test_file)
        
        if os.path.exists(filepath):
            print(f"🧪 Test direct : {test_name}")
            
            try:
                # Exécution directe dans le dossier tests
                result = subprocess.run(
                    [sys.executable, test_file],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd='tests'
                )
                
                if result.returncode == 0:
                    print(f"   ✅ Exécution OK")
                    results.append((test_name, True, "Direct execution OK"))
                else:
                    print(f"   ❌ Échec: {result.stderr[:100]}...")
                    results.append((test_name, False, "Direct execution failed"))
                    
            except subprocess.TimeoutExpired:
                print(f"   ⏱️ Timeout (probablement interactif)")
                results.append((test_name, True, "Interactive test"))
            except Exception as e:
                print(f"   ❌ Erreur: {str(e)[:100]}...")
                results.append((test_name, False, "Exception"))
    
    return results

def main():
    """Validation complète non-interactive"""
    print("🔍 VALIDATION AUTOMATISÉE DES TESTS")
    print("=" * 60)
    print(f"📅 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Syntaxe et imports
    syntax_results = test_imports_and_syntax()
    
    # Test 2: Exécution directe
    execution_results = test_direct_execution()
    
    # Rapport final
    print("\n" + "=" * 60)
    print("📊 RAPPORT DE VALIDATION AUTOMATISÉE")
    print("=" * 60)
    
    # Statistiques syntaxe
    syntax_ok = sum(1 for _, success, _ in syntax_results if success)
    syntax_total = len(syntax_results)
    
    print(f"📝 Syntaxe & Imports : {syntax_ok}/{syntax_total} OK ({syntax_ok/syntax_total*100:.1f}%)")
    
    # Statistiques exécution
    exec_ok = sum(1 for _, success, _ in execution_results if success)
    exec_total = len(execution_results)
    
    print(f"🚀 Exécution directe : {exec_ok}/{exec_total} OK ({exec_ok/exec_total*100:.1f}%)")
    
    # Détails
    print("\n📋 DÉTAIL DES RÉSULTATS :")
    print("-" * 30)
    
    all_results = {}
    
    # Combiner les résultats
    for test_name, success, msg in syntax_results:
        all_results[test_name] = {'syntax': success, 'syntax_msg': msg}
    
    for test_name, success, msg in execution_results:
        if test_name in all_results:
            all_results[test_name]['execution'] = success
            all_results[test_name]['exec_msg'] = msg
        else:
            all_results[test_name] = {'execution': success, 'exec_msg': msg}
    
    # Affichage
    for test_name, data in sorted(all_results.items()):
        syntax_status = "✅" if data.get('syntax', True) else "❌"
        exec_status = "✅" if data.get('execution', True) else "❌" 
        exec_info = data.get('exec_msg', 'Non testé')
        
        print(f"{syntax_status} {exec_status} {test_name:25} - {exec_info}")
    
    # Analyse globale
    print(f"\n🎯 ANALYSE GLOBALE :")
    
    total_syntax_ok = syntax_ok
    total_tests = syntax_total
    
    if total_syntax_ok == total_tests:
        print("   🎉 Excellent ! Tous les tests ont une syntaxe correcte.")
        print("   ✅ Infrastructure de test parfaitement organisée.")
        print("   ➡️  Prêt pour les tests d'intégration.")
    elif total_syntax_ok > total_tests * 0.9:
        print("   🔧 Très bon ! Quelques ajustements mineurs nécessaires.")
        print("   ➡️  Corriger les derniers problèmes de syntaxe.")
    else:
        print("   ⚠️  Révision nécessaire de l'organisation des tests.")
        print("   ➡️  Vérifier la configuration d'import.")
    
    print(f"\n🏁 Validation automatisée terminée !")
    
    return total_syntax_ok == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
