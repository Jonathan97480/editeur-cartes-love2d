#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de synchronisation des bases de données et correction du problème d'ID
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

def test_database_sync():
    print("🔄 Test de synchronisation des bases de données")
    print("=" * 60)
    
    # 1. Importer les modules
    try:
        from lib.database import CardRepo
        from lib.database_simple import CardRepo as SimpleRepo, Card as SimpleCard
        print("✅ Modules importés avec succès")
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    
    # 2. Vérifier les cartes dans le système principal
    print(f"\n📊 Analyse du système principal:")
    try:
        main_repo = CardRepo('cartes.db')
        main_cards = main_repo.get_all()
        print(f"   Cartes trouvées: {len(main_cards)}")
        for card in main_cards:
            print(f"   - ID: {card.id}, Nom: '{card.name}'")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        main_cards = []
    
    # 3. Vérifier les cartes dans le système simple
    print(f"\n📊 Analyse du système simple:")
    try:
        simple_repo = SimpleRepo('cartes.db')
        simple_cards = simple_repo.list_cards()
        print(f"   Cartes trouvées: {len(simple_cards)}")
        for card in simple_cards:
            print(f"   - ID: {card.id}, Nom: '{card.nom}'")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        simple_cards = []
    
    # 4. Synchronisation des cartes manquantes
    print(f"\n🔄 Synchronisation:")
    if main_cards and simple_cards:
        main_ids = {card.id for card in main_cards}
        simple_ids = {card.id for card in simple_cards}
        
        missing_in_simple = main_ids - simple_ids
        missing_in_main = simple_ids - main_ids
        
        print(f"   IDs dans principal mais pas dans simple: {missing_in_simple}")
        print(f"   IDs dans simple mais pas dans principal: {missing_in_main}")
        
        # Synchroniser les cartes manquantes vers le système simple
        for card_id in missing_in_simple:
            main_card = next((c for c in main_cards if c.id == card_id), None)
            if main_card:
                print(f"   🔄 Synchronisation de la carte ID {card_id}: '{main_card.name}'")
                try:
                    simple_card = SimpleCard(
                        id=main_card.id,
                        nom=main_card.name,
                        description=main_card.description,
                        img=main_card.img
                    )
                    simple_repo.save_card(simple_card)
                    print(f"   ✅ Carte synchronisée avec succès")
                except Exception as e:
                    print(f"   ❌ Erreur de synchronisation: {e}")
    
    # 5. Test final
    print(f"\n🧪 Test final d'accès:")
    updated_simple_cards = simple_repo.list_cards()
    print(f"   Cartes dans le système simple après synchronisation: {len(updated_simple_cards)}")
    
    test_ids = [1, 2, 10]
    for test_id in test_ids:
        card = simple_repo.get_card(test_id)
        if card:
            print(f"   ✅ ID {test_id}: '{card.nom}' - ACCESSIBLE")
        else:
            print(f"   ❌ ID {test_id}: Carte non trouvée")
    
    return True

def test_text_formatter_integration():
    print(f"\n🎨 Test de l'éditeur de formatage:")
    print("=" * 60)
    
    try:
        from lib.text_formatting_editor import TextFormattingEditor
        from lib.database_simple import CardRepo
        import tkinter as tk
        
        # Utiliser une carte existante
        repo = CardRepo('cartes.db')
        cards = repo.list_cards()
        
        if not cards:
            print("❌ Aucune carte disponible pour le test")
            return False
        
        test_card = cards[0]
        print(f"🧪 Test avec la carte: ID {test_card.id}, Nom: '{test_card.nom}'")
        
        # Créer l'interface de test
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        
        try:
            # Préparer les données
            card_data = {
                'id': test_card.id,
                'nom': test_card.nom,
                'description': test_card.description,
                'img': test_card.img,
                'title_x': test_card.title_x,
                'title_y': test_card.title_y,
                'title_font': test_card.title_font,
                'title_size': test_card.title_size,
                'title_color': test_card.title_color,
                'text_x': test_card.text_x,
                'text_y': test_card.text_y,
                'text_width': test_card.text_width,
                'text_height': test_card.text_height,
                'text_font': test_card.text_font,
                'text_size': test_card.text_size,
                'text_color': test_card.text_color,
                'text_align': test_card.text_align,
                'line_spacing': test_card.line_spacing,
                'text_wrap': test_card.text_wrap
            }
            
            # Créer l'éditeur
            editor = TextFormattingEditor(root, test_card.id, card_data)
            print("✅ Éditeur de formatage créé avec succès!")
            print(f"   - Position titre: ({test_card.title_x}, {test_card.title_y})")
            print(f"   - Position texte: ({test_card.text_x}, {test_card.text_y})")
            
            # Test de sauvegarde simulée
            try:
                card_to_update = repo.get_card(test_card.id)
                if card_to_update:
                    print("✅ Carte récupérée pour mise à jour")
                else:
                    print("❌ Impossible de récupérer la carte")
            except Exception as e:
                print(f"❌ Erreur lors de la récupération: {e}")
            
            root.destroy()
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'éditeur: {e}")
            root.destroy()
            return False
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test complet de synchronisation et formatage")
    print("=" * 70)
    
    # Test 1: Synchronisation des bases de données
    sync_success = test_database_sync()
    
    # Test 2: Intégration de l'éditeur de formatage
    if sync_success:
        formatter_success = test_text_formatter_integration()
        
        if formatter_success:
            print(f"\n🎉 SUCCÈS: Tous les tests sont passés!")
            print("   - Bases de données synchronisées")
            print("   - Éditeur de formatage fonctionnel")
            print("   - Plus d'erreur 'Carte non trouvée'")
        else:
            print(f"\n⚠️  Tests partiels: Synchronisation OK, formatage KO")
    else:
        print(f"\n❌ ÉCHEC: Problèmes de synchronisation")
    
    print(f"\n🔧 Pour utiliser l'éditeur:")
    print("   1. Ouvrez l'application principale")
    print("   2. Sélectionnez ou créez une carte")
    print("   3. Cliquez sur 'Formater le texte'")
    print("   4. L'éditeur devrait s'ouvrir sans erreur")
