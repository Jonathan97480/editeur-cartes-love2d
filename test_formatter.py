#!/usr/bin/env python3
"""
Test de l'éditeur de formatage de texte
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import tkinter as tk
from database_simple import CardRepo, Card
from text_formatting_editor import TextFormattingEditor

def test_text_editor():
    print('🧪 Test de l\'éditeur de formatage de texte...')
    
    # Initialiser le repo
    repo = CardRepo('cartes.db')
    cards = repo.list_cards()
    
    if not cards:
        print('❌ Aucune carte trouvée pour le test')
        return
    
    card = cards[0]
    print(f'📝 Test avec la carte: {card.nom}')
    
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Test Éditeur de Formatage")
    root.geometry("300x200")
    
    def open_formatter():
        try:
            # Convertir la carte en dictionnaire pour l'éditeur
            card_data = card.to_dict()
            editor = TextFormattingEditor(root, card.id, card_data)
            print('✅ Éditeur de formatage ouvert!')
        except Exception as e:
            print(f'❌ Erreur: {e}')
            import traceback
            traceback.print_exc()
    
    # Bouton pour ouvrir l'éditeur
    btn = tk.Button(root, text="📝 Ouvrir Éditeur de Formatage", 
                    command=open_formatter, 
                    font=('Arial', 12), 
                    bg='lightblue',
                    pady=20)
    btn.pack(expand=True, pady=50)
    
    # Affichage des infos de la carte
    info_label = tk.Label(root, 
                          text=f"Carte: {card.nom}\nType: {card.type}\nRareté: {card.rarete}",
                          font=('Arial', 10))
    info_label.pack(pady=10)
    
    print('🚀 Interface de test lancée. Cliquez sur le bouton pour tester l\'éditeur.')
    root.mainloop()

if __name__ == "__main__":
    test_text_editor()
