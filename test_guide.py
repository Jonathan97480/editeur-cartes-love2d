#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du menu Guide d'utilisation
"""

import tkinter as tk
from tkinter import messagebox
import os
from pathlib import Path

def show_guide():
    """Ouvre le guide d'utilisation."""
    try:
        # Essayer plusieurs emplacements possibles pour le fichier GUIDE.md
        possible_paths = [
            Path(__file__).parent / "GUIDE.md",  # Même dossier que le script
            Path.cwd() / "GUIDE.md",             # Répertoire de travail actuel
            Path("GUIDE.md")                     # Répertoire courant relatif
        ]
        
        guide_path = None
        for path in possible_paths:
            if path.exists():
                guide_path = path
                break
        
        if guide_path:
            print(f"✅ Guide trouvé: {guide_path}")
            os.startfile(str(guide_path))
            messagebox.showinfo("Succès", f"Guide ouvert: {guide_path.name}")
        else:
            # Afficher où on a cherché pour aider au debug
            search_locations = [str(p) for p in possible_paths]
            message = f"Le fichier GUIDE.md n'a pas été trouvé.\n\nEmplacements vérifiés:\n" + "\n".join(search_locations)
            messagebox.showwarning("Guide non trouvé", message)
    except Exception as e:
        error_msg = f"Impossible d'ouvrir le guide: {e}"
        print(f"❌ {error_msg}")
        messagebox.showerror("Erreur", error_msg)

def test_guide_menu():
    """Test simple du menu Guide d'utilisation."""
    print("🧪 Test du menu Guide d'utilisation")
    print("=====================================")
    
    # Test direct de la fonction
    print("\n📂 Vérification des chemins...")
    possible_paths = [
        Path(__file__).parent / "GUIDE.md",
        Path.cwd() / "GUIDE.md",
        Path("GUIDE.md")
    ]
    
    for i, path in enumerate(possible_paths, 1):
        print(f"   {i}. {path} - {'✅ Existe' if path.exists() else '❌ Manquant'}")
    
    # Créer une interface de test
    root = tk.Tk()
    root.title("Test Guide d'utilisation")
    root.geometry("400x200")
    
    tk.Label(root, text="Test du menu Guide d'utilisation", font=("Arial", 12, "bold")).pack(pady=20)
    
    tk.Button(root, text="📚 Ouvrir le Guide", command=show_guide, 
              font=("Arial", 10), padx=20, pady=10).pack(pady=10)
    
    tk.Button(root, text="❌ Fermer", command=root.destroy, 
              font=("Arial", 10), padx=20, pady=5).pack(pady=5)
    
    print("\n🖱️  Interface de test créée. Cliquez sur 'Ouvrir le Guide' pour tester.")
    root.mainloop()

if __name__ == "__main__":
    test_guide_menu()
