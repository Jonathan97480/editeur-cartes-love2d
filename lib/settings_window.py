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
        self.window.geometry("650x450")
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
        title_label = ttk.Label(main_frame, text="Configuration des Images", 
                               font=('TkDefaultFont', 12, 'bold'))
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Section Template
        template_section = ttk.LabelFrame(main_frame, text="Image Template", padding=10)
        template_section.pack(fill='x', pady=(0, 15))
        
        ttk.Label(template_section, text="Sélectionnez l'image template (zones de texte et contours) :", 
                 font=('TkDefaultFont', 9, 'bold')).pack(anchor='w', pady=(0, 8))
        
        template_frame = ttk.Frame(template_section)
        template_frame.pack(fill='x', pady=(0, 5))
        
        self.template_var = tk.StringVar()
        entry = ttk.Entry(template_frame, textvariable=self.template_var, state='readonly', width=50)
        entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(template_frame, text="📁 Parcourir...", command=self._browse_template, width=15)
        browse_btn.pack(side='right')
        
        # Section Information
        info_section = ttk.LabelFrame(main_frame, text="Comment ça marche", padding=10)
        info_section.pack(fill='both', expand=True, pady=(0, 15))
        
        info_text = """1. Sélectionnez une image template qui contient les zones de texte et contours de carte
        
2. Cette image doit avoir un fond transparent (PNG avec transparence recommandé)

3. Quand vous sauvegardez une carte, l'application :
   • Prend l'image de la carte (illustration)
   • La redimensionne pour correspondre au template
   • Superpose le template par-dessus
   • Sauvegarde le résultat dans le dossier 'images'
   • Nomme le fichier avec le nom de la carte (espaces remplacés par _)
   
4. Le fichier final peut être utilisé dans votre jeu Love2D"""
        
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
        
        # Boutons de droite
        right_btns = ttk.Frame(btn_section)
        right_btns.pack(side='right')
        
        ttk.Button(right_btns, text="❌ Annuler", 
                  command=self._on_close, width=12).pack(side='right', padx=(10, 0))
        ttk.Button(right_btns, text="✅ Appliquer", 
                  command=self._apply_settings, width=12).pack(side='right')

    def _load_current_settings(self):
        self.template_var.set(APP_SETTINGS.get("template_image", ""))

    def _browse_template(self):
        path = filedialog.askopenfilename(
            title="Choisir l'image template",
            filetypes=[
                ("Images PNG", "*.png"),
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if path:
            self.template_var.set(path)

    def _apply_settings(self):
        APP_SETTINGS["template_image"] = self.template_var.get()
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
