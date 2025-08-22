#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de visibilité des boutons de validation
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_boutons_visibles():
    """Test de visibilité des boutons de validation"""
    print("🎯 Test Visibilité des Boutons")
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
        
        # Données de test
        card_data = {
            'id': test_card.id,
            'nom': test_card.name,
            'description': test_card.description,
            'img': getattr(test_card, 'img', ''),
            'title_x': 150, 'title_y': 100, 'title_font': 'Arial', 'title_size': 18,
            'title_color': '#2c3e50', 'text_x': 100, 'text_y': 200,
            'text_width': 180, 'text_height': 200, 'text_font': 'Arial',
            'text_size': 11, 'text_color': '#34495e', 'text_align': 'left',
            'line_spacing': 1.3, 'text_wrap': 1
        }
        
        # Interface
        root = tk.Tk()
        root.title("🔍 Test Boutons Visibles")
        
        # Informations sur les dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1182
        window_height = 780  # Nouvelle hauteur réduite
        
        print(f"📺 Taille de l'écran : {screen_width}×{screen_height}")
        print(f"🖼️ Taille fenêtre : {window_width}×{window_height}")
        print(f"📏 Hauteur réduite : 878 → 780px (-98px)")
        print(f"📏 Canvas contrôles : 800 → 680px (-120px)")
        print(f"📏 Aperçu : 820 → 700px (-120px)")
        
        # Calcul de centrage
        pos_x = (screen_width // 2) - (window_width // 2)
        pos_y = (screen_height // 2) - (window_height // 2)
        print(f"📍 Position calculée : x={pos_x}, y={pos_y}")
        
        # Vérification si la fenêtre rentre entièrement
        if pos_y + window_height <= screen_height:
            print("✅ La fenêtre rentre entièrement dans l'écran")
        else:
            print("⚠️ La fenêtre pourrait encore dépasser")
        
        editor = TextFormattingEditor(root, test_card.id, card_data)
        
        print("\n🎉 Interface optimisée ouverte !")
        print("\n🔍 VÉRIFIEZ QUE :")
        print("   ✅ La fenêtre est entièrement visible")
        print("   ✅ Les 3 boutons sont visibles en bas :")
        print("      - 💾 Sauvegarder (gauche)")
        print("      - 🔄 Réinitialiser (centre)")
        print("      - ❌ Annuler (droite)")
        print("   ✅ Tous les contrôles restent accessibles")
        print("   ✅ L'aperçu reste suffisamment grand")
        
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_boutons_visibles()
