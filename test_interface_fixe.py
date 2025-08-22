#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'interface fixe 1182×878
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_interface_fixe():
    """Test de l'interface fixe avec dimensions optimisées"""
    print("🎯 Test Interface Fixe 1182×878")
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
        root.title("🧪 Test Interface 1182×878")
        
        # Afficher la taille de l'écran et calculer les dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1182
        window_height = 878
        
        print(f"📺 Taille de l'écran: {screen_width}x{screen_height}")
        print(f"🖼️ Taille fenêtre: {window_width}x{window_height}")
        
        # Calculer les zones
        controls_width = (window_width - 60) // 4  # 1/4 pour les contrôles
        preview_width = ((window_width - 60) * 3) // 4  # 3/4 pour l'aperçu
        
        print(f"📋 Zone contrôles: {controls_width}px (1/4)")
        print(f"👁️ Zone aperçu: {preview_width}px (3/4)")
        
        # Vérifier si la fenêtre rentre dans l'écran
        if window_width <= screen_width and window_height <= screen_height:
            print("✅ La fenêtre rentre dans l'écran")
        else:
            print("⚠️ La fenêtre risque de dépasser de l'écran")
        
        editor = TextFormattingEditor(root, test_card.id, card_data)
        
        print("\n🎉 Interface ouverte ! Vérifiez que :")
        print("   ✅ Fenêtre fixe 1182×878 pixels")
        print("   ✅ Contrôles à gauche (1/4 de la largeur)")
        print("   ✅ Aperçu à droite (3/4 de la largeur)")
        print("   ✅ Tous les curseurs visibles dans leur zone")
        print("   ✅ Aucun débordement de l'interface")
        print("   ✅ Image de carte bien proportionnée")
        
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_interface_fixe()
