#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de l'éditeur de formatage
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_final_editor():
    """Test final de l'éditeur"""
    print("🎯 Test final de l'éditeur de formatage")
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
        
        # Trouver une carte avec une image
        card_with_image = None
        for card in cards:
            if card.img and card.img.strip():
                card_with_image = card
                break
        
        if not card_with_image:
            print("❌ Aucune carte avec image trouvée")
            return False
        
        print(f"✅ Test avec la carte: {card_with_image.name}")
        
        # Données comme dans l'application réelle
        card_data = {
            'id': card_with_image.id,
            'nom': card_with_image.name,
            'description': card_with_image.description,
            'img': card_with_image.img,
            'title_x': getattr(card_with_image, 'title_x', 50),
            'title_y': getattr(card_with_image, 'title_y', 30),
            'title_font': getattr(card_with_image, 'title_font', 'Arial'),
            'title_size': getattr(card_with_image, 'title_size', 16),
            'title_color': getattr(card_with_image, 'title_color', '#000000'),
            'text_x': getattr(card_with_image, 'text_x', 50),
            'text_y': getattr(card_with_image, 'text_y', 100),
            'text_width': getattr(card_with_image, 'text_width', 200),
            'text_height': getattr(card_with_image, 'text_height', 150),
            'text_font': getattr(card_with_image, 'text_font', 'Arial'),
            'text_size': getattr(card_with_image, 'text_size', 12),
            'text_color': getattr(card_with_image, 'text_color', '#000000'),
            'text_align': getattr(card_with_image, 'text_align', 'left'),
            'line_spacing': getattr(card_with_image, 'line_spacing', 1.2),
            'text_wrap': getattr(card_with_image, 'text_wrap', 1)
        }
        
        # Interface
        root = tk.Tk()
        root.title("🎯 Test Final - Éditeur de Formatage")
        
        editor = TextFormattingEditor(root, card_with_image.id, card_data)
        
        print("🎉 Éditeur ouvert ! Vérifiez que :")
        print("   ✅ L'image de la carte s'affiche correctement")
        print("   ✅ Le titre et le texte sont positionnés sur l'image")
        print("   ✅ Les contrôles permettent de modifier les positions")
        print("   ✅ L'aperçu se met à jour en temps réel")
        
        # Lancer l'interface
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_final_editor()
    if success:
        print("\n🎉 Test terminé ! L'éditeur de formatage devrait maintenant afficher correctement les images de cartes.")
    else:
        print("\n❌ Test échoué.")
