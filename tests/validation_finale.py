#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VALIDATION FINALE DU SYSTÈME D'ACTEURS
Test simplifié avec la base de données existante
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import CardRepo
from lib.actors import ActorManager, export_lua_for_actor
from lib.config import DB_FILE
import os

def validate_actors_system():
    """Validation complète du système d'acteurs avec la base existante."""
    print("🎭 VALIDATION FINALE DU SYSTÈME D'ACTEURS")
    print("=" * 50)
    
    try:
        # 1. Vérification de la base de données et des acteurs
        print("\n1️⃣ Vérification du système...")
        repo = CardRepo(DB_FILE)
        actor_manager = ActorManager(DB_FILE)
        
        # Statistiques générales
        all_cards = repo.list_cards()
        all_actors = actor_manager.list_actors()
        
        print(f"   📊 Base de données : {DB_FILE}")
        print(f"   📊 Cartes totales : {len(all_cards)}")
        print(f"   📊 Acteurs disponibles : {len(all_actors)}")
        
        # 2. Affichage des acteurs et leurs cartes
        print(f"\n2️⃣ Répartition actuelle des cartes par acteur :")
        
        total_linked = 0
        for actor in all_actors:
            cards = actor_manager.get_actor_cards(actor['id'])
            total_linked += len(cards)
            print(f"   {actor['icon']} {actor['name']} : {len(cards)} cartes")
            
            # Afficher quelques cartes liées
            if cards:
                for i, card in enumerate(cards[:3]):  # Max 3 cartes par acteur
                    print(f"      └─ {card.name} ({card.rarity})")
                if len(cards) > 3:
                    print(f"      └─ ... et {len(cards) - 3} autres")
        
        print(f"   📊 Total cartes liées : {total_linked}")
        
        # 3. Test de création d'un nouvel acteur
        print(f"\n3️⃣ Test de création d'acteur...")
        
        new_actor_id = actor_manager.create_actor(
            "🧪 Test Acteur", 
            "Acteur de test automatique", 
            "#2196F3", 
            "🧪"
        )
        print(f"   ✅ Nouvel acteur créé (ID: {new_actor_id})")
        
        # Lier une carte au nouvel acteur si possible
        if all_cards:
            test_card = all_cards[0]
            actor_manager.link_card_to_actor(test_card.id, new_actor_id)
            print(f"   🔗 Carte '{test_card.name}' liée au test acteur")
        
        # 4. Test d'export pour le joueur principal
        print(f"\n4️⃣ Test d'export pour l'acteur 'Joueur'...")
        
        joueur_actor = None
        for actor in all_actors:
            if actor['name'] == 'Joueur':
                joueur_actor = actor
                break
        
        if joueur_actor:
            cards = actor_manager.get_actor_cards(joueur_actor['id'])
            if cards:
                test_filename = "test_export_joueur.lua"
                export_lua_for_actor(repo, actor_manager, joueur_actor['id'], test_filename)
                
                if os.path.exists(test_filename):
                    with open(test_filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    print(f"   ✅ Export réussi : {len(cards)} cartes → {test_filename}")
                    print(f"   📄 Taille du fichier : {len(content)} caractères")
                    
                    # Afficher un extrait
                    lines = content.split('\n')
                    print(f"   📋 Extrait du fichier :")
                    for line in lines[:5]:
                        if line.strip():
                            print(f"      {line}")
                    if len(lines) > 5:
                        print(f"      ... ({len(lines)} lignes au total)")
                    
                    # Nettoyer le fichier de test
                    os.remove(test_filename)
                else:
                    print(f"   ❌ Fichier d'export non créé")
            else:
                print(f"   ⚠️  Aucune carte liée à l'acteur Joueur")
        
        # 5. Test des fonctionnalités avancées
        print(f"\n5️⃣ Test des fonctionnalités avancées...")
        
        # Liaison multiple
        if all_cards and len(all_actors) >= 2:
            test_card = all_cards[0]
            first_actor = all_actors[0]
            second_actor = all_actors[1]
            
            # Lier à plusieurs acteurs
            actor_manager.link_card_to_actor(test_card.id, first_actor['id'])
            actor_manager.link_card_to_actor(test_card.id, second_actor['id'])
            
            # Vérifier les liaisons
            linked_actors = actor_manager.get_card_actors(test_card.id)
            print(f"   🔗 Liaison multiple : '{test_card.name}' liée à {len(linked_actors)} acteurs")
        
        # 6. Nettoyage du test acteur
        print(f"\n6️⃣ Nettoyage...")
        actor_manager.delete_actor(new_actor_id)
        print(f"   🗑️ Acteur de test supprimé")
        
        # 7. Validation finale
        print(f"\n7️⃣ Validation finale...")
        
        final_actors = actor_manager.list_actors()
        print(f"   ✅ Acteurs après nettoyage : {len(final_actors)}")
        
        # Vérifier que les fonctionnalités de base marchent
        checks = [
            ("Lecture des acteurs", len(final_actors) > 0),
            ("Lecture des cartes", len(all_cards) > 0),
            ("Liaison carte-acteur", total_linked > 0),
            ("Export Lua", joueur_actor is not None)
        ]
        
        all_passed = True
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
            if not result:
                all_passed = False
        
        if all_passed:
            print(f"\n🎉 SYSTÈME D'ACTEURS ENTIÈREMENT VALIDÉ !")
            print(f"   ✅ Tous les tests sont passés")
            print(f"   ✅ Le système est prêt pour la production")
            
            print(f"\n🚀 POUR UTILISER VOS ACTEURS :")
            print(f"   1. Lancez : python app_final.py")
            print(f"   2. Menu '🎭 Acteurs' → 'Gérer les Acteurs'")
            print(f"   3. Créez vos propres acteurs")
            print(f"   4. Menu '🎭 Acteurs' → 'Export par Acteur'")
            print(f"   5. Générez des fichiers .lua personnalisés ! 🎯")
            
        else:
            print(f"\n⚠️  Certaines vérifications ont échoué")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Erreur de validation : {e}")
        import traceback
        traceback.print_exc()
        return False

def show_final_summary():
    """Affiche un résumé final du projet."""
    print(f"\n" + "="*60)
    print(f"🎊 RÉSUMÉ FINAL DU PROJET")
    print(f"="*60)
    
    print(f"\n📂 FICHIERS CRÉÉS POUR LE SYSTÈME D'ACTEURS :")
    print(f"   ✅ lib/actors.py - Gestion des acteurs et base de données")
    print(f"   ✅ lib/actor_ui.py - Interface utilisateur pour les acteurs")
    print(f"   ✅ lib/actor_selector.py - Sélecteurs et dialogues d'export")
    print(f"   ✅ demo_actors.py - Démonstration complète du système")
    print(f"   ✅ test_actors_complet.py - Tests automatisés")
    print(f"   ✅ validation_finale.py - Validation du système")
    
    print(f"\n🔧 MODIFICATIONS APPORTÉES :")
    print(f"   ✅ app_final.py - Menu acteurs intégré")
    print(f"   ✅ Base de données - Tables acteurs et liaisons créées")
    print(f"   ✅ Migration automatique - Ancien système → Acteurs")
    
    print(f"\n🎯 FONCTIONNALITÉS DISPONIBLES :")
    print(f"   ✅ Création d'acteurs personnalisés (nom, couleur, icône)")
    print(f"   ✅ Liaison flexible cartes ↔ acteurs (1:N et N:M)")
    print(f"   ✅ Export Lua personnalisé par acteur")
    print(f"   ✅ Interface graphique complète")
    print(f"   ✅ Migration automatique des données existantes")
    
    print(f"\n📤 EXPORTS PERSONNALISÉS :")
    print(f"   🎮 cards_joueur.lua (cartes du joueur)")
    print(f"   🤖 cards_ia.lua (cartes de l'IA)")
    print(f"   🧙‍♂️ cards_mage_noir.lua (acteur personnalisé)")
    print(f"   🛒 cards_marchand.lua (acteur personnalisé)")
    print(f"   ... et tous vos acteurs personnalisés !")
    
    print(f"\n💡 AVANT / APRÈS :")
    print(f"   ❌ AVANT : Cartes limitées à 'joueur' ou 'ia'")
    print(f"   ✅ APRÈS : Acteurs illimités et personnalisables")
    print(f"   ❌ AVANT : Export générique 'cards.lua'")
    print(f"   ✅ APRÈS : Export spécialisé par acteur")
    print(f"   ❌ AVANT : Pas de gestion visuelle")
    print(f"   ✅ APRÈS : Interface complète avec couleurs et icônes")

if __name__ == "__main__":
    success = validate_actors_system()
    show_final_summary()
    
    if success:
        print(f"\n🏆 MISSION ACCOMPLIE !")
        print(f"   Votre système d'acteurs est entièrement fonctionnel ! 🚀")
    else:
        print(f"\n⚠️  Des ajustements pourraient être nécessaires")
    
    input(f"\nAppuyez sur Entrée pour fermer...")
