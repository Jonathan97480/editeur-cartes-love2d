#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'éditeur de formatage avec support du coût en énergie
"""

import tkinter as tk
from lib.database import CardRepo
from lib.config import DB_FILE
from lib.text_formatting_editor import TextFormattingEditor

def test_energy_formatting():
    """Test de l'éditeur de formatage avec énergie"""
    print("⚡ TEST DE L'ÉDITEUR AVEC FORMATAGE ÉNERGIE")
    print("=" * 60)
    
    # Créer une fenêtre de test
    root = tk.Tk()
    root.title("Test Éditeur avec Énergie")
    root.withdraw()  # Cacher la fenêtre principale
    
    # Créer le repo et récupérer une carte
    repo = CardRepo(DB_FILE)
    cards = repo.list_cards()
    
    if cards:
        card = cards[0]  # Prendre la première carte
        print(f"📝 Test avec la carte: {card.name}")
        print(f"   PowerBlow (énergie): {card.powerblow}")
        print(f"   Position énergie actuelle: ({card.energy_x}, {card.energy_y})")
        print(f"   Style énergie: {card.energy_font} {card.energy_size}px {card.energy_color}")
        
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
                    print(f"   Titre: ({card_data.title_x}, {card_data.title_y})")
                    print(f"   Texte: ({card_data.text_x}, {card_data.text_y})")
                    print(f"   Énergie: ({card_data.energy_x}, {card_data.energy_y}) {card_data.energy_color}")
                    return True
            
            test_repo = TestRepo()
            
            # Créer l'éditeur
            editor = TextFormattingEditor(
                parent=root, 
                card_id=card.id, 
                card_data=card_data, 
                repo=test_repo
            )
            
            print(f"✅ Éditeur de formatage avec énergie créé avec succès!")
            print(f"   - Section énergie disponible avec contrôles de position")
            print(f"   - Aperçu visuel du coût en énergie sur la carte")
            print(f"   - Sauvegarde intégrée des paramètres d'énergie")
            print(f"\n🎯 Interface ouverte - testez les contrôles d'énergie!")
            
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
    test_energy_formatting()
