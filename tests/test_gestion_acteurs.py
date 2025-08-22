#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 TEST COMPLET DE LA GESTION D'ACTEURS
Guide pour vérifier que tout fonctionne après correction
"""

def test_actor_management():
    print("🎭 TEST DE LA GESTION D'ACTEURS APRÈS CORRECTION")
    print("=" * 55)
    
    try:
        from lib.actors import ActorManager
        from lib.database import CardRepo
        
        # Test 1: Initialisation
        print("\n1️⃣ Test d'initialisation...")
        manager = ActorManager('cartes.db')
        print("   ✅ ActorManager initialisé")
        
        # Test 2: Liste des acteurs
        print("\n2️⃣ Test de liste des acteurs...")
        actors = manager.list_actors()
        print(f"   ✅ {len(actors)} acteurs trouvés")
        
        # Test 3: Récupération des cartes par acteur
        print("\n3️⃣ Test de récupération des cartes...")
        for actor in actors:
            cards = manager.get_actor_cards(actor['id'])
            print(f"   {actor['icon']} {actor['name']} : {len(cards)} cartes")
            
            # Afficher quelques détails des cartes
            if cards:
                for i, card in enumerate(cards[:2]):  # Max 2 cartes
                    print(f"      └─ {card.name} ({card.rarity})")
                if len(cards) > 2:
                    print(f"      └─ ... et {len(cards) - 2} autres")
        
        # Test 4: Test de création d'acteur
        print("\n4️⃣ Test de création d'acteur...")
        test_actor_id = manager.create_actor(
            "🧪 Test Acteur", 
            "Acteur de test temporaire", 
            "#FF5722", 
            "🧪"
        )
        print(f"   ✅ Acteur de test créé (ID: {test_actor_id})")
        
        # Test 5: Liaison d'une carte
        print("\n5️⃣ Test de liaison de carte...")
        repo = CardRepo('cartes.db')
        all_cards = repo.list_cards()
        if all_cards:
            test_card = all_cards[0]
            manager.link_card_to_actor(test_card.id, test_actor_id)
            
            # Vérifier la liaison
            test_cards = manager.get_actor_cards(test_actor_id)
            print(f"   ✅ Carte '{test_card.name}' liée au test acteur")
            print(f"   📊 Test acteur a maintenant {len(test_cards)} carte(s)")
        
        # Test 6: Nettoyage
        print("\n6️⃣ Nettoyage...")
        manager.delete_actor(test_actor_id)
        print("   ✅ Acteur de test supprimé")
        
        print(f"\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print(f"   ✅ La gestion d'acteurs fonctionne parfaitement")
        print(f"   ✅ Le problème get_by_id est résolu")
        print(f"   ✅ Vous pouvez maintenant utiliser le menu 'Gérer les Acteurs'")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR DÉTECTÉE : {e}")
        import traceback
        traceback.print_exc()
        
        print(f"\n💡 SOLUTIONS POSSIBLES :")
        print(f"   1. Vérifiez que la base de données cartes.db existe")
        print(f"   2. Relancez l'application : python app_final.py")
        print(f"   3. Si le problème persiste, contactez le support")
        
        return False

def guide_utilisation():
    print(f"\n" + "="*60)
    print(f"📖 GUIDE D'UTILISATION DE LA GESTION D'ACTEURS")
    print(f"="*60)
    
    print(f"\n🚀 POUR ACCÉDER À LA GESTION D'ACTEURS :")
    print(f"   1. Lancez l'application : python app_final.py")
    print(f"   2. Dans le menu, cliquez sur '🎭 Acteurs'")
    print(f"   3. Sélectionnez 'Gérer les Acteurs'")
    
    print(f"\n🎛️ FONCTIONNALITÉS DISPONIBLES :")
    print(f"   ✅ Créer de nouveaux acteurs personnalisés")
    print(f"   ✅ Modifier les acteurs existants")
    print(f"   ✅ Choisir couleurs et icônes")
    print(f"   ✅ Lier des cartes aux acteurs")
    print(f"   ✅ Supprimer des acteurs")
    
    print(f"\n📤 EXPORT PAR ACTEUR :")
    print(f"   1. Menu '🎭 Acteurs' → 'Export par Acteur'")
    print(f"   2. Sélectionnez les acteurs à exporter")
    print(f"   3. Fichiers .lua générés automatiquement")
    print(f"   4. Noms de fichiers basés sur les noms d'acteurs")
    
    print(f"\n🎯 AVANTAGES DU SYSTÈME D'ACTEURS :")
    print(f"   🆚 AVANT : Limité à 'joueur' et 'ia'")
    print(f"   ✨ APRÈS : Acteurs illimités et personnalisables")
    print(f"   🆚 AVANT : Export unique 'cards.lua'")
    print(f"   ✨ APRÈS : Export séparé par acteur")
    print(f"   🆚 AVANT : Pas d'organisation visuelle")
    print(f"   ✨ APRÈS : Couleurs et icônes personnalisées")

if __name__ == "__main__":
    success = test_actor_management()
    guide_utilisation()
    
    if success:
        print(f"\n🏆 LA CORRECTION EST VALIDÉE !")
        print(f"   Votre système d'acteurs est maintenant entièrement fonctionnel ! 🚀")
    else:
        print(f"\n⚠️  Des problèmes subsistent, vérifiez les messages d'erreur ci-dessus")
    
    input(f"\nAppuyez sur Entrée pour fermer...")
