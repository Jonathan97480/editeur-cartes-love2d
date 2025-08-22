#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test direct de l'éditeur de formatage sans migration complexe
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import tkinter as tk
from tkinter import ttk, messagebox

def test_direct_formatter():
    print("🎯 Test direct de l'éditeur de formatage")
    print("=" * 50)
    
    try:
        # Importer directement les modules nécessaires
        from lib.database_simple import CardRepo, Card
        from lib.text_formatting_editor import TextFormattingEditor
        from lib.config import DB_FILE
        
        # Créer l'interface principale
        root = tk.Tk()
        root.title("Test Direct - Éditeur de formatage")
        root.geometry("400x300")
        
        # Récupérer les cartes existantes
        repo = CardRepo(DB_FILE)
        cards = repo.list_cards()
        
        print(f"📊 Cartes disponibles: {len(cards)}")
        for card in cards:
            print(f"   - ID: {card.id}, Nom: '{card.nom}'")
        
        if not cards:
            messagebox.showerror("Erreur", "Aucune carte trouvée dans la base de données")
            root.destroy()
            return
        
        # Prendre la première carte pour le test
        test_card = cards[0]
        
        # Interface de test
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Test de l'éditeur de formatage", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(main_frame, text=f"Carte sélectionnée: {test_card.nom} (ID: {test_card.id})").pack(pady=5)
        
        def open_formatter():
            try:
                print(f"🎨 Ouverture de l'éditeur pour la carte ID {test_card.id}")
                
                # Préparer les données de la carte
                card_data = {
                    'id': test_card.id,
                    'nom': test_card.nom,
                    'description': test_card.description,
                    'img': test_card.img,
                    'title_x': test_card.title_x,
                    'title_y': test_card.title_y,
                    'title_font': test_card.title_font,
                    'title_size': test_card.title_size,
                    'title_color': test_card.title_color,
                    'text_x': test_card.text_x,
                    'text_y': test_card.text_y,
                    'text_width': test_card.text_width,
                    'text_height': test_card.text_height,
                    'text_font': test_card.text_font,
                    'text_size': test_card.text_size,
                    'text_color': test_card.text_color,
                    'text_align': test_card.text_align,
                    'line_spacing': test_card.line_spacing,
                    'text_wrap': test_card.text_wrap
                }
                
                # Créer l'éditeur
                editor = TextFormattingEditor(root, test_card.id, card_data)
                print("✅ Éditeur de formatage ouvert avec succès!")
                
                messagebox.showinfo("Succès", 
                    f"Éditeur ouvert pour la carte '{test_card.nom}'!\n"
                    f"L'erreur 'Carte non trouvée' est corrigée.")
                
            except Exception as e:
                print(f"❌ Erreur: {e}")
                messagebox.showerror("Erreur", f"Erreur lors de l'ouverture de l'éditeur:\n{e}")
        
        # Bouton de test
        ttk.Button(main_frame, text="🎨 Ouvrir l'éditeur de formatage", 
                  command=open_formatter).pack(pady=20)
        
        # Info
        info_text = f"""Informations sur la carte:
• Nom: {test_card.nom}
• Description: {test_card.description[:50]}{'...' if len(test_card.description) > 50 else ''}
• Position titre: ({test_card.title_x}, {test_card.title_y})
• Position texte: ({test_card.text_x}, {test_card.text_y})"""
        
        ttk.Label(main_frame, text=info_text, justify='left').pack(pady=10)
        
        print("✅ Interface de test créée")
        print("🎯 Cliquez sur le bouton pour tester l'éditeur")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_formatter()
