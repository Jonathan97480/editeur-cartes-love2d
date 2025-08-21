#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de l'application sans thèmes
"""
# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()



import tkinter as tk
from tkinter import ttk
from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE

# Test simple sans thèmes
def test_simple():
    try:
        # Base de données
        ensure_db(DB_FILE)
        repo = CardRepo(DB_FILE)
        
        # Interface simple
        root = tk.Tk()
        root.title("Test Éditeur de Cartes")
        root.geometry("800x600")
        
        # Interface basique
        label = tk.Label(root, text="Application lancée avec succès !")
        label.pack(pady=20)
        
        button = tk.Button(root, text="Fermer", command=root.destroy)
        button.pack(pady=10)
        
        print("Interface créée avec succès")
        root.mainloop()
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
