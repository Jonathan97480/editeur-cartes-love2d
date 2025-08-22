#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des corrections d'affichage - Image et curseurs
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_corrections_affichage():
    """Test des corrections d'affichage"""
    print("🎯 Test Corrections Affichage")
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
            'title_x': 75, 'title_y': 45, 'title_font': 'Arial', 'title_size': 18,
            'title_color': '#2c3e50', 'text_x': 60, 'text_y': 120,
            'text_width': 180, 'text_height': 200, 'text_font': 'Arial',
            'text_size': 11, 'text_color': '#34495e', 'text_align': 'left',
            'line_spacing': 1.3, 'text_wrap': 1
        }
        
        # Interface
        root = tk.Tk()
        root.title("🔧 Test Corrections Affichage")
        
        # Calculer les dimensions
        controls_width = (1182 - 60) // 4
        preview_width = ((1182 - 60) * 3) // 4
        slider_length = controls_width - 80
        
        print(f"📋 Zone contrôles: {controls_width}px")
        print(f"👁️ Zone aperçu: {preview_width}px") 
        print(f"🎚️ Longueur curseurs: {slider_length}px")
        
        editor = TextFormattingEditor(root, test_card.id, card_data)
        
        print("\n🎉 Interface corrigée ouverte ! Vérifiez que :")
        print("   ✅ L'image de la carte garde ses proportions")
        print("   ✅ L'image n'est pas déformée ou trop zoomée")
        print("   ✅ Les curseurs sont plus longs et utilisent mieux l'espace")
        print("   ✅ L'aperçu est plus grand et plus clair")
        print("   ✅ L'interface est bien équilibrée")
        
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_corrections_affichage()
