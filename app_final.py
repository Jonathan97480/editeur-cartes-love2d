#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version finale de l'éditeur de cartes Love2D
Mode compatibilité avec interface complète
"""
import argparse
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import os

# Import des modules de l'application
from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE, APP_TITLE, load_settings
from lib.utils import write_bat_scripts
from lib.tests import run_tests
from lib.ui_components import CardForm, CardList
from lib.settings_window import SettingsWindow
from lib.utils import ensure_images_folder

def default_db_path() -> str:
    """Retourne le chemin par défaut de la base de données."""
    return str(Path(__file__).parent / DB_FILE)

class FinalMainApp(tk.Tk):
    """Application finale avec interface complète en mode compatibilité."""
    
    def __init__(self, repo: CardRepo):
        super().__init__()
        self.repo = repo
        self.title(APP_TITLE)
        self.geometry('1281x879')
        self.minsize(800, 600)
        
        # Configuration de style basique
        self.configure_styles()
        
        # Interface utilisateur
        self.setup_ui()
        
        # Charger les données
        self.refresh_all_tabs()
    
    def configure_styles(self):
        """Configuration des styles basiques."""
        try:
            style = ttk.Style(self)
            style.theme_use('clam')
        except Exception:
            pass  # Utiliser les styles par défaut
    
    def setup_ui(self):
        """Interface utilisateur complète."""
        # Menu complet
        self.create_menu()
        
        # Barre d'outils
        self.create_toolbar()
        
        # Interface principale
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Panneau gauche : formulaire
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=False, padx=(0, 10))
        
        # Panneau droit : liste des cartes
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Onglets des cartes avec icônes
        tabs = ttk.Notebook(right_frame)
        tabs.pack(fill='both', expand=True)
        
        # Créer les onglets
        self.tab_all = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label=None)
        self.tab_comm = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label='Commun')
        self.tab_rare = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label='Rare')
        self.tab_legen = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label='Légendaire')
        self.tab_myth = CardList(tabs, self.repo, on_select=self.load_card, fixed_rarity_label='Mythique')
        
        tabs.add(self.tab_all, text='📋 Toutes')
        tabs.add(self.tab_comm, text='⚪ Commun')
        tabs.add(self.tab_rare, text='🔵 Rare')
        tabs.add(self.tab_legen, text='🟠 Légendaire')
        tabs.add(self.tab_myth, text='🟣 Mythique')
        
        # Formulaire avec cadre
        form_frame = ttk.LabelFrame(left_frame, text="Édition de Carte", padding=10)
        form_frame.pack(fill='both', expand=True)
        
        self.form = CardForm(form_frame, self.repo, on_saved=self.refresh_all_tabs)
        self.form.pack(fill='both', expand=True)
    
    def create_menu(self):
        """Crée le menu complet."""
        menubar = tk.Menu(self)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="🆕 Nouvelle carte", command=self.new_card, accelerator="Ctrl+N")
        file_menu.add_command(label="💾 Sauvegarder", command=self.save_card, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="📤 Exporter Joueur", command=self.export_player)
        file_menu.add_command(label="📤 Exporter IA", command=self.export_ia)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Quitter", command=self.destroy, accelerator="Ctrl+Q")
        menubar.add_cascade(label="📁 Fichier", menu=file_menu)
        
        # Menu Édition
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="🗑️ Supprimer carte", command=self.delete_card, accelerator="Del")
        edit_menu.add_command(label="📋 Dupliquer carte", command=self.duplicate_card, accelerator="Ctrl+D")
        menubar.add_cascade(label="✏️ Édition", menu=edit_menu)
        
        # Menu Affichage
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="🔄 Actualiser", command=self.refresh_all_tabs, accelerator="F5")
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
        help_menu.add_command(label="📚 Guide d'utilisation", command=self.show_guide)
        menubar.add_cascade(label="❓ Aide", menu=help_menu)
        
        self.config(menu=menubar)
        
        # Raccourcis clavier
        self.bind_all("<Control-n>", lambda e: self.new_card())
        self.bind_all("<Control-s>", lambda e: self.save_card())
        self.bind_all("<Control-d>", lambda e: self.duplicate_card())
        self.bind_all("<Control-q>", lambda e: self.destroy())
        self.bind_all("<Delete>", lambda e: self.delete_card())
        self.bind_all("<F5>", lambda e: self.refresh_all_tabs())
    
    def create_toolbar(self):
        """Crée une barre d'outils avec les actions principales."""
        toolbar = ttk.Frame(self, relief='solid', borderwidth=1)
        toolbar.pack(fill='x', padx=5, pady=(5,0))
        
        # Test d'affichage des émojis
        try:
            # Boutons principaux avec icônes
            ttk.Button(toolbar, text="🆕Nouveau", command=self.new_card, width=12).pack(side='left', padx=2, pady=2)
            ttk.Button(toolbar, text="💾Sauvegarder", command=self.save_card, width=14).pack(side='left', padx=2, pady=2)
            ttk.Button(toolbar, text="🗑️Supprimer", command=self.delete_card, width=14).pack(side='left', padx=2, pady=2)
            
            # Séparateur
            ttk.Separator(toolbar, orient='vertical').pack(side='left', fill='y', padx=5, pady=2)
            
            # Actions supplémentaires
            ttk.Button(toolbar, text="📋Dupliquer", command=self.duplicate_card, width=12).pack(side='left', padx=2, pady=2)
            ttk.Button(toolbar, text="🔄Actualiser", command=self.refresh_all_tabs, width=12).pack(side='left', padx=2, pady=2)
            
            # Séparateur
            ttk.Separator(toolbar, orient='vertical').pack(side='left', fill='y', padx=5, pady=2)
            
            # Exports
            ttk.Button(toolbar, text="📤Export Joueur", command=self.export_player, width=15).pack(side='left', padx=2, pady=2)
            ttk.Button(toolbar, text="📤Export IA", command=self.export_ia, width=12).pack(side='left', padx=2, pady=2)
        except:
            # Fallback sans émojis
            ttk.Button(toolbar, text="Nouveau", command=self.new_card, width=10).pack(side='left', padx=2, pady=2)
            ttk.Button(toolbar, text="Sauvegarder", command=self.save_card, width=12).pack(side='left', padx=2, pady=2)
            ttk.Button(toolbar, text="Supprimer", command=self.delete_card, width=12).pack(side='left', padx=2, pady=2)
            ttk.Separator(toolbar, orient='vertical').pack(side='left', fill='y', padx=5, pady=2)
            ttk.Button(toolbar, text="Dupliquer", command=self.duplicate_card, width=10).pack(side='left', padx=2, pady=2)
            ttk.Button(toolbar, text="Actualiser", command=self.refresh_all_tabs, width=10).pack(side='left', padx=2, pady=2)
            ttk.Separator(toolbar, orient='vertical').pack(side='left', fill='y', padx=5, pady=2)
            ttk.Button(toolbar, text="Export Joueur", command=self.export_player, width=12).pack(side='left', padx=2, pady=2)
            ttk.Button(toolbar, text="Export IA", command=self.export_ia, width=10).pack(side='left', padx=2, pady=2)
    
    def load_card(self, card):
        """Charge une carte dans le formulaire."""
        self.form.load_card(card)
    
    def refresh_all_tabs(self):
        """Actualise toutes les listes."""
        for tab in [self.tab_all, self.tab_comm, self.tab_rare, self.tab_legen, self.tab_myth]:
            tab.refresh()
    
    def new_card(self):
        """Nouvelle carte."""
        self.form.clear_form()
    
    def save_card(self):
        """Sauvegarde la carte actuelle."""
        self.form.save()
    
    def delete_card(self):
        """Supprime la carte actuelle."""
        self.form.delete_current()
    
    def duplicate_card(self):
        """Duplique la carte actuelle."""
        # Pour l'instant, on copie le contenu et on efface l'ID
        if self.form.current_id is not None:
            # Sauvegarder d'abord
            self.form.save()
            # Puis effacer l'ID pour créer une nouvelle carte
            self.form.current_id = None
            # Modifier le nom pour indiquer que c'est une copie
            current_name = self.form.name_var.get()
            if not current_name.endswith(" (Copie)"):
                self.form.name_var.set(current_name + " (Copie)")
            messagebox.showinfo("Duplication", "Carte dupliquée ! Modifiez le nom et sauvegardez.")
    
    def export_player(self):
        """Export des cartes joueur."""
        self.tab_all.export_side('joueur')
    
    def export_ia(self):
        """Export des cartes IA."""
        self.tab_all.export_side('ia')
    
    def show_settings(self):
        """Affiche la fenêtre de paramètres des images."""
        try:
            # Essayer d'abord la version normale
            from lib.settings_window import SettingsWindow
            settings_window = SettingsWindow(self)
            settings_window.show()
        except Exception as e:
            print(f"Erreur avec settings_window: {e}")
            try:
                # Fallback vers la version simple
                from lib.simple_settings_window import SimpleSettingsWindow
                settings_window = SimpleSettingsWindow(self)
                settings_window.show()
            except Exception as e2:
                # En cas d'erreur totale, afficher une messagebox d'information
                messagebox.showwarning("Information", 
                    f"Impossible d'ouvrir la fenêtre de paramètres.\n\n"
                    f"Erreur: {e2}\n\n"
                    f"Vous pouvez configurer manuellement :\n"
                    f"- Placez votre image template dans le dossier 'images'\n"
                    f"- Elle sera utilisée automatiquement pour créer les cartes finales")
                
                # Ouvrir le dossier images à la place
                try:
                    self.open_images_folder()
                except:
                    pass
    
    def open_images_folder(self):
        """Ouvre le dossier des images."""
        try:
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
        about_text = f"""Éditeur de cartes Love2D

— Interface française moderne (tkinter)
— SQLite local : cartes.db
— Exports : cards_player.lua et cards_ai.lua
— Rareté & Types exportés dans le Lua
— Génération automatique d'images de cartes

Version stable avec interface complète.
Compatible tous environnements Windows.

Astuce : 
1. Configurez un template dans Réglages
2. Les images fusionnées seront automatiquement 
   créées lors de la sauvegarde des cartes
3. Utilisez les raccourcis clavier pour plus d'efficacité
"""
        messagebox.showinfo("À propos", about_text)
    
    def show_guide(self):
        """Ouvre le guide d'utilisation."""
        try:
            guide_path = Path(__file__).parent / "GUIDE.md"
            if guide_path.exists():
                os.startfile(str(guide_path))
            else:
                messagebox.showinfo("Guide", "Le fichier GUIDE.md n'a pas été trouvé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le guide: {e}")

def main(argv=None):
    """Point d'entrée principal de l'application."""
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument('--test', action='store_true', help='Exécuter la suite de tests et quitter')
    parser.add_argument('--write-bats', action='store_true', help='Générer run.bat et build.bat dans le dossier du script')
    args = parser.parse_args(argv)

    if args.test:
        print("Exécution des tests...")
        success = run_tests()
        sys.exit(0 if success else 1)

    if getattr(args, 'write_bats', False):
        paths = write_bat_scripts()
        print("Scripts générés :", paths)
        sys.exit(0)

    # Initialisation de la base de données
    db_path = default_db_path()
    ensure_db(db_path)
    repo = CardRepo(db_path)
    
    # Charge les paramètres de l'application
    load_settings()

    try:
        print("Lancement de l'éditeur de cartes Love2D...")
        app = FinalMainApp(repo)
        app.mainloop()
    except Exception as e:
        print(f"[ERREUR] Impossible de lancer l'application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
