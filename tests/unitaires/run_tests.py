#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 LANCEUR DE TESTS - ÉDITEUR DE CARTES LOVE2D
==============================================

Script principal pour exécuter les tests depuis la racine du projet.
"""
import os
import sys
import subprocess
from pathlib import Path

def list_available_tests():
    """Liste tous les tests disponibles."""
    tests_dir = Path("tests")
    if not tests_dir.exists():
        print("❌ Dossier tests/ introuvable")
        return []
    
    test_files = list(tests_dir.glob("test_*.py"))
    return sorted([f.stem for f in test_files])

def run_test(test_name):
    """Exécute un test spécifique."""
    test_path = Path("tests") / f"{test_name}.py"
    
    if not test_path.exists():
        print(f"❌ Test {test_name} introuvable dans tests/")
        return False
    
    print(f"🚀 Exécution de {test_name}...")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, str(test_path)
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✅ {test_name} terminé avec succès")
            return True
        else:
            print(f"❌ {test_name} a échoué (code {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de {test_name}: {e}")
        return False

def run_test_suite():
    """Exécute une suite de tests critique."""
    critical_tests = [
        "test_simple",
        "test_compat", 
        "test_migration",
        "test_final_verification"
    ]
    
    print("🧪 SUITE DE TESTS CRITIQUE")
    print("=" * 40)
    print("Tests sélectionnés pour validation rapide du système")
    print()
    
    results = {}
    
    for test in critical_tests:
        success = run_test(test)
        results[test] = success
        print()
    
    # Résumé
    print("📊 RÉSUMÉ DE LA SUITE DE TESTS")
    print("=" * 40)
    
    passed = sum(results.values())
    total = len(results)
    
    for test, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {test}")
    
    print(f"\n🎯 Résultat : {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS CRITIQUES SONT PASSÉS !")
        return True
    else:
        print("⚠️ Certains tests critiques ont échoué")
        return False

def main():
    """Point d'entrée principal."""
    
    print("🧪 LANCEUR DE TESTS - ÉDITEUR DE CARTES LOVE2D")
    print("=" * 55)
    
    if len(sys.argv) == 1:
        print("\n📋 Utilisation :")
        print("   python run_tests.py [nom_du_test]")
        print("   python run_tests.py --suite    (tests critiques)")
        print("   python run_tests.py --list     (lister les tests)")
        print("   python run_tests.py --index    (documentation)")
        print()
        
        # Affichage par défaut
        tests = list_available_tests()
        if tests:
            print(f"📁 Tests disponibles ({len(tests)}) :")
            for test in tests:
                print(f"   • {test}")
            print(f"\n💡 Exemple : python run_tests.py {tests[0]}")
        else:
            print("❌ Aucun test trouvé dans tests/")
        
        return
    
    arg = sys.argv[1]
    
    if arg == "--list":
        tests = list_available_tests()
        print(f"\n📁 Tests disponibles ({len(tests)}) :")
        for test in tests:
            print(f"   • {test}")
    
    elif arg == "--suite":
        success = run_test_suite()
        sys.exit(0 if success else 1)
    
    elif arg == "--index":
        try:
            # Importer et exécuter l'index des tests
            index_path = Path("tests") / "__index__.py"
            if index_path.exists():
                subprocess.run([sys.executable, str(index_path)])
            else:
                print("❌ Fichier d'index introuvable dans tests/")
        except Exception as e:
            print(f"❌ Erreur chargement index : {e}")
    
    elif arg.startswith("--"):
        print(f"❌ Option inconnue : {arg}")
        print("Options valides : --list, --suite, --index")
    
    else:
        # Exécuter un test spécifique
        test_name = arg
        if not test_name.startswith("test_"):
            test_name = f"test_{test_name}"
        
        success = run_test(test_name)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Exécution interrompue")
        sys.exit(1)
