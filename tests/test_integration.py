#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTS D'INTÉGRATION - ÉDITEUR DE CARTES LOVE2D
===============================================

Tests d'intégration pour valider le fonctionnement complet du système.
"""
# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()

import os
import sys
import sqlite3
import json
import tempfile
import shutil
from datetime import datetime
from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE
from lib.lua_export import export_lua
from lib.utils import get_card_image_for_export

def test_full_workflow():
    """Test du workflow complet : création carte → export Lua → validation"""
    print("🔄 TEST WORKFLOW COMPLET")
    print("=" * 50)
    
    success = True
    
    try:
        # 1. Initialiser la base de données
        print("1️⃣ Initialisation base de données...")
        ensure_db(DB_FILE)
        repo = CardRepo(DB_FILE)
        print("   ✅ Base initialisée")
        
        # 2. Créer une carte de test
        print("2️⃣ Création carte de test...")
        test_card = {
            'name': 'Carte Test Intégration',
            'cost': 3,
            'attack': 2,
            'defense': 3,
            'description': 'Carte créée pour test d\'intégration complet',
            'rarity': 'commun',
            'types_json': json.dumps(['attaque', 'test']),
            'image_path': None,
            'final_image_path': None
        }
        
        card_id = repo.create_card(**test_card)
        print(f"   ✅ Carte créée (ID: {card_id})")
        
        # 3. Vérifier la carte en base
        print("3️⃣ Vérification en base...")
        card = repo.get_card(card_id)
        assert card is not None, "Carte non trouvée en base"
        assert card[1] == test_card['name'], "Nom incorrect"
        assert card[7] == test_card['rarity'], "Rareté incorrecte"
        print("   ✅ Carte vérifiée en base")
        
        # 4. Export Lua
        print("4️⃣ Export Lua...")
        lua_file = "cards_integration_test.lua"
        export_lua(repo, "player", lua_file)
        assert os.path.exists(lua_file), "Fichier Lua non créé"
        print(f"   ✅ Export Lua créé: {lua_file}")
        
        # 5. Vérifier contenu Lua
        print("5️⃣ Vérification contenu Lua...")
        with open(lua_file, 'r', encoding='utf-8') as f:
            lua_content = f.read()
        
        assert 'Carte Test Intégration' in lua_content, "Nom carte absent du Lua"
        assert 'local cards = {' in lua_content, "Structure Lua incorrecte"
        assert 'return cards' in lua_content, "Return manquant"
        print("   ✅ Contenu Lua valide")
        
        # 6. Nettoyage
        print("6️⃣ Nettoyage...")
        repo.delete_card(card_id)
        if os.path.exists(lua_file):
            os.remove(lua_file)
        print("   ✅ Nettoyage terminé")
        
        print("\n🎉 WORKFLOW COMPLET RÉUSSI !")
        
    except Exception as e:
        print(f"\n❌ ERREUR WORKFLOW: {e}")
        success = False
    
    return success

def test_database_integrity():
    """Test d'intégrité de la base de données"""
    print("\n🗃️ TEST INTÉGRITÉ BASE DE DONNÉES")
    print("=" * 50)
    
    success = True
    
    try:
        # 1. Vérifier structure de la base
        print("1️⃣ Vérification structure...")
        ensure_db(DB_FILE)
        
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            
            # Vérifier les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            assert 'cards' in tables, "Table cards manquante"
            assert 'schema_version' in tables, "Table schema_version manquante"
            print("   ✅ Tables présentes")
            
            # Vérifier les colonnes
            cursor.execute("PRAGMA table_info(cards)")
            columns = [row[1] for row in cursor.fetchall()]
            
            expected_columns = ['id', 'name', 'cost', 'attack', 'defense', 'description', 'image_path', 'rarity', 'types_json', 'final_image_path', 'created_at', 'updated_at']
            
            for col in expected_columns:
                assert col in columns, f"Colonne {col} manquante"
            print("   ✅ Colonnes présentes")
            
            # Vérifier version
            cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
            version = cursor.fetchone()
            assert version and version[0] >= 4, "Version base incorrecte"
            print(f"   ✅ Version base: {version[0]}")
        
        print("\n✅ INTÉGRITÉ BASE VALIDÉE !")
        
    except Exception as e:
        print(f"\n❌ ERREUR INTÉGRITÉ: {e}")
        success = False
    
    return success

def test_image_workflow():
    """Test du workflow de gestion d'images"""
    print("\n🖼️ TEST WORKFLOW IMAGES")
    print("=" * 50)
    
    success = True
    
    try:
        # 1. Vérifier dossiers d'images
        print("1️⃣ Vérification dossiers...")
        
        required_dirs = [
            'images',
            'images/originals',
            'images/cards', 
            'images/templates'
        ]
        
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"   📁 Dossier créé: {dir_path}")
            else:
                print(f"   ✅ Dossier présent: {dir_path}")
        
        # 2. Test utilitaire d'export image
        print("2️⃣ Test utilitaire export...")
        
        # Test avec None
        relative_path = get_card_image_for_export(None)
        assert relative_path is None, "Devrait retourner None pour None"
        print("   ✅ Gestion None")
        
        # Créer un objet mock pour test
        class MockCard:
            def __init__(self, name):
                self.name = name
        
        # Test avec image inexistante
        mock_card = MockCard("nonexistent_card")
        relative_path = get_card_image_for_export(mock_card)
        # La fonction peut retourner None ou un chemin, on vérifie juste qu'elle ne plante pas
        print("   ✅ Gestion carte inexistante")
        
        print("\n✅ WORKFLOW IMAGES VALIDÉ !")
        
    except Exception as e:
        print(f"\n❌ ERREUR IMAGES: {e}")
        success = False
    
    return success

def test_export_validation():
    """Test de validation des exports"""
    print("\n📤 TEST VALIDATION EXPORTS")
    print("=" * 50)
    
    success = True
    
    try:
        # 1. Export avec base vide
        print("1️⃣ Export base vide...")
        empty_lua = "cards_empty_test.lua"
        repo = CardRepo(DB_FILE)
        export_lua(repo, "player", empty_lua)
        
        assert os.path.exists(empty_lua), "Fichier export vide non créé"
        
        with open(empty_lua, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'local cards = {}' in content, "Structure vide incorrecte"
        print("   ✅ Export base vide valide")
        
        # 2. Nettoyage
        if os.path.exists(empty_lua):
            os.remove(empty_lua)
        
        print("\n✅ VALIDATION EXPORTS RÉUSSIE !")
        
    except Exception as e:
        print(f"\n❌ ERREUR EXPORTS: {e}")
        success = False
    
    return success

def test_module_integration():
    """Test d'intégration entre modules"""
    print("\n🔗 TEST INTÉGRATION MODULES")
    print("=" * 50)
    
    success = True
    
    try:
        # 1. Test imports critiques
        print("1️⃣ Test imports...")
        
        from lib.database import CardRepo
        from lib.lua_export import export_lua
        from lib.utils import get_card_image_for_export
        from lib.config import DB_FILE
        
        print("   ✅ Imports modules principaux")
        
        # 2. Test interfaces
        print("2️⃣ Test interfaces...")
        
        repo = CardRepo(DB_FILE)
        assert hasattr(repo, 'get_all_cards'), "Méthode get_all_cards manquante"
        assert hasattr(repo, 'create_card'), "Méthode create_card manquante"
        print("   ✅ Interface CardRepo")
        
        assert callable(export_lua), "export_lua non callable"
        assert callable(get_card_image_for_export), "get_card_image_for_export non callable"
        print("   ✅ Fonctions utilitaires")
        
        print("\n✅ INTÉGRATION MODULES VALIDÉE !")
        
    except Exception as e:
        print(f"\n❌ ERREUR INTÉGRATION: {e}")
        success = False
    
    return success

def main():
    """Lance tous les tests d'intégration"""
    print("🧪 TESTS D'INTÉGRATION COMPLETS")
    print("=" * 60)
    print(f"📅 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Base de données", test_database_integrity),
        ("Modules", test_module_integration),
        ("Images", test_image_workflow),
        ("Exports", test_export_validation),
        ("Workflow complet", test_full_workflow),
    ]
    
    results = []
    success_count = 0
    
    for test_name, test_func in tests:
        print(f"🧪 Test : {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                success_count += 1
        except Exception as e:
            print(f"❌ ERREUR INATTENDUE: {e}")
            results.append((test_name, False))
    
    # Rapport final
    print("\n" + "=" * 60)
    print("📊 RAPPORT TESTS D'INTÉGRATION")
    print("=" * 60)
    
    print(f"✅ Tests réussis : {success_count}/{len(tests)} ({success_count/len(tests)*100:.1f}%)")
    print()
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print()
    
    if success_count == len(tests):
        print("🎉 TOUS LES TESTS D'INTÉGRATION RÉUSSIS !")
        print("✅ Système entièrement fonctionnel")
        print("➡️  Prêt pour les hooks automatisés")
    else:
        print("⚠️  Certains tests d'intégration ont échoué")
        print("🔧 Vérification nécessaire avant production")
    
    print("\n🏁 Tests d'intégration terminés !")
    
    return success_count == len(tests)

if __name__ == "__main__":
    success = main()
    print("\nAppuyez sur Entrée pour fermer...")
    input()
    sys.exit(0 if success else 1)
