#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la sauvegarde des paramètres de formatage
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_sauvegarde_formatage():
    """Test de la sauvegarde des paramètres de formatage"""
    print("🎯 Test Sauvegarde Formatage")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from lib.database import CardRepo, ensure_db
        from lib.text_formatting_editor import TextFormattingEditor
        from lib.config import DB_FILE
        from lib.database_simple import CardRepo as SimpleRepo
        
        # Configurer la base de données
        db_path = str(Path(__file__).parent / DB_FILE)
        ensure_db(db_path)
        repo = CardRepo(db_path)
        
        cards = repo.list_cards()
        if not cards:
            print("❌ Aucune carte trouvée")
            return False
        
        # Prendre la première carte
        test_card = cards[0]
        print(f"✅ Test avec la carte: {test_card.name}")
        
        # Vérifier que la carte existe dans le système simplifié
        simple_repo = SimpleRepo(str(Path(__file__).parent / "cartes.db"))
        simple_cards = simple_repo.list_cards()
        
        print(f"📊 Cartes dans système principal: {len(cards)}")
        print(f"📊 Cartes dans système formatage: {len(simple_cards)}")
        
        # Synchroniser si nécessaire
        if len(simple_cards) == 0:
            print("🔄 Synchronisation des cartes...")
            # Ajouter les cartes du système principal au système de formatage
            for card in cards:
                simple_card = simple_repo.get_by_name(card.name)
                if not simple_card:
                    # Créer une nouvelle carte dans le système de formatage
                    print(f"➕ Ajout de {card.name} au système de formatage")
        
        # Données de test avec des valeurs spécifiques pour la sauvegarde
        card_data = {
            'id': test_card.id,
            'nom': test_card.name,
            'description': test_card.description,
            'img': getattr(test_card, 'img', ''),
            'title_x': 123, 'title_y': 456, 'title_font': 'Verdana', 'title_size': 20,
            'title_color': '#ff0000', 'text_x': 789, 'text_y': 321,
            'text_width': 250, 'text_height': 180, 'text_font': 'Courier New',
            'text_size': 14, 'text_color': '#0000ff', 'text_align': 'center',
            'line_spacing': 1.8, 'text_wrap': 1
        }
        
        # Interface
        root = tk.Tk()
        root.title("💾 Test Sauvegarde Formatage")
        
        print("\n📝 VALEURS DE TEST POUR SAUVEGARDE :")
        print(f"   📍 Position titre : ({card_data['title_x']}, {card_data['title_y']})")
        print(f"   🎨 Police titre   : {card_data['title_font']} {card_data['title_size']}px")
        print(f"   🌈 Couleur titre  : {card_data['title_color']}")
        print(f"   📍 Position texte : ({card_data['text_x']}, {card_data['text_y']})")
        print(f"   📐 Taille texte   : {card_data['text_width']}×{card_data['text_height']}")
        print(f"   🎨 Police texte   : {card_data['text_font']} {card_data['text_size']}px")
        print(f"   🌈 Couleur texte  : {card_data['text_color']}")
        print(f"   ↔️ Alignement     : {card_data['text_align']}")
        print(f"   📏 Espacement     : {card_data['line_spacing']}")
        
        editor = TextFormattingEditor(root, test_card.id, card_data)
        
        print("\n🎉 Interface de test ouverte !")
        print("\n🧪 PROCÉDURE DE TEST :")
        print("   1. ✅ Vérifiez que les valeurs sont correctement affichées")
        print("   2. ✅ Modifiez quelques paramètres si vous voulez")
        print("   3. ✅ Cliquez sur '💾 Sauvegarder'")
        print("   4. ✅ Vérifiez qu'aucune erreur n'apparaît")
        print("   5. ✅ Confirmez le message de succès")
        
        print("\n🔧 SYSTÈME DE SAUVEGARDE :")
        print("   🗄️ Base de données : cartes.db")
        print("   📦 Système utilisé : database_simple.py")
        print("   🔄 Méthode : repo.update(card)")
        
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_sauvegarde_formatage()
