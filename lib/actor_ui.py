#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 INTERFACE DE GESTION DES ACTEURS
Interface graphique pour créer, modifier et gérer les acteurs
"""
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from lib.actors import ActorManager
from lib.config import APP_TITLE

class ActorManagerWindow:
    """Fenêtre de gestion des acteurs."""
    
    def __init__(self, parent, db_path: str):
        self.parent = parent
        self.actor_manager = ActorManager(db_path)
        self.window = tk.Toplevel(parent)
        self.window.title(f"{APP_TITLE} - Gestion des Acteurs")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Variables
        self.selected_actor_id = None
        
        self.build_ui()
        self.refresh_actors()
        
        # Centrer la fenêtre
        self.window.transient(parent)
        self.window.grab_set()
    
    def build_ui(self):
        """Construit l'interface utilisateur."""
        # Frame principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titre
        title = ttk.Label(main_frame, text="🎭 Gestion des Acteurs", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Frame horizontal pour la liste et les détails
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # === LISTE DES ACTEURS (Gauche) ===
        left_frame = ttk.LabelFrame(content_frame, text="📋 Acteurs Existants")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Liste des acteurs
        self.actors_tree = ttk.Treeview(left_frame, columns=("id", "name", "description", "cards"), show="headings", height=15)
        self.actors_tree.heading("id", text="ID")
        self.actors_tree.heading("name", text="Nom")
        self.actors_tree.heading("description", text="Description")
        self.actors_tree.heading("cards", text="Cartes")
        
        self.actors_tree.column("id", width=50)
        self.actors_tree.column("name", width=120)
        self.actors_tree.column("description", width=200)
        self.actors_tree.column("cards", width=80)
        
        self.actors_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.actors_tree.bind("<<TreeviewSelect>>", self.on_actor_select)
        
        # Boutons de gestion
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="🗑️ Supprimer", command=self.delete_actor).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="📤 Exporter", command=self.export_actor).pack(side=tk.LEFT, padx=(0, 5))
        
        # === CRÉATION/ÉDITION (Droite) ===
        right_frame = ttk.LabelFrame(content_frame, text="✨ Créer un Nouvel Acteur")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Formulaire de création
        form_frame = ttk.Frame(right_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Nom
        ttk.Label(form_frame, text="📝 Nom de l'acteur :").pack(anchor=tk.W)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var, font=("Segoe UI", 11))
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Description
        ttk.Label(form_frame, text="📄 Description :").pack(anchor=tk.W)
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(form_frame, textvariable=self.desc_var, font=("Segoe UI", 10))
        self.desc_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Icône
        icon_frame = ttk.Frame(form_frame)
        icon_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(icon_frame, text="🎨 Icône :").pack(side=tk.LEFT)
        self.icon_var = tk.StringVar(value="🎭")
        self.icon_entry = ttk.Entry(icon_frame, textvariable=self.icon_var, width=5, font=("Segoe UI", 14))
        self.icon_entry.pack(side=tk.RIGHT)
        
        # Couleur
        color_frame = ttk.Frame(form_frame)
        color_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(color_frame, text="🎨 Couleur :").pack(side=tk.LEFT)
        self.color_var = tk.StringVar(value="#2196F3")
        self.color_button = tk.Button(color_frame, textvariable=self.color_var, 
                                     command=self.choose_color, width=10,
                                     bg=self.color_var.get(), fg="white", font=("Segoe UI", 10))
        self.color_button.pack(side=tk.RIGHT)
        
        # Boutons d'action
        action_frame = ttk.Frame(form_frame)
        action_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.create_button = ttk.Button(action_frame, text="✅ Créer Acteur", command=self.create_actor)
        self.create_button.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(action_frame, text="🔄 Rafraîchir", command=self.refresh_actors).pack(fill=tk.X, pady=(0, 5))
        
        # === EXEMPLES D'ACTEURS ===
        examples_frame = ttk.LabelFrame(right_frame, text="💡 Exemples d'Acteurs")
        examples_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        examples_text = """
🏰 Boss Final - Cartes du boss de fin
🧙 Mage - Cartes de magie et sorts
⚔️ Guerrier - Cartes d'attaque physique
🛡️ Défenseur - Cartes défensives
🏹 Archer - Cartes à distance
🐲 Dragon - Cartes de créatures
💰 Marchand - Cartes d'objets
🎪 Événement - Cartes spéciales
        """.strip()
        
        examples_label = ttk.Label(examples_frame, text=examples_text, font=("Segoe UI", 9))
        examples_label.pack(padx=5, pady=5)
        
        # === BOUTONS DE FERMETURE ===
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(bottom_frame, text="❌ Fermer", command=self.window.destroy).pack(side=tk.RIGHT)
    
    def refresh_actors(self):
        """Rafraîchit la liste des acteurs."""
        # Vider la liste
        for item in self.actors_tree.get_children():
            self.actors_tree.delete(item)
        
        # Recharger les acteurs
        actors = self.actor_manager.list_actors()
        for actor in actors:
            # Compter les cartes pour cet acteur
            cards = self.actor_manager.get_actor_cards(actor['id'])
            card_count = len(cards)
            
            # Ajouter à la liste
            self.actors_tree.insert("", "end", values=(
                actor['id'],
                f"{actor['icon']} {actor['name']}",
                actor['description'],
                f"{card_count} cartes"
            ))
    
    def on_actor_select(self, event):
        """Gestionnaire de sélection d'acteur."""
        selection = self.actors_tree.selection()
        if selection:
            item = self.actors_tree.item(selection[0])
            self.selected_actor_id = int(item['values'][0])
    
    def create_actor(self):
        """Crée un nouvel acteur."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Erreur", "Le nom de l'acteur est obligatoire !")
            return
        
        description = self.desc_var.get().strip()
        icon = self.icon_var.get().strip() or "🎭"
        color = self.color_var.get()
        
        try:
            actor_id = self.actor_manager.create_actor(name, description, color, icon)
            messagebox.showinfo("Succès", f"Acteur '{name}' créé avec succès !\nID: {actor_id}")
            
            # Réinitialiser le formulaire
            self.name_var.set("")
            self.desc_var.set("")
            self.icon_var.set("🎭")
            self.color_var.set("#2196F3")
            self.color_button.config(bg="#2196F3")
            
            # Rafraîchir la liste
            self.refresh_actors()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création de l'acteur :\n{e}")
    
    def delete_actor(self):
        """Supprime l'acteur sélectionné."""
        if not self.selected_actor_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner un acteur à supprimer.")
            return
        
        # Confirmer la suppression
        if not messagebox.askyesno("Confirmation", 
                                  "Êtes-vous sûr de vouloir supprimer cet acteur ?\n"
                                  "Les cartes associées ne seront pas supprimées, "
                                  "mais ne seront plus liées à cet acteur."):
            return
        
        try:
            self.actor_manager.delete_actor(self.selected_actor_id)
            messagebox.showinfo("Succès", "Acteur supprimé avec succès !")
            self.selected_actor_id = None
            self.refresh_actors()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression :\n{e}")
    
    def export_actor(self):
        """Exporte les cartes de l'acteur sélectionné."""
        if not self.selected_actor_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner un acteur à exporter.")
            return
        
        from tkinter import filedialog
        from lib.actors import export_lua_for_actor
        from lib.database import CardRepo
        
        # Récupérer le nom de l'acteur
        actors = self.actor_manager.list_actors()
        actor = next((a for a in actors if a['id'] == self.selected_actor_id), None)
        if not actor:
            messagebox.showerror("Erreur", "Acteur introuvable !")
            return
        
        # Demander le fichier de destination
        default_filename = f"cards_{actor['name'].lower().replace(' ', '_')}.lua"
        filepath = filedialog.asksaveasfilename(
            title=f"Exporter les cartes de '{actor['name']}'",
            defaultextension=".lua",
            filetypes=[("Fichiers Lua", "*.lua"), ("Tous les fichiers", "*.*")],
            initialname=default_filename
        )
        
        if not filepath:
            return
        
        try:
            repo = CardRepo(self.actor_manager.db_path)
            export_lua_for_actor(repo, self.actor_manager, self.selected_actor_id, filepath)
            
            cards = self.actor_manager.get_actor_cards(self.selected_actor_id)
            messagebox.showinfo("Succès", 
                              f"Export réussi !\n"
                              f"Acteur : {actor['icon']} {actor['name']}\n"
                              f"Cartes : {len(cards)}\n"
                              f"Fichier : {filepath}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export :\n{e}")
    
    def choose_color(self):
        """Ouvre le sélecteur de couleur."""
        color = colorchooser.askcolor(color=self.color_var.get())[1]
        if color:
            self.color_var.set(color)
            self.color_button.config(bg=color)

def open_actor_manager(parent, db_path: str):
    """Ouvre la fenêtre de gestion des acteurs."""
    ActorManagerWindow(parent, db_path)
