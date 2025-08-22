#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 INTÉGRATION DE L'EXPORTEUR DE PACKAGE DANS L'UI
=================================================

Ajoute le bouton "Export Package" dans l'interface principale
pour créer des packages ZIP complets.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from pathlib import Path

# Import depuis lib si possible
try:
    from lib.game_package_exporter import GamePackageExporter
    from lib.database import CardRepo
    from lib.config import DB_FILE
except ImportError:
    import sys
    sys.path.insert(0, 'lib')
    from game_package_exporter import GamePackageExporter
    from database import CardRepo
    from config import DB_FILE

class PackageExportDialog:
    """Dialog pour configurer et lancer l'export de package."""
    
    def __init__(self, parent, repo):
        """
        Initialise le dialog d'export.
        
        Args:
            parent: Fenêtre parent
            repo: Repository des cartes
        """
        self.parent = parent
        self.repo = repo
        self.result = None
        
        # Créer la fenêtre
        self.window = tk.Toplevel(parent)
        self.window.title("🎮 Export Package de Jeu")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Centrer la fenêtre
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="🎮 Export Package de Jeu Complet", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_text = """Créez un package ZIP structuré contenant :
• Fichier Lua des cartes avec formatage
• Images fusionnées des cartes
• Polices utilisées
• Documentation complète

Prêt pour intégration Love2D !"""
        
        desc_label = ttk.Label(main_frame, text=desc_text, justify="left")
        desc_label.pack(pady=(0, 20), anchor="w")
        
        # Configuration du package
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.pack(fill="x", pady=(0, 20))
        
        # Nom du package
        ttk.Label(config_frame, text="Nom du package:").pack(anchor="w")
        self.package_name_var = tk.StringVar(value="mon_jeu_cartes")
        package_name_entry = ttk.Entry(config_frame, textvariable=self.package_name_var, width=40)
        package_name_entry.pack(fill="x", pady=(5, 10))
        
        # Dossier de sortie
        ttk.Label(config_frame, text="Dossier de sortie:").pack(anchor="w")
        
        output_frame = ttk.Frame(config_frame)
        output_frame.pack(fill="x", pady=(5, 10))
        
        self.output_dir_var = tk.StringVar(value="game_packages")
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        output_entry.pack(side="left", fill="x", expand=True)
        
        browse_btn = ttk.Button(output_frame, text="Parcourir...", 
                               command=self.browse_output_dir)
        browse_btn.pack(side="right", padx=(5, 0))
        
        # Options d'export
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill="x", pady=(0, 20))
        
        self.include_images_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Inclure les images fusionnées", 
                       variable=self.include_images_var).pack(anchor="w")
        
        self.include_fonts_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Inclure les polices utilisées", 
                       variable=self.include_fonts_var).pack(anchor="w")
        
        self.include_docs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Inclure la documentation", 
                       variable=self.include_docs_var).pack(anchor="w")
        
        # Informations sur les cartes
        info_frame = ttk.LabelFrame(main_frame, text="Informations", padding="10")
        info_frame.pack(fill="x", pady=(0, 20))
        
        self.update_info(info_frame)
        
        # Boutons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x")
        
        ttk.Button(buttons_frame, text="Annuler", 
                  command=self.cancel).pack(side="right", padx=(5, 0))
        
        self.export_btn = ttk.Button(buttons_frame, text="🎮 Créer Package", 
                                    command=self.start_export)
        self.export_btn.pack(side="right")
        
        # Barre de progression (cachée initialement)
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_var = tk.StringVar(value="")
        self.progress_label = ttk.Label(self.progress_frame, textvariable=self.progress_var)
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        
    def update_info(self, parent_frame):
        """Met à jour les informations sur les cartes."""
        try:
            cards = self.repo.list_cards()
            
            info_text = f"Cartes disponibles: {len(cards)}"
            if cards:
                # Analyser rapidement les ressources
                fonts_used = set()
                images_used = set()
                
                for card in cards:
                    if hasattr(card, 'title_font') and card.title_font:
                        fonts_used.add(card.title_font)
                    if hasattr(card, 'text_font') and card.text_font:
                        fonts_used.add(card.text_font)
                    if hasattr(card, 'img') and card.img:
                        images_used.add(card.img)
                
                info_text += f"\nPolices utilisées: {len(fonts_used)}"
                info_text += f"\nImages référencées: {len(images_used)}"
            
            ttk.Label(parent_frame, text=info_text, justify="left").pack(anchor="w")
            
        except Exception as e:
            ttk.Label(parent_frame, text=f"Erreur: {e}", foreground="red").pack(anchor="w")
    
    def browse_output_dir(self):
        """Ouvre le dialog de sélection de dossier."""
        directory = filedialog.askdirectory(
            title="Choisir le dossier de sortie",
            initialdir=self.output_dir_var.get()
        )
        if directory:
            self.output_dir_var.set(directory)
    
    def start_export(self):
        """Lance l'export en arrière-plan."""
        
        # Validation
        package_name = self.package_name_var.get().strip()
        if not package_name:
            messagebox.showerror("Erreur", "Le nom du package est requis.")
            return
        
        output_dir = self.output_dir_var.get().strip()
        if not output_dir:
            messagebox.showerror("Erreur", "Le dossier de sortie est requis.")
            return
        
        # Créer le dossier si nécessaire
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier: {e}")
            return
        
        # Désactiver le bouton et afficher la progression
        self.export_btn.config(state="disabled")
        self.progress_frame.pack(fill="x", pady=(10, 0))
        self.progress_label.pack(fill="x")
        self.progress_bar.pack(fill="x", pady=(5, 0))
        self.progress_bar.start(10)
        
        # Lancer l'export en arrière-plan
        self.progress_var.set("Initialisation de l'export...")
        thread = threading.Thread(target=self.do_export, args=(package_name, output_dir))
        thread.daemon = True
        thread.start()
    
    def do_export(self, package_name, output_dir):
        """Effectue l'export (dans un thread séparé)."""
        try:
            # Mettre à jour le statut
            self.window.after(0, lambda: self.progress_var.set("Création de l'exporteur..."))
            
            # Créer l'exporteur
            exporter = GamePackageExporter(self.repo, output_dir)
            
            # Configurer les options
            if not self.include_images_var.get():
                # Option pour désactiver les images (si implémentée)
                pass
            
            # Mettre à jour le statut
            self.window.after(0, lambda: self.progress_var.set("Export en cours..."))
            
            # Effectuer l'export
            package_path = exporter.export_complete_package(package_name)
            
            # Succès
            self.window.after(0, lambda: self.export_success(package_path))
            
        except Exception as e:
            # Erreur
            self.window.after(0, lambda: self.export_error(str(e)))
    
    def export_success(self, package_path):
        """Appelé quand l'export réussit."""
        self.progress_bar.stop()
        self.progress_frame.pack_forget()
        self.export_btn.config(state="normal")
        
        # Calculer la taille du fichier
        if os.path.exists(package_path):
            size = os.path.getsize(package_path)
            size_text = f"{size:,} octets ({size/1024:.1f} KB)"
        else:
            size_text = "Taille inconnue"
        
        # Message de succès
        message = f"Package créé avec succès !\n\nFichier: {os.path.basename(package_path)}\nTaille: {size_text}\n\nVoulez-vous ouvrir le dossier contenant le package ?"
        
        if messagebox.askyesno("Succès", message):
            # Ouvrir le dossier
            folder_path = os.path.dirname(package_path)
            os.startfile(folder_path)  # Windows
        
        self.result = package_path
        self.window.destroy()
    
    def export_error(self, error_message):
        """Appelé quand l'export échoue."""
        self.progress_bar.stop()
        self.progress_frame.pack_forget()
        self.export_btn.config(state="normal")
        
        messagebox.showerror("Erreur d'export", f"Erreur lors de la création du package:\n\n{error_message}")
    
    def cancel(self):
        """Annule l'export."""
        self.result = None
        self.window.destroy()

def add_package_export_to_ui(parent_frame, repo):
    """
    Ajoute le bouton d'export de package dans l'interface.
    
    Args:
        parent_frame: Frame parent où ajouter le bouton
        repo: Repository des cartes
    """
    
    def open_package_export():
        """Ouvre le dialog d'export de package."""
        dialog = PackageExportDialog(parent_frame.winfo_toplevel(), repo)
        parent_frame.wait_window(dialog.window)
        return dialog.result
    
    # Créer le bouton
    package_btn = ttk.Button(parent_frame, text="🎮 Export Package Jeu",
                            command=open_package_export)
    package_btn.pack(side="left", padx=(5, 0))
    
    return package_btn

def test_dialog():
    """Test du dialog d'export."""
    
    # Créer une fenêtre de test
    root = tk.Tk()
    root.title("Test Export Package")
    root.geometry("300x200")
    
    # Repository de test
    try:
        repo = CardRepo(DB_FILE)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger la base de données: {e}")
        root.destroy()
        return
    
    # Bouton pour ouvrir le dialog
    def open_dialog():
        dialog = PackageExportDialog(root, repo)
        root.wait_window(dialog.window)
        if dialog.result:
            messagebox.showinfo("Résultat", f"Package créé: {dialog.result}")
    
    ttk.Button(root, text="Ouvrir Dialog Export", 
              command=open_dialog).pack(expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    test_dialog()
