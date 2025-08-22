#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Éditeur de formatage de texte pour les cartes
Permet le positionnement précis du titre et du texte avec aperçu visuel
"""
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font
import sqlite3
import json
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
from .font_manager import get_font_manager, get_available_fonts

class TextFormattingEditor:
    def __init__(self, parent, card_id=None, card_data=None, repo=None):
        self.parent = parent
        self.card_id = card_id
        self.card_data = card_data or {}
        self.repo = repo  # Repo pour sauvegarder
        
        # Initialiser le gestionnaire de polices
        self.font_manager = get_font_manager()
        self.available_fonts = get_available_fonts()
        
        # Valeurs par défaut
        self.title_x = self.card_data.get('title_x', 50)
        self.title_y = self.card_data.get('title_y', 30)
        self.title_font = self.card_data.get('title_font', 'Arial')
        self.title_size = self.card_data.get('title_size', 16)
        self.title_color = self.card_data.get('title_color', '#000000')
        
        self.text_x = self.card_data.get('text_x', 50)
        self.text_y = self.card_data.get('text_y', 100)
        self.text_width = self.card_data.get('text_width', 200)
        self.text_height = self.card_data.get('text_height', 150)
        self.text_font = self.card_data.get('text_font', 'Arial')
        self.text_size = self.card_data.get('text_size', 12)
        self.text_color = self.card_data.get('text_color', '#000000')
        self.text_align = self.card_data.get('text_align', 'left')
        self.line_spacing = self.card_data.get('line_spacing', 1.2)
        self.text_wrap = self.card_data.get('text_wrap', 1)
        
        # Formatage du coût en énergie
        self.energy_x = self.card_data.get('energy_x', 25)
        self.energy_y = self.card_data.get('energy_y', 25)
        self.energy_font = self.card_data.get('energy_font', 'Arial')
        self.energy_size = self.card_data.get('energy_size', 14)
        self.energy_color = self.card_data.get('energy_color', '#FFFFFF')
        
        # Coût en énergie (PowerBlow)
        self.energy_value = self.card_data.get('powerblow', 0)
        
        # Texte d'exemple
        self.title_text = self.card_data.get('nom', 'Titre de la carte')
        self.content_text = self.card_data.get('description', 'Description de la carte avec du texte plus long pour tester le retour à la ligne automatique.')
        
        # Image de la carte
        self.card_image_path = self.card_data.get('img', None)
        self.card_image = None
        self.card_image_tk = None
        
        self.create_window()
        # L'image sera chargée dans create_window() avant le premier update_preview
        
    def load_card_image(self):
        """Charge l'image de la carte pour l'aperçu"""
        if not self.card_image_path:
            return
            
        try:
            # Construire le chemin de l'image
            if Path(self.card_image_path).is_absolute():
                # Chemin absolu
                image_path = Path(self.card_image_path.strip())
            else:
                # Chemin relatif
                base_path = Path(__file__).parent.parent
                image_path = base_path / self.card_image_path.strip()
            
            if image_path.exists():
                # Charger l'image
                self.card_image = Image.open(image_path)
                
                # S'adapter dynamiquement à la taille du canvas
                # Le canvas sera créé avec des dimensions calculées
                if hasattr(self, 'preview_canvas'):
                    canvas_width = self.preview_canvas.winfo_reqwidth()
                    canvas_height = self.preview_canvas.winfo_reqheight()
                else:
                    # Valeurs par défaut basées sur la nouvelle taille
                    preview_width = ((1182 - 60) * 3) // 4  # ~830px
                    card_ratio = 5/7
                    canvas_width = preview_width - 40
                    canvas_height = int(canvas_width * (1/card_ratio))
                
                # Redimensionner l'image pour s'adapter au canvas avec marge, mais garder les proportions
                # Ne pas forcer la taille exacte du canvas, mais s'adapter en gardant le ratio
                original_width, original_height = self.card_image.size
                max_width = canvas_width - 40  # Marge plus grande
                max_height = canvas_height - 40
                
                # Calculer le ratio de redimensionnement en gardant les proportions
                ratio_width = max_width / original_width
                ratio_height = max_height / original_height
                ratio = min(ratio_width, ratio_height)  # Prendre le plus petit ratio
                
                # Nouvelles dimensions
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                
                self.card_image = self.card_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.card_image_tk = ImageTk.PhotoImage(self.card_image)
            else:
                print(f"⚠️ Image non trouvée : {image_path}")
                
        except Exception as e:
            print(f"❌ Erreur lors du chargement de l'image : {e}")
            self.card_image = None
            self.card_image_tk = None
            
        # Rafraîchir l'aperçu après chargement
        # (sera appelé une fois que le canvas est créé)
        
    def create_window(self):
        """Crée la fenêtre d'édition"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🎨 Éditeur de Formatage de Texte")
        
        # Taille par défaut optimisée
        window_width = 1182
        window_height = 780
        self.window.geometry(f"{window_width}x{window_height}")
        self.window.grab_set()  # Modal
        
        # Permettre le redimensionnement pour s'adapter à tous les écrans
        self.window.resizable(True, True)
        
        # Définir une taille minimale pour garder l'interface utilisable
        self.window.minsize(900, 600)
        
        # Centrer la fenêtre
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (window_width // 2)
        y = (self.window.winfo_screenheight() // 2) - (window_height // 2)
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Frame principal avec splitter
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame gauche - Contrôles (30% de la largeur pour plus de place)
        controls_width = int((window_width - 40) * 0.3)  # 30% au lieu de 25%
        controls_frame = ttk.LabelFrame(main_frame, text="📝 Contrôles de Formatage", padding=5)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        controls_frame.configure(width=controls_width)
        controls_frame.pack_propagate(False)  # Forcer la taille
        
        # Frame droite - Aperçu (70% de la largeur)
        preview_frame = ttk.LabelFrame(main_frame, text="👁️ Aperçu de la Carte", padding=10)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_controls(controls_frame)
        self.create_preview(preview_frame)
        
        # Charger l'image avant la mise à jour initiale
        self.load_card_image()
        
        # Boutons action
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="💾 Sauvegarder", command=self.save_formatting).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="🔄 Réinitialiser", command=self.reset_values).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🎨 Actualiser polices", command=self.refresh_fonts).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Annuler", command=self.window.destroy).pack(side=tk.RIGHT)
        
        # Mise à jour initiale (après chargement de l'image)
        self.update_preview()
        
    def create_controls(self, parent):
        """Crée les contrôles de formatage"""
        # Calculer la largeur disponible (30% de la fenêtre moins les marges)
        controls_width = int((1182 - 60) * 0.3)  # ~345px
        
        # Spécifications standardisées pour les curseurs - PLEINE LARGEUR
        slider_length = controls_width - 40  # Utilise toute la largeur disponible
        slider_margin_right = 20  # Marge réduite pour plus d'espace
        
        # Frame scrollable avec hauteur optimisée et SCROLLBAR PLUS VISIBLE
        canvas = tk.Canvas(parent, width=controls_width-20, height=680, bg="#f8f8f8", relief=tk.SUNKEN, bd=1)
        
        # Scrollbar plus visible et accessible
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Activer la roulette de souris pour le scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # === CONTRÔLES TITRE ===
        title_frame = ttk.LabelFrame(scrollable_frame, text="📍 Formatage du Titre", padding=5)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Position X
        pos_frame = ttk.Frame(title_frame)
        pos_frame.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_x = ttk.Frame(pos_frame)
        label_frame_x.pack(fill=tk.X)
        ttk.Label(label_frame_x, text="Position X:").pack(side=tk.LEFT)
        self.title_x_var = tk.IntVar(value=self.title_x)
        ttk.Label(label_frame_x, textvariable=self.title_x_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        scale_x = ttk.Scale(pos_frame, from_=0, to=500, variable=self.title_x_var, 
                           command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL)
        scale_x.pack(fill=tk.X, pady=(2, 0))
        
        # Position Y
        pos_frame2 = ttk.Frame(title_frame)
        pos_frame2.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_y = ttk.Frame(pos_frame2)
        label_frame_y.pack(fill=tk.X)
        ttk.Label(label_frame_y, text="Position Y:").pack(side=tk.LEFT)
        self.title_y_var = tk.IntVar(value=self.title_y)
        ttk.Label(label_frame_y, textvariable=self.title_y_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        scale_y = ttk.Scale(pos_frame2, from_=0, to=600, variable=self.title_y_var,
                           command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL)
        scale_y.pack(fill=tk.X, pady=(2, 0))
        
        # Police et taille
        font_frame = ttk.Frame(title_frame)
        font_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(font_frame, text="Police:").pack(side=tk.LEFT)
        self.title_font_var = tk.StringVar(value=self.title_font)
        
        # Utiliser le gestionnaire de polices pour obtenir toutes les polices disponibles
        font_combo = ttk.Combobox(font_frame, textvariable=self.title_font_var, 
                                 values=self.available_fonts, state="readonly", width=15)
        font_combo.pack(side=tk.LEFT, padx=5)
        font_combo.bind('<<ComboboxSelected>>', self.on_value_change)
        
        # Taille
        size_frame = ttk.Frame(title_frame)
        size_frame.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_size = ttk.Frame(size_frame)
        label_frame_size.pack(fill=tk.X)
        ttk.Label(label_frame_size, text="Taille:").pack(side=tk.LEFT)
        self.title_size_var = tk.IntVar(value=self.title_size)
        ttk.Label(label_frame_size, textvariable=self.title_size_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        ttk.Scale(size_frame, from_=8, to=48, variable=self.title_size_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(2, 0))
        
        # Couleur
        color_frame = ttk.Frame(title_frame)
        color_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(color_frame, text="Couleur:").pack(side=tk.LEFT)
        self.title_color_var = tk.StringVar(value=self.title_color)
        ttk.Button(color_frame, text="🎨 Choisir", 
                  command=lambda: self.choose_color(self.title_color_var, "titre")).pack(side=tk.RIGHT)
        
        # === CONTRÔLES TEXTE ===
        text_frame = ttk.LabelFrame(scrollable_frame, text="📝 Formatage du Texte", padding=10)
        text_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Position X du texte
        pos_frame3 = ttk.Frame(text_frame)
        pos_frame3.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_text_x = ttk.Frame(pos_frame3)
        label_frame_text_x.pack(fill=tk.X)
        ttk.Label(label_frame_text_x, text="Position X:").pack(side=tk.LEFT)
        self.text_x_var = tk.IntVar(value=self.text_x)
        ttk.Label(label_frame_text_x, textvariable=self.text_x_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        ttk.Scale(pos_frame3, from_=0, to=500, variable=self.text_x_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(2, 0))
        
        # Position Y du texte
        pos_frame4 = ttk.Frame(text_frame)
        pos_frame4.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_text_y = ttk.Frame(pos_frame4)
        label_frame_text_y.pack(fill=tk.X)
        ttk.Label(label_frame_text_y, text="Position Y:").pack(side=tk.LEFT)
        self.text_y_var = tk.IntVar(value=self.text_y)
        ttk.Label(label_frame_text_y, textvariable=self.text_y_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        ttk.Scale(pos_frame4, from_=0, to=700, variable=self.text_y_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(2, 0))
        
        # Largeur du texte
        dim_frame = ttk.Frame(text_frame)
        dim_frame.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_width = ttk.Frame(dim_frame)
        label_frame_width.pack(fill=tk.X)
        ttk.Label(label_frame_width, text="Largeur:").pack(side=tk.LEFT)
        self.text_width_var = tk.IntVar(value=self.text_width)
        ttk.Label(label_frame_width, textvariable=self.text_width_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        ttk.Scale(dim_frame, from_=50, to=400, variable=self.text_width_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(2, 0))
        
        # Hauteur du texte
        dim_frame2 = ttk.Frame(text_frame)
        dim_frame2.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_height = ttk.Frame(dim_frame2)
        label_frame_height.pack(fill=tk.X)
        ttk.Label(label_frame_height, text="Hauteur:").pack(side=tk.LEFT)
        self.text_height_var = tk.IntVar(value=self.text_height)
        ttk.Label(label_frame_height, textvariable=self.text_height_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        ttk.Scale(dim_frame2, from_=50, to=300, variable=self.text_height_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(2, 0))
        
        # Police et taille pour le texte
        font_frame2 = ttk.Frame(text_frame)
        font_frame2.pack(fill=tk.X, pady=2)
        
        ttk.Label(font_frame2, text="Police:").pack(side=tk.LEFT)
        self.text_font_var = tk.StringVar(value=self.text_font)
        
        # Utiliser le gestionnaire de polices pour le texte aussi
        font_combo2 = ttk.Combobox(font_frame2, textvariable=self.text_font_var,
                                  values=self.available_fonts, state="readonly")
        font_combo2.pack(side=tk.LEFT, padx=5)
        font_combo2.bind('<<ComboboxSelected>>', self.on_value_change)
        
        # Taille du texte
        size_frame2 = ttk.Frame(text_frame)
        size_frame2.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_text_size = ttk.Frame(size_frame2)
        label_frame_text_size.pack(fill=tk.X)
        ttk.Label(label_frame_text_size, text="Taille:").pack(side=tk.LEFT)
        self.text_size_var = tk.IntVar(value=self.text_size)
        ttk.Label(label_frame_text_size, textvariable=self.text_size_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        ttk.Scale(size_frame2, from_=8, to=24, variable=self.text_size_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(2, 0))
        
        # Couleur du texte
        color_frame2 = ttk.Frame(text_frame)
        color_frame2.pack(fill=tk.X, pady=2)
        
        ttk.Label(color_frame2, text="Couleur:").pack(side=tk.LEFT)
        self.text_color_var = tk.StringVar(value=self.text_color)
        ttk.Button(color_frame2, text="🎨 Choisir",
                  command=lambda: self.choose_color(self.text_color_var, "texte")).pack(side=tk.RIGHT)
        
        # Alignement
        align_frame = ttk.Frame(text_frame)
        align_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(align_frame, text="Alignement:").pack(side=tk.LEFT)
        self.text_align_var = tk.StringVar(value=self.text_align)
        align_combo = ttk.Combobox(align_frame, textvariable=self.text_align_var,
                                  values=['left', 'center', 'right'], state="readonly")
        align_combo.pack(side=tk.LEFT, padx=5)
        align_combo.bind('<<ComboboxSelected>>', self.on_value_change)
        
        # Espacement des lignes
        spacing_frame = ttk.Frame(text_frame)
        spacing_frame.pack(fill=tk.X, pady=2)
        
        # Label et valeur au-dessus
        label_frame_spacing = ttk.Frame(spacing_frame)
        label_frame_spacing.pack(fill=tk.X)
        ttk.Label(label_frame_spacing, text="Espacement:").pack(side=tk.LEFT)
        self.line_spacing_var = tk.DoubleVar(value=self.line_spacing)
        ttk.Label(label_frame_spacing, textvariable=self.line_spacing_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur
        ttk.Scale(spacing_frame, from_=0.8, to=3.0, variable=self.line_spacing_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(2, 0))
        
        # Retour à la ligne automatique
        self.text_wrap_var = tk.BooleanVar(value=bool(self.text_wrap))
        ttk.Checkbutton(text_frame, text="Retour à la ligne automatique",
                       variable=self.text_wrap_var, command=self.on_value_change).pack(pady=5)
        
        # === FORMATAGE DU COÛT EN ÉNERGIE ===
        energy_frame = ttk.LabelFrame(scrollable_frame, text="⚡ Formatage du Coût en Énergie", padding=10)
        energy_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Position X (ligne complète)
        pos_x_energy_frame = ttk.Frame(energy_frame)
        pos_x_energy_frame.pack(fill=tk.X, pady=(0, 5))
        
        label_frame_energy_x = ttk.Frame(pos_x_energy_frame)
        label_frame_energy_x.pack(fill=tk.X)
        ttk.Label(label_frame_energy_x, text="Position X:").pack(side=tk.LEFT)
        self.energy_x_var = tk.IntVar(value=self.energy_x)
        ttk.Label(label_frame_energy_x, textvariable=self.energy_x_var).pack(side=tk.RIGHT)
        
        # Curseur X plus grand - PLEINE LARGEUR
        scale_x_frame = ttk.Frame(pos_x_energy_frame)
        scale_x_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Scale(scale_x_frame, from_=0, to=400, variable=self.energy_x_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X)
        
        # Position Y (ligne complète)
        pos_y_energy_frame = ttk.Frame(energy_frame)
        pos_y_energy_frame.pack(fill=tk.X, pady=(5, 5))
        
        label_frame_energy_y = ttk.Frame(pos_y_energy_frame)
        label_frame_energy_y.pack(fill=tk.X)
        ttk.Label(label_frame_energy_y, text="Position Y:").pack(side=tk.LEFT)
        self.energy_y_var = tk.IntVar(value=self.energy_y)
        ttk.Label(label_frame_energy_y, textvariable=self.energy_y_var).pack(side=tk.RIGHT)
        
        # Curseur Y plus grand - PLEINE LARGEUR
        scale_y_frame = ttk.Frame(pos_y_energy_frame)
        scale_y_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Scale(scale_y_frame, from_=0, to=600, variable=self.energy_y_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X)
        
        # Préréglages de position - AMÉLIORÉS ET PLUS VISIBLES
        presets_frame = ttk.LabelFrame(energy_frame, text="🎯 Préréglages Position", padding=8)
        presets_frame.pack(fill=tk.X, pady=(10, 10))
        
        # AMÉLIORATION: 3 lignes de boutons pour plus de visibilité
        # Ligne 1: Positions hautes
        row1 = ttk.Frame(presets_frame)
        row1.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(row1, text="↖ Haut G.", width=10, 
                  command=lambda: self.set_energy_position(25, 25)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row1, text="↑ Haut C.", width=10,
                  command=lambda: self.set_energy_position(140, 25)).pack(side=tk.LEFT, padx=5)
        ttk.Button(row1, text="↗ Haut D.", width=10,
                  command=lambda: self.set_energy_position(255, 25)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Ligne 2: Positions milieu
        row2 = ttk.Frame(presets_frame)
        row2.pack(fill=tk.X, pady=(5, 5))
        ttk.Button(row2, text="← Milieu G.", width=10,
                  command=lambda: self.set_energy_position(25, 235)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row2, text="⚫ Centre", width=10,
                  command=lambda: self.set_energy_position(140, 235)).pack(side=tk.LEFT, padx=5)
        ttk.Button(row2, text="→ Milieu D.", width=10,
                  command=lambda: self.set_energy_position(255, 235)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Ligne 3: Positions basses (NOUVELLE)
        row3 = ttk.Frame(presets_frame)
        row3.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(row3, text="↙ Bas G.", width=10,
                  command=lambda: self.set_energy_position(25, 445)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row3, text="↓ Bas C.", width=10,
                  command=lambda: self.set_energy_position(140, 445)).pack(side=tk.LEFT, padx=5)
        ttk.Button(row3, text="↘ Bas D.", width=10,
                  command=lambda: self.set_energy_position(255, 445)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Police et taille
        font_energy_frame = ttk.Frame(energy_frame)
        font_energy_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(font_energy_frame, text="Police:").pack(side=tk.LEFT)
        self.energy_font_var = tk.StringVar(value=self.energy_font)
        
        # Utiliser le gestionnaire de polices pour l'énergie aussi
        energy_font_combo = ttk.Combobox(font_energy_frame, textvariable=self.energy_font_var, 
                                        values=self.available_fonts, 
                                        width=15)
        energy_font_combo.pack(side=tk.LEFT, padx=(5, 20))
        energy_font_combo.bind('<<ComboboxSelected>>', self.on_value_change)
        
        ttk.Label(font_energy_frame, text="Taille:").pack(side=tk.LEFT)
        self.energy_size_var = tk.IntVar(value=self.energy_size)
        ttk.Label(font_energy_frame, textvariable=self.energy_size_var).pack(side=tk.RIGHT, padx=(0, slider_margin_right))
        
        # Curseur taille énergie sur sa propre ligne pour plus de place
        size_energy_frame = ttk.Frame(energy_frame)
        size_energy_frame.pack(fill=tk.X, pady=(5, 5))
        ttk.Scale(size_energy_frame, from_=8, to=32, variable=self.energy_size_var,
                 command=self.on_value_change, length=slider_length, orient=tk.HORIZONTAL).pack(fill=tk.X)
        
        # Couleur
        color_energy_frame = ttk.Frame(energy_frame)
        color_energy_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(color_energy_frame, text="Couleur:").pack(side=tk.LEFT)
        self.energy_color_var = tk.StringVar(value=self.energy_color)
        self.energy_color_display = tk.Label(color_energy_frame, text="   ", bg=self.energy_color, width=4, relief="raised")
        self.energy_color_display.pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(color_energy_frame, text="Choisir couleur", 
                  command=self.choose_energy_color).pack(side=tk.LEFT)
        
        # Affichage de la valeur d'énergie
        value_energy_frame = ttk.Frame(energy_frame)
        value_energy_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(value_energy_frame, text=f"💎 Valeur énergétique: {self.energy_value}", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        # === ZONE DE TEXTE ÉDITABLE ===
        edit_frame = ttk.LabelFrame(scrollable_frame, text="✏️ Édition du Texte", padding=10)
        edit_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(edit_frame, text="Titre:").pack(anchor=tk.W)
        self.title_entry = tk.Entry(edit_frame, textvariable=tk.StringVar(value=self.title_text))
        self.title_entry.pack(fill=tk.X, pady=(0, 5))
        self.title_entry.bind('<KeyRelease>', self.on_text_change)
        
        ttk.Label(edit_frame, text="Contenu:").pack(anchor=tk.W)
        self.content_text_widget = tk.Text(edit_frame, height=4, wrap=tk.WORD)
        self.content_text_widget.pack(fill=tk.X)
        self.content_text_widget.insert('1.0', self.content_text)
        self.content_text_widget.bind('<KeyRelease>', self.on_text_change)
        
        # Configuration du canvas et scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_preview(self, parent):
        """Crée l'aperçu de la carte"""
        # Calculer la largeur disponible pour l'aperçu (70% de la fenêtre)
        preview_width = int((1182 - 60) * 0.7)  # ~785px
        preview_height = 700  # Hauteur réduite pour laisser place aux boutons
        
        # Ajuster les dimensions pour maintenir un ratio correct pour une carte
        card_ratio = 5/7  # Ratio typique d'une carte (largeur/hauteur)
        if preview_width * (1/card_ratio) <= preview_height:
            canvas_width = preview_width - 20  # Marge réduite pour plus d'espace
            canvas_height = int(canvas_width * (1/card_ratio))
        else:
            canvas_height = preview_height - 20  # Marge réduite
            canvas_width = int(canvas_height * card_ratio)
        
        self.preview_canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height, 
                                      bg='white', relief=tk.SUNKEN, bd=2)
        self.preview_canvas.pack(padx=10, pady=10)
        
    def on_value_change(self, event=None):
        """Callback pour les changements de valeurs"""
        self.update_preview()
        
    def on_text_change(self, event=None):
        """Callback pour les changements de texte"""
        self.title_text = self.title_entry.get()
        self.content_text = self.content_text_widget.get('1.0', tk.END).strip()
        self.update_preview()
        
    def choose_color(self, color_var, element_type):
        """Ouvre le sélecteur de couleur"""
        color = colorchooser.askcolor(color=color_var.get())[1]
        if color:
            color_var.set(color)
            self.update_preview()
    
    def choose_energy_color(self):
        """Ouvre le sélecteur de couleur pour l'énergie"""
        color = colorchooser.askcolor(color=self.energy_color_var.get())[1]
        if color:
            self.energy_color_var.set(color)
            self.energy_color_display.config(bg=color)
            self.update_preview()
    
    def set_energy_position(self, x, y):
        """Définit la position de l'énergie avec des préréglages"""
        self.energy_x_var.set(x)
        self.energy_y_var.set(y)
        self.update_preview()
            
    def update_preview(self):
        """Met à jour l'aperçu de la carte"""
        # Effacer le canvas
        self.preview_canvas.delete("all")
        
        # Taille du canvas et de la carte
        canvas_width = 380
        canvas_height = 580
        card_width = 280
        card_height = 470
        
        # Centrer la carte
        card_x = (canvas_width - card_width) // 2
        card_y = (canvas_height - card_height) // 2
        
        # Dessiner l'image de la carte ou un fond par défaut
        if self.card_image_tk:
            # Afficher l'image réelle de la carte
            self.preview_canvas.create_image(
                card_x, card_y,
                image=self.card_image_tk,
                anchor='nw'
            )
        else:
            # Dessiner un fond par défaut si pas d'image
            self.preview_canvas.create_rectangle(
                card_x, card_y, card_x + card_width, card_y + card_height,
                fill='#f0f0f0', outline='#333333', width=2
            )
            
            # Ajouter un texte d'indication
            self.preview_canvas.create_text(
                card_x + card_width//2, card_y + card_height//2,
                text="Image de carte\nnon trouvée",
                font=('Arial', 16),
                fill='#666666',
                justify='center'
            )
        
        # Dessiner le titre
        title_x = card_x + self.title_x_var.get()
        title_y = card_y + self.title_y_var.get()
        
        self.preview_canvas.create_text(
            title_x, title_y,
            text=self.title_text,
            font=(self.title_font_var.get(), self.title_size_var.get(), 'bold'),
            fill=self.title_color_var.get(),
            anchor='nw'
        )
        
        # Dessiner le coût en énergie
        energy_x = card_x + self.energy_x_var.get()
        energy_y = card_y + self.energy_y_var.get()
        
        # Dessiner un cercle de fond pour l'énergie (optionnel)
        energy_radius = self.energy_size_var.get() + 5
        self.preview_canvas.create_oval(
            energy_x - energy_radius, energy_y - energy_radius,
            energy_x + energy_radius, energy_y + energy_radius,
            fill='#1e3a8a', outline='#fbbf24', width=2
        )
        
        # Dessiner la valeur de l'énergie
        self.preview_canvas.create_text(
            energy_x, energy_y,
            text=str(self.energy_value),
            font=(self.energy_font_var.get(), self.energy_size_var.get(), 'bold'),
            fill=self.energy_color_var.get(),
            anchor='center'
        )
        
        # Dessiner le cadre du texte (pour visualisation)
        text_x = card_x + self.text_x_var.get()
        text_y = card_y + self.text_y_var.get()
        text_width = self.text_width_var.get()
        text_height = self.text_height_var.get()
        
        self.preview_canvas.create_rectangle(
            text_x, text_y, text_x + text_width, text_y + text_height,
            outline='#cccccc', width=1, dash=(2, 2)
        )
        
        # Dessiner le texte avec retour à la ligne
        self.draw_wrapped_text(
            text_x, text_y, text_width, text_height,
            self.content_text,
            (self.text_font_var.get(), self.text_size_var.get()),
            self.text_color_var.get(),
            self.text_align_var.get(),
            self.line_spacing_var.get()
        )
        
        # Ajouter des guides visuels
        self.preview_canvas.create_text(
            card_x + 5, card_y + card_height - 35,
            text=f"Position titre: ({self.title_x_var.get()}, {self.title_y_var.get()})",
            font=('Arial', 8), fill='#666666', anchor='sw'
        )
        
        self.preview_canvas.create_text(
            card_x + 5, card_y + card_height - 20,
            text=f"Zone texte: ({self.text_x_var.get()}, {self.text_y_var.get()}) {text_width}x{text_height}",
            font=('Arial', 8), fill='#666666', anchor='sw'
        )
        
        self.preview_canvas.create_text(
            card_x + 5, card_y + card_height - 5,
            text=f"Énergie: ({self.energy_x_var.get()}, {self.energy_y_var.get()}) val:{self.energy_value}",
            font=('Arial', 8), fill='#666666', anchor='sw'
        )
        
    def draw_wrapped_text(self, x, y, width, height, text, font_tuple, color, align, line_spacing):
        """Dessine du texte avec retour à la ligne"""
        if not text.strip():
            return
            
        # Simuler le retour à la ligne (basique)
        font_size = font_tuple[1]
        line_height = int(font_size * line_spacing)
        
        # Diviser le texte en mots
        words = text.split()
        lines = []
        current_line = ""
        
        # Estimation approximative de la largeur des caractères
        avg_char_width = font_size * 0.6
        max_chars_per_line = int(width / avg_char_width)
        
        for word in words:
            if len(current_line + " " + word) < max_chars_per_line:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Dessiner chaque ligne
        for i, line in enumerate(lines):
            line_y = y + (i * line_height)
            if line_y + line_height > y + height:
                break  # Ne pas dépasser la zone
                
            if align == 'center':
                line_x = x + width // 2
                anchor = 'n'
            elif align == 'right':
                line_x = x + width - 5
                anchor = 'ne'
            else:  # left
                line_x = x + 5
                anchor = 'nw'
                
            self.preview_canvas.create_text(
                line_x, line_y,
                text=line,
                font=font_tuple,
                fill=color,
                anchor=anchor
            )
            
    def save_formatting(self):
        """Sauvegarde les paramètres de formatage en base de données"""
        if not self.card_id:
            messagebox.showwarning("Attention", "Aucune carte sélectionnée pour la sauvegarde.")
            return
            
        try:
            if self.repo:
                # Utiliser le repo personnalisé
                # Créer un objet avec les données de formatage
                class FormattingData:
                    pass
                
                card_data = FormattingData()
                card_data.id = self.card_id
                card_data.title_x = self.title_x_var.get()
                card_data.title_y = self.title_y_var.get()
                card_data.title_font = self.title_font_var.get()
                card_data.title_size = self.title_size_var.get()
                card_data.title_color = self.title_color_var.get()
                
                card_data.text_x = self.text_x_var.get()
                card_data.text_y = self.text_y_var.get()
                card_data.text_width = self.text_width_var.get()
                card_data.text_height = self.text_height_var.get()
                card_data.text_font = self.text_font_var.get()
                card_data.text_size = self.text_size_var.get()
                card_data.text_color = self.text_color_var.get()
                card_data.text_align = self.text_align_var.get()
                card_data.line_spacing = self.line_spacing_var.get()
                card_data.text_wrap = bool(self.text_wrap_var.get())
                
                # Données de formatage de l'énergie
                card_data.energy_x = self.energy_x_var.get()
                card_data.energy_y = self.energy_y_var.get()
                card_data.energy_font = self.energy_font_var.get()
                card_data.energy_size = self.energy_size_var.get()
                card_data.energy_color = self.energy_color_var.get()
                
                # Sauvegarder via le repo personnalisé
                self.repo.save_card(card_data)
                
                messagebox.showinfo("Succès", "Paramètres de formatage sauvegardés !")
                self.window.destroy()
            else:
                # Fallback vers l'ancien système pour compatibilité
                # Utiliser le système de base de données simplifié pour le formatage
                import sys
                import os
                sys.path.insert(0, os.path.dirname(__file__))
                from database_simple import CardRepo
                
                # Chemin vers la base de données
                db_path = Path(__file__).parent.parent / "data/cartes.db"
                repo = CardRepo(str(db_path))
                
                # Récupérer la carte existante
                card = repo.get_card(self.card_id)
                
                if not card:
                    messagebox.showerror("Erreur", f"Carte non trouvée pour l'ID {self.card_id}.")
                    return
                
                # Mettre à jour les paramètres de formatage
                card.title_x = self.title_x_var.get()
                card.title_y = self.title_y_var.get()
                card.title_font = self.title_font_var.get()
                card.title_size = self.title_size_var.get()
                card.title_color = self.title_color_var.get()
                
                card.text_x = self.text_x_var.get()
                card.text_y = self.text_y_var.get()
                card.text_width = self.text_width_var.get()
                card.text_height = self.text_height_var.get()
                card.text_font = self.text_font_var.get()
                card.text_size = self.text_size_var.get()
                card.text_color = self.text_color_var.get()
                card.text_align = self.text_align_var.get()
                card.line_spacing = self.line_spacing_var.get()
                card.text_wrap = int(self.text_wrap_var.get())
                
                # Paramètres d'énergie
                card.energy_x = self.energy_x_var.get()
                card.energy_y = self.energy_y_var.get()
                card.energy_font = self.energy_font_var.get()
                card.energy_size = self.energy_size_var.get()
                card.energy_color = self.energy_color_var.get()
                
                # Sauvegarder en base
                repo.save_card(card)
                
                messagebox.showinfo("Succès", "Paramètres de formatage sauvegardés !")
                self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
            import traceback
            traceback.print_exc()
            
    def reset_values(self):
        """Réinitialise les valeurs par défaut"""
        self.title_x_var.set(50)
        self.title_y_var.set(30)
        self.title_font_var.set('Arial')
        self.title_size_var.set(16)
        self.title_color_var.set('#000000')
        
        self.text_x_var.set(50)
        self.text_y_var.set(100)
        self.text_width_var.set(200)
        self.text_height_var.set(150)
        self.text_font_var.set('Arial')
        self.text_size_var.set(12)
        self.text_color_var.set('#000000')
        self.text_align_var.set('left')
        self.line_spacing_var.set(1.2)
        self.text_wrap_var.set(True)
        
        self.update_preview()
    
    def refresh_fonts(self):
        """Actualise la liste des polices disponibles."""
        try:
            # Recharger les polices du gestionnaire
            self.font_manager.refresh_fonts()
            self.available_fonts = get_available_fonts()
            
            # Mettre à jour les comboboxes si elles existent
            if hasattr(self, 'title_font_var'):
                # Sauvegarder les valeurs actuelles
                title_font = self.title_font_var.get()
                text_font = self.text_font_var.get()
                energy_font = self.energy_font_var.get()
                
                # Recréer l'interface complète serait complexe,
                # donc on informe l'utilisateur
                messagebox.showinfo(
                    "🎨 Polices actualisées",
                    f"Les polices ont été rechargées !\n\n"
                    f"📊 {len(self.available_fonts)} polices disponibles\n"
                    f"🎨 {len(self.font_manager.get_custom_fonts())} polices personnalisées\n\n"
                    f"💡 Redémarrez l'éditeur pour voir les nouvelles polices."
                )
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'actualiser les polices:\n{e}")

def open_text_formatting_editor(parent, card_id=None, card_data=None):
    """Fonction utilitaire pour ouvrir l'éditeur"""
    return TextFormattingEditor(parent, card_id, card_data)
