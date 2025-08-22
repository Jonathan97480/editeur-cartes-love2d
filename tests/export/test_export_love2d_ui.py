#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du nouveau bouton d'export Love2D avec formatage
"""

import tkinter as tk
from tkinter import messagebox
from lib.database import CardRepo
from lib.config import DB_FILE
from lua_exporter_love2d import Love2DLuaExporter

def test_export_love2d():
    """Test de l'export Love2D avec interface utilisateur"""
    print("🎮 TEST DU NOUVEL EXPORT LOVE2D")
    print("=" * 50)
    
    # Créer une fenêtre de test
    root = tk.Tk()
    root.title("Test Export Love2D")
    root.geometry("400x300")
    
    # Créer le repo
    repo = CardRepo(DB_FILE)
    cards = repo.list_cards()
    
    # Informations
    info_text = f"""
📊 Cartes disponibles: {len(cards)}

📋 Liste des cartes:
"""
    for i, card in enumerate(cards, 1):
        info_text += f"  {i}. {card.name}\n"
        info_text += f"     Formatage: titre({card.title_x},{card.title_y}) texte({card.text_x},{card.text_y})\n"
    
    info_text += f"\n🎯 Cliquez sur 'Exporter' pour tester l'export Love2D"
    
    # Label d'information
    label = tk.Label(root, text=info_text, justify='left', font=('Consolas', 9))
    label.pack(padx=10, pady=10, fill='both', expand=True)
    
    def do_export():
        """Fonction d'export de test"""
        try:
            exporter = Love2DLuaExporter(repo)
            filename = 'test_export_love2d.lua'
            size = exporter.export_to_file(filename)
            
            messagebox.showinfo(
                "Export réussi", 
                f"✅ Export Love2D réussi !\n\n"
                f"📁 Fichier: {filename}\n"
                f"📊 Cartes: {len(cards)}\n"
                f"📝 Taille: {size:,} caractères\n\n"
                f"🎮 Format Love2D avec formatage complet"
            )
            
            # Afficher un aperçu
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            preview = content[:500] + "..." if len(content) > 500 else content
            print(f"\n📋 Aperçu du fichier généré:")
            print(preview)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur lors de l'export:\n{e}")
    
    # Bouton d'export
    export_btn = tk.Button(
        root, 
        text="🎮 Exporter Love2D + Formatage", 
        command=do_export,
        bg='#4CAF50',
        fg='white',
        font=('Arial', 12, 'bold'),
        height=2
    )
    export_btn.pack(pady=20)
    
    # Bouton de fermeture
    close_btn = tk.Button(root, text="Fermer", command=root.destroy)
    close_btn.pack(pady=10)
    
    print(f"🎯 Interface de test ouverte")
    root.mainloop()

if __name__ == "__main__":
    test_export_love2d()
