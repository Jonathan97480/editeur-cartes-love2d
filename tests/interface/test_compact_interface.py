#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'interface compacte
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_compact_interface():
    """Test de l'interface compacte"""
    print("🎯 Test de l'interface compacte")
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
            test_card = cards[0]  # Prendre n'importe quelle carte
        
        print(f"✅ Test avec la carte: {test_card.name}")
        
        # Données de test
        card_data = {
            'id': test_card.id,
            'nom': test_card.name,
            'description': test_card.description,
            'img': getattr(test_card, 'img', ''),
            'title_x': 50, 'title_y': 30, 'title_font': 'Arial', 'title_size': 16,
            'title_color': '#000000', 'text_x': 50, 'text_y': 100,
            'text_width': 200, 'text_height': 150, 'text_font': 'Arial',
            'text_size': 12, 'text_color': '#000000', 'text_align': 'left',
            'line_spacing': 1.2, 'text_wrap': 1
        }
        
        # Interface
        root = tk.Tk()
        root.title("🧪 Test Interface Compacte")
        
        # Afficher la taille de l'écran
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        print(f"📺 Taille de l'écran: {screen_width}x{screen_height}")
        
        editor = TextFormattingEditor(root, test_card.id, card_data)
        
        print("🎉 Interface ouverte ! Vérifiez que :")
        print("   ✅ La fenêtre rentre entièrement à l'écran")
        print("   ✅ Toutes les barres de défilement sont visibles")
        print("   ✅ Les poignées des barres sont accessibles")
        print("   ✅ L'interface est compacte mais utilisable")
        print("   ✅ Vous pouvez faire défiler les contrôles")
        
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_compact_interface()
