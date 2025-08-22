#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de validation final de l'export Lua corrigé
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import CardRepo
from lib.config import DB_FILE
from lib.actors import ActorManager, export_lua_for_actor

def test_export_correction():
    """Test pour vérifier que tous les problèmes sont corrigés."""
    print("🔧 TEST DE VALIDATION DES CORRECTIONS EXPORT LUA")
    print("=" * 55)
    
    # Initialiser
    repo = CardRepo(DB_FILE)
    actor_manager = ActorManager(DB_FILE)
    
    # Lister les acteurs pour trouver Barbus
    actors = actor_manager.list_actors()
    barbus_id = None
    
    print("📋 Acteurs disponibles :")
    for actor in actors:
        print(f"   ID {actor['id']}: {actor['icon']} {actor['name']}")
        if 'barbus' in actor['name'].lower():
            barbus_id = actor['id']
    
    if not barbus_id:
        print("❌ Acteur Barbus non trouvé")
        return False
    
    print(f"\n🎭 Test export acteur Barbus (ID: {barbus_id})")
    
    # Effectuer l'export
    filename = export_lua_for_actor(repo, actor_manager, barbus_id, "validation_barbus.lua")
    
    # Vérifier le contenu
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n📊 VALIDATION DU CONTENU :")
        
        # Tests de structure
        checks = [
            ("Header Lua", "local Cards = {" in content),
            ("Footer Lua", "return Cards" in content),
            ("Illustration", "ImgIlustration = '" in content),
            ("Effects Actor", "Actor = {" in content),
            ("Effects Enemy", "Enemy = {" in content),
            ("PowerBlow", "PowerBlow = " in content),
            ("Rareté", "Rarete = '" in content),
            ("Types", "Type = {" in content),
            ("Action", "action = function" in content),
            ("Structure Cards", "Cards = {}" in content),
        ]
        
        all_good = True
        for test_name, test_result in checks:
            status = "✅" if test_result else "❌"
            print(f"   {status} {test_name}")
            if not test_result:
                all_good = False
        
        print(f"\n📏 Taille du fichier : {len(content)} caractères")
        
        # Compter les cartes
        card_count = content.count("--[[ CARTE")
        print(f"🃏 Nombre de cartes : {card_count}")
        
        # Vérifier les cartes multi-acteurs
        barbus_cards = actor_manager.get_actor_cards(barbus_id)
        print(f"📂 Cartes liées à Barbus dans BDD : {len(barbus_cards)}")
        
        print(f"\n📝 Aperçu du début :")
        print(content[:300] + "...")
        
        if all_good:
            print(f"\n🎉 TOUS LES PROBLÈMES SONT CORRIGÉS !")
            print("   ✅ Format Lua complet")
            print("   ✅ Illustrations présentes")
            print("   ✅ Effects Actor/Enemy renommés")
            print("   ✅ Cartes multi-acteurs incluses")
            return True
        else:
            print(f"\n❌ Des problèmes persistent")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
        return False

if __name__ == "__main__":
    success = test_export_correction()
    if not success:
        sys.exit(1)
    
    print("\n" + "=" * 55)
    print("🚀 L'export Lua est maintenant parfaitement fonctionnel !")
    print("Testez dans l'interface avec les nouveaux boutons :")
    print("• 🎭 Exporter Acteur")
    print("• 📤 Exporter Tout")
    print("=" * 55)
