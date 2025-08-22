#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la standardisation des curseurs
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_curseurs_standardises():
    """Test de la standardisation des curseurs"""
    print("🎯 Test Curseurs Standardisés")
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
        root.title("🎚️ Test Curseurs Standardisés")
        
        print("\n📏 SPÉCIFICATIONS DES CURSEURS :")
        print("   🎛️ Longueur fixe : 199px")
        print("   📐 Marge droite : 45px")
        print("   📝 Texte au-dessus du curseur")
        print("   ↔️ Orientation : Horizontale")
        
        print("\n🎚️ CURSEURS À VÉRIFIER :")
        curseurs = [
            "Position X (Titre)",
            "Position Y (Titre)", 
            "Taille (Titre)",
            "Position X (Texte)",
            "Position Y (Texte)",
            "Largeur (Texte)",
            "Hauteur (Texte)",
            "Taille (Texte)",
            "Espacement (Lignes)"
        ]
        
        for i, curseur in enumerate(curseurs, 1):
            print(f"   {i}. ✅ {curseur}")
        
        editor = TextFormattingEditor(root, test_card.id, card_data)
        
        print("\n🎉 Interface standardisée ouverte ! Vérifiez que :")
        print("   ✅ Tous les curseurs font exactement 199px")
        print("   ✅ Le texte est positionné au-dessus de chaque curseur")
        print("   ✅ La valeur numérique a une marge de 45px à droite")
        print("   ✅ Tous les curseurs sont horizontaux")
        print("   ✅ L'interface est propre et bien alignée")
        print("   ✅ Les curseurs sont facilement manipulables")
        
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_curseurs_standardises()
