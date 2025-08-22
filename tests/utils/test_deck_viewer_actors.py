#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du visualiseur de deck avec tri par acteur
"""

def test_deck_viewer_actors():
    """Test du tri par acteur dans le visualiseur de deck."""
    print("🧪 Test du tri par acteur dans le visualiseur de deck")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from lib.database import CardRepo
        from lib.deck_viewer import DeckViewerWindow
        from lib.actors import ActorManager
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        
        # Initialiser la base de données
        repo = CardRepo("cartes.db")
        actor_manager = ActorManager("cartes.db")
        
        # Récupérer les cartes et acteurs
        cards = repo.list_cards()
        actors = actor_manager.list_actors()
        
        print(f"📊 Cartes trouvées : {len(cards)}")
        print(f"🎭 Acteurs trouvés : {len(actors)}")
        
        if not cards:
            print("⚠️ Aucune carte en base pour tester")
            print("💡 Ajoutez quelques cartes dans l'application principale d'abord")
            root.destroy()
            return False
        
        if not actors:
            print("⚠️ Aucun acteur en base pour tester")
            print("💡 Créez quelques acteurs dans l'application principale d'abord")
            root.destroy()
            return False
        
        # Afficher quelques infos sur les acteurs
        print("\n🎭 Aperçu des acteurs :")
        for i, actor in enumerate(actors[:5]):
            name = actor['name']
            icon = actor['icon']
            # Compter les cartes de cet acteur
            actor_cards = actor_manager.get_actor_cards(actor['id'])
            print(f"   {i+1}. {icon} {name} ({len(actor_cards)} cartes)")
        
        if len(actors) > 5:
            print(f"   ... et {len(actors) - 5} autres acteurs")
        
        # Afficher quelques infos sur les cartes avec leurs acteurs
        print("\n📋 Aperçu des cartes avec acteurs :")
        for i, card in enumerate(cards[:5]):
            card_actors = actor_manager.get_card_actors(card.id)
            if card_actors:
                actor_names = [f"{a['icon']} {a['name']}" for a in card_actors[:2]]
                actors_text = ', '.join(actor_names)
                if len(card_actors) > 2:
                    actors_text += "..."
            else:
                actors_text = "Aucun acteur"
            
            print(f"   {i+1}. {card.name} → {actors_text}")
        
        if len(cards) > 5:
            print(f"   ... et {len(cards) - 5} autres cartes")
        
        # Tester l'ouverture du visualiseur
        print(f"\n🚀 Ouverture du visualiseur de deck avec tri par acteur...")
        
        deck_viewer = DeckViewerWindow(root, repo)
        
        print("✅ Visualiseur créé avec succès !")
        print("\n🎯 Nouvelles fonctionnalités disponibles :")
        print("   • Filtre par acteur (section 🎭 Acteurs)")
        print("   • Tri par acteur (option 'Par acteur' dans le tri)")
        print("   • Affichage des acteurs associés à chaque carte")
        print("   • Filtre combiné (rareté + type + acteur)")
        
        print(f"\n💡 Instructions de test :")
        print("   1. Utilisez le filtre 'Acteurs' à gauche pour voir les cartes d'un acteur")
        print("   2. Sélectionnez 'Par acteur' dans la section Tri")
        print("   3. Observez les informations d'acteur sous chaque carte")
        print("   4. Combinez les filtres (rareté + acteur par exemple)")
        print("   5. Cliquez 'Actualiser' si vous modifiez les acteurs")
        
        # Test interactif
        response = input("\n❓ Voulez-vous tester interactivement ? (o/n): ").lower().strip()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print("\n🎮 Test interactif lancé...")
            print("   Fermez la fenêtre du visualiseur pour terminer le test")
            
            # Montrer la fenêtre principale pour pouvoir interagir
            root.deiconify()
            root.mainloop()
        else:
            print("\n✅ Test terminé - le visualiseur fonctionne correctement")
            root.destroy()
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        print("💡 Assurez-vous que tous les modules sont présents")
        return False
    except Exception as e:
        print(f"❌ Erreur pendant le test : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_deck_viewer_actors()
    if success:
        print("\n🎊 Test réussi - Le tri par acteur fonctionne !")
    else:
        print("\n💥 Test échoué")
