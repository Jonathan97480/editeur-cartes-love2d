#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre de paramètres des thèmes
"""
import tkinter as tk
from tkinter import ttk
from .themes import get_theme_manager, THEMES

class ThemeSettingsWindow:
    """Fenêtre de configuration des thèmes."""
    
    def __init__(self, parent):
        self.parent = parent
        self.theme_manager = get_theme_manager()
        self.window = None
        
    def show(self):
        """Affiche la fenêtre de paramètres des thèmes."""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("Paramètres des Thèmes")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Centrer la fenêtre
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self._create_widgets()
        self._apply_theme()
        
        # Callback pour mise à jour automatique
        self.theme_manager.add_theme_callback(self._apply_theme)
        
        # Centrer sur parent
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Crée les widgets de l'interface."""
        main_frame = ttk.Frame(self.window, style="Modern.TFrame", padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Apparence", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Section thème
        theme_section = ttk.LabelFrame(main_frame, text="Thème de l'application", 
                                     style="Modern.TLabelframe", padding=15)
        theme_section.pack(fill="x", pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(theme_section, 
                             text="Choisissez l'apparence de l'application :",
                             style="Modern.TLabel")
        desc_label.pack(anchor="w", pady=(0, 10))
        
        # Sélecteur de thème
        self.theme_var = tk.StringVar(value=self.theme_manager.current_theme_name)
        
        # Option Automatique
        auto_radio = ttk.Radiobutton(theme_section, 
                                   text="🔄 Automatique (suit le thème Windows)",
                                   variable=self.theme_var, 
                                   value="auto",
                                   command=self._on_theme_change,
                                   style="Modern.TRadiobutton")
        auto_radio.pack(anchor="w", pady=2)
        
        # Option Clair
        light_radio = ttk.Radiobutton(theme_section, 
                                    text="☀️ Clair",
                                    variable=self.theme_var, 
                                    value="light",
                                    command=self._on_theme_change,
                                    style="Modern.TRadiobutton")
        light_radio.pack(anchor="w", pady=2)
        
        # Option Sombre
        dark_radio = ttk.Radiobutton(theme_section, 
                                   text="🌙 Sombre",
                                   variable=self.theme_var, 
                                   value="dark",
                                   command=self._on_theme_change,
                                   style="Modern.TRadiobutton")
        dark_radio.pack(anchor="w", pady=2)
        
        # Aperçu du thème actuel
        preview_section = ttk.LabelFrame(main_frame, text="Aperçu", 
                                       style="Modern.TLabelframe", padding=15)
        preview_section.pack(fill="both", expand=True, pady=(0, 20))
        
        self.preview_frame = ttk.Frame(preview_section, style="Card.TFrame", padding=10)
        self.preview_frame.pack(fill="both", expand=True)
        
        # Éléments d'aperçu
        preview_label = ttk.Label(self.preview_frame, 
                                text="Aperçu du thème actuel",
                                style="Heading.TLabel")
        preview_label.pack(pady=(0, 10))
        
        self.current_theme_label = ttk.Label(self.preview_frame, 
                                           text=f"Thème : {self.theme_manager.get_current_theme_name()}",
                                           style="Modern.TLabel")
        self.current_theme_label.pack(pady=2)
        
        # Échantillons de couleurs
        colors_frame = ttk.Frame(self.preview_frame, style="Modern.TFrame")
        colors_frame.pack(pady=10)
        
        # Boutons d'aperçu
        buttons_frame = ttk.Frame(self.preview_frame, style="Modern.TFrame")
        buttons_frame.pack(pady=5)
        
        sample_button = ttk.Button(buttons_frame, text="Bouton Normal", 
                                 style="Modern.TButton")
        sample_button.pack(side="left", padx=5)
        
        accent_button = ttk.Button(buttons_frame, text="Bouton Accent", 
                                 style="Accent.TButton")
        accent_button.pack(side="left", padx=5)
        
        # Champ d'exemple
        sample_entry = ttk.Entry(self.preview_frame, style="Modern.TEntry")
        sample_entry.insert(0, "Exemple de texte")
        sample_entry.pack(pady=5, padx=20, fill="x")
        
        # Boutons d'action
        buttons_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        buttons_frame.pack(fill="x")
        
        close_button = ttk.Button(buttons_frame, text="Fermer", 
                                command=self.window.destroy,
                                style="Modern.TButton")
        close_button.pack(side="right")
        
        reset_button = ttk.Button(buttons_frame, text="Réinitialiser", 
                                command=self._reset_theme,
                                style="Modern.TButton")
        reset_button.pack(side="right", padx=(0, 10))
    
    def _on_theme_change(self):
        """Appelé quand l'utilisateur change de thème."""
        new_theme = self.theme_var.get()
        self.theme_manager.set_theme(new_theme)
        self._update_preview()
    
    def _reset_theme(self):
        """Remet le thème par défaut."""
        self.theme_var.set("auto")
        self.theme_manager.set_theme("auto")
        self._update_preview()
    
    def _update_preview(self):
        """Met à jour l'aperçu du thème."""
        if hasattr(self, 'current_theme_label'):
            self.current_theme_label.config(
                text=f"Thème : {self.theme_manager.get_current_theme_name()}")
    
    def _apply_theme(self):
        """Applique le thème à cette fenêtre."""
        if not self.window or not self.window.winfo_exists():
            return
            
        theme = self.theme_manager.current_theme
        if theme:
            self.window.configure(bg=theme["bg"])
            self._update_preview()
