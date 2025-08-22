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

class TextFormattingEditor:
    def __init__(self, parent, card_id=None, card_data=None):
        self.parent = parent
        self.card_id = card_id
        self.card_data = card_data or {}
        
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
        
        # Texte d'exemple
        self.title_text = self.card_data.get('nom', 'Titre de la carte')
        self.content_text = self.card_data.get('description', 'Description de la carte avec du texte plus long pour tester le retour à la ligne automatique.')
        
        self.create_window()
        
    def create_window(self):
        """Crée la fenêtre d'édition"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🎨 Éditeur de Formatage de Texte")
        self.window.geometry("1200x800")
        self.window.grab_set()  # Modal
        
        # Frame principal avec splitter
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame gauche - Contrôles
        controls_frame = ttk.LabelFrame(main_frame, text="📝 Contrôles de Formatage", padding=10)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Frame droite - Aperçu
        preview_frame = ttk.LabelFrame(main_frame, text="👁️ Aperçu de la Carte", padding=10)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_controls(controls_frame)
        self.create_preview(preview_frame)
        
        # Boutons action
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="💾 Sauvegarder", command=self.save_formatting).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="🔄 Réinitialiser", command=self.reset_values).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Annuler", command=self.window.destroy).pack(side=tk.RIGHT)
        
        # Mise à jour initiale
        self.update_preview()
        
    def create_controls(self, parent):
        """Crée les contrôles de formatage"""
        # Frame scrollable
        canvas = tk.Canvas(parent, width=350)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # === CONTRÔLES TITRE ===
        title_frame = ttk.LabelFrame(scrollable_frame, text="📍 Formatage du Titre", padding=10)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Position
        pos_frame = ttk.Frame(title_frame)
        pos_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pos_frame, text="Position X:").pack(side=tk.LEFT)
        self.title_x_var = tk.IntVar(value=self.title_x)
        ttk.Scale(pos_frame, from_=0, to=300, variable=self.title_x_var, 
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(pos_frame, textvariable=self.title_x_var).pack(side=tk.RIGHT)
        
        pos_frame2 = ttk.Frame(title_frame)
        pos_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(pos_frame2, text="Position Y:").pack(side=tk.LEFT)
        self.title_y_var = tk.IntVar(value=self.title_y)
        ttk.Scale(pos_frame2, from_=0, to=300, variable=self.title_y_var,
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(pos_frame2, textvariable=self.title_y_var).pack(side=tk.RIGHT)
        
        # Police et taille
        font_frame = ttk.Frame(title_frame)
        font_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(font_frame, text="Police:").pack(side=tk.LEFT)
        self.title_font_var = tk.StringVar(value=self.title_font)
        font_combo = ttk.Combobox(font_frame, textvariable=self.title_font_var, 
                                 values=list(font.families()), state="readonly")
        font_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        font_combo.bind('<<ComboboxSelected>>', self.on_value_change)
        
        size_frame = ttk.Frame(title_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="Taille:").pack(side=tk.LEFT)
        self.title_size_var = tk.IntVar(value=self.title_size)
        ttk.Scale(size_frame, from_=8, to=48, variable=self.title_size_var,
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(size_frame, textvariable=self.title_size_var).pack(side=tk.RIGHT)
        
        # Couleur
        color_frame = ttk.Frame(title_frame)
        color_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(color_frame, text="Couleur:").pack(side=tk.LEFT)
        self.title_color_var = tk.StringVar(value=self.title_color)
        ttk.Button(color_frame, text="🎨 Choisir", 
                  command=lambda: self.choose_color(self.title_color_var, "titre")).pack(side=tk.RIGHT)
        
        # === CONTRÔLES TEXTE ===
        text_frame = ttk.LabelFrame(scrollable_frame, text="📝 Formatage du Texte", padding=10)
        text_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Position et dimensions
        pos_frame3 = ttk.Frame(text_frame)
        pos_frame3.pack(fill=tk.X, pady=5)
        
        ttk.Label(pos_frame3, text="Position X:").pack(side=tk.LEFT)
        self.text_x_var = tk.IntVar(value=self.text_x)
        ttk.Scale(pos_frame3, from_=0, to=300, variable=self.text_x_var,
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(pos_frame3, textvariable=self.text_x_var).pack(side=tk.RIGHT)
        
        pos_frame4 = ttk.Frame(text_frame)
        pos_frame4.pack(fill=tk.X, pady=5)
        
        ttk.Label(pos_frame4, text="Position Y:").pack(side=tk.LEFT)
        self.text_y_var = tk.IntVar(value=self.text_y)
        ttk.Scale(pos_frame4, from_=0, to=400, variable=self.text_y_var,
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(pos_frame4, textvariable=self.text_y_var).pack(side=tk.RIGHT)
        
        # Largeur et hauteur
        dim_frame = ttk.Frame(text_frame)
        dim_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dim_frame, text="Largeur:").pack(side=tk.LEFT)
        self.text_width_var = tk.IntVar(value=self.text_width)
        ttk.Scale(dim_frame, from_=50, to=400, variable=self.text_width_var,
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(dim_frame, textvariable=self.text_width_var).pack(side=tk.RIGHT)
        
        dim_frame2 = ttk.Frame(text_frame)
        dim_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(dim_frame2, text="Hauteur:").pack(side=tk.LEFT)
        self.text_height_var = tk.IntVar(value=self.text_height)
        ttk.Scale(dim_frame2, from_=50, to=300, variable=self.text_height_var,
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(dim_frame2, textvariable=self.text_height_var).pack(side=tk.RIGHT)
        
        # Police et taille pour le texte
        font_frame2 = ttk.Frame(text_frame)
        font_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(font_frame2, text="Police:").pack(side=tk.LEFT)
        self.text_font_var = tk.StringVar(value=self.text_font)
        font_combo2 = ttk.Combobox(font_frame2, textvariable=self.text_font_var,
                                  values=list(font.families()), state="readonly")
        font_combo2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        font_combo2.bind('<<ComboboxSelected>>', self.on_value_change)
        
        size_frame2 = ttk.Frame(text_frame)
        size_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame2, text="Taille:").pack(side=tk.LEFT)
        self.text_size_var = tk.IntVar(value=self.text_size)
        ttk.Scale(size_frame2, from_=8, to=24, variable=self.text_size_var,
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(size_frame2, textvariable=self.text_size_var).pack(side=tk.RIGHT)
        
        # Couleur du texte
        color_frame2 = ttk.Frame(text_frame)
        color_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(color_frame2, text="Couleur:").pack(side=tk.LEFT)
        self.text_color_var = tk.StringVar(value=self.text_color)
        ttk.Button(color_frame2, text="🎨 Choisir",
                  command=lambda: self.choose_color(self.text_color_var, "texte")).pack(side=tk.RIGHT)
        
        # Alignement
        align_frame = ttk.Frame(text_frame)
        align_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(align_frame, text="Alignement:").pack(side=tk.LEFT)
        self.text_align_var = tk.StringVar(value=self.text_align)
        align_combo = ttk.Combobox(align_frame, textvariable=self.text_align_var,
                                  values=['left', 'center', 'right'], state="readonly")
        align_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        align_combo.bind('<<ComboboxSelected>>', self.on_value_change)
        
        # Espacement des lignes
        spacing_frame = ttk.Frame(text_frame)
        spacing_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(spacing_frame, text="Espacement:").pack(side=tk.LEFT)
        self.line_spacing_var = tk.DoubleVar(value=self.line_spacing)
        ttk.Scale(spacing_frame, from_=0.8, to=3.0, variable=self.line_spacing_var,
                 command=self.on_value_change).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(spacing_frame, textvariable=self.line_spacing_var).pack(side=tk.RIGHT)
        
        # Retour à la ligne automatique
        self.text_wrap_var = tk.BooleanVar(value=bool(self.text_wrap))
        ttk.Checkbutton(text_frame, text="Retour à la ligne automatique",
                       variable=self.text_wrap_var, command=self.on_value_change).pack(pady=5)
        
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
        self.preview_canvas = tk.Canvas(parent, width=400, height=600, bg='white', relief=tk.SUNKEN, bd=2)
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
            
    def update_preview(self):
        """Met à jour l'aperçu de la carte"""
        # Effacer le canvas
        self.preview_canvas.delete("all")
        
        # Dessiner le fond de carte (rectangle avec bordure)
        canvas_width = 400
        canvas_height = 600
        card_width = 300
        card_height = 500
        
        # Centrer la carte
        card_x = (canvas_width - card_width) // 2
        card_y = (canvas_height - card_height) // 2
        
        # Dessiner la carte
        self.preview_canvas.create_rectangle(
            card_x, card_y, card_x + card_width, card_y + card_height,
            fill='#f0f0f0', outline='#333333', width=2
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
            card_x + 5, card_y + card_height - 20,
            text=f"Position titre: ({self.title_x_var.get()}, {self.title_y_var.get()})",
            font=('Arial', 8), fill='#666666', anchor='sw'
        )
        
        self.preview_canvas.create_text(
            card_x + 5, card_y + card_height - 5,
            text=f"Zone texte: ({self.text_x_var.get()}, {self.text_y_var.get()}) {text_width}x{text_height}",
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
            db_path = Path(__file__).parent.parent / "cartes.db"
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Mise à jour des paramètres de formatage
            cursor.execute("""
                UPDATE cards SET
                    title_x = ?, title_y = ?, title_font = ?, title_size = ?, title_color = ?,
                    text_x = ?, text_y = ?, text_width = ?, text_height = ?,
                    text_font = ?, text_size = ?, text_color = ?, text_align = ?,
                    line_spacing = ?, text_wrap = ?
                WHERE id = ?
            """, (
                self.title_x_var.get(), self.title_y_var.get(), self.title_font_var.get(),
                self.title_size_var.get(), self.title_color_var.get(),
                self.text_x_var.get(), self.text_y_var.get(), self.text_width_var.get(),
                self.text_height_var.get(), self.text_font_var.get(), self.text_size_var.get(),
                self.text_color_var.get(), self.text_align_var.get(),
                self.line_spacing_var.get(), int(self.text_wrap_var.get()),
                self.card_id
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Succès", "Paramètres de formatage sauvegardés !")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
            
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

def open_text_formatting_editor(parent, card_id=None, card_data=None):
    """Fonction utilitaire pour ouvrir l'éditeur"""
    return TextFormattingEditor(parent, card_id, card_data)
