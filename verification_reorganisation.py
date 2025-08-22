#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VÉRIFICATION POST-RÉORGANISATION
===================================

Script pour vérifier que toutes les fonctionnalités fonctionnent 
correctement après la réorganisation du projet.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test des imports principaux"""
    print("🔗 Test des imports principaux...")
    
    try:
        from lib.database import CardRepo, ensure_db
        print("  ✅ lib.database")
        
        from lib.config import DB_FILE, APP_TITLE
        print("  ✅ lib.config")
        
        from lib.text_formatting_editor import TextFormattingEditor
        print("  ✅ lib.text_formatting_editor")
        
        from lua_exporter_love2d import Love2DLuaExporter
        print("  ✅ lua_exporter_love2d")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Erreur d'import: {e}")
        return False

def test_app_startup():
    """Test du démarrage de l'application"""
    print("\n🚀 Test du démarrage de l'application...")
    
    try:
        import app_final
        print("  ✅ app_final.py peut être importé")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur app_final: {e}")
        return False

def test_love2d_exporter():
    """Test de l'exporteur Love2D"""
    print("\n💎 Test de l'exporteur Love2D...")
    
    try:
        from lua_exporter_love2d import Love2DLuaExporter
        from lib.database import CardRepo, ensure_db
        from lib.config import DB_FILE
        
        # Initialiser la base de données
        ensure_db(DB_FILE)
        repo = CardRepo(DB_FILE)
        
        # Créer l'exporteur
        exporter = Love2DLuaExporter(repo)
        
        # Test d'export basique (sans données)
        result = exporter.export_all_cards_love2d()
        
        if result:
            print(f"  ✅ Export Love2D réussi ({len(result)} caractères)")
            return True
        else:
            print("  ❌ Export Love2D vide")
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur exporteur Love2D: {e}")
        return False

def test_project_structure():
    """Vérification de la structure du projet"""
    print("\n📁 Vérification de la structure du projet...")
    
    required_paths = [
        "lib/",
        "tests/",
        "tests/interface/",
        "tests/export/",  # Correct name
        "tests/database/",
        "dev/",
        "docs/",
        "cartes.db"
    ]
    
    all_good = True
    for path_str in required_paths:
        path = Path(path_str)
        if path.exists():
            print(f"  ✅ {path_str}")
        else:
            print(f"  ❌ {path_str} manquant")
            all_good = False
    
    return all_good

def main():
    """Fonction principale de vérification"""
    print("🔍 VÉRIFICATION POST-RÉORGANISATION")
    print("=" * 50)
    
    tests = [
        ("Structure du projet", test_project_structure),
        ("Imports principaux", test_imports),
        ("Démarrage app", test_app_startup),
        ("Exporteur Love2D", test_love2d_exporter)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erreur test {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS:")
    
    success_count = 0
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
        if result:
            success_count += 1
    
    print(f"\n🎯 Résultat: {success_count}/{len(results)} tests réussis")
    
    if success_count == len(results):
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("La réorganisation a été effectuée avec succès.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérification nécessaire.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
