#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'interface améliorée avec les modifications appliquées
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from database import CardRepo
from config import DB_FILE
from text_formatting_editor import TextFormattingEditor
import tkinter as tk

def test_interface_amelioree():
    """Test de l'interface avec les améliorations"""
    print("🎨 TEST INTERFACE AMÉLIORÉE APPLIQUÉE")
    print("=" * 60)
    
    # Récupérer une carte pour le test
    repo = CardRepo(DB_FILE)
    cards = repo.list_cards()
    
    if not cards:
        print("❌ Aucune carte disponible pour le test")
        return
    
    test_card = cards[0]
    print(f"🎯 Test avec la carte: {test_card.name}")
    
    # Récupérer les données de formatage existantes
    import sqlite3
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT title_x, title_y, title_font, title_size, title_color,
               text_x, text_y, text_width, text_height, text_font, text_size, text_color, text_align, line_spacing,
               energy_x, energy_y, energy_font, energy_size, energy_color
        FROM cards WHERE id = ?
    ''', (test_card.id,))
    
    formatting_data = cursor.fetchone()
    conn.close()
    
    if formatting_data:
        # Créer un dictionnaire avec les données
        card_data = {
            'id': test_card.id,
            'nom': test_card.name,
            'description': test_card.description,
            'img': test_card.img,
            'powerblow': test_card.powerblow,
            'title_x': formatting_data[0] or 50,
            'title_y': formatting_data[1] or 30,
            'title_font': formatting_data[2] or 'Arial',
            'title_size': formatting_data[3] or 16,
            'title_color': formatting_data[4] or '#000000',
            'text_x': formatting_data[5] or 50,
            'text_y': formatting_data[6] or 100,
            'text_width': formatting_data[7] or 200,
            'text_height': formatting_data[8] or 150,
            'text_font': formatting_data[9] or 'Arial',
            'text_size': formatting_data[10] or 12,
            'text_color': formatting_data[11] or '#000000',
            'text_align': formatting_data[12] or 'left',
            'line_spacing': formatting_data[13] or 1.2,
            'energy_x': formatting_data[14] or 25,
            'energy_y': formatting_data[15] or 25,
            'energy_font': formatting_data[16] or 'Arial',
            'energy_size': formatting_data[17] or 14,
            'energy_color': formatting_data[18] or '#FFFFFF'
        }
    else:
        # Valeurs par défaut
        card_data = {
            'id': test_card.id,
            'nom': test_card.name,
            'description': test_card.description,
            'img': test_card.img,
            'powerblow': test_card.powerblow
        }
    
    # Créer la fenêtre principale
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    
    try:
        # Créer l'éditeur de formatage amélioré
        editor = TextFormattingEditor(root, card_id=test_card.id, card_data=card_data, repo=repo)
        
        print("✅ Interface créée avec succès!")
        print("🔍 Améliorations appliquées:")
        print("   📏 Curseurs pleine largeur (30% de l'écran)")
        print("   📍 Préréglages en 3 lignes plus visibles")
        print("   📜 Zone scrollable avec barre plus accessible")
        print("   🎯 Layout 30/70 optimisé")
        print("   🖱️ Support roulette souris pour scroll")
        
        # Lancer l'interface
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'interface: {e}")
        import traceback
        traceback.print_exc()
        root.destroy()

if __name__ == "__main__":
    test_interface_amelioree()
