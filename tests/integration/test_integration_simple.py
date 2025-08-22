#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTS D'INTÉGRATION SIMPLIFIÉS
===============================

Tests d'intégration fonctionnels adaptés à l'API actuelle.
"""
# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()

import os
import sys
import sqlite3
import json
from datetime import datetime
from lib.database import CardRepo, ensure_db, Card
from lib.config import DB_FILE
from lib.lua_export import export_lua

def test_basic_database():
    """Test de base de la base de données"""
    print("🗃️ TEST BASE DE DONNÉES BASIQUE")
    print("=" * 50)
    
    try:
        # 1. Initialiser
        print("1️⃣ Initialisation...")
        ensure_db(DB_FILE)
        repo = CardRepo(DB_FILE)
        print("   ✅ Base initialisée")
        
        # 2. Lister les cartes
        print("2️⃣ Lecture cartes...")
        cards = repo.list_cards()
        print(f"   ✅ {len(cards)} cartes trouvées")
        
        # 3. Test de connexion
        print("3️⃣ Test connexion...")
        with repo.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cards")
            count = cursor.fetchone()[0]
            print(f"   ✅ {count} cartes en base")
        
        print("\n✅ BASE DE DONNÉES FONCTIONNELLE !")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR BASE: {e}")
        return False

def test_basic_export():
    """Test d'export basique"""
    print("\n📤 TEST EXPORT BASIQUE")
    print("=" * 50)
    
    try:
        # 1. Préparer
        print("1️⃣ Préparation...")
        repo = CardRepo(DB_FILE)
        test_file = "test_integration_basic.lua"
        print("   ✅ Préparé")
        
        # 2. Export
        print("2️⃣ Export...")
        export_lua(repo, "player", test_file)
        assert os.path.exists(test_file), "Fichier non créé"
        print(f"   ✅ Fichier créé: {test_file}")
        
        # 3. Vérifier contenu
        print("3️⃣ Vérification...")
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'local cards = ' in content, "Structure manquante"
        assert 'return cards' in content, "Return manquant"
        print("   ✅ Structure Lua correcte")
        
        # 4. Nettoyage
        os.remove(test_file)
        print("   ✅ Nettoyé")
        
        print("\n✅ EXPORT FONCTIONNEL !")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR EXPORT: {e}")
        return False

def test_basic_card_operations():
    """Test des opérations de base sur les cartes"""
    print("\n🃏 TEST OPÉRATIONS CARTES")
    print("=" * 50)
    
    try:
        # 1. Préparer
        print("1️⃣ Préparation...")
        repo = CardRepo(DB_FILE)
        print("   ✅ Repo préparé")
        
        # 2. Créer une carte de test
        print("2️⃣ Création carte test...")
        test_card = Card()
        test_card.name = "Test Intégration"
        test_card.cost = 1
        test_card.attack = 1
        test_card.defense = 1
        test_card.description = "Carte de test d'intégration"
        test_card.rarity = "commun"
        test_card.types_json = json.dumps(["test"])
        
        card_id = repo.insert(test_card)
        print(f"   ✅ Carte créée (ID: {card_id})")
        
        # 3. Récupérer la carte
        print("3️⃣ Récupération...")
        retrieved_card = repo.get(card_id)
        assert retrieved_card is not None, "Carte non trouvée"
        assert retrieved_card.name == "Test Intégration", "Nom incorrect"
        print("   ✅ Carte récupérée")
        
        # 4. Modifier la carte
        print("4️⃣ Modification...")
        retrieved_card.cost = 2
        repo.update(retrieved_card)
        
        modified_card = repo.get(card_id)
        assert modified_card.cost == 2, "Modification non appliquée"
        print("   ✅ Carte modifiée")
        
        # 5. Supprimer la carte
        print("5️⃣ Suppression...")
        repo.delete(card_id)
        
        deleted_card = repo.get(card_id)
        assert deleted_card is None, "Carte non supprimée"
        print("   ✅ Carte supprimée")
        
        print("\n✅ OPÉRATIONS CARTES FONCTIONNELLES !")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR CARTES: {e}")
        return False

def test_basic_modules():
    """Test d'import des modules"""
    print("\n🔗 TEST MODULES BASIQUES")
    print("=" * 50)
    
    try:
        # 1. Imports critiques
        print("1️⃣ Imports...")
        from lib.database import CardRepo, ensure_db, Card
        from lib.lua_export import export_lua
        from lib.config import DB_FILE
        print("   ✅ Imports réussis")
        
        # 2. Interfaces
        print("2️⃣ Interfaces...")
        repo = CardRepo(DB_FILE)
        assert hasattr(repo, 'list_cards'), "Méthode list_cards manquante"
        assert hasattr(repo, 'get'), "Méthode get manquante"
        assert hasattr(repo, 'insert'), "Méthode insert manquante"
        assert hasattr(repo, 'update'), "Méthode update manquante"
        assert hasattr(repo, 'delete'), "Méthode delete manquante"
        print("   ✅ Interface CardRepo")
        
        assert callable(export_lua), "export_lua non callable"
        print("   ✅ Fonctions utilitaires")
        
        print("\n✅ MODULES FONCTIONNELS !")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR MODULES: {e}")
        return False

def main():
    """Lance tous les tests d'intégration simplifiés"""
    print("🧪 TESTS D'INTÉGRATION SIMPLIFIÉS")
    print("=" * 60)
    print(f"📅 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Modules", test_basic_modules),
        ("Base de données", test_basic_database),
        ("Export Lua", test_basic_export),
        ("Opérations cartes", test_basic_card_operations),
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
    print("📊 RAPPORT TESTS D'INTÉGRATION SIMPLIFIÉS")
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
        print("✅ Infrastructure test validée")
        print("➡️  Prêt pour les hooks automatisés")
    elif success_count > len(tests) * 0.75:
        print("🔧 Très bon ! Tests majoritairement réussis")
        print("➡️  Corriger les derniers problèmes")
    else:
        print("⚠️  Certains tests critiques ont échoué")
        print("🔧 Vérification nécessaire")
    
    print("\n🏁 Tests d'intégration simplifiés terminés !")
    
    return success_count == len(tests)

if __name__ == "__main__":
    success = main()
    print("\nAppuyez sur Entrée pour fermer...")
    input()
    sys.exit(0 if success else 1)
