#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour redémarrer l'éditeur avec les nouveaux sliders 300px
"""

import sys
import os
import importlib

def clear_module_cache():
    """Nettoyer le cache des modules pour forcer le rechargement"""
    modules_to_clear = [
        'lib.text_formatting_editor',
        'text_formatting_editor',
        'lib.ui_components', 
        'ui_components'
    ]
    
    for module_name in modules_to_clear:
        if module_name in sys.modules:
            print(f"🧹 Nettoyage cache: {module_name}")
            del sys.modules[module_name]

def force_reload_editor():
    """Forcer le rechargement de l'éditeur avec les nouvelles dimensions"""
    
    print("🔄 RECHARGEMENT FORCÉ DE L'ÉDITEUR")
    print("=" * 50)
    
    # Nettoyer le cache
    clear_module_cache()
    
    # Ajouter le chemin lib
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
    
    try:
        # Import frais
        import tkinter as tk
        from tkinter import ttk
        
        # Importer l'éditeur (rechargé)
        from text_formatting_editor import TextFormattingEditor
        from database_simple import CardRepo
        
        print("✅ Modules rechargés avec succès")
        
        # Créer une carte de test simple
        class TestCard:
            def __init__(self):
                self.id = 1
                self.nom = "Carte Test"
                self.description = "Description de test pour l'éditeur de formatage"
                self.title_x = 50
                self.title_y = 30
                self.title_font = "Arial"
                self.title_size = 16
                self.title_color = "#000000"
                self.text_x = 40
                self.text_y = 100
                self.text_width = 200
                self.text_height = 150
                self.text_font = "Arial"
                self.text_size = 12
                self.text_color = "#000000"
                self.text_align = "left"
                self.line_spacing = 1.2
                self.energy_x = 200
                self.energy_y = 20
                self.energy_size = 14
                self.energy_font = "Arial"
                self.energy_color = "#FF0000"
        
        # Créer un repo simple
        class TestRepo:
            def save_card_formatting(self, card):
                print(f"💾 Sauvegarde simulée pour carte {card.nom}")
                return True
        
        # Créer la fenêtre de test
        root = tk.Tk()
        test_card = TestCard()
        test_repo = TestRepo()
        
        print("🚀 Lancement de l'éditeur avec sliders 300px...")
        
        # Créer l'éditeur avec les nouvelles dimensions
        editor = TextFormattingEditor(root, test_card, test_repo)
        
        print("✅ Éditeur lancé avec succès!")
        print("   - Sliders limités à 300px de longueur visuelle")
        print("   - Modules rechargés depuis le disque")
        print("   - Cache système nettoyé")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur lors du rechargement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    force_reload_editor()
