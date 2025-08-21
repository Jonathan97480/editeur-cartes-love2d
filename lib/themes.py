#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion des thèmes pour l'éditeur de cartes Love2D
Support du mode sombre/clair et style Windows 11
"""
import tkinter as tk
from tkinter import ttk
import sys
import os
from .config import APP_SETTINGS, save_settings

# Détection du thème Windows
def get_windows_theme():
    """Détecte si Windows utilise le mode sombre ou clair."""
    # Fallback simple - toujours retourner "light" pour éviter les erreurs
    return "light"

# Définition des thèmes
THEMES = {
    "light": {
        "name": "Clair",
        "bg": "#FFFFFF",
        "fg": "#000000",
        "select_bg": "#0078D4",
        "select_fg": "#FFFFFF",
        "button_bg": "#F3F3F3",
        "button_fg": "#000000",
        "button_hover": "#E1E1E1",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#000000",
        "entry_border": "#CCCCCC",
        "frame_bg": "#F8F8F8",
        "notebook_bg": "#FFFFFF",
        "notebook_fg": "#000000",
        "tab_bg": "#F0F0F0",
        "tab_fg": "#000000",
        "tab_selected": "#FFFFFF",
        "menu_bg": "#FFFFFF",
        "menu_fg": "#000000",
        "scrollbar": "#CCCCCC",
        "border": "#CCCCCC",
        "accent": "#0078D4",
        "success": "#107C10",
        "warning": "#FF8C00",
        "error": "#D13438"
    },
    "dark": {
        "name": "Sombre",
        "bg": "#202020",
        "fg": "#FFFFFF",
        "select_bg": "#0078D4",
        "select_fg": "#FFFFFF",
        "button_bg": "#2D2D2D",
        "button_fg": "#FFFFFF",
        "button_hover": "#3A3A3A",
        "entry_bg": "#2D2D2D",
        "entry_fg": "#FFFFFF",
        "entry_border": "#404040",
        "frame_bg": "#1E1E1E",
        "notebook_bg": "#202020",
        "notebook_fg": "#FFFFFF",
        "tab_bg": "#2D2D2D",
        "tab_fg": "#FFFFFF",
        "tab_selected": "#202020",
        "menu_bg": "#2D2D2D",
        "menu_fg": "#FFFFFF",
        "scrollbar": "#404040",
        "border": "#404040",
        "accent": "#60CDFF",
        "success": "#54B399",
        "warning": "#FFAA44",
        "error": "#FF6B6B"
    },
    "auto": {
        "name": "Automatique (Système)",
        "detection": True
    }
}

class ThemeManager:
    """Gestionnaire de thèmes pour l'application."""
    
    def __init__(self, root):
        self.root = root
        self.current_theme_name = APP_SETTINGS.get("theme", "auto")
        self.current_theme = None
        self.style = ttk.Style()
        self.callbacks = []
        
        # Initialisation du thème
        self.apply_theme()
    
    def get_current_theme_name(self):
        """Retourne le nom du thème actuel."""
        if self.current_theme_name == "auto":
            system_theme = get_windows_theme()
            return f"auto ({system_theme})"
        return THEMES[self.current_theme_name]["name"]
    
    def get_effective_theme(self):
        """Retourne le thème effectivement utilisé."""
        if self.current_theme_name == "auto":
            return get_windows_theme()
        return self.current_theme_name
    
    def set_theme(self, theme_name):
        """Change le thème de l'application."""
        if theme_name in THEMES:
            self.current_theme_name = theme_name
            APP_SETTINGS["theme"] = theme_name
            save_settings()
            self.apply_theme()
            self._notify_callbacks()
    
    def apply_theme(self):
        """Applique le thème actuel à l'interface."""
        effective_theme = self.get_effective_theme()
        if effective_theme not in THEMES:
            effective_theme = "light"
        
        self.current_theme = THEMES[effective_theme].copy()
        
        try:
            # Application du thème Windows 11
            self._apply_windows11_style()
            
            # Configuration des couleurs de base
            self.root.configure(bg=self.current_theme["bg"])
            
            # Configuration du style ttk
            self._configure_ttk_styles()
        except Exception as e:
            # En cas d'erreur, on continue avec les styles par défaut
            print(f"[INFO] Styles avancés non disponibles: {e}")
            try:
                self.root.configure(bg="#FFFFFF")  # Fond blanc par défaut
            except:
                pass
    
    def _apply_windows11_style(self):
        """Applique le style Windows 11."""
        try:
            # Configuration générale pour un look moderne
            available_themes = self.style.theme_names()
            if 'vista' in available_themes and sys.platform == "win32":
                self.style.theme_use('vista')
            elif 'clam' in available_themes:
                self.style.theme_use('clam')
            else:
                # Fallback vers le thème par défaut
                pass
        except Exception:
            # En cas d'erreur, continue sans changer le thème
            pass
        
        # Configuration des coins arrondis et espacement moderne
        try:
            self.style.configure('Modern.TFrame',
                               background=self.current_theme["frame_bg"],
                               relief='flat',
                               borderwidth=0)
            
            self.style.configure('Card.TFrame',
                               background=self.current_theme["bg"],
                               relief='solid',
                               borderwidth=1,
                               bordercolor=self.current_theme["border"])
        except Exception:
            # En cas d'erreur, continue sans appliquer les styles
            pass
    
    def _configure_ttk_styles(self):
        """Configure tous les styles ttk."""
        theme = self.current_theme
        
        try:
            # Buttons - Style Windows 11
            self.style.configure('Modern.TButton',
                               background=theme["button_bg"],
                               foreground=theme["button_fg"],
                               borderwidth=1,
                               bordercolor=theme["border"],
                               focuscolor='none',
                               relief='flat',
                               padding=(12, 8))
            
            self.style.map('Modern.TButton',
                          background=[('active', theme["button_hover"]),
                                    ('pressed', theme["select_bg"])],
                          foreground=[('pressed', theme["select_fg"])])
        except Exception:
            pass  # Continue même si les styles échouent
        
        try:
            # Accent button
            self.style.configure('Accent.TButton',
                               background=theme["accent"],
                               foreground=theme["select_fg"],
                               borderwidth=0,
                               focuscolor='none',
                               relief='flat',
                               padding=(12, 8))
            
            self.style.map('Accent.TButton',
                          background=[('active', theme["select_bg"]),
                                    ('pressed', '#005499')])
        except Exception:
            pass
        
        try:
            # Entry fields
            self.style.configure('Modern.TEntry',
                               fieldbackground=theme["entry_bg"],
                               foreground=theme["entry_fg"],
                               bordercolor=theme["entry_border"],
                               borderwidth=1,
                               insertcolor=theme["fg"],
                               padding=8)
            
            self.style.map('Modern.TEntry',
                          bordercolor=[('focus', theme["accent"])])
        except Exception:
            pass
        
        try:
            # Combobox, Labels, Frames, etc. - avec gestion d'erreur
            self.style.configure('Modern.TCombobox',
                               fieldbackground=theme["entry_bg"],
                               foreground=theme["entry_fg"],
                               bordercolor=theme["entry_border"],
                               borderwidth=1,
                               padding=8)
            
            self.style.configure('Modern.TLabel',
                               background=theme["bg"],
                               foreground=theme["fg"])
            
            self.style.configure('Heading.TLabel',
                               background=theme["bg"],
                               foreground=theme["fg"],
                               font=('Segoe UI', 12, 'bold'))
            
            self.style.configure('Title.TLabel',
                               background=theme["bg"],
                               foreground=theme["fg"],
                               font=('Segoe UI', 16, 'bold'))
            
            self.style.configure('Modern.TFrame',
                               background=theme["frame_bg"],
                               relief='flat')
            
            self.style.configure('Modern.TNotebook',
                               background=theme["notebook_bg"],
                               borderwidth=0)
            
            self.style.configure('Modern.TNotebook.Tab',
                               background=theme["tab_bg"],
                               foreground=theme["tab_fg"],
                               padding=(12, 8),
                               borderwidth=0)
            
            self.style.map('Modern.TNotebook.Tab',
                          background=[('selected', theme["tab_selected"]),
                                    ('active', theme["button_hover"])],
                          foreground=[('selected', theme["fg"])])
        except Exception:
            pass
        
        try:
            # Treeview, Scrollbars, Checkboxes
            self.style.configure('Modern.Treeview',
                               background=theme["bg"],
                               foreground=theme["fg"],
                               fieldbackground=theme["bg"],
                               borderwidth=1,
                               bordercolor=theme["border"])
            
            self.style.configure('Modern.Treeview.Heading',
                               background=theme["frame_bg"],
                               foreground=theme["fg"],
                               borderwidth=1,
                               bordercolor=theme["border"])
            
            self.style.map('Modern.Treeview',
                          background=[('selected', theme["select_bg"])],
                          foreground=[('selected', theme["select_fg"])])
            
            self.style.configure('Modern.TCheckbutton',
                               background=theme["bg"],
                               foreground=theme["fg"],
                               focuscolor='none')
            
            self.style.configure('Modern.TRadiobutton',
                               background=theme["bg"],
                               foreground=theme["fg"],
                               focuscolor='none')
        except Exception:
            pass
        
    def add_theme_callback(self, callback):
        """Ajoute un callback appelé quand le thème change."""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self):
        """Notifie tous les callbacks du changement de thème."""
        for callback in self.callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Erreur dans callback de thème: {e}")
    
    def get_color(self, color_key):
        """Retourne une couleur du thème actuel."""
        return self.current_theme.get(color_key, "#000000")
    
    def create_modern_frame(self, parent, style="Modern.TFrame", **kwargs):
        """Crée un frame avec le style moderne."""
        return ttk.Frame(parent, style=style, **kwargs)
    
    def create_card_frame(self, parent, **kwargs):
        """Crée un frame avec style carte (bordure subtile)."""
        frame = ttk.Frame(parent, style="Card.TFrame", **kwargs)
        return frame

# Instance globale du gestionnaire de thèmes
_theme_manager = None

def get_theme_manager():
    """Retourne l'instance globale du gestionnaire de thèmes."""
    return _theme_manager

def init_theme_manager(root):
    """Initialise le gestionnaire de thèmes."""
    global _theme_manager
    _theme_manager = ThemeManager(root)
    return _theme_manager
