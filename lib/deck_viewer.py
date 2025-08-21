#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre de visualisation du deck
"""
import os
import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageTk
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

from .database import CardRepo

class DeckViewerWindow:
    """Fenêtre de visualisation du deck avec tri et affichage en grille."""
    
    def __init__(self, parent, repo: CardRepo):
        self.parent = parent
        self.repo = repo
        self.window = None
        self.cards = []
        self.filtered_cards = []
        self.images = {}  # Cache des images chargées
        self.current_filter = "Toutes"
        self.current_sort = "rarity"
        
        # Tailles d'images
        self.card_width = 120
        self.card_height = 160
        self.cards_per_row = 5
        
        # Initialiser l'ActorManager pour le tri par acteur
        from .actors import ActorManager
        self.actor_manager = ActorManager(repo.db_file)
        
        self.create_window()
        
    def create_window(self):
        """Crée la fenêtre principale."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🃏 Visualiseur de Deck")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Empêcher la fermeture avec Alt+F4
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Configuration de la grille
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        
        self.create_sidebar()
        self.create_main_area()
        self.load_cards()
        
    def create_sidebar(self):
        """Crée la barre latérale avec les onglets de tri."""
        sidebar_frame = ttk.Frame(self.window)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(5,0), pady=5)
        
        # Titre
        title_label = ttk.Label(sidebar_frame, text="🔽 Filtres", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Section Rareté
        rarity_frame = ttk.LabelFrame(sidebar_frame, text="📊 Rareté", padding=5)
        rarity_frame.pack(fill="x", pady=(0, 10))
        
        self.rarity_var = tk.StringVar(value="Toutes")
        rarity_options = ["Toutes", "commun", "rare", "epique", "legendaire", "mythique"]
        
        for rarity in rarity_options:
            rb = ttk.Radiobutton(
                rarity_frame, 
                text=rarity.title(), 
                variable=self.rarity_var, 
                value=rarity,
                command=lambda: self.filter_by_rarity()
            )
            rb.pack(anchor="w")
        
        # Section Types
        types_frame = ttk.LabelFrame(sidebar_frame, text="🎯 Types", padding=5)
        types_frame.pack(fill="x", pady=(0, 10))
        
        self.type_var = tk.StringVar(value="Tous")
        type_options = ["Tous", "attaque", "defense", "soutien", "sort", "piege"]
        
        for card_type in type_options:
            rb = ttk.Radiobutton(
                types_frame, 
                text=card_type.title(), 
                variable=self.type_var, 
                value=card_type,
                command=lambda: self.filter_by_type()
            )
            rb.pack(anchor="w")
        
        # Section Acteurs
        actors_frame = ttk.LabelFrame(sidebar_frame, text="🎭 Acteurs", padding=5)
        actors_frame.pack(fill="x", pady=(0, 10))
        
        self.actor_var = tk.StringVar(value="Tous")
        
        # Récupérer la liste des acteurs
        self.update_actor_options(actors_frame)
        
        # Section Tri
        sort_frame = ttk.LabelFrame(sidebar_frame, text="📋 Tri", padding=5)
        sort_frame.pack(fill="x", pady=(0, 10))
        
        self.sort_var = tk.StringVar(value="rarity")
        sort_options = [
            ("Par rareté", "rarity"),
            ("Par nom", "name"),
            ("Par type", "type"),
            ("Par puissance", "power"),
            ("Par acteur", "actor")
        ]
        
        for text, value in sort_options:
            rb = ttk.Radiobutton(
                sort_frame, 
                text=text, 
                variable=self.sort_var, 
                value=value,
                command=lambda: self.sort_cards()
            )
            rb.pack(anchor="w")
        
        # Boutons d'action
        action_frame = ttk.Frame(sidebar_frame)
        action_frame.pack(fill="x", pady=(10, 0))
        
        refresh_btn = ttk.Button(
            action_frame, 
            text="🔄 Actualiser", 
            command=self.refresh_deck
        )
        refresh_btn.pack(fill="x", pady=(0, 5))
        
        close_btn = ttk.Button(
            action_frame, 
            text="❌ Fermer", 
            command=self.on_close
        )
        close_btn.pack(fill="x")
        
    def create_main_area(self):
        """Crée la zone principale d'affichage."""
        main_frame = ttk.Frame(self.window)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Barre d'informations
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        self.info_label = ttk.Label(
            info_frame, 
            text="🃏 Chargement du deck...", 
            font=("Arial", 11)
        )
        self.info_label.pack(side="left")
        
        # Zone scrollable pour les cartes
        self.canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Bind scroll wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        """Gestion de la molette de souris."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def load_cards(self):
        """Charge toutes les cartes depuis la base."""
        self.cards = self.repo.list_cards()
        self.filtered_cards = self.cards.copy()
        self.update_info_label()
        self.display_cards()
        
    def filter_by_rarity(self):
        """Filtre les cartes par rareté."""
        rarity = self.rarity_var.get()
        self.current_filter = rarity
        self.apply_filters()
        
    def filter_by_type(self):
        """Filtre les cartes par type."""
        card_type = self.type_var.get()
        self.current_filter = card_type
        self.apply_filters()
        
    def filter_by_actor(self):
        """Filtre les cartes par acteur."""
        actor = self.actor_var.get()
        self.current_filter = actor
        self.apply_filters()
        
    def update_actor_options(self, actors_frame):
        """Met à jour les options d'acteurs dans l'interface."""
        # Supprimer les widgets existants (sauf le premier qui sera "Tous")
        for widget in actors_frame.winfo_children():
            widget.destroy()
        
        # Option "Tous"
        rb_all = ttk.Radiobutton(
            actors_frame, 
            text="Tous", 
            variable=self.actor_var, 
            value="Tous",
            command=lambda: self.filter_by_actor()
        )
        rb_all.pack(anchor="w")
        
        # Récupérer tous les acteurs actifs
        actors = self.actor_manager.list_actors()
        for actor in actors:
            rb = ttk.Radiobutton(
                actors_frame, 
                text=f"{actor['icon']} {actor['name']}", 
                variable=self.actor_var, 
                value=str(actor['id']),
                command=lambda: self.filter_by_actor()
            )
            rb.pack(anchor="w")
        
    def apply_filters(self):
        """Applique tous les filtres actifs."""
        self.filtered_cards = self.cards.copy()
        
        # Filtre par rareté
        rarity = self.rarity_var.get()
        if rarity != "Toutes":
            self.filtered_cards = [c for c in self.filtered_cards if c.rarity == rarity]
        
        # Filtre par type
        card_type = self.type_var.get()
        if card_type != "Tous":
            self.filtered_cards = [c for c in self.filtered_cards 
                                 if card_type in (c.types or [])]
        
        # Filtre par acteur
        actor = self.actor_var.get()
        if actor != "Tous":
            try:
                actor_id = int(actor)
                # Récupérer les cartes de cet acteur
                actor_cards = self.actor_manager.get_actor_cards(actor_id)
                actor_card_ids = {card.id for card in actor_cards}
                self.filtered_cards = [c for c in self.filtered_cards if c.id in actor_card_ids]
            except ValueError:
                # Si conversion échoue, ne pas filtrer par acteur
                pass
        
        self.sort_cards()
        
    def sort_cards(self):
        """Trie les cartes selon le critère sélectionné."""
        sort_by = self.sort_var.get()
        
        if sort_by == "rarity":
            # Ordre de rareté
            rarity_order = {"commun": 1, "rare": 2, "epique": 3, "legendaire": 4, "mythique": 5}
            self.filtered_cards.sort(key=lambda c: rarity_order.get(c.rarity, 0))
        elif sort_by == "name":
            self.filtered_cards.sort(key=lambda c: c.name.lower())
        elif sort_by == "type":
            self.filtered_cards.sort(key=lambda c: (c.types or [""])[0] if c.types else "")
        elif sort_by == "power":
            self.filtered_cards.sort(key=lambda c: c.powerblow, reverse=True)
        elif sort_by == "actor":
            # Tri par acteur - regrouper les cartes par acteur
            def get_card_actors(card):
                actors = self.actor_manager.get_card_actors(card.id)
                if actors:
                    return actors[0]['name']  # Premier acteur si plusieurs
                return "Zzz_Aucun"  # Mettre à la fin les cartes sans acteur
            
            self.filtered_cards.sort(key=get_card_actors)
        
        self.update_info_label()
        self.display_cards()
        
    def update_info_label(self):
        """Met à jour le label d'informations."""
        total = len(self.cards)
        filtered = len(self.filtered_cards)
        
        if filtered == total:
            text = f"🃏 {total} cartes au total"
        else:
            text = f"🃏 {filtered} / {total} cartes (filtrées)"
        
        # Ajouter info sur le filtre actuel
        rarity = self.rarity_var.get()
        card_type = self.type_var.get()
        actor = self.actor_var.get()
        
        if rarity != "Toutes" or card_type != "Tous" or actor != "Tous":
            filters = []
            if rarity != "Toutes":
                filters.append(f"Rareté: {rarity}")
            if card_type != "Tous":
                filters.append(f"Type: {card_type}")
            if actor != "Tous":
                # Récupérer le nom de l'acteur
                try:
                    actor_id = int(actor)
                    actors = self.actor_manager.list_actors()
                    actor_name = next((a['name'] for a in actors if a['id'] == actor_id), "Inconnu")
                    filters.append(f"Acteur: {actor_name}")
                except ValueError:
                    pass
            text += f" | {', '.join(filters)}"
        
        self.info_label.config(text=text)
        
    def display_cards(self):
        """Affiche les cartes dans la grille."""
        # Nettoyer l'affichage précédent
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.filtered_cards:
            no_cards_label = ttk.Label(
                self.scrollable_frame, 
                text="🚫 Aucune carte trouvée avec ces filtres",
                font=("Arial", 14)
            )
            no_cards_label.pack(pady=50)
            return
        
        # Afficher les cartes en grille
        for i, card in enumerate(self.filtered_cards):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            card_frame = self.create_card_widget(card)
            card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="n")
        
        # Configurer les colonnes pour qu'elles aient la même largeur
        for col in range(self.cards_per_row):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)
            
    def create_card_widget(self, card):
        """Crée le widget d'affichage d'une carte."""
        card_frame = ttk.Frame(self.scrollable_frame)
        
        # Chargement de l'image
        img_widget = self.load_card_image(card, card_frame)  # Passer le parent
        if img_widget:
            img_widget.pack()
        
        # Nom de la carte
        name_label = ttk.Label(
            card_frame, 
            text=card.name, 
            font=("Arial", 10, "bold"),
            wraplength=self.card_width
        )
        name_label.pack(pady=(5, 0))
        
        # Informations sur la carte
        info_text = f"⭐ {card.rarity.title()}"
        if card.types:
            info_text += f"\n🎯 {', '.join(card.types)}"
        info_text += f"\n⚡ {card.powerblow}"
        
        # Ajouter les acteurs associés
        actors = self.actor_manager.get_card_actors(card.id)
        if actors:
            actor_names = [f"{actor['icon']} {actor['name']}" for actor in actors[:2]]  # Limiter à 2 acteurs
            info_text += f"\n🎭 {', '.join(actor_names)}"
            if len(actors) > 2:
                info_text += "..."
        else:
            info_text += "\n🎭 Aucun acteur"
        
        info_label = ttk.Label(
            card_frame, 
            text=info_text, 
            font=("Arial", 8),
            justify="center"
        )
        info_label.pack(pady=(2, 0))
        
        return card_frame
        
    def load_card_image(self, card, parent_frame):
        """Charge l'image d'une carte."""
        if not card.img or not os.path.exists(card.img):
            # Image par défaut si pas d'image
            placeholder = tk.Label(
                parent_frame,
                text="🃏\nPas d'image",
                width=15, height=8,
                bg="lightgray",
                font=("Arial", 10)
            )
            return placeholder
        
        try:
            # Utiliser le cache si disponible
            if card.img in self.images:
                img_label = tk.Label(parent_frame, image=self.images[card.img])
                return img_label
            
            if PILLOW_AVAILABLE:
                # Charger et redimensionner l'image avec PIL
                pil_image = Image.open(card.img)
                pil_image = pil_image.resize((self.card_width, self.card_height), Image.Resampling.LANCZOS)
                
                # Convertir pour Tkinter
                tk_image = ImageTk.PhotoImage(pil_image)
                self.images[card.img] = tk_image  # Cache
                
                img_label = tk.Label(parent_frame, image=tk_image)
                return img_label
            else:
                # Fallback sans PIL - juste un placeholder avec le nom du fichier
                filename = os.path.basename(card.img)
                placeholder = tk.Label(
                    parent_frame,
                    text=f"🖼️\n{filename[:15]}...",
                    width=15, height=8,
                    bg="lightblue",
                    font=("Arial", 9),
                    wraplength=self.card_width-20
                )
                return placeholder
            
        except Exception as e:
            print(f"Erreur chargement image {card.img}: {e}")
            # Image d'erreur
            error_label = tk.Label(
                parent_frame,
                text="❌\nErreur image",
                width=15, height=8,
                bg="salmon",
                font=("Arial", 10)
            )
            return error_label
            
    def refresh_deck(self):
        """Actualise l'affichage du deck."""
        self.images.clear()  # Vider le cache d'images
        
        # Trouver le frame des acteurs et le mettre à jour
        for widget in self.window.winfo_children():
            if isinstance(widget, ttk.Frame):
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, ttk.LabelFrame) and "Acteurs" in subwidget.cget("text"):
                        self.update_actor_options(subwidget)
                        break
        
        self.load_cards()
        
    def on_close(self):
        """Gestionnaire de fermeture de fenêtre."""
        self.images.clear()  # Libérer la mémoire
        self.window.destroy()

def open_deck_viewer(parent, repo: CardRepo):
    """Fonction utilitaire pour ouvrir le visualiseur de deck."""
    return DeckViewerWindow(parent, repo)
