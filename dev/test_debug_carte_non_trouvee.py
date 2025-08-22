#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Debug - Problème "Carte non trouvée" dans l'éditeur de formatage
====================================================================

Ce test reproduit spécifiquement le problème signalé par l'utilisateur.
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire lib au path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "lib"))

import tkinter as tk
from database_simple import CardRepo, Card
from text_formatting_editor import TextFormattingEditor

def test_card_not_found_issue():
    """Test pour reproduire le problème 'Carte non trouvée'"""
    print("🔍 TEST DEBUG - Problème 'Carte non trouvée'")
    print("=" * 60)
    
    # Utiliser la vraie base de données
    db_path = project_root / "cartes.db"
    repo = CardRepo(str(db_path))
    
    # Lister les cartes existantes
    cards = repo.list_cards()
    print(f"📊 Cartes en base : {len(cards)}")
    
    if not cards:
        print("❌ Aucune carte en base pour le test")
        return
        
    # Prendre la première carte
    test_card = cards[0]
    print(f"✅ Carte de test : ID={test_card.id}, Nom='{test_card.nom}'")
    
    # Préparer les données comme l'application principale
    card_data = {
        'nom': test_card.nom,
        'description': test_card.description,
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
    
    print(f"🗄️ Données préparées pour la carte ID {test_card.id}")
    
    # Créer l'interface comme dans l'application
    root = tk.Tk()
    root.title("Test Debug Éditeur")
    root.geometry("400x300")
    
    def open_editor():
        """Ouvre l'éditeur comme le ferait l'application"""
        try:
            print(f"\n🚀 Ouverture éditeur pour carte ID: {test_card.id}")
            editor = TextFormattingEditor(root, test_card.id, card_data)
            print("✅ Éditeur ouvert avec succès")
            
            # Simuler un changement et une sauvegarde
            def test_save():
                print("\n💾 Test de sauvegarde...")
                editor.title_x_var.set(100)  # Modifier une valeur
                editor.save_formatting()  # Ici on devrait voir le problème
                
            # Ajouter un bouton de test de sauvegarde
            test_btn = tk.Button(editor.window, text="🔍 Tester Sauvegarde", command=test_save)
            test_btn.pack(pady=10)
            
        except Exception as e:
            print(f"❌ Erreur ouverture éditeur : {e}")
            import traceback
            traceback.print_exc()
    
    # Interface de test
    tk.Label(root, text="Test Debug - Éditeur de Formatage", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(root, text=f"Carte: {test_card.nom} (ID: {test_card.id})").pack(pady=5)
    
    tk.Button(root, text="🎨 Ouvrir Éditeur Formatage", command=open_editor, 
              font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)
    
    tk.Button(root, text="❌ Fermer", command=root.quit,
              font=("Arial", 10)).pack(pady=10)
    
    print("\n🎮 Interface de test lancée")
    print("📋 Instructions :")
    print("   1. Cliquez sur 'Ouvrir Éditeur Formatage'")
    print("   2. Dans l'éditeur, cliquez sur 'Tester Sauvegarde'")
    print("   3. Observez si le message 'Carte non trouvée' apparaît")
    
    root.mainloop()

if __name__ == "__main__":
    test_card_not_found_issue()
