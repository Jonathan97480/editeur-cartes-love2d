#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version de compatibilité maximale de l'éditeur de cartes
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

# Import des modules de base seulement
from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE, APP_TITLE, load_settings
from lib.ui_components import CardForm, CardList

def default_db_path() -> str:
    return str(Path(__file__).parent / DB_FILE)

class SimpleMainApp(tk.Tk):
    """Version simplifiée de l'application sans thèmes."""
    
    def __init__(self, repo: CardRepo):
        super().__init__()
        self.repo = repo
        self.title(APP_TITLE + " - Mode Compatibilité")
        self.geometry('1200x700')
        self.setup_ui()
    
    def setup_ui(self):
        """Interface utilisateur simplifiée."""
        # Menu complet
        menubar = tk.Menu(self)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="📤 Exporter Joueur", command=self.export_player)
        file_menu.add_command(label="📤 Exporter IA", command=self.export_ia)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Quitter", command=self.destroy)
        menubar.add_cascade(label="📁 Fichier", menu=file_menu)
        
        # Menu Affichage
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="🔄 Actualiser", command=self.refresh_all_tabs)
        menubar.add_cascade(label="👁️ Affichage", menu=view_menu)
        
        # Menu Réglages
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="⚙️ Configuration des images...", command=self.show_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="📂 Ouvrir dossier images", command=self.open_images_folder)
        menubar.add_cascade(label="🔧 Réglages", menu=settings_menu)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="ℹ️ À propos", command=self.show_about)
        menubar.add_cascade(label="❓ Aide", menu=help_menu)
        
        self.config(menu=menubar)
        
        # Interface principale
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Panneau gauche : formulaire
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=False, padx=(0, 10))
        
        # Panneau droit : liste des cartes
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Onglets des cartes
        tabs = ttk.Notebook(right_frame)
        tabs.pack(fill='both', expand=True)
        
        # Créer les onglets
        self.tab_all = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label=None)
        self.tab_comm = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label='Commun')
        self.tab_rare = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label='Rare')
        self.tab_legen = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label='Légendaire')
        self.tab_myth = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label='Mythique')
        
        tabs.add(self.tab_all, text='Toutes')
        tabs.add(self.tab_comm, text='Commun')
        tabs.add(self.tab_rare, text='Rare')
        tabs.add(self.tab_legen, text='Légendaire')
        tabs.add(self.tab_myth, text='Mythique')
        
        # Formulaire
        self.form = CardForm(left_frame, self.repo, on_saved=self.refresh_all_tabs)
        self.form.pack(fill='both', expand=True)
        
        # Charger les données
        self.refresh_all_tabs()
    
    def load_card(self, card):
        """Charge une carte dans le formulaire."""
        self.form.load_card(card)
    
    def refresh_all_tabs(self):
        """Actualise toutes les listes."""
        for tab in [self.tab_all, self.tab_comm, self.tab_rare, self.tab_legen, self.tab_myth]:
            tab.refresh()
    
    def export_player(self):
        """Export des cartes joueur."""
        self.tab_all.export_side('joueur')
    
    def export_ia(self):
        """Export des cartes IA."""
        self.tab_all.export_side('ia')
    
    def show_settings(self):
        """Affiche la fenêtre de paramètres des images."""
        try:
            from lib.settings_window import SettingsWindow
            SettingsWindow(self).show()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir les paramètres: {e}")
    
    def open_images_folder(self):
        """Ouvre le dossier des images."""
        try:
            from lib.utils import ensure_images_folder
            import os
            folder_path = ensure_images_folder()
            try:
                os.startfile(folder_path)  # Windows
            except AttributeError:
                try:
                    os.system(f'open "{folder_path}"')  # macOS
                except:
                    os.system(f'xdg-open "{folder_path}"')  # Linux
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier: {e}")
    
    def show_about(self):
        """Affiche la fenêtre À propos."""
        about_text = """Éditeur de cartes Love2D - Mode Compatibilité

— Interface française (tkinter)
— SQLite local : cartes.db
— Exports : cards_player.lua et cards_ai.lua
— Rareté & Types exportés dans le Lua
— Génération automatique d'images de cartes

Mode Compatibilité:
- Interface standard garantie de fonctionner
- Toutes les fonctionnalités principales
- Compatible tous environnements Windows

Version avec thèmes disponible via 'python test.py --force-advanced'
"""
        messagebox.showinfo("À propos", about_text)

def main_compat():
    """Fonction principale en mode compatibilité."""
    try:
        # Vérification basique de Tkinter
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre de test
        root.destroy()
        
        # Initialisation de la base de données
        db_path = default_db_path()
        ensure_db(db_path)
        repo = CardRepo(db_path)
        
        # Chargement des paramètres
        load_settings()
        
        # Lancement de l'application
        print("Lancement en mode compatibilité...")
        app = SimpleMainApp(repo)
        app.mainloop()
        
    except Exception as e:
        print(f"Erreur en mode compatibilité: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--compat":
        main_compat()
    else:
        print("Usage: python test_compat.py --compat")
        print("Cette version lance l'éditeur en mode compatibilité maximale.")
