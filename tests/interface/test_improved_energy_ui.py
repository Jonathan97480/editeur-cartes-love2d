#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'interface améliorée pour le positionnement de l'énergie
"""

import tkinter as tk
from lib.database import CardRepo
from lib.config import DB_FILE
from lib.text_formatting_editor import TextFormattingEditor

def test_improved_energy_interface():
    """Test de l'interface améliorée d'énergie"""
    print("🎯 TEST INTERFACE AMÉLIORÉE - POSITIONNEMENT ÉNERGIE")
    print("=" * 70)
    
    # Créer une fenêtre de test
    root = tk.Tk()
    root.title("Test Interface Énergie Améliorée")
    root.withdraw()  # Cacher la fenêtre principale
    
    # Créer le repo et récupérer une carte
    repo = CardRepo(DB_FILE)
    cards = repo.list_cards()
    
    if cards:
        card = cards[0]  # Prendre la première carte
        print(f"📝 Test avec la carte: {card.name}")
        print(f"   PowerBlow (énergie): {card.powerblow}")
        print(f"   Position initiale: ({card.energy_x}, {card.energy_y})")
        
        # Créer les données pour l'éditeur
        card_data = {
            'nom': card.name,
            'description': card.description,
            'img': card.img,
            'powerblow': card.powerblow,
            'title_x': card.title_x,
            'title_y': card.title_y,
            'title_font': card.title_font,
            'title_size': card.title_size,
            'title_color': card.title_color,
            'text_x': card.text_x,
            'text_y': card.text_y,
            'text_width': card.text_width,
            'text_height': card.text_height,
            'text_font': card.text_font,
            'text_size': card.text_size,
            'text_color': card.text_color,
            'text_align': card.text_align,
            'line_spacing': card.line_spacing,
            'text_wrap': card.text_wrap,
            'energy_x': card.energy_x,
            'energy_y': card.energy_y,
            'energy_font': card.energy_font,
            'energy_size': card.energy_size,
            'energy_color': card.energy_color
        }
        
        try:
            # Créer une classe repo personnalisée pour le test
            class TestRepo:
                def save_card(self, card_data):
                    print(f"💾 Sauvegarde simulée:")
                    print(f"   Position énergie finale: ({card_data.energy_x}, {card_data.energy_y})")
                    print(f"   Style: {card_data.energy_font} {card_data.energy_size}px {card_data.energy_color}")
                    return True
            
            test_repo = TestRepo()
            
            # Créer l'éditeur
            editor = TextFormattingEditor(
                parent=root, 
                card_id=card.id, 
                card_data=card_data, 
                repo=test_repo
            )
            
            print(f"✅ Interface améliorée créée avec succès!")
            print(f"\n🎯 NOUVELLES FONCTIONNALITÉS:")
            print(f"   📏 Curseurs X et Y pleine largeur (plus précis)")
            print(f"   📍 Boutons de préréglages pour positions courantes:")
            print(f"      - Haut Gauche, Centre, Droit")
            print(f"      - Milieu Gauche, Centre, Droit")
            print(f"   👁️ Aperçu visuel en temps réel")
            print(f"   💾 Sauvegarde automatique des paramètres")
            
            print(f"\n🎮 TESTEZ LES FONCTIONNALITÉS:")
            print(f"   1. Utilisez les curseurs X/Y pour ajuster précisément")
            print(f"   2. Cliquez sur les boutons de préréglages")
            print(f"   3. Observez l'aperçu en temps réel")
            print(f"   4. Modifiez la couleur et la taille")
            print(f"   5. Sauvegardez pour valider")
            
            # Lancer l'interface
            root.mainloop()
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'éditeur: {e}")
            import traceback
            traceback.print_exc()
            root.destroy()
    else:
        print("❌ Aucune carte trouvée pour le test")
        root.destroy()

if __name__ == "__main__":
    test_improved_energy_interface()
