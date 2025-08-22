#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'amélioration de l'interface de positionnement des éléments
- Boutons de préréglages mieux organisés et plus visibles
- Zone de réglages avec scroll plus accessible
- Réorganisation pour une meilleure utilisation
"""
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font
import sqlite3
from lib.database import CardRepo
from lib.config import DB_FILE

def test_improved_position_ui():
    """Test de l'interface améliorée"""
    print("🎨 TEST INTERFACE POSITIONNEMENT AMÉLIORÉE")
    print("=" * 60)
    
    # Récupérer une carte pour le test
    repo = CardRepo(DB_FILE)
    cards = repo.list_cards()
    
    if not cards:
        print("❌ Aucune carte disponible pour le test")
        return
    
    test_card = cards[0]
    print(f"🎯 Test avec la carte: {test_card.name}")
    
    # Créer la fenêtre de test
    root = tk.Tk()
    root.title("🎨 Interface Positionnement Améliorée")
    root.geometry("1200x800")
    
    # Variables pour les tests
    energy_x_var = tk.IntVar(value=25)
    energy_y_var = tk.IntVar(value=25)
    
    def set_energy_position(x, y):
        """Défini la position de l'énergie"""
        energy_x_var.set(x)
        energy_y_var.set(y)
        print(f"📍 Position énergie définie: ({x}, {y})")
    
    def on_value_change(value=None):
        """Appelé quand une valeur change"""
        print(f"🔄 Position mise à jour: ({energy_x_var.get()}, {energy_y_var.get()})")
    
    # Frame principal avec amélioration
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Frame gauche - AVEC SCROLL AMÉLIORÉ (30% de la largeur)
    controls_frame = ttk.LabelFrame(main_frame, text="📝 Contrôles de Formatage", padding=5)
    controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
    controls_frame.configure(width=360)  # Plus large pour mieux voir
    controls_frame.pack_propagate(False)
    
    # === ZONE SCROLLABLE AMÉLIORÉE ===
    # Canvas avec scrollbar PLUS VISIBLE
    canvas = tk.Canvas(controls_frame, width=340, height=720, bg="#f8f8f8")
    
    # Scrollbar PLUS LARGE et PLUS VISIBLE
    scrollbar = ttk.Scrollbar(controls_frame, orient="vertical", command=canvas.yview)
    scrollbar.configure(style="Vertical.TScrollbar")  # Style plus visible
    
    # Frame scrollable
    scrollable_frame = ttk.Frame(canvas)
    
    # Configuration scroll
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # === SECTION ÉNERGIE AVEC PRÉRÉGLAGES AMÉLIORÉS ===
    energy_frame = ttk.LabelFrame(scrollable_frame, text="⚡ Formatage du Coût en Énergie", padding=10)
    energy_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Position X avec curseur pleine largeur
    pos_x_frame = ttk.Frame(energy_frame)
    pos_x_frame.pack(fill=tk.X, pady=(0, 5))
    
    x_label_frame = ttk.Frame(pos_x_frame)
    x_label_frame.pack(fill=tk.X)
    ttk.Label(x_label_frame, text="Position X:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
    ttk.Label(x_label_frame, textvariable=energy_x_var, font=('Arial', 9)).pack(side=tk.RIGHT)
    
    # Curseur X - LARGEUR LIMITÉE À 300PX
    ttk.Scale(pos_x_frame, from_=0, to=300, variable=energy_x_var,
             command=on_value_change, length=300, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 0))
    
    # Position Y avec curseur pleine largeur
    pos_y_frame = ttk.Frame(energy_frame)
    pos_y_frame.pack(fill=tk.X, pady=(5, 10))
    
    y_label_frame = ttk.Frame(pos_y_frame)
    y_label_frame.pack(fill=tk.X)
    ttk.Label(y_label_frame, text="Position Y:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
    ttk.Label(y_label_frame, textvariable=energy_y_var, font=('Arial', 9)).pack(side=tk.RIGHT)
    
    # Curseur Y - LARGEUR LIMITÉE À 300PX
    ttk.Scale(pos_y_frame, from_=0, to=600, variable=energy_y_var,
             command=on_value_change, length=300, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 0))
    
    # === PRÉRÉGLAGES REPOSITIONNÉS ET PLUS VISIBLES ===
    presets_frame = ttk.LabelFrame(energy_frame, text="🎯 Préréglages Position", padding=8)
    presets_frame.pack(fill=tk.X, pady=(10, 10))
    
    # AMÉLIORATION: Boutons plus grands et mieux espacés
    # Ligne 1: Positions hautes
    row1 = ttk.Frame(presets_frame)
    row1.pack(fill=tk.X, pady=(0, 5))
    
    ttk.Button(row1, text="↖ Haut G.", width=10, 
              command=lambda: set_energy_position(25, 25)).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(row1, text="↑ Haut C.", width=10,
              command=lambda: set_energy_position(140, 25)).pack(side=tk.LEFT, padx=5)
    ttk.Button(row1, text="↗ Haut D.", width=10,
              command=lambda: set_energy_position(255, 25)).pack(side=tk.LEFT, padx=(5, 0))
    
    # Ligne 2: Positions milieu
    row2 = ttk.Frame(presets_frame)
    row2.pack(fill=tk.X, pady=(5, 5))
    
    ttk.Button(row2, text="← Milieu G.", width=10,
              command=lambda: set_energy_position(25, 235)).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(row2, text="⚫ Centre", width=10,
              command=lambda: set_energy_position(140, 235)).pack(side=tk.LEFT, padx=5)
    ttk.Button(row2, text="→ Milieu D.", width=10,
              command=lambda: set_energy_position(255, 235)).pack(side=tk.LEFT, padx=(5, 0))
    
    # Ligne 3: Positions basses (NOUVELLE LIGNE)
    row3 = ttk.Frame(presets_frame)
    row3.pack(fill=tk.X, pady=(5, 0))
    
    ttk.Button(row3, text="↙ Bas G.", width=10,
              command=lambda: set_energy_position(25, 445)).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(row3, text="↓ Bas C.", width=10,
              command=lambda: set_energy_position(140, 445)).pack(side=tk.LEFT, padx=5)
    ttk.Button(row3, text="↘ Bas D.", width=10,
              command=lambda: set_energy_position(255, 445)).pack(side=tk.LEFT, padx=(5, 0))
    
    # Autres contrôles pour le test...
    other_frame = ttk.LabelFrame(scrollable_frame, text="📝 Autres Réglages", padding=10)
    other_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Ajouter du contenu pour tester le scroll
    for i in range(5):
        test_section = ttk.LabelFrame(scrollable_frame, text=f"🔧 Section Test {i+1}", padding=10)
        test_section.pack(fill=tk.X, pady=(0, 10))
        
        for j in range(3):
            ttk.Label(test_section, text=f"Option {j+1} de la section {i+1}").pack(anchor=tk.W)
            ttk.Scale(test_section, from_=0, to=100, length=300, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 5))
    
    # PLACEMENT AMÉLIORÉ DU CANVAS ET SCROLLBAR
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Activer la roulette de souris sur le canvas
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind("<MouseWheel>", _on_mousewheel)
    
    # Frame droite - Aperçu (70% de la largeur)
    preview_frame = ttk.LabelFrame(main_frame, text="👁️ Aperçu", padding=10)
    preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Canvas d'aperçu simple pour le test
    preview_canvas = tk.Canvas(preview_frame, width=800, height=600, bg="#e0e0e0")
    preview_canvas.pack(fill=tk.BOTH, expand=True)
    
    # Afficher les informations de test
    info_frame = ttk.Frame(preview_frame)
    info_frame.pack(fill=tk.X, pady=(10, 0))
    
    status_label = ttk.Label(info_frame, text="🎯 Interface améliorée avec scroll fonctionnel et préréglages visibles")
    status_label.pack()
    
    # Boutons de test
    button_frame = ttk.Frame(root)
    button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    ttk.Button(button_frame, text="✅ Test Réussi", 
              command=lambda: print("✅ Interface améliorée validée!")).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="❌ Fermer", command=root.destroy).pack(side=tk.RIGHT)
    
    print("✅ Interface créée avec améliorations:")
    print("   📍 Préréglages mieux organisés en 3 lignes")
    print("   📏 Curseurs pleine largeur plus accessibles")
    print("   📜 Zone scrollable avec barre visible")
    print("   🎯 Layout 30/70 pour plus d'espace aux contrôles")
    
    root.mainloop()

if __name__ == "__main__":
    test_improved_position_ui()
