#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 DÉMONSTRATION DU SYSTÈME D'ACTEURS
Application de test pour le nouveau système d'acteurs
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import ensure_db, CardRepo
from lib.config import DB_FILE
from lib.actors import ActorManager
from lib.actor_ui import open_actor_manager
from lib.actor_selector import open_actor_export_dialog

class ActorDemoApp:
    """Application de démonstration du système d'acteurs."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎭 Démonstration Système d'Acteurs - Éditeur de Cartes Love2D")
        self.root.geometry("900x700")
        
        # Initialiser la base de données et le système d'acteurs
        ensure_db(DB_FILE)
        self.repo = CardRepo(DB_FILE)
        self.actor_manager = ActorManager(DB_FILE)
        
        self.build_ui()
        self.refresh_all()
    
    def build_ui(self):
        """Construit l'interface de démonstration."""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Titre
        title = ttk.Label(main_frame, 
                         text="🎭 Système d'Acteurs pour l'Éditeur de Cartes Love2D",
                         font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Description
        desc_text = """
🚀 NOUVEAU SYSTÈME D'ACTEURS

Remplace le système rigide "Joueur/IA" par un système flexible d'acteurs :
• Créez autant d'acteurs que nécessaire (Boss, PNJ, Factions, etc.)
• Liez chaque carte à un ou plusieurs acteurs
• Exportez les cartes par acteur avec des noms de fichiers personnalisés
• Interface intuitive avec icônes et couleurs
        """.strip()
        
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.LEFT, 
                              font=("Segoe UI", 10), foreground="dark blue")
        desc_label.pack(pady=(0, 20))
        
        # Notebook avec onglets
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet 1 : Vue des acteurs
        self.actors_tab = ttk.Frame(notebook)
        notebook.add(self.actors_tab, text="🎭 Acteurs")
        self.build_actors_tab()
        
        # Onglet 2 : Cartes par acteur
        self.cards_tab = ttk.Frame(notebook)
        notebook.add(self.cards_tab, text="🃏 Cartes par Acteur")
        self.build_cards_tab()
        
        # Onglet 3 : Export
        self.export_tab = ttk.Frame(notebook)
        notebook.add(self.export_tab, text="📤 Export")
        self.build_export_tab()
        
        # Boutons de gestion
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(button_frame, text="⚙️ Gérer les Acteurs", 
                  command=self.open_actor_manager).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📤 Export par Acteur", 
                  command=self.open_export_dialog).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🔄 Rafraîchir", 
                  command=self.refresh_all).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Button(button_frame, text="❌ Fermer", 
                  command=self.root.destroy).pack(side=tk.RIGHT)
    
    def build_actors_tab(self):
        """Construit l'onglet des acteurs."""
        frame = ttk.Frame(self.actors_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="📋 Liste des Acteurs Disponibles", 
                 font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        
        # Liste des acteurs
        columns = ("id", "icon", "name", "description", "cards")
        self.actors_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        self.actors_tree.heading("id", text="ID")
        self.actors_tree.heading("icon", text="Icône")
        self.actors_tree.heading("name", text="Nom")
        self.actors_tree.heading("description", text="Description")
        self.actors_tree.heading("cards", text="Cartes")
        
        self.actors_tree.column("id", width=50)
        self.actors_tree.column("icon", width=60)
        self.actors_tree.column("name", width=120)
        self.actors_tree.column("description", width=300)
        self.actors_tree.column("cards", width=80)
        
        self.actors_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar1 = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.actors_tree.yview)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        self.actors_tree.configure(yscrollcommand=scrollbar1.set)
    
    def build_cards_tab(self):
        """Construit l'onglet des cartes par acteur."""
        frame = ttk.Frame(self.cards_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sélecteur d'acteur
        selector_frame = ttk.Frame(frame)
        selector_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(selector_frame, text="🎭 Choisir un acteur :").pack(side=tk.LEFT)
        
        self.selected_actor_var = tk.StringVar()
        self.actor_combo = ttk.Combobox(selector_frame, textvariable=self.selected_actor_var,
                                       state="readonly", width=30)
        self.actor_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.actor_combo.bind("<<ComboboxSelected>>", self.on_actor_selected)
        
        # Liste des cartes
        ttk.Label(frame, text="🃏 Cartes de l'acteur sélectionné", 
                 font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))
        
        columns = ("id", "name", "description", "rarity", "types")
        self.cards_tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        
        self.cards_tree.heading("id", text="ID")
        self.cards_tree.heading("name", text="Nom")
        self.cards_tree.heading("description", text="Description")
        self.cards_tree.heading("rarity", text="Rareté")
        self.cards_tree.heading("types", text="Types")
        
        self.cards_tree.column("id", width=50)
        self.cards_tree.column("name", width=150)
        self.cards_tree.column("description", width=250)
        self.cards_tree.column("rarity", width=100)
        self.cards_tree.column("types", width=150)
        
        self.cards_tree.pack(fill=tk.BOTH, expand=True)
    
    def build_export_tab(self):
        """Construit l'onglet d'export."""
        frame = ttk.Frame(self.export_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="📤 Export des Cartes par Acteur", 
                 font=("Segoe UI", 12, "bold")).pack(pady=(0, 20))
        
        # Instructions
        instructions = """
🎯 FONCTIONNALITÉS D'EXPORT :

1. Export Individuel :
   • Sélectionnez un acteur spécifique
   • Exportez ses cartes dans un fichier .lua personnalisé
   • Nom de fichier automatique : cards_nom_acteur.lua

2. Export Multiple :
   • Sélectionnez plusieurs acteurs à la fois
   • Un fichier .lua est créé pour chaque acteur
   • Dossier de destination configurable

3. Avantages :
   • Organisation claire des cartes par fonction/rôle
   • Facilite l'intégration dans Love2D
   • Gestion modulaire des contenus de jeu
   • Noms de fichiers descriptifs et explicites
        """.strip()
        
        instructions_label = ttk.Label(frame, text=instructions, justify=tk.LEFT,
                                     font=("Segoe UI", 10))
        instructions_label.pack(fill=tk.BOTH, expand=True)
        
        # Exemple de fichiers générés
        example_frame = ttk.LabelFrame(frame, text="📁 Exemples de Fichiers Générés")
        example_frame.pack(fill=tk.X, pady=(20, 0))
        
        examples = """
cards_joueur.lua          → Cartes du joueur principal
cards_ia.lua              → Cartes de l'IA
cards_boss.lua             → Cartes des boss
cards_pnj.lua              → Cartes des PNJ
cards_marchand.lua         → Cartes des marchands
cards_dragon.lua           → Cartes de créatures dragon
        """.strip()
        
        ttk.Label(example_frame, text=examples, font=("Consolas", 9),
                 justify=tk.LEFT).pack(padx=10, pady=10)
    
    def refresh_all(self):
        """Rafraîchit toutes les données."""
        self.refresh_actors()
        self.refresh_actor_combo()
    
    def refresh_actors(self):
        """Rafraîchit la liste des acteurs."""
        # Vider la liste
        for item in self.actors_tree.get_children():
            self.actors_tree.delete(item)
        
        # Recharger les acteurs
        actors = self.actor_manager.list_actors()
        for actor in actors:
            cards = self.actor_manager.get_actor_cards(actor['id'])
            card_count = len(cards)
            
            self.actors_tree.insert("", "end", values=(
                actor['id'],
                actor['icon'],
                actor['name'],
                actor['description'],
                f"{card_count} cartes"
            ))
    
    def refresh_actor_combo(self):
        """Rafraîchit le combobox des acteurs."""
        actors = self.actor_manager.list_actors()
        values = [f"{actor['icon']} {actor['name']}" for actor in actors]
        self.actor_combo['values'] = values
        
        if values and not self.selected_actor_var.get():
            self.actor_combo.current(0)
            self.on_actor_selected()
    
    def on_actor_selected(self, event=None):
        """Gestionnaire de sélection d'acteur."""
        selection = self.selected_actor_var.get()
        if not selection:
            return
        
        # Extraire le nom de l'acteur
        actor_name = selection.split(' ', 1)[1]  # Enlever l'icône
        
        # Trouver l'acteur correspondant
        actors = self.actor_manager.list_actors()
        selected_actor = next((a for a in actors if a['name'] == actor_name), None)
        
        if not selected_actor:
            return
        
        # Vider la liste des cartes
        for item in self.cards_tree.get_children():
            self.cards_tree.delete(item)
        
        # Charger les cartes de l'acteur
        cards = self.actor_manager.get_actor_cards(selected_actor['id'])
        
        for card_row in cards:
            from lib.database import Card
            card = Card(card_row)
            
            # Formater les types
            types_str = ", ".join(card.types) if card.types else "Aucun"
            
            self.cards_tree.insert("", "end", values=(
                card.id,
                card.name,
                card.description[:50] + "..." if len(card.description) > 50 else card.description,
                card.rarity,
                types_str
            ))
    
    def open_actor_manager(self):
        """Ouvre la fenêtre de gestion des acteurs."""
        open_actor_manager(self.root, DB_FILE)
        # Rafraîchir après fermeture
        self.root.after(1000, self.refresh_all)
    
    def open_export_dialog(self):
        """Ouvre le dialogue d'export par acteur."""
        open_actor_export_dialog(self.root, DB_FILE)
    
    def run(self):
        """Lance l'application."""
        self.root.mainloop()

def main():
    """Point d'entrée principal."""
    print("🎭 Lancement de la démonstration du système d'acteurs...")
    
    try:
        app = ActorDemoApp()
        app.run()
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
