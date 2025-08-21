#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application principale pour l'éditeur de cartes Love2D
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
from .config import APP_TITLE
from .database import CardRepo
from .ui_components import CardForm, CardList
from .settings_window import SettingsWindow
from .theme_settings import ThemeSettingsWindow
from .themes import init_theme_manager, get_theme_manager
from .utils import ensure_images_folder

class MainApp(tk.Tk):
    def __init__(self, repo: CardRepo):
        super().__init__()
        self.repo = repo
        self.title(APP_TITLE)
        self.geometry('1280x780')
        
        # Tentative d'initialisation du gestionnaire de thèmes
        try:
            self.theme_manager = init_theme_manager(self)
            self.themes_enabled = True
        except Exception as e:
            print(f"[INFO] Thèmes non disponibles, utilisation de l'interface standard: {e}")
            self.theme_manager = None
            self.themes_enabled = False
        
        self._style()
        self._build_layout()

    def _style(self):
        """Configuration des styles avec support des thèmes."""
        if self.themes_enabled and self.theme_manager:
            # Le gestionnaire de thèmes s'occupe des styles
            self.theme_manager.add_theme_callback(self._on_theme_change)
        else:
            # Styles basiques sans thèmes
            style = ttk.Style(self)
            try:
                style.theme_use('clam')
            except Exception:
                pass  # Utiliser le thème par défaut
        
        # Configuration de police par défaut
        try:
            self.option_add('*Font', 'Segoe UI 9')
        except:
            pass

    def _on_theme_change(self):
        """Appelé quand le thème change."""
        # Mettre à jour les composants si nécessaire
        pass

    def _build_layout(self):
        # Menu principal
        self._create_menu()
        
        # Split layout (2 colonnes) avec style moderne si possible
        if self.themes_enabled and self.theme_manager:
            main_frame = self.theme_manager.create_modern_frame(self, padding=10)
            main_frame.pack(fill='both', expand=True)
            
            left = self.theme_manager.create_modern_frame(main_frame)
            left.pack(side='left', fill='both', expand=False, padx=(0, 10))
            
            right = self.theme_manager.create_modern_frame(main_frame)
            right.pack(side='right', fill='both', expand=True)
        else:
            # Layout basique sans thèmes
            main_frame = ttk.Frame(self, padding=10)
            main_frame.pack(fill='both', expand=True)
            
            left = ttk.Frame(main_frame)
            left.pack(side='left', fill='both', expand=False, padx=(0, 10))
            
            right = ttk.Frame(main_frame)
            right.pack(side='right', fill='both', expand=True)

        # À droite : Notebook par rareté avec style moderne si possible
        if self.themes_enabled:
            tabs = ttk.Notebook(right, style="Modern.TNotebook")
        else:
            tabs = ttk.Notebook(right)
        tabs.pack(fill='both', expand=True)
        self.tab_all = CardList(tabs, self.repo, on_select=self._load_from_list, fixed_rarity_label=None)
        self.tab_comm = CardList(tabs, self.repo, on_select=self._load_from_list, fixed_rarity_label='Commun')
        self.tab_rare = CardList(tabs, self.repo, on_select=self._load_from_list, fixed_rarity_label='Rare')
        self.tab_legen = CardList(tabs, self.repo, on_select=self._load_from_list, fixed_rarity_label='Légendaire')
        self.tab_myth = CardList(tabs, self.repo, on_select=self._load_from_list, fixed_rarity_label='Mythique')
        tabs.add(self.tab_all, text='📋 Toutes')
        tabs.add(self.tab_comm, text='⚪ Commun')
        tabs.add(self.tab_rare, text='🔵 Rare')
        tabs.add(self.tab_legen, text='🟠 Légendaire')
        tabs.add(self.tab_myth, text='🟣 Mythique')
        
        # À gauche : Formulaire d'édition avec style moderne si possible
        if self.themes_enabled and self.theme_manager:
            form_frame = self.theme_manager.create_card_frame(left, padding=10)
        else:
            form_frame = ttk.Frame(left, padding=10)
        form_frame.pack(fill='both', expand=True)
        
        self.form = CardForm(form_frame, self.repo, on_saved=self._refresh_all_tabs)
        self.form.pack(fill='both', expand=True)        # Menu moderne avec icônes
        self._create_menu()

    def _create_menu(self):
        """Crée le menu principal avec style moderne."""
        menubar = tk.Menu(self)
        
        # Menu Fichier
        mf = tk.Menu(menubar, tearoff=0)
        mf.add_command(label='📤 Exporter Joueur…', command=lambda: self.tab_all.export_side('joueur'))
        mf.add_command(label='📤 Exporter IA…', command=lambda: self.tab_all.export_side('ia'))
        mf.add_separator()
        mf.add_command(label='❌ Quitter', command=self.destroy)
        menubar.add_cascade(label='📁 Fichier', menu=mf)

        # Menu Affichage
        mv = tk.Menu(menubar, tearoff=0)
        if self.themes_enabled:
            mv.add_command(label='🎨 Thèmes et Apparence...', command=self._show_theme_settings)
            mv.add_separator()
        mv.add_command(label='🔄 Actualiser', command=self._refresh_all_tabs)
        menubar.add_cascade(label='👁️ Affichage', menu=mv)

        # Menu Réglages
        mr = tk.Menu(menubar, tearoff=0)
        mr.add_command(label='⚙️ Configuration des images...', command=self._open_settings)
        mr.add_separator()
        mr.add_command(label='📂 Ouvrir dossier images', command=self._open_images_folder)
        menubar.add_cascade(label='🔧 Réglages', menu=mr)

        # Menu Aide
        ma = tk.Menu(menubar, tearoff=0)
        ma.add_command(label='ℹ️ À propos', command=self._about)
        menubar.add_cascade(label='❓ Aide', menu=ma)
        
        self.config(menu=menubar)

    def _refresh_all_tabs(self):
        # rafraîchir toutes les listes
        for tab in (self.tab_all, self.tab_comm, self.tab_rare, self.tab_legen, self.tab_myth):
            tab.refresh()

    def _open_settings(self):
        """Ouvre la fenêtre de paramètres des images."""
        SettingsWindow(self).show()
    
    def _show_theme_settings(self):
        """Affiche la fenêtre de paramètres des thèmes."""
        if self.themes_enabled:
            ThemeSettingsWindow(self).show()
        else:
            messagebox.showinfo("Thèmes", "Les thèmes ne sont pas disponibles dans cette configuration.")

    def _open_images_folder(self):
        folder_path = ensure_images_folder()
        try:
            os.startfile(folder_path)  # Windows
        except AttributeError:
            try:
                os.system(f'open "{folder_path}"')  # macOS
            except:
                os.system(f'xdg-open "{folder_path}"')  # Linux

    def _about(self):
        about_text = """Éditeur de cartes Love2D

— Interface française (tkinter)
— SQLite local : cartes.db
— Exports : cards_player.lua et cards_ai.lua
— Rareté & Types exportés dans le Lua
— Génération automatique d'images de cartes

Astuce : 
1. Configurez un template dans Réglages
2. Les images fusionnées seront automatiquement 
   créées lors de la sauvegarde des cartes
3. Utilisez l'onglet Action pour insérer
   les appels à graveyardPioche() et findCard()."""
        messagebox.showinfo(APP_TITLE, about_text)

    def _load_from_list(self, card_id: int):
        card = self.repo.get(card_id)
        if card:
            self.form.load_card(card)
