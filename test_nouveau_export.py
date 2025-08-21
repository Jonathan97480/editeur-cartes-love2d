#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des nouvelles fonctionnalités d'export d'acteurs
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE
from lib.actors import ActorManager, export_lua_for_actor, export_all_actors_lua

def default_db_path():
    """Retourne le chemin par défaut de la base de données."""
    return DB_FILE

def test_new_export_system():
    """Test des nouvelles fonctions d'export d'acteurs."""
    print("🧪 Test du nouveau système d'export d'acteurs")
    print("=" * 50)
    
    # Initialiser la base de données
    db_path = default_db_path()
    ensure_db(db_path)
    repo = CardRepo(db_path)
    actor_manager = ActorManager(db_path)
    
    # Lister les acteurs disponibles
    actors = actor_manager.list_actors()
    print(f"📋 Acteurs disponibles : {len(actors)}")
    for actor in actors:
        card_count = len(actor_manager.get_actor_cards(actor['id']))
        print(f"   {actor['icon']} {actor['name']} : {card_count} cartes")
    
    if not actors:
        print("❌ Aucun acteur trouvé")
        return False
    
    print("\n" + "="*50)
    
    # Test 1 : Export d'un acteur spécifique (Barbus)
    print("🎭 Test 1 : Export d'un acteur spécifique")
    barbus_actor = None
    for actor in actors:
        if 'barbus' in actor['name'].lower():
            barbus_actor = actor
            break
    
    if barbus_actor:
        try:
            filename = export_lua_for_actor(repo, actor_manager, barbus_actor['id'], "test_export_barbus.lua")
            print(f"✅ Export de {barbus_actor['icon']} {barbus_actor['name']} réussi : {filename}")
            
            # Vérifier le fichier
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"📊 Taille du fichier : {len(content)} caractères")
                print(f"📝 Aperçu du début :\n{content[:200]}...")
            else:
                print("❌ Fichier non créé")
                return False
                
        except Exception as e:
            print(f"❌ Erreur export Barbus : {e}")
            return False
    else:
        print("⚠️  Acteur Barbus non trouvé, test avec le premier acteur")
        try:
            first_actor = actors[0]
            filename = export_lua_for_actor(repo, actor_manager, first_actor['id'], "test_export_first.lua")
            print(f"✅ Export de {first_actor['icon']} {first_actor['name']} réussi : {filename}")
        except Exception as e:
            print(f"❌ Erreur export premier acteur : {e}")
            return False
    
    print("\n" + "="*50)
    
    # Test 2 : Export de tous les acteurs
    print("📤 Test 2 : Export de tous les acteurs")
    try:
        filename = export_all_actors_lua(repo, actor_manager, "test_export_all_actors.lua")
        print(f"✅ Export de tous les acteurs réussi : {filename}")
        
        # Vérifier le fichier
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"📊 Taille du fichier : {len(content)} caractères")
            
            # Compter les sections d'acteurs
            actor_sections = content.count("--[[ ACTEUR:")
            print(f"🎭 Sections d'acteurs trouvées : {actor_sections}")
            
            print(f"📝 Aperçu du début :\n{content[:300]}...")
        else:
            print("❌ Fichier non créé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur export tous acteurs : {e}")
        return False
    
    print("\n" + "="*50)
    print("🎉 Tests d'export réussis !")
    print("\nFichiers créés :")
    test_files = ["test_export_barbus.lua", "test_export_first.lua", "test_export_all_actors.lua"]
    for test_file in test_files:
        if os.path.exists(test_file):
            size = os.path.getsize(test_file)
            print(f"   ✅ {test_file} ({size} octets)")
    
    return True

if __name__ == "__main__":
    try:
        success = test_new_export_system()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Appuyez sur Entrée pour fermer...")
    input()
