#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de l'éditeur de formatage depuis l'interface principale
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import tkinter as tk
from tkinter import ttk, messagebox

def test_main_interface():
    print("🎯 Test de l'éditeur de formatage dans l'interface principale")
    print("=" * 70)
    
    try:
        # Importer les composants nécessaires
        from lib.database import CardRepo, ensure_db
        from lib.ui_components import CardForm
        from lib.database_simple import CardRepo as SimpleRepo
        
        # Préparer la base de données
        ensure_db('cartes.db')
        
        # Créer l'interface de test
        root = tk.Tk()
        root.title("Test - Éditeur de formatage")
        root.geometry("800x600")
        
        # Préparer le repo
        repo = CardRepo('cartes.db')
        
        # Créer un frame de test
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Test de l'éditeur de formatage", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Créer le formulaire de carte
        form_frame = ttk.LabelFrame(main_frame, text="Formulaire de carte", padding=10)
        form_frame.pack(fill='both', expand=True, pady=10)
        
        def on_saved():
            print("✅ Carte sauvegardée - callback appelé")
        
        form = CardForm(form_frame, repo, on_saved=on_saved)
        form.pack(fill='both', expand=True)
        
        # Vérifier les cartes existantes
        simple_repo = SimpleRepo('cartes.db')
        cards = simple_repo.list_cards()
        
        if cards:
            # Charger la première carte pour test
            test_card = cards[0]
            print(f"📋 Chargement de la carte de test: ID {test_card.id}, Nom: '{test_card.nom}'")
            
            # Simuler le chargement de la carte dans le formulaire
            form.current_id = test_card.id
            form.name_var.set(test_card.nom)
            form.description_var.set(test_card.description)
            
            # Frame d'instructions
            instructions_frame = ttk.Frame(main_frame)
            instructions_frame.pack(fill='x', pady=10)
            
            ttk.Label(instructions_frame, 
                     text=f"Carte chargée : '{test_card.nom}' (ID: {test_card.id})",
                     font=('Arial', 12, 'bold')).pack()
            
            ttk.Label(instructions_frame, 
                     text="Cliquez sur 'Formater le texte' pour tester l'éditeur",
                     foreground='blue').pack()
            
            # Fonction de test pour le bouton
            def test_formatter():
                try:
                    print(f"🧪 Test du formatage pour la carte ID {form.current_id}")
                    form.open_text_formatter()
                    print("✅ Éditeur de formatage ouvert avec succès!")
                except Exception as e:
                    print(f"❌ Erreur lors de l'ouverture de l'éditeur: {e}")
                    messagebox.showerror("Erreur", f"Erreur lors du test:\n{e}")
            
            # Bouton de test
            test_btn = ttk.Button(instructions_frame, 
                                 text="🎨 Tester l'éditeur de formatage",
                                 command=test_formatter)
            test_btn.pack(pady=10)
            
        else:
            ttk.Label(main_frame, 
                     text="❌ Aucune carte trouvée pour le test",
                     foreground='red').pack()
        
        print("✅ Interface de test créée avec succès")
        print("🎯 Testez maintenant en cliquant sur le bouton dans l'interface")
        
        # Démarrer l'interface
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'interface de test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_interface()
