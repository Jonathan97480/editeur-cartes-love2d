#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation complète de la sélection multiple d'acteurs
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.database import CardRepo, ensure_db, Card
from lib.actors import ActorManager
from lib.config import DB_FILE


def test_integration_complete():
    """Test d'intégration complet de la sélection multiple."""
    
    print("🔄 VALIDATION INTÉGRATION SÉLECTION MULTIPLE")
    print("=" * 55)
    
    # Initialiser la base
    ensure_db(DB_FILE)
    repo = CardRepo(DB_FILE)
    actor_manager = ActorManager(DB_FILE)
    
    # Créer une carte de test
    test_card = Card()
    test_card.name = "Carte Multi-Acteurs Test"
    test_card.img = "multi_test.png"
    test_card.description = "Test de validation sélection multiple"
    test_card.powerblow = 7
    test_card.side = "joueur"
    test_card.rarity = "rare"
    
    # Sauvegarder la carte
    card_id = repo.insert(test_card)
    print(f"✅ Carte créée avec ID : {card_id}")
    
    # Obtenir tous les acteurs
    all_actors = actor_manager.list_actors()
    print(f"📋 {len(all_actors)} acteurs disponibles :")
    for actor in all_actors:
        print(f"   - {actor['name']} (ID: {actor['id']})")
    
    # Test 1 : Liaison avec 3 acteurs
    print(f"\n🔗 Test 1 : Liaison avec 3 acteurs")
    selected_actors = all_actors[:3]
    
    for actor in selected_actors:
        actor_manager.link_card_to_actor(card_id, actor['id'])
        print(f"   ✅ Lié à {actor['name']}")
    
    # Vérifier les liaisons
    linked_actors = actor_manager.get_card_actors(card_id)
    print(f"   📊 Résultat : {len(linked_actors)} acteurs liés")
    
    if len(linked_actors) == 3:
        print("   ✅ Test 1 RÉUSSI")
        test1_ok = True
    else:
        print("   ❌ Test 1 ÉCHEC")
        test1_ok = False
    
    # Test 2 : Modification de la sélection
    print(f"\n🔄 Test 2 : Modification sélection (retirer 1, ajouter 2)")
    
    # Supprimer toutes les liaisons
    for actor in all_actors:
        actor_manager.unlink_card_from_actor(card_id, actor['id'])
    
    # Ajouter une nouvelle sélection (acteurs 2, 3, 4, 5)
    new_selection = all_actors[1:5] if len(all_actors) >= 5 else all_actors[1:]
    
    for actor in new_selection:
        actor_manager.link_card_to_actor(card_id, actor['id'])
        print(f"   ✅ Lié à {actor['name']}")
    
    # Vérifier
    new_linked = actor_manager.get_card_actors(card_id)
    print(f"   📊 Résultat : {len(new_linked)} acteurs liés")
    
    if len(new_linked) == len(new_selection):
        print("   ✅ Test 2 RÉUSSI")
        test2_ok = True
    else:
        print("   ❌ Test 2 ÉCHEC")
        test2_ok = False
    
    # Test 3 : Chargement et affichage des liaisons
    print(f"\n📖 Test 3 : Chargement carte et vérification liaisons")
    
    # Charger la carte depuis la base
    loaded_card = repo.get(card_id)
    if loaded_card:
        print(f"   ✅ Carte chargée : {loaded_card.name}")
        
        # Obtenir les acteurs liés
        card_actors = actor_manager.get_card_actors(card_id)
        print(f"   📋 Acteurs liés à cette carte :")
        for actor in card_actors:
            print(f"      - {actor['name']} (ID: {actor['id']})")
        
        if len(card_actors) > 0:
            print("   ✅ Test 3 RÉUSSI")
            test3_ok = True
        else:
            print("   ❌ Test 3 ÉCHEC")
            test3_ok = False
    else:
        print("   ❌ Impossible de charger la carte")
        test3_ok = False
    
    # Test 4 : Export et intégrité des données
    print(f"\n💾 Test 4 : Vérification intégrité export")
    
    try:
        # Exporter les acteurs d'une carte
        export_data = {
            'card_id': card_id,
            'card_name': loaded_card.name if loaded_card else 'Unknown',
            'actors': [actor['name'] for actor in actor_manager.get_card_actors(card_id)]
        }
        
        print(f"   📤 Données d'export :")
        print(f"      Carte : {export_data['card_name']}")
        print(f"      Acteurs : {', '.join(export_data['actors'])}")
        
        if len(export_data['actors']) > 0:
            print("   ✅ Test 4 RÉUSSI")
            test4_ok = True
        else:
            print("   ❌ Test 4 ÉCHEC")
            test4_ok = False
    except Exception as e:
        print(f"   ❌ Erreur export : {e}")
        test4_ok = False
    
    # Résultats finaux
    print(f"\n" + "=" * 55)
    print("📊 RÉSULTATS DE VALIDATION :")
    print(f"   Test 1 (Liaison multiple)     : {'✅ RÉUSSI' if test1_ok else '❌ ÉCHEC'}")
    print(f"   Test 2 (Modification sélection): {'✅ RÉUSSI' if test2_ok else '❌ ÉCHEC'}")
    print(f"   Test 3 (Chargement liaisons)  : {'✅ RÉUSSI' if test3_ok else '❌ ÉCHEC'}")
    print(f"   Test 4 (Intégrité export)     : {'✅ RÉUSSI' if test4_ok else '❌ ÉCHEC'}")
    
    all_ok = test1_ok and test2_ok and test3_ok and test4_ok
    
    if all_ok:
        print(f"\n🎉 VALIDATION COMPLÈTE RÉUSSIE !")
        print(f"   La sélection multiple d'acteurs fonctionne parfaitement")
        print(f"   Toutes les fonctionnalités sont opérationnelles")
    else:
        print(f"\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print(f"   Vérifiez les erreurs ci-dessus")
    
    print("=" * 55)
    return all_ok


def demo_usage_examples():
    """Démonstration avec des exemples d'usage concrets."""
    
    print("\n🎮 EXEMPLES D'USAGE CONCRETS")
    print("=" * 40)
    
    ensure_db(DB_FILE)
    repo = CardRepo(DB_FILE)
    actor_manager = ActorManager(DB_FILE)
    
    # Exemple 1 : Carte commune Joueur-IA
    print("\n💫 Exemple 1 : Carte accessible au Joueur ET à l'IA")
    
    common_card = Card()
    common_card.name = "Potion de Soin"
    common_card.img = "potion_heal.png"
    common_card.description = "Restaure 50 HP. Utilisable par tous."
    common_card.powerblow = 2
    common_card.side = "joueur"
    common_card.rarity = "commun"
    
    card_id = repo.insert(common_card)
    
    # Lier aux deux acteurs principaux
    actors = actor_manager.list_actors()
    joueur_actor = next((a for a in actors if a['name'] == 'Joueur'), None)
    ia_actor = next((a for a in actors if a['name'] == 'IA'), None)
    
    if joueur_actor and ia_actor:
        actor_manager.link_card_to_actor(card_id, joueur_actor['id'])
        actor_manager.link_card_to_actor(card_id, ia_actor['id'])
        print(f"   ✅ Carte '{common_card.name}' liée à Joueur ET IA")
    
    # Exemple 2 : Carte de PNJ multiple
    print("\n🏪 Exemple 2 : Carte de PNJ (Marchand, Boss)")
    
    npc_card = Card()
    npc_card.name = "Attaque Coordonnée"
    npc_card.img = "coordinated_attack.png"
    npc_card.description = "Les PNJ attaquent ensemble."
    npc_card.powerblow = 8
    npc_card.side = "ia"
    npc_card.rarity = "rare"
    
    card_id2 = repo.insert(npc_card)
    
    # Lier aux PNJ
    marchand_actor = next((a for a in actors if a['name'] == 'Marchand'), None)
    boss_actor = next((a for a in actors if a['name'] == 'Boss'), None)
    
    if marchand_actor and boss_actor:
        actor_manager.link_card_to_actor(card_id2, marchand_actor['id'])
        actor_manager.link_card_to_actor(card_id2, boss_actor['id'])
        print(f"   ✅ Carte '{npc_card.name}' liée à Marchand ET Boss")
    
    # Exemple 3 : Carte universelle
    print("\n🌟 Exemple 3 : Carte universelle (tous les acteurs)")
    
    universal_card = Card()
    universal_card.name = "Équilibrage Cosmique"
    universal_card.img = "cosmic_balance.png"
    universal_card.description = "Affecte tous les acteurs du jeu."
    universal_card.powerblow = 15
    universal_card.side = "joueur"
    universal_card.rarity = "mythique"
    
    card_id3 = repo.insert(universal_card)
    
    # Lier à tous les acteurs
    for actor in actors:
        actor_manager.link_card_to_actor(card_id3, actor['id'])
    
    print(f"   ✅ Carte '{universal_card.name}' liée à TOUS les acteurs ({len(actors)})")
    
    print(f"\n📋 Récapitulatif des exemples créés :")
    for i, (card_id, card_name) in enumerate([(card_id, common_card.name), 
                                               (card_id2, npc_card.name), 
                                               (card_id3, universal_card.name)], 1):
        linked = actor_manager.get_card_actors(card_id)
        actors_names = [a['name'] for a in linked]
        print(f"   {i}. {card_name} → {', '.join(actors_names)}")
    
    print("\n✨ Ces exemples montrent la flexibilité du nouveau système !")


if __name__ == "__main__":
    print("🧪 VALIDATION SÉLECTION MULTIPLE D'ACTEURS")
    print("=" * 60)
    
    # Tests de validation
    validation_ok = test_integration_complete()
    
    # Exemples d'usage
    demo_usage_examples()
    
    print("\n" + "=" * 60)
    if validation_ok:
        print("🎉 VALIDATION TERMINÉE AVEC SUCCÈS !")
        print("   La sélection multiple d'acteurs est pleinement fonctionnelle")
        print("   Vous pouvez utiliser la nouvelle fonctionnalité en toute confiance")
    else:
        print("⚠️  VALIDATION INCOMPLÈTE")
        print("   Certains tests ont échoué, vérifiez les détails ci-dessus")
    
    print("\n🚀 Lancez l'application pour tester l'interface :")
    print("   python app_final.py")
    print("=" * 60)
