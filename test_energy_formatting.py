#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'éditeur de formatage pour vérifier la mémorisation des réglages d'énergie
"""
import sys
import os
sys.path.insert(0, 'lib')

from database import CardRepo
from config import DB_FILE
import tkinter as tk
from text_formatting_editor import TextFormattingEditor

def test_energy_formatting():
    """Test de l'éditeur de formatage avec les réglages d'énergie"""
    print("🧪 TEST ÉDITEUR DE FORMATAGE - RÉGLAGES ÉNERGIE")
    print("=" * 60)
    
    # Initialiser la base de données
    repo = CardRepo(DB_FILE)
    cards = repo.list_cards()
    
    if not cards:
        print("❌ Aucune carte trouvée pour le test")
        return
    
    test_card = cards[0]
    print(f"🎯 Carte de test: {test_card.name} (ID: {test_card.id})")
    
    # Récupérer les données de formatage actuelles
    import sqlite3
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT energy_x, energy_y, energy_font, energy_size, energy_color 
        FROM cards WHERE id = ?
    ''', (test_card.id,))
    
    current_energy = cursor.fetchone()
    if current_energy:
        print(f"📊 Réglages d'énergie actuels:")
        print(f"   Position: ({current_energy[0]}, {current_energy[1]})")
        print(f"   Police: {current_energy[2]}, Taille: {current_energy[3]}")
        print(f"   Couleur: {current_energy[4]}")
    
    # Préparer les données pour l'éditeur
    card_data = {
        'id': test_card.id,
        'nom': test_card.name,
        'description': test_card.description,
        'img': test_card.img,
        'powerblow': test_card.powerblow,
        'energy_x': current_energy[0] if current_energy else 25,
        'energy_y': current_energy[1] if current_energy else 25,
        'energy_font': current_energy[2] if current_energy else 'Arial',
        'energy_size': current_energy[3] if current_energy else 14,
        'energy_color': current_energy[4] if current_energy else '#FFFFFF',
        # Autres champs par défaut
        'title_x': 50, 'title_y': 30, 'title_font': 'Arial', 'title_size': 16, 'title_color': '#000000',
        'text_x': 50, 'text_y': 100, 'text_width': 200, 'text_height': 150, 
        'text_font': 'Arial', 'text_size': 12, 'text_color': '#000000',
        'text_align': 'left', 'line_spacing': 1.2, 'text_wrap': True
    }
    
    # Créer une fenêtre Tkinter pour l'éditeur
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    
    try:
        # Créer un repo de formatage
        class TestFormattingRepo:
            def __init__(self, main_repo):
                self.main_repo = main_repo
                self.db_file = main_repo.db_file
            
            def get_card(self, card_id):
                card = self.main_repo.get(card_id)
                if card:
                    class FormattingCard:
                        pass
                    fc = FormattingCard()
                    fc.id = card.id
                    fc.nom = card.name
                    fc.description = card.description
                    fc.img = card.img
                    return fc
                return None
            
            def save_card(self, card_data):
                print(f"💾 Sauvegarde des données:")
                print(f"   Énergie: pos({card_data.energy_x}, {card_data.energy_y})")
                print(f"   Police: {card_data.energy_font}, Taille: {card_data.energy_size}")
                print(f"   Couleur: {card_data.energy_color}")
                
                # Sauvegarder dans la base
                conn = sqlite3.connect(self.main_repo.db_file)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE cards SET 
                        energy_x=?, energy_y=?, energy_font=?, energy_size=?, energy_color=?
                    WHERE id=?
                """, (
                    card_data.energy_x, card_data.energy_y, card_data.energy_font,
                    card_data.energy_size, card_data.energy_color, card_data.id
                ))
                conn.commit()
                conn.close()
        
        formatting_repo = TestFormattingRepo(repo)
        
        # Créer l'éditeur
        print(f"\n🎨 Ouverture de l'éditeur de formatage...")
        editor = TextFormattingEditor(root, test_card.id, card_data, formatting_repo)
        
        print(f"✅ Éditeur créé avec succès!")
        print(f"📝 L'éditeur devrait afficher les réglages d'énergie actuels")
        print(f"💡 Fermez l'éditeur pour terminer le test")
        
        # L'éditeur s'ouvre dans sa propre fenêtre
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()
    
    print(f"\n✅ Test terminé!")

if __name__ == "__main__":
    test_energy_formatting()
