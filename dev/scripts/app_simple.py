#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version finale simplifiée avec boutons courts
"""
import tkinter as tk
from tkinter import ttk
from lib.ui_components import CardForm

# Patch pour des boutons plus courts
original_build_ui = CardForm._build_ui

def new_build_ui(self):
    """Version avec boutons courts sans émojis."""
    original_build_ui(self)
    
    # Remplacer les boutons du bas
    for widget in self.winfo_children():
        if isinstance(widget, ttk.Frame):
            # Chercher le frame contenant les boutons
            buttons_found = False
            for child in widget.winfo_children():
                if isinstance(child, ttk.Button):
                    text = child.cget('text')
                    if 'Nouveau' in text or 'Sauvegarder' in text or 'Supprimer' in text:
                        buttons_found = True
                        break
            
            if buttons_found:
                # Supprimer les anciens boutons
                for child in list(widget.winfo_children()):
                    if isinstance(child, ttk.Button):
                        child.destroy()
                
                # Ajouter les nouveaux boutons courts
                ttk.Button(widget, text="Nouveau", command=self.clear_form, width=10).pack(side='left', padx=(0,5))
                ttk.Button(widget, text="Sauvegarder", command=self.save, width=12).pack(side='left', padx=(0,5))
                ttk.Button(widget, text="Supprimer", command=self.delete_current, width=10).pack(side='left')
                break

# Appliquer le patch
CardForm._build_ui = new_build_ui

# Importer et utiliser l'application finale
from app_final import *

if __name__ == '__main__':
    main()
