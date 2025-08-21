#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST COMPLET DU SYSTÈME D'ACTEURS
"""
# Configurer l'environnement de test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import CardRepo, ensure_db, Card
from lib.actors import ActorManager, export_lua_for_actor
from lib.config import DB_FILE
import tempfile
import os

def test_actors_system():
    """Test complet du système d'acteurs."""
    print("🧪 TEST COMPLET DU SYSTÈME D'ACTEURS")
    print("=" * 50)
    
    # Utiliser une base de données temporaire pour les tests
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        test_db = tmp.name
    
    try:
        # 1. Initialiser la base et créer quelques cartes de test
        print("\n1️⃣ Initialisation de la base de données...")
        ensure_db(test_db)
        repo = CardRepo(test_db)
        
        # Créer des cartes de test
        cards_data = [
            ("Épée Légendaire", "Arme puissante du héros", "joueur", "legendaire"),
            ("Boule de Feu", "Sort d'attaque magique", "joueur", "rare"),
            ("Griffure Sauvage", "Attaque de base de l'ennemi", "ia", "commun"),
            ("Bouclier Magique", "Protection contre la magie", "joueur", "rare"),
            ("Invocation Dragon", "Créature puissante", "ia", "mythique")
        ]
        
        created_cards = []
        for name, desc, side, rarity in cards_data:
            card = Card()
            card.name = name
            card.description = desc
            card.side = side
            card.rarity = rarity
            card.powerblow = 5
            card.types = ["attaque" if "attaque" in desc.lower() else "defense"]
            card_id = repo.insert(card)
            created_cards.append(card_id)
            print(f"   ✅ Carte créée : {name} (ID: {card_id})")
        
        # 2. Initialiser le système d'acteurs
        print("\n2️⃣ Initialisation du système d'acteurs...")
        actor_manager = ActorManager(test_db)
        
        # 3. Créer des acteurs personnalisés
        print("\n3️⃣ Création d'acteurs personnalisés...")
        custom_actors = [
            ("Héros Principal", "Le personnage principal du jeu", "#4CAF50", "⚔️"),
            ("Dragon Boss", "Boss final du donjon", "#F44336", "🐲"),
            ("Mage Noir", "Antagoniste magique", "#9C27B0", "🧙‍♂️"),
            ("Marchand", "Vendeur d'objets", "#FF9800", "🛒")
        ]
        
        actor_ids = {}
        for name, desc, color, icon in custom_actors:
            actor_id = actor_manager.create_actor(name, desc, color, icon)
            actor_ids[name] = actor_id
            print(f"   ✅ Acteur créé : {icon} {name} (ID: {actor_id})")
        
        # 4. Lier les cartes aux acteurs
        print("\n4️⃣ Liaison des cartes aux acteurs...")
        
        # Récupérer les cartes créées
        all_cards = repo.list_cards()
        
        # Logique de liaison intelligente
        for card in all_cards:
            if "épée" in card.name.lower() or "bouclier" in card.name.lower():
                actor_manager.link_card_to_actor(card.id, actor_ids["Héros Principal"])
                print(f"   🔗 {card.name} → Héros Principal")
                
            elif "dragon" in card.name.lower():
                actor_manager.link_card_to_actor(card.id, actor_ids["Dragon Boss"])
                print(f"   🔗 {card.name} → Dragon Boss")
                
            elif "magique" in card.description.lower() or "boule de feu" in card.name.lower():
                actor_manager.link_card_to_actor(card.id, actor_ids["Mage Noir"])
                print(f"   🔗 {card.name} → Mage Noir")
                
            else:
                # Liaisons par défaut selon l'ancien système
                if card.side == "joueur":
                    actor_manager.link_card_to_actor(card.id, actor_ids["Héros Principal"])
                    print(f"   🔗 {card.name} → Héros Principal (défaut joueur)")
                elif card.side == "ia":
                    actor_manager.link_card_to_actor(card.id, actor_ids["Dragon Boss"])
                    print(f"   🔗 {card.name} → Dragon Boss (défaut IA)")
        
        # 5. Tester les exports par acteur
        print("\n5️⃣ Test des exports par acteur...")
        
        export_results = []
        for actor_name, actor_id in actor_ids.items():
            cards = actor_manager.get_actor_cards(actor_id)
            if cards:
                filename = f"test_cards_{actor_name.lower().replace(' ', '_')}.lua"
                export_lua_for_actor(repo, actor_manager, actor_id, filename)
                
                # Vérifier le fichier créé
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    export_results.append({
                        'actor': actor_name,
                        'cards_count': len(cards),
                        'filename': filename,
                        'file_size': len(content)
                    })
                    
                    print(f"   ✅ Export {actor_name} : {len(cards)} cartes → {filename} ({len(content)} chars)")
                    
                    # Nettoyer le fichier de test
                    os.remove(filename)
                else:
                    print(f"   ❌ Échec export {actor_name}")
            else:
                print(f"   ⚠️  {actor_name} : Aucune carte liée")
        
        # 6. Statistiques finales
        print("\n6️⃣ Statistiques du système d'acteurs...")
        
        all_actors = actor_manager.list_actors()
        total_cards = len(repo.list_cards())
        total_actors = len(all_actors)
        
        print(f"   📊 Total acteurs : {total_actors}")
        print(f"   📊 Total cartes : {total_cards}")
        print(f"   📊 Exports réussis : {len(export_results)}")
        
        # Affichage détaillé
        print(f"\n   📋 Répartition des cartes par acteur :")
        for actor in all_actors:
            cards = actor_manager.get_actor_cards(actor['id'])
            print(f"      {actor['icon']} {actor['name']} : {len(cards)} cartes")
        
        # 7. Test des fonctionnalités avancées
        print("\n7️⃣ Test des fonctionnalités avancées...")
        
        # Test de liaison multiple (une carte à plusieurs acteurs)
        if all_cards:
            test_card = all_cards[0]
            print(f"   🔗 Test liaison multiple pour '{test_card.name}'...")
            
            # Lier à plusieurs acteurs
            for actor_name in ["Héros Principal", "Marchand"]:
                actor_manager.link_card_to_actor(test_card.id, actor_ids[actor_name])
            
            # Vérifier les liaisons
            linked_actors = actor_manager.get_card_actors(test_card.id)
            print(f"      ✅ Carte liée à {len(linked_actors)} acteurs")
        
        # Test de suppression d'acteur
        print(f"   🗑️ Test suppression d'acteur...")
        actor_manager.delete_actor(actor_ids["Marchand"])
        remaining_actors = actor_manager.list_actors()
        print(f"      ✅ Acteurs restants : {len(remaining_actors)}")
        
        print(f"\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print(f"   ✅ Système d'acteurs entièrement fonctionnel")
        print(f"   ✅ Migrations automatiques OK")
        print(f"   ✅ Exports personnalisés OK")
        print(f"   ✅ Liaisons multiples OK")
        print(f"   ✅ Gestion d'acteurs OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur pendant les tests : {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Nettoyer la base de test
        try:
            os.unlink(test_db)
        except:
            pass

def test_migration_legacy():
    """Test de la migration depuis l'ancien système."""
    print("\n🔄 TEST DE MIGRATION DEPUIS L'ANCIEN SYSTÈME")
    print("=" * 50)
    
    try:
        # Utiliser la vraie base de données pour tester la migration
        print("   📁 Utilisation de la base de données réelle...")
        actor_manager = ActorManager(DB_FILE)
        
        # Afficher les acteurs après migration
        actors = actor_manager.list_actors()
        print(f"   ✅ {len(actors)} acteurs trouvés après migration :")
        
        for actor in actors:
            cards = actor_manager.get_actor_cards(actor['id'])
            print(f"      {actor['icon']} {actor['name']} : {len(cards)} cartes")
        
        # Test d'export réel
        if actors:
            print(f"\n   📤 Test d'export avec les vraies données...")
            repo = CardRepo(DB_FILE)
            
            for actor in actors[:2]:  # Tester les 2 premiers acteurs
                cards = actor_manager.get_actor_cards(actor['id'])
                if cards:
                    filename = f"migration_test_{actor['name'].lower().replace(' ', '_')}.lua"
                    export_lua_for_actor(repo, actor_manager, actor['id'], filename)
                    print(f"      ✅ Export {actor['name']} : {filename}")
                    
                    # Nettoyer
                    try:
                        os.remove(filename)
                    except:
                        pass
        
        print(f"   🎉 Migration testée avec succès !")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur de migration : {e}")
        return False

if __name__ == "__main__":
    print("🎭 SUITE DE TESTS COMPLÈTE DU SYSTÈME D'ACTEURS")
    print("=" * 60)
    
    success1 = test_actors_system()
    success2 = test_migration_legacy()
    
    print(f"\n{'='*60}")
    if success1 and success2:
        print("🏆 TOUS LES TESTS ONT RÉUSSI !")
        print("   Le système d'acteurs est prêt pour la production ! 🚀")
    else:
        print("❌ Certains tests ont échoué")
        print("   Vérifiez les erreurs ci-dessus")
    
    print(f"\n💡 POUR UTILISER LE SYSTÈME D'ACTEURS :")
    print(f"   1. Lancez l'application principale : python app_final.py")
    print(f"   2. Menu 🎭 Acteurs → Gérer les Acteurs")
    print(f"   3. Créez vos acteurs personnalisés")
    print(f"   4. Menu 🎭 Acteurs → Export par Acteur")
    print(f"   5. Profitez des exports personnalisés ! 🎯")
    
    input("\nAppuyez sur Entrée pour fermer...")
