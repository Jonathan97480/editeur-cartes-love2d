#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre de réglages simple sans émojis
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .config import APP_SETTINGS, save_settings
from .utils import ensure_images_folder

class SimpleSettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        
    def show(self):
        """Affiche la fenêtre de réglages."""
        if self.window is not None:
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("Reglages - Configuration des Images")
        self.window.geometry("850x700")
        self.window.resizable(True, True)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Quand la fenêtre est fermée
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._build_ui()
        self._load_current_settings()
        
        # Centre la fenêtre
        self.window.geometry("+%d+%d" % (self.parent.winfo_rootx() + 50, self.parent.winfo_rooty() + 50))
    
    def _on_close(self):
        """Appelé quand la fenêtre est fermée."""
        self.window.destroy()
        self.window = None

    def _build_ui(self):
        # Frame principal avec scrollbar au cas où
        canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = ttk.Frame(scrollable_frame, padding=25)
        main_frame.pack(fill='both', expand=True)
        
        # Titre principal
        title_label = ttk.Label(main_frame, text="CONFIGURATION DES IMAGES PAR RARETE", 
                               font=('TkDefaultFont', 14, 'bold'))
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Variables pour stocker les chemins des templates
        self.rarity_vars = {}
        
        # Créer une section pour chaque rareté
        from .config import RARITY_VALUES, RARITY_LABELS
        
        for rarity in RARITY_VALUES:
            rarity_section = ttk.LabelFrame(main_frame, text=f"TEMPLATE {RARITY_LABELS[rarity].upper()}", padding=15)
            rarity_section.pack(fill='x', pady=(0, 15))
            
            # Description
            desc_label = ttk.Label(rarity_section, 
                                 text=f"Image superposee pour les cartes {RARITY_LABELS[rarity].lower()}s :", 
                                 font=('TkDefaultFont', 10))
            desc_label.pack(anchor='w', pady=(0, 8))
            
            # Frame pour l'entrée et le bouton
            template_frame = ttk.Frame(rarity_section)
            template_frame.pack(fill='x', pady=(0, 8))
            
            # Variable pour cette rareté
            self.rarity_vars[rarity] = tk.StringVar()
            
            # Entrée
            entry = ttk.Entry(template_frame, textvariable=self.rarity_vars[rarity], 
                            state='readonly', font=('TkDefaultFont', 9), width=50)
            entry.pack(side='left', fill='x', expand=True, padx=(0, 15))
            
            # Bouton parcourir
            browse_btn = ttk.Button(template_frame, text="PARCOURIR", 
                                  command=lambda r=rarity: self._browse_rarity_template(r), 
                                  width=12)
            browse_btn.pack(side='right', padx=(0, 8))
            
            # Bouton effacer
            clear_btn = ttk.Button(template_frame, text="EFFACER", 
                                 command=lambda r=rarity: self.rarity_vars[r].set(""), 
                                 width=10)
            clear_btn.pack(side='right')
        
        # Section Information
        info_section = ttk.LabelFrame(main_frame, text="COMMENT CA MARCHE", padding=15)
        info_section.pack(fill='x', pady=(0, 20))
        
        steps = [
            "1. Selectionnez une image template qui contient les zones de texte et contours de carte",
            "",
            "2. Cette image doit avoir un fond transparent (PNG avec transparence recommande)",
            "",
            "3. Quand vous sauvegardez une carte, l'application :",
            "   • Prend l'image de la carte (illustration)",
            "   • La redimensionne pour correspondre au template", 
            "   • Superpose le template par-dessus",
            "   • Sauvegarde le resultat dans le dossier 'images'",
            "   • Nomme le fichier avec le nom de la carte (espaces remplaces par _)",
            "",
            "4. Le fichier final peut etre utilise dans votre jeu Love2D",
            "",
            "CONSEIL : Utilisez une image PNG transparente avec des contours nets",
            "pour un meilleur resultat de fusion."
        ]
        
        for step in steps:
            if step == "":
                ttk.Label(info_section, text="").pack(anchor='w')
            else:
                ttk.Label(info_section, text=step, 
                         font=('TkDefaultFont', 9), 
                         wraplength=600).pack(anchor='w', padx=(0, 0))
        
        # Section Actions
        action_section = ttk.LabelFrame(main_frame, text="ACTIONS", padding=15)
        action_section.pack(fill='x', pady=(0, 20))
        
        # Première ligne d'actions
        action_frame1 = ttk.Frame(action_section)
        action_frame1.pack(fill='x', pady=(0, 10))
        
        ttk.Button(action_frame1, text="OUVRIR DOSSIER IMAGES", 
                  command=self._open_images_folder, width=25).pack(side='left', padx=(0, 15))
        
        ttk.Button(action_frame1, text="EFFACER TOUTES SELECTIONS", 
                  command=self._clear_all_templates, width=25).pack(side='left')
        
        # Section Boutons principaux
        btn_section = ttk.Frame(main_frame)
        btn_section.pack(fill='x', pady=(20, 0))
        
        # Boutons de validation
        ttk.Button(btn_section, text="ANNULER", 
                  command=self._on_close, width=15).pack(side='right', padx=(15, 0))
        ttk.Button(btn_section, text="APPLIQUER ET FERMER", 
                  command=self._apply_settings, width=20).pack(side='right')

    def _load_current_settings(self):
        """Charge les paramètres actuels depuis la configuration."""
        # Charger les templates par rareté
        rarity_templates = APP_SETTINGS.get("rarity_templates", {})
        for rarity in self.rarity_vars:
            self.rarity_vars[rarity].set(rarity_templates.get(rarity, ""))

    def _browse_rarity_template(self, rarity):
        """Ouvre le dialogue de sélection pour un template de rareté spécifique."""
        from .config import RARITY_LABELS
        path = filedialog.askopenfilename(
            title=f"Choisir l'image template pour {RARITY_LABELS[rarity]}",
            filetypes=[
                ("Images PNG", "*.png"),
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if path:
            self.rarity_vars[rarity].set(path)

    def _apply_settings(self):
        """Applique et sauvegarde les paramètres."""
        # Sauvegarder les templates par rareté
        APP_SETTINGS["rarity_templates"] = {}
        for rarity, var in self.rarity_vars.items():
            APP_SETTINGS["rarity_templates"][rarity] = var.get()
        
        save_settings()
        messagebox.showinfo("Reglages", "Parametres sauvegardes avec succes !")
        self._on_close()

    def _clear_all_templates(self):
        """Efface toutes les sélections de templates."""
        for var in self.rarity_vars.values():
            var.set("")

    def _open_images_folder(self):
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
