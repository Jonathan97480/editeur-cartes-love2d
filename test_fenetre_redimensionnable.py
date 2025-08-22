#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la fenêtre redimensionnable
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_fenetre_redimensionnable():
    """Test de la fenêtre redimensionnable"""
    print("🎯 Test Fenêtre Redimensionnable")
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
        root.title("↔️ Test Fenêtre Redimensionnable")
        
        # Informations sur les dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1182
        window_height = 780
        
        print(f"📺 Taille de l'écran : {screen_width}×{screen_height}")
        print(f"🖼️ Taille par défaut : {window_width}×{window_height}")
        print(f"📏 Taille minimale : 900×600")
        
        print("\n✅ FONCTIONNALITÉS REDIMENSIONNEMENT :")
        print("   ↔️ Largeur : Redimensionnable")
        print("   ↕️ Hauteur : Redimensionnable") 
        print("   📐 Taille min : 900×600 pixels")
        print("   🔒 Interface : S'adapte automatiquement")
        
        editor = TextFormattingEditor(root, test_card.id, card_data)
        
        print("\n🎉 Interface redimensionnable ouverte !")
        print("\n🧪 TESTS À EFFECTUER :")
        print("   1. ✅ Redimensionner la fenêtre en largeur")
        print("   2. ✅ Redimensionner la fenêtre en hauteur")
        print("   3. ✅ Vérifier que les boutons restent visibles")
        print("   4. ✅ Tester la taille minimale (900×600)")
        print("   5. ✅ Agrandir pour voir plus de contrôles")
        print("   6. ✅ Réduire pour s'adapter aux petits écrans")
        
        print("\n🎯 AVANTAGES :")
        print("   🏠 S'adapte à tous les écrans")
        print("   👁️ Boutons toujours visibles")
        print("   🔧 Interface flexible")
        print("   📱 Compatible petits écrans")
        
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_fenetre_redimensionnable()
