#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre de réglages pour l'éditeur de cartes
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .config import APP_SETTINGS, save_settings
from .utils import ensure_images_folder

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        
    def show(self):
        """Affiche la fenêtre de réglages."""
        if self.window is not None:
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("Réglages")
        self.window.geometry("1195x646")
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
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Titre principal
        title_label = ttk.Label(main_frame, text="Configuration des Images par Rareté", 
                               font=('TkDefaultFont', 12, 'bold'))
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Frame scrollable pour les templates
        canvas = tk.Canvas(main_frame, height=400)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Variables pour stocker les chemins des templates
        self.rarity_vars = {}
        
        # Créer une section pour chaque rareté
        from .config import RARITY_VALUES, RARITY_LABELS
        
        for rarity in RARITY_VALUES:
            rarity_section = ttk.LabelFrame(scrollable_frame, text=f"Template {RARITY_LABELS[rarity]}", padding=15)
            rarity_section.pack(fill='x', pady=(0, 15), padx=8)
            
            # Description
            desc_label = ttk.Label(rarity_section, 
                                 text=f"Image superposée pour les cartes {RARITY_LABELS[rarity].lower()}s :", 
                                 font=('TkDefaultFont', 9))
            desc_label.pack(anchor='w', pady=(0, 8))
            
            # Frame pour l'entrée et le bouton
            template_frame = ttk.Frame(rarity_section)
            template_frame.pack(fill='x', pady=(0, 8))
            
            # Variable pour cette rareté
            self.rarity_vars[rarity] = tk.StringVar()
            
            # Entrée
            entry = ttk.Entry(template_frame, textvariable=self.rarity_vars[rarity], 
                            state='readonly', width=50)
            entry.pack(side='left', fill='x', expand=True, padx=(0, 12))
            
            # Bouton parcourir
            browse_btn = ttk.Button(template_frame, text="📁 Parcourir", 
                                  command=lambda r=rarity: self._browse_rarity_template(r), 
                                  width=12)
            browse_btn.pack(side='right', padx=(0, 8))
            
            # Bouton effacer
            clear_btn = ttk.Button(template_frame, text="🗑️ Effacer", 
                                 command=lambda r=rarity: self.rarity_vars[r].set(""), 
                                 width=10)
            clear_btn.pack(side='right')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Section Information
        info_section = ttk.LabelFrame(main_frame, text="Comment ça marche", padding=10)
        info_section.pack(fill='both', expand=True, pady=(15, 15))
        
        info_text = """1. Sélectionnez une image template pour chaque rareté de carte :
   • Commun : Image superposée pour les cartes communes
   • Rare : Image superposée pour les cartes rares  
   • Légendaire : Image superposée pour les cartes légendaires
   • Mythique : Image superposée pour les cartes mythiques

2. Ces images doivent avoir un fond transparent (PNG avec transparence recommandé)

3. Quand vous sauvegardez une carte, l'application :
   • Prend l'image de la carte (illustration)
   • La redimensionne pour correspondre au template
   • Sélectionne le template selon la rareté de la carte
   • Superpose le template correspondant par-dessus
   • Sauvegarde le résultat dans le dossier 'images'
   • Nomme le fichier avec le nom de la carte (espaces remplacés par _)
   
4. Si aucun template n'est défini pour une rareté, l'image originale est utilisée

5. Le fichier final peut être utilisé dans votre jeu Love2D"""
        
        # Utiliser un Text widget avec scrollbar pour le texte d'information
        text_frame = ttk.Frame(info_section)
        text_frame.pack(fill='both', expand=True)
        
        info_text_widget = tk.Text(text_frame, height=8, wrap='word', 
                                  font=('TkDefaultFont', 9), 
                                  bg='#f0f0f0', relief='flat', 
                                  state='normal')
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=info_text_widget.yview)
        info_text_widget.configure(yscrollcommand=scrollbar.set)
        
        info_text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        info_text_widget.insert('1.0', info_text)
        info_text_widget.configure(state='disabled')
        
        # Section Boutons
        btn_section = ttk.Frame(main_frame)
        btn_section.pack(fill='x', pady=(15, 0))
        
        # Boutons de gauche
        left_btns = ttk.Frame(btn_section)
        left_btns.pack(side='left')
        
        ttk.Button(left_btns, text="📂 Ouvrir dossier images", 
                  command=self._open_images_folder, width=20).pack(side='left', padx=(0, 10))
        
        ttk.Button(left_btns, text="🗂️ Organiser templates", 
                  command=self._organize_templates, width=18).pack(side='left', padx=(0, 10))
        
        # Boutons de droite
        right_btns = ttk.Frame(btn_section)
        right_btns.pack(side='right')
        
        ttk.Button(right_btns, text="❌ Annuler", 
                  command=self._on_close, width=12).pack(side='right', padx=(10, 0))
        ttk.Button(right_btns, text="✅ Appliquer", 
                  command=self._apply_settings, width=12).pack(side='right')

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

    def _organize_templates(self):
        """Organise les templates dans le dossier templates/."""
        response = messagebox.askyesno(
            "Organiser les templates",
            "Cette fonction va :\n\n"
            "✅ Copier tous les templates configurés vers le dossier 'images/templates/'\n"
            "✅ Mettre à jour automatiquement les paramètres\n"
            "✅ Créer une structure organisée\n\n"
            "⚠️  Les fichiers originaux ne seront pas supprimés.\n\n"
            "Continuer ?"
        )
        
        if not response:
            return
            
        try:
            from .utils import organize_all_images
            
            # Organiser les images
            results = organize_all_images()
            
            # Recharger les paramètres mis à jour
            self._load_current_settings()
            
            # Afficher le résultat
            messagebox.showinfo("Organisation terminée", results['summary'])
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'organisation :\n{e}")

    def _apply_settings(self):
        """Applique et sauvegarde les paramètres."""
        # Sauvegarder les templates par rareté
        APP_SETTINGS["rarity_templates"] = {}
        for rarity, var in self.rarity_vars.items():
            APP_SETTINGS["rarity_templates"][rarity] = var.get()
        
        save_settings()
        messagebox.showinfo("Réglages", "Paramètres sauvegardés avec succès !")
        self._on_close()

    def _open_images_folder(self):
        folder_path = ensure_images_folder()
        try:
            os.startfile(folder_path)  # Windows
        except AttributeError:
            try:
                os.system(f'open "{folder_path}"')  # macOS
            except:
                os.system(f'xdg-open "{folder_path}"')  # Linux
