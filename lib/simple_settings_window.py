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
        self.window.geometry("700x500")
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
        title_label = ttk.Label(main_frame, text="CONFIGURATION DES IMAGES", 
                               font=('TkDefaultFont', 14, 'bold'))
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Section Template
        template_section = ttk.LabelFrame(main_frame, text="IMAGE TEMPLATE", padding=15)
        template_section.pack(fill='x', pady=(0, 20))
        
        ttk.Label(template_section, text="Selectionnez l'image template (zones de texte et contours) :", 
                 font=('TkDefaultFont', 10, 'bold')).pack(anchor='w', pady=(0, 10))
        
        template_frame = ttk.Frame(template_section)
        template_frame.pack(fill='x', pady=(0, 10))
        
        self.template_var = tk.StringVar()
        entry = ttk.Entry(template_frame, textvariable=self.template_var, state='readonly', 
                         font=('TkDefaultFont', 10), width=60)
        entry.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        browse_btn = ttk.Button(template_frame, text="PARCOURIR...", 
                               command=self._browse_template, width=15)
        browse_btn.pack(side='right')
        
        # Affichage du chemin actuel
        current_label = ttk.Label(template_section, text="Fichier actuel :", 
                                 font=('TkDefaultFont', 9))
        current_label.pack(anchor='w', pady=(5, 0))
        
        self.current_path_label = ttk.Label(template_section, text="Aucun fichier selectionne", 
                                           font=('TkDefaultFont', 9), foreground='gray')
        self.current_path_label.pack(anchor='w', pady=(0, 10))
        
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
        
        ttk.Button(action_frame1, text="EFFACER SELECTION", 
                  command=self._clear_template, width=20).pack(side='left')
        
        # Section Boutons principaux
        btn_section = ttk.Frame(main_frame)
        btn_section.pack(fill='x', pady=(20, 0))
        
        # Boutons de validation
        ttk.Button(btn_section, text="ANNULER", 
                  command=self._on_close, width=15).pack(side='right', padx=(15, 0))
        ttk.Button(btn_section, text="APPLIQUER ET FERMER", 
                  command=self._apply_settings, width=20).pack(side='right')

    def _load_current_settings(self):
        current_template = APP_SETTINGS.get("template_image", "")
        self.template_var.set(current_template)
        
        if current_template:
            if os.path.exists(current_template):
                self.current_path_label.config(text=f"✓ {current_template}", foreground='green')
            else:
                self.current_path_label.config(text=f"✗ Fichier introuvable: {current_template}", foreground='red')
        else:
            self.current_path_label.config(text="Aucun fichier selectionne", foreground='gray')

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
            self.current_path_label.config(text=f"Nouveau: {path}", foreground='blue')

    def _clear_template(self):
        self.template_var.set("")
        self.current_path_label.config(text="Selection effacee", foreground='orange')

    def _apply_settings(self):
        APP_SETTINGS["template_image"] = self.template_var.get()
        save_settings()
        messagebox.showinfo("Reglages", "Parametres sauvegardes avec succes !")
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
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier: {e}")
