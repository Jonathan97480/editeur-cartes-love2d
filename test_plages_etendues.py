#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des plages étendues des curseurs de position
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_plages_etendues():
    """Test des plages étendues des curseurs"""
    print("🎯 Test Plages Étendues des Curseurs")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from lib.database import CardRepo, ensure_db
        from lib.text_formatting_editor import TextFormattingEditor
        from lib.config import DB_FILE
        
        # Configurer la base de données
        db_path = str(Path(__file__).parent / DB_FILE)
        ensure_db(db_path)
        repo = CardRepo(db_path)
        
        cards = repo.list_cards()
        if not cards:
            print("❌ Aucune carte trouvée")
            return False
        
        # Prendre la première carte avec image
        test_card = None
        for card in cards:
            if card.img and card.img.strip():
                test_card = card
                break
        
        if not test_card:
            test_card = cards[0]
        
        print(f"✅ Test avec la carte: {test_card.name}")
        
        # Données de test avec valeurs élevées pour tester les nouvelles plages
        card_data = {
            'id': test_card.id,
            'nom': test_card.name,
            'description': test_card.description,
            'img': getattr(test_card, 'img', ''),
            'title_x': 250, 'title_y': 400, 'title_font': 'Arial', 'title_size': 18,
            'title_color': '#2c3e50', 'text_x': 300, 'text_y': 500,
            'text_width': 180, 'text_height': 200, 'text_font': 'Arial',
            'text_size': 11, 'text_color': '#34495e', 'text_align': 'left',
            'line_spacing': 1.3, 'text_wrap': 1
        }
        
        # Interface
        root = tk.Tk()
        root.title("📏 Test Plages Étendues")
        
        print("\n📏 NOUVELLES PLAGES DE CURSEURS :")
        print("   📍 Position X (Titre) : 0 → 500px")
        print("   📍 Position Y (Titre) : 0 → 600px")
        print("   📍 Position X (Texte) : 0 → 500px")
        print("   📍 Position Y (Texte) : 0 → 700px")
        print("   📐 Largeur (Texte)    : 50 → 400px")
        print("   📐 Hauteur (Texte)    : 50 → 300px")
        
        print("\n🎯 TAILLE TYPIQUE D'UNE CARTE :")
        print("   📱 Largeur  : ~400-500px")
        print("   📱 Hauteur  : ~600-800px")
        
        print("\n✅ AMÉLIORATIONS :")
        print("   🔄 Position Y titre : 300 → 600px (+100%)")
        print("   🔄 Position Y texte : 400 → 700px (+75%)")
        print("   🔄 Position X titre : 300 → 500px (+67%)")
        print("   🔄 Position X texte : 300 → 500px (+67%)")
        
        editor = TextFormattingEditor(root, test_card.id, card_data)
        
        print("\n🎉 Interface avec plages étendues ouverte !")
        print("\n🧪 TESTS À EFFECTUER :")
        print("   1. ✅ Déplacer le titre jusqu'en bas de la carte")
        print("   2. ✅ Déplacer le texte jusqu'en bas de la carte") 
        print("   3. ✅ Positionner les éléments sur toute la largeur")
        print("   4. ✅ Vérifier que les valeurs maximales sont accessibles")
        print("   5. ✅ Confirmer que le positionnement est précis")
        
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_plages_etendues()
