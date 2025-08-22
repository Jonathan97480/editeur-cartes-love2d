#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test direct de l'éditeur avec sliders limités à 300px
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Ajouter le chemin lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

def test_slider_direct():
    """Test direct des sliders avec longueur limitée à 300px"""
    
    print("🧪 TEST DIRECT DES SLIDERS 300PX")
    print("=" * 50)
    
    # Créer la fenêtre de test
    root = tk.Tk()
    root.title("Test Sliders 300px - Interface Compacte")
    root.geometry("800x600")
    
    # Frame principal
    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Titre
    title_label = ttk.Label(main_frame, text="🔧 Test des Sliders avec Longueur Limitée", 
                           font=('Arial', 14, 'bold'))
    title_label.pack(pady=(0, 20))
    
    # Variables de test
    pos_x = tk.IntVar(value=140)
    pos_y = tk.IntVar(value=50)
    width_var = tk.IntVar(value=200)
    height_var = tk.IntVar(value=100)
    
    # ===== COMPARAISON AVANT/APRÈS =====
    
    # Frame de comparaison
    comparison_frame = ttk.LabelFrame(main_frame, text="📊 Comparaison Longueur Sliders", padding=10)
    comparison_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Colonnes
    left_col = ttk.Frame(comparison_frame)
    left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    right_col = ttk.Frame(comparison_frame)
    right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    # AVANT (slider long)
    ttk.Label(left_col, text="❌ AVANT: Slider trop long", font=('Arial', 10, 'bold')).pack()
    long_slider = ttk.Scale(left_col, from_=0, to=470, variable=pos_x,
                           length=500, orient=tk.HORIZONTAL)  # Ancien: très long
    long_slider.pack(fill=tk.X, pady=5)
    ttk.Label(left_col, text="Longueur: 500px (trop long)", foreground='red').pack()
    
    # APRÈS (slider compact)
    ttk.Label(right_col, text="✅ APRÈS: Slider compact", font=('Arial', 10, 'bold')).pack()
    compact_slider = ttk.Scale(right_col, from_=0, to=470, variable=pos_y,
                              length=300, orient=tk.HORIZONTAL)  # Nouveau: compact
    compact_slider.pack(fill=tk.X, pady=5)
    ttk.Label(right_col, text="Longueur: 300px (optimal)", foreground='green').pack()
    
    # ===== SIMULATION DE L'ÉDITEUR =====
    
    editor_frame = ttk.LabelFrame(main_frame, text="🎮 Simulation Éditeur de Formatage", padding=10)
    editor_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    # Contrôles formatage
    controls_frame = ttk.Frame(editor_frame)
    controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
    
    # Position X
    ttk.Label(controls_frame, text="Position X:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
    pos_x_frame = ttk.Frame(controls_frame)
    pos_x_frame.pack(fill=tk.X, pady=(2, 10))
    ttk.Scale(pos_x_frame, from_=0, to=280, variable=pos_x,
             length=300, orient=tk.HORIZONTAL).pack()
    ttk.Label(pos_x_frame, textvariable=pos_x).pack()
    
    # Position Y  
    ttk.Label(controls_frame, text="Position Y:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
    pos_y_frame = ttk.Frame(controls_frame)
    pos_y_frame.pack(fill=tk.X, pady=(2, 10))
    ttk.Scale(pos_y_frame, from_=0, to=470, variable=pos_y,
             length=300, orient=tk.HORIZONTAL).pack()
    ttk.Label(pos_y_frame, textvariable=pos_y).pack()
    
    # Largeur
    ttk.Label(controls_frame, text="Largeur:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
    width_frame = ttk.Frame(controls_frame)
    width_frame.pack(fill=tk.X, pady=(2, 10))
    ttk.Scale(width_frame, from_=20, to=260, variable=width_var,
             length=300, orient=tk.HORIZONTAL).pack()
    ttk.Label(width_frame, textvariable=width_var).pack()
    
    # Hauteur
    ttk.Label(controls_frame, text="Hauteur:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
    height_frame = ttk.Frame(controls_frame)
    height_frame.pack(fill=tk.X, pady=(2, 10))
    ttk.Scale(height_frame, from_=20, to=250, variable=height_var,
             length=300, orient=tk.HORIZONTAL).pack()
    ttk.Label(height_frame, textvariable=height_var).pack()
    
    # Aperçu
    preview_frame = ttk.LabelFrame(editor_frame, text="🔍 Aperçu", padding=10)
    preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Canvas de prévisualisation
    canvas = tk.Canvas(preview_frame, width=300, height=400, bg='lightgray', relief=tk.SUNKEN, bd=1)
    canvas.pack()
    
    # Dessiner un rectangle simulant la carte
    card_rect = canvas.create_rectangle(10, 10, 290, 390, fill='white', outline='black', width=2)
    
    def update_preview():
        """Mettre à jour l'aperçu en temps réel"""
        # Effacer les éléments précédents
        canvas.delete("preview_items")
        
        # Position du texte (simulé)
        x = pos_x.get() * 0.9 + 15  # Adapter à la taille du canvas
        y = pos_y.get() * 0.8 + 15
        w = width_var.get() * 0.9
        h = height_var.get() * 0.8
        
        # Dessiner la zone de texte
        text_rect = canvas.create_rectangle(x, y, x+w, y+h, 
                                          fill='lightblue', outline='blue', 
                                          tags="preview_items")
        canvas.create_text(x+w/2, y+h/2, text="Zone de texte", 
                          tags="preview_items", font=('Arial', 8))
    
    # Lier les variables aux mises à jour
    for var in [pos_x, pos_y, width_var, height_var]:
        var.trace_add('write', lambda *args: update_preview())
    
    # Première mise à jour
    update_preview()
    
    # ===== INFORMATIONS =====
    
    info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Informations", padding=10)
    info_frame.pack(fill=tk.X)
    
    info_text = """✅ CORRECTIONS APPLIQUÉES:
• Longueur visuelle des sliders: Limitée à 300px maximum
• Plage fonctionnelle: Complète (0-470px pour Y, 0-280px pour X)
• Interface: Plus compacte et ergonomique
• Fonctionnalité: Inchangée - peut toujours positionner en bas de carte"""
    
    ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
    
    # Bouton fermer
    ttk.Button(main_frame, text="Fermer le test", 
              command=root.destroy).pack(pady=10)
    
    print("✅ Interface de test lancée!")
    print("   - Sliders limités à 300px de longueur visuelle")
    print("   - Plage fonctionnelle complète préservée")
    print("   - Comparaison avant/après visible")
    
    root.mainloop()

if __name__ == "__main__":
    test_slider_direct()
