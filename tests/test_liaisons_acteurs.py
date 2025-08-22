#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de vérification des liaisons carte-acteur
"""

import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.database import CardRepo, ensure_db, Card
from lib.actors import ActorManager
from lib.config import DB_FILE

def test_card_actor_links():
    """Vérifie les liaisons entre cartes et acteurs."""
    
    print("🔗 VÉRIFICATION DES LIAISONS CARTE-ACTEUR")
    print("=" * 55)
    
    # Initialiser la base
    ensure_db(DB_FILE)
    repo = CardRepo(DB_FILE)
    actor_manager = ActorManager(DB_FILE)
    
    # Obtenir toutes les cartes
    all_cards = repo.list_cards()
    print(f"📋 Nombre total de cartes : {len(all_cards)}")
    
    # Vérifier chaque carte
    cards_with_actors = 0
    cards_without_actors = 0
    
    print(f"\n🔍 Détail des liaisons :")
    print("-" * 55)
    
    for card in all_cards:
        try:
            # Obtenir les acteurs liés à cette carte
            linked_actors = actor_manager.get_card_actors(card.id)
            
            if linked_actors:
                cards_with_actors += 1
                actor_names = [actor['name'] for actor in linked_actors]
                status = "✅"
                actors_str = ", ".join(actor_names)
            else:
                cards_without_actors += 1
                status = "❌"
                actors_str = "AUCUN ACTEUR LIÉ"
            
            print(f"{status} Carte {card.id:2d} : {card.name[:30]:30} → {actors_str}")
            
        except Exception as e:
            print(f"💥 Erreur carte {card.id} : {e}")
    
    # Résumé
    print("-" * 55)
    print(f"📊 RÉSUMÉ :")
    print(f"   Cartes avec acteurs    : {cards_with_actors}")
    print(f"   Cartes sans acteurs    : {cards_without_actors}")
    print(f"   Total                  : {len(all_cards)}")
    
    # Vérifier les acteurs disponibles
    print(f"\n🎭 ACTEURS DISPONIBLES :")
    actors = actor_manager.list_actors()
    for actor in actors:
        # Compter les cartes liées à cet acteur
        linked_cards = []
        for card in all_cards:
            card_actors = actor_manager.get_card_actors(card.id)
            if any(a['id'] == actor['id'] for a in card_actors):
                linked_cards.append(card)
        
        print(f"   - {actor['name']:12} : {len(linked_cards)} cartes liées")
    
    return cards_without_actors == 0

def fix_orphan_cards():
    """Corrige les cartes orphelines en leur assignant des acteurs."""
    
    print(f"\n🔧 CORRECTION DES CARTES ORPHELINES")
    print("=" * 40)
    
    # Initialiser
    ensure_db(DB_FILE)
    repo = CardRepo(DB_FILE)
    actor_manager = ActorManager(DB_FILE)
    
    # Obtenir toutes les cartes
    all_cards = repo.list_cards()
    actors = actor_manager.list_actors()
    
    if not actors:
        print("❌ Aucun acteur disponible pour assigner")
        return False
    
    # Créer un mapping side -> acteur par défaut
    default_actors = {}
    for actor in actors:
        if actor['name'] == 'Joueur':
            default_actors['joueur'] = actor['id']
        elif actor['name'] == 'IA':
            default_actors['ia'] = actor['id']
    
    # Si pas d'acteurs Joueur/IA, utiliser les premiers disponibles
    if 'joueur' not in default_actors and actors:
        default_actors['joueur'] = actors[0]['id']
    if 'ia' not in default_actors and len(actors) > 1:
        default_actors['ia'] = actors[1]['id']
    elif 'ia' not in default_actors:
        default_actors['ia'] = actors[0]['id']
    
    print(f"🎯 Acteurs par défaut configurés :")
    for side, actor_id in default_actors.items():
        actor_name = next((a['name'] for a in actors if a['id'] == actor_id), 'Inconnu')
        print(f"   {side:8} → {actor_name}")
    
    # Corriger les cartes orphelines
    fixed_count = 0
    
    for card in all_cards:
        linked_actors = actor_manager.get_card_actors(card.id)
        
        if not linked_actors:
            # Carte orpheline, assigner un acteur basé sur son 'side'
            if card.side in default_actors:
                actor_id = default_actors[card.side]
                actor_manager.link_card_to_actor(card.id, actor_id)
                
                actor_name = next((a['name'] for a in actors if a['id'] == actor_id), 'Inconnu')
                print(f"   ✅ Carte {card.id} '{card.name}' → {actor_name}")
                fixed_count += 1
            else:
                print(f"   ⚠️  Carte {card.id} '{card.name}' : side '{card.side}' non reconnu")
    
    print(f"\n📊 CORRECTION TERMINÉE :")
    print(f"   Cartes corrigées : {fixed_count}")
    
    return True

def create_test_card_with_actor():
    """Crée une carte de test avec un acteur spécifique."""
    
    print(f"\n🧪 CRÉATION CARTE DE TEST")
    print("=" * 30)
    
    # Initialiser
    ensure_db(DB_FILE)
    repo = CardRepo(DB_FILE)
    actor_manager = ActorManager(DB_FILE)
    
    # Créer une carte de test
    test_card = Card()
    test_card.name = "Test Liaison Acteur"
    test_card.img = "test_liaison.png"
    test_card.description = "Carte créée pour tester les liaisons acteur-carte"
    test_card.powerblow = 5
    test_card.side = "joueur"  # Legacy, mais on va lier à un acteur spécifique
    test_card.rarity = "commun"
    
    # Sauvegarder la carte
    card_id = repo.insert(test_card)
    print(f"✅ Carte créée avec ID : {card_id}")
    
    # Obtenir un acteur à lier
    actors = actor_manager.list_actors()
    if not actors:
        print("❌ Aucun acteur disponible")
        return False
    
    # Lier à Barbus si disponible, sinon au premier acteur
    target_actor = None
    for actor in actors:
        if actor['name'] == 'Barbus':
            target_actor = actor
            break
    
    if not target_actor:
        target_actor = actors[0]
    
    # Créer la liaison
    actor_manager.link_card_to_actor(card_id, target_actor['id'])
    print(f"✅ Carte liée à l'acteur : {target_actor['name']}")
    
    # Vérifier la liaison
    linked_actors = actor_manager.get_card_actors(card_id)
    if linked_actors:
        print(f"✅ Vérification : {len(linked_actors)} acteur(s) lié(s)")
        for actor in linked_actors:
            print(f"   - {actor['name']}")
        return True
    else:
        print("❌ Échec de la liaison")
        return False

if __name__ == "__main__":
    print("🔗 DIAGNOSTIC COMPLET LIAISONS CARTE-ACTEUR")
    print("=" * 60)
    
    # Test 1 : Vérification des liaisons existantes
    print("\n1️⃣ VÉRIFICATION DES LIAISONS EXISTANTES")
    links_ok = test_card_actor_links()
    
    # Test 2 : Correction des cartes orphelines
    if not links_ok:
        print("\n2️⃣ CORRECTION DES CARTES ORPHELINES")
        fix_orphan_cards()
        
        # Re-vérifier après correction
        print("\n🔄 RE-VÉRIFICATION APRÈS CORRECTION")
        links_ok = test_card_actor_links()
    
    # Test 3 : Créer une carte de test
    print("\n3️⃣ TEST DE CRÉATION AVEC LIAISON")
    test_creation_ok = create_test_card_with_actor()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS FINAUX :")
    print(f"   Liaisons existantes    : {'✅ OK' if links_ok else '❌ PROBLÈME'}")
    print(f"   Test création          : {'✅ OK' if test_creation_ok else '❌ PROBLÈME'}")
    
    if links_ok and test_creation_ok:
        print("\n🎉 SYSTÈME DE LIAISONS FONCTIONNEL !")
        print("   Les cartes sont correctement liées aux acteurs")
        print("   L'affichage dans l'interface devrait maintenant montrer les vrais acteurs")
    else:
        print("\n⚠️  PROBLÈMES DÉTECTÉS")
        print("   Vérifiez les erreurs ci-dessus")
    
    print("=" * 60)
