#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du panneau de gauche redimensionnable
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Ajouter le chemin lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

def test_resizable_panel():
    """Test du panneau redimensionnable"""
    
    print("🔧 TEST DU PANNEAU REDIMENSIONNABLE")
    print("=" * 50)
    
    # Créer la fenêtre de test
    root = tk.Tk()
    root.title("Test Panneau Redimensionnable - Éditeur de Formatage")
    root.geometry("1200x800")
    
    # Frame principal
    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Titre
    title_label = ttk.Label(main_frame, text="🔧 Panneau de Contrôles Redimensionnable", 
                           font=('Arial', 14, 'bold'))
    title_label.pack(pady=(0, 20))
    
    # PanedWindow pour panneau redimensionnable
    paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)
    
    # ===== PANNEAU GAUCHE - CONTRÔLES =====
    
    controls_frame = ttk.LabelFrame(paned_window, text="📝 Contrôles de Formatage (Redimensionnable)", padding=5)
    paned_window.add(controls_frame, weight=1)
    
    # Contenu des contrôles
    controls_content = ttk.Frame(controls_frame)
    controls_content.pack(fill=tk.BOTH, expand=True)
    
    # Variables de test
    pos_x = tk.IntVar(value=140)
    pos_y = tk.IntVar(value=50)
    width_var = tk.IntVar(value=200)
    
    def get_dynamic_slider_length():
        """Calculer la longueur des sliders en fonction de la largeur du panneau"""
        try:
            controls_content.update_idletasks()
            current_width = controls_content.winfo_width()
            if current_width <= 1:
                current_width = 300
            return min(300, max(150, current_width - 50))
        except:
            return 250
    
    def update_sliders():
        """Mettre à jour la longueur des sliders quand le panneau est redimensionné"""
        slider_length = get_dynamic_slider_length()
        for slider in sliders_list:
            slider.configure(length=slider_length)
        # Programmer la prochaine mise à jour
        root.after(100, update_sliders)
    
    # Liste pour stocker les sliders
    sliders_list = []
    
    # ===== CONTRÔLES DE TEST =====
    
    # Position X
    ttk.Label(controls_content, text="Position X:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(10, 2))
    pos_x_frame = ttk.Frame(controls_content)
    pos_x_frame.pack(fill=tk.X, pady=(0, 10))
    
    slider_x = ttk.Scale(pos_x_frame, from_=0, to=280, variable=pos_x,
                        length=get_dynamic_slider_length(), orient=tk.HORIZONTAL)
    slider_x.pack(fill=tk.X)
    sliders_list.append(slider_x)
    
    ttk.Label(pos_x_frame, textvariable=pos_x).pack()
    
    # Position Y
    ttk.Label(controls_content, text="Position Y:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(10, 2))
    pos_y_frame = ttk.Frame(controls_content)
    pos_y_frame.pack(fill=tk.X, pady=(0, 10))
    
    slider_y = ttk.Scale(pos_y_frame, from_=0, to=470, variable=pos_y,
                        length=get_dynamic_slider_length(), orient=tk.HORIZONTAL)
    slider_y.pack(fill=tk.X)
    sliders_list.append(slider_y)
    
    ttk.Label(pos_y_frame, textvariable=pos_y).pack()
    
    # Largeur
    ttk.Label(controls_content, text="Largeur:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(10, 2))
    width_frame = ttk.Frame(controls_content)
    width_frame.pack(fill=tk.X, pady=(0, 10))
    
    slider_w = ttk.Scale(width_frame, from_=20, to=260, variable=width_var,
                        length=get_dynamic_slider_length(), orient=tk.HORIZONTAL)
    slider_w.pack(fill=tk.X)
    sliders_list.append(slider_w)
    
    ttk.Label(width_frame, textvariable=width_var).pack()
    
    # Informations dynamiques
    info_frame = ttk.LabelFrame(controls_content, text="ℹ️ Informations Dynamiques", padding=5)
    info_frame.pack(fill=tk.X, pady=(20, 10))
    
    width_label = ttk.Label(info_frame, text="Largeur panneau: -")
    width_label.pack(anchor=tk.W)
    
    slider_length_label = ttk.Label(info_frame, text="Longueur sliders: -")
    slider_length_label.pack(anchor=tk.W)
    
    def update_info():
        """Mettre à jour les informations affichées"""
        try:
            current_width = controls_content.winfo_width()
            slider_length = get_dynamic_slider_length()
            width_label.config(text=f"Largeur panneau: {current_width}px")
            slider_length_label.config(text=f"Longueur sliders: {slider_length}px")
        except:
            pass
        root.after(500, update_info)
    
    # ===== PANNEAU DROIT - APERÇU =====
    
    preview_frame = ttk.LabelFrame(paned_window, text="👁️ Aperçu de la Carte (Redimensionnable)", padding=10)
    paned_window.add(preview_frame, weight=2)
    
    # Canvas de prévisualisation
    canvas = tk.Canvas(preview_frame, width=400, height=600, bg='lightgray', relief=tk.SUNKEN, bd=2)
    canvas.pack(expand=True)
    
    # Dessiner une carte simulée
    card_rect = canvas.create_rectangle(50, 50, 350, 550, fill='white', outline='black', width=3)
    
    def update_preview():
        """Mettre à jour l'aperçu en temps réel"""
        # Effacer les éléments précédents
        canvas.delete("preview_items")
        
        # Position du texte (simulé)
        x = pos_x.get() * 0.8 + 60
        y = pos_y.get() * 0.8 + 60
        w = width_var.get() * 0.8
        h = 30
        
        # Dessiner la zone de texte
        text_rect = canvas.create_rectangle(x, y, x+w, y+h, 
                                          fill='lightblue', outline='blue', width=2,
                                          tags="preview_items")
        canvas.create_text(x+w/2, y+h/2, text="Zone de texte", 
                          tags="preview_items", font=('Arial', 8))
    
    # Lier les variables aux mises à jour
    for var in [pos_x, pos_y, width_var]:
        var.trace_add('write', lambda *args: update_preview())
    
    # ===== INSTRUCTIONS =====
    
    instructions_frame = ttk.LabelFrame(main_frame, text="📋 Instructions", padding=10)
    instructions_frame.pack(fill=tk.X, pady=(10, 0))
    
    instructions_text = """✅ PANNEAU REDIMENSIONNABLE ACTIVÉ:
• Glissez le séparateur vertical pour redimensionner les panneaux
• Les sliders s'adaptent automatiquement à la largeur du panneau
• Largeur maximale des sliders: 300px (pour éviter qu'ils soient trop longs)
• Largeur minimale des sliders: 150px (pour rester utilisables)"""
    
    ttk.Label(instructions_frame, text=instructions_text, justify=tk.LEFT).pack(anchor=tk.W)
    
    # Configurer la position initiale du séparateur (30% / 70%)
    initial_width = 360  # 30% de 1200px
    root.after(100, lambda: paned_window.sashpos(0, initial_width))
    
    # Démarrer les mises à jour
    root.after(100, update_sliders)
    root.after(100, update_info)
    update_preview()
    
    print("✅ Interface de test lancée!")
    print("   - Panneau gauche redimensionnable")
    print("   - Sliders adaptatifs (150-300px)")
    print("   - Aperçu dynamique")
    print()
    print("🎯 Testez le redimensionnement en glissant le séparateur!")
    
    root.mainloop()

if __name__ == "__main__":
    test_resizable_panel()
