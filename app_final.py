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
import shutil

# Import des modules de l'application
from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE, APP_TITLE, load_settings
from lib.utils import write_bat_scripts
from lib.tests import run_tests
from lib.ui_components import CardForm, CardList
from lib.settings_window import SettingsWindow
from lib.deck_viewer import open_deck_viewer
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
        file_menu.add_command(label="🎭 Export par Acteur...", command=self.export_by_actor)
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
        view_menu.add_separator()
        view_menu.add_command(label="🃏 Voir le deck", command=self.show_deck_viewer, accelerator="Ctrl+V")
        menubar.add_cascade(label="👁️ Affichage", menu=view_menu)
        
        # Menu Acteurs (NOUVEAU)
        actors_menu = tk.Menu(menubar, tearoff=0)
        actors_menu.add_command(label="🎭 Gérer les Acteurs...", command=self.manage_actors)
        actors_menu.add_command(label="📤 Export par Acteur...", command=self.export_by_actor)
        actors_menu.add_separator()
        actors_menu.add_command(label="🔄 Migration vers Acteurs...", command=self.demo_actors)
        menubar.add_cascade(label="🎭 Acteurs", menu=actors_menu)
        
        # Menu Réglages
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="⚙️ Configuration des images...", command=self.show_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="📂 Ouvrir dossier images", command=self.open_images_folder)
        settings_menu.add_command(label="🗂️ Organiser les images...", command=self.migrate_images)
        settings_menu.add_command(label="📋 Organiser les templates...", command=self.organize_templates)
        settings_menu.add_separator()
        settings_menu.add_command(label="🗑️ Clear Data (Vider tout)", command=self.clear_all_data)
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
        self.bind_all("<Control-v>", lambda e: self.show_deck_viewer())
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
    
    def load_card(self, card_id):
        """Charge une carte dans le formulaire."""
        # Si card_id est déjà un objet Card, l'utiliser directement
        if hasattr(card_id, 'id'):
            card = card_id
        else:
            # Sinon, récupérer la carte depuis la base de données
            card = self.repo.get(card_id)
            if not card:
                return  # Carte non trouvée
        
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
    
    def migrate_images(self):
        """Lance la migration des images vers la nouvelle structure organisée."""
        response = messagebox.askyesno(
            "Organiser les images", 
            "Cette fonction va :\n\n"
            "✅ Créer une structure de dossiers organisée :\n"
            "   • images/originals/ - Images sources\n"
            "   • images/cards/ - Images fusionnées finales\n"
            "   • images/templates/ - Templates par rareté\n\n"
            "✅ Copier toutes vos images actuelles vers 'originals'\n"
            "✅ Mettre à jour la base de données\n\n"
            "⚠️  Cette opération est sûre mais irréversible.\n\n"
            "Continuer ?"
        )
        
        if not response:
            return
            
        try:
            from lib.utils import ensure_images_subfolders, copy_image_to_originals
            
            # Créer la structure
            subfolders = ensure_images_subfolders()
            
            # Migrer toutes les cartes
            migrated_count = 0
            error_count = 0
            
            cards = self.repo.list_cards()
            
            for card in cards:
                if not card.img or not os.path.exists(card.img):
                    continue
                    
                # Vérifier si déjà dans originals
                if subfolders['originals'] in card.img:
                    continue
                    
                # Copier vers originals
                new_path = copy_image_to_originals(card.img, card.name)
                
                if new_path:
                    # Mettre à jour en base
                    card.img = new_path.replace('\\', '/')
                    self.repo.update(card)
                    migrated_count += 1
                else:
                    error_count += 1
            
            # Actualiser l'interface
            self.refresh_all_tabs()
            
            # Afficher le résultat
            result_msg = f"Migration terminée !\n\n"
            result_msg += f"✅ Images migrées : {migrated_count}\n"
            if error_count > 0:
                result_msg += f"❌ Erreurs : {error_count}\n"
            result_msg += f"\n📁 Structure créée :\n"
            result_msg += f"   • Originaux : images/originals/\n"
            result_msg += f"   • Cartes : images/cards/\n"
            result_msg += f"   • Templates : images/templates/"
            
            messagebox.showinfo("Migration terminée", result_msg)
            
        except Exception as e:
            messagebox.showerror("Erreur de migration", f"Erreur lors de la migration :\n{e}")
    
    def organize_templates(self):
        """Organise les templates dans le dossier templates/."""
        response = messagebox.askyesno(
            "Organiser les templates",
            "Cette fonction va :\n\n"
            "✅ Copier tous les templates configurés vers 'images/templates/'\n"
            "✅ Mettre à jour automatiquement les paramètres\n"
            "✅ Créer des noms de fichiers organisés\n\n"
            "ℹ️  Utile pour centraliser vos templates par rareté.\n\n"
            "Continuer ?"
        )
        
        if not response:
            return
            
        try:
            from lib.utils import organize_all_images
            
            # Organiser les templates
            results = organize_all_images()
            
            # Afficher le résultat
            messagebox.showinfo("Organisation terminée", results['summary'])
            
        except Exception as e:
            messagebox.showerror("Erreur d'organisation", f"Erreur lors de l'organisation :\n{e}")
    
    def show_deck_viewer(self):
        """Ouvre la fenêtre de visualisation du deck."""
        try:
            open_deck_viewer(self, self.repo)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le visualiseur de deck :\n{e}")
    
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
    
    def clear_all_data(self):
        """Vide complètement la base de données et supprime toutes les images."""
        # Confirmation en plusieurs étapes pour éviter les accidents
        warning_text = """⚠️ ATTENTION - SUPPRESSION COMPLÈTE ⚠️

Cette action va DÉFINITIVEMENT supprimer :
• TOUTES les cartes de la base de données
• TOUS les acteurs et leurs liaisons
• TOUTES les images dans le dossier images/
• TOUTES les images générées et templates

Cette action est IRRÉVERSIBLE !

Êtes-vous ABSOLUMENT sûr de vouloir continuer ?"""
        
        if not messagebox.askyesno("⚠️ Confirmation - Clear Data", warning_text, icon='warning'):
            return
        
        # Seconde confirmation plus stricte
        final_text = """🚨 DERNIÈRE CONFIRMATION 🚨

Vous allez perdre TOUTES vos données !

Pour confirmer, tapez exactement : SUPPRIMER TOUT

Cette action ne peut pas être annulée."""
        
        from tkinter import simpledialog
        confirmation = simpledialog.askstring(
            "🚨 Confirmation finale", 
            final_text,
            show='*'  # Masquer le texte
        )
        
        if confirmation != "SUPPRIMER TOUT":
            messagebox.showinfo("Annulé", "Suppression annulée.")
            return
        
        try:
            # Supprimer toutes les images
            images_folder = Path("images")
            if images_folder.exists():
                import shutil
                deleted_files = []
                for item in images_folder.rglob("*"):
                    if item.is_file():
                        deleted_files.append(item)
                        item.unlink()
                    elif item.is_dir() and not any(item.iterdir()):
                        item.rmdir()
                
                # Recréer le dossier vide
                if not images_folder.exists():
                    images_folder.mkdir(exist_ok=True)
                
                print(f"🗑️ {len(deleted_files)} fichiers supprimés du dossier images/")
            
            # Vider complètement la base de données
            import sqlite3
            with sqlite3.connect(self.repo.db_path) as conn:
                # Obtenir toutes les tables
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                # Supprimer toutes les données de toutes les tables
                for table in tables:
                    if table != 'sqlite_sequence':  # Table système SQLite
                        conn.execute(f"DELETE FROM {table}")
                
                # Réinitialiser les séquences d'auto-increment
                conn.execute("DELETE FROM sqlite_sequence")
                conn.commit()
                
                print(f"🗑️ Toutes les données supprimées de {len(tables)} tables")
            
            # Actualiser l'interface
            self.refresh_all_tabs()
            
            success_text = """✅ SUPPRESSION TERMINÉE

Toutes les données ont été supprimées :
• Base de données vidée
• Dossier images/ nettoyé
• Interface actualisée

L'application est maintenant dans un état vierge."""
            
            messagebox.showinfo("✅ Terminé", success_text)
            
        except Exception as e:
            error_text = f"""❌ ERREUR lors de la suppression

Une erreur s'est produite :
{str(e)}

Certaines données peuvent ne pas avoir été supprimées.
Vérifiez manuellement les fichiers si nécessaire."""
            
            messagebox.showerror("❌ Erreur", error_text)
    
    def show_guide(self):
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
                print(f"[INFO] Ouverture du guide: {guide_path}")
                os.startfile(str(guide_path))
            else:
                # Afficher où on a cherché pour aider au debug
                search_locations = [str(p) for p in possible_paths]
                message = f"Le fichier GUIDE.md n'a pas été trouvé.\n\nEmplacements vérifiés:\n" + "\n".join(search_locations)
                messagebox.showinfo("Guide non trouvé", message)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le guide: {e}")
    
    # === NOUVELLES MÉTHODES POUR LES ACTEURS ===
    
    def manage_actors(self):
        """Ouvre la fenêtre de gestion des acteurs."""
        try:
            from lib.actor_ui import open_actor_manager
            open_actor_manager(self, default_db_path())
            # Rafraîchir l'interface après fermeture
            self.after(500, self.refresh_all_tabs)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture de la gestion d'acteurs :\n{e}")
    
    def export_by_actor(self):
        """Ouvre le dialogue d'export par acteur."""
        try:
            from lib.actor_selector import open_actor_export_dialog
            open_actor_export_dialog(self, default_db_path())
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture de l'export par acteur :\n{e}")
    
    def demo_actors(self):
        """Lance la démonstration du système d'acteurs."""
        try:
            import subprocess
            import sys
            from pathlib import Path
            
            # Demander confirmation
            response = messagebox.askyesno(
                "Démonstration Acteurs",
                "Voulez-vous ouvrir la démonstration complète du système d'acteurs ?\n\n"
                "Cela ouvrira une nouvelle fenêtre avec :\n"
                "• Interface de gestion des acteurs\n"
                "• Visualisation des cartes par acteur\n"
                "• Outils d'export personnalisés\n\n"
                "L'application actuelle restera ouverte."
            )
            
            if response:
                demo_path = Path(__file__).parent / "demo_actors.py"
                if demo_path.exists():
                    # Lancer la démo dans un processus séparé
                    subprocess.Popen([sys.executable, str(demo_path)], 
                                   cwd=str(Path(__file__).parent))
                    messagebox.showinfo("Info", "Démonstration lancée dans une nouvelle fenêtre !")
                else:
                    messagebox.showerror("Erreur", f"Fichier de démonstration introuvable :\n{demo_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du lancement de la démonstration :\n{e}")

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

    # Initialisation et vérification de la base de données
    print("🚀 Démarrage de l'éditeur de cartes Love2D...")
    print("=" * 50)
    
    db_path = default_db_path()
    
    try:
        # Vérification et migration de la base de données
        ensure_db(db_path)
        print("✅ Base de données initialisée et vérifiée")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données :")
        print(f"   {e}")
        
        # Demander à l'utilisateur s'il veut continuer avec la version legacy
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Masquer la fenêtre principale
        
        response = messagebox.askyesno(
            "Erreur de base de données",
            "Une erreur s'est produite lors de la vérification de la base de données.\n\n"
            f"Erreur : {e}\n\n"
            "Voulez-vous essayer de continuer avec le système legacy ?\n"
            "(Non recommandé, mais peut permettre de récupérer vos données)",
            icon="warning"
        )
        
        root.destroy()
        
        if not response:
            print("❌ Arrêt de l'application.")
            sys.exit(1)
        
        # Essayer avec le système legacy
        try:
            from lib.database import ensure_db_legacy
            ensure_db_legacy(db_path)
            print("⚠️  Mode de compatibilité activé (legacy)")
        except Exception as e2:
            print(f"❌ Impossible de continuer même en mode legacy : {e2}")
            sys.exit(1)
    
    repo = CardRepo(db_path)
    
    # Charge les paramètres de l'application
    load_settings()
    
    print("=" * 50)

    try:
        app = FinalMainApp(repo)
        app.mainloop()
    except Exception as e:
        print(f"[ERREUR] Impossible de lancer l'application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
