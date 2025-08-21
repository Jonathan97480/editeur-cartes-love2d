#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 COMPOSANT DE SÉLECTION D'ACTEURS POUR LES CARTES
Remplace le système joueur/IA par un système d'acteurs flexibles
"""
import tkinter as tk
from tkinter import ttk, messagebox
from lib.actors import ActorManager
from lib.actor_ui import open_actor_manager

class ActorSelector(ttk.Frame):
    """Widget de sélection d'acteurs pour une carte."""
    
    def __init__(self, master, db_path: str, **kw):
        super().__init__(master, **kw)
        self.db_path = db_path
        self.actor_manager = ActorManager(db_path)
        self.selected_actor_ids = set()
        
        self.build_ui()
        self.refresh_actors()
    
    def build_ui(self):
        """Construit l'interface de sélection d'acteurs."""
        # Frame titre avec gestion
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="🎭 Acteurs liés à cette carte :", 
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(title_frame, text="⚙️ Gérer Acteurs", 
                  command=self.open_actor_manager).pack(side=tk.RIGHT)
        
        # Frame de sélection avec scrollbar
        selection_frame = ttk.LabelFrame(self, text="Sélectionnez les acteurs concernés")
        selection_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas pour scrolling
        canvas = tk.Canvas(selection_frame, height=120)
        scrollbar = ttk.Scrollbar(selection_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas = canvas
        
        # Binding pour la molette
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Dictionnaire pour stocker les checkboxes
        self.actor_checkboxes = {}
    
    def refresh_actors(self):
        """Rafraîchit la liste des acteurs disponibles."""
        # Nettoyer les checkboxes existantes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.actor_checkboxes.clear()
        
        # Récupérer les acteurs
        actors = self.actor_manager.list_actors()
        
        if not actors:
            ttk.Label(self.scrollable_frame, 
                     text="Aucun acteur disponible.\nCliquez sur 'Gérer Acteurs' pour en créer.",
                     justify=tk.CENTER).pack(pady=20)
            return
        
        # Créer les checkboxes
        for i, actor in enumerate(actors):
            var = tk.BooleanVar()
            
            # Frame pour chaque acteur
            actor_frame = ttk.Frame(self.scrollable_frame)
            actor_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Checkbox avec icône et nom
            checkbox = ttk.Checkbutton(
                actor_frame,
                text=f"{actor['icon']} {actor['name']}",
                variable=var,
                command=lambda aid=actor['id'], v=var: self._on_actor_toggle(aid, v)
            )
            checkbox.pack(side=tk.LEFT)
            
            # Description
            if actor['description']:
                desc_label = ttk.Label(actor_frame, text=f"- {actor['description']}", 
                                     foreground="gray", font=("Segoe UI", 9))
                desc_label.pack(side=tk.LEFT, padx=(10, 0))
            
            # Nombre de cartes
            cards = self.actor_manager.get_actor_cards(actor['id'])
            count_label = ttk.Label(actor_frame, text=f"({len(cards)} cartes)", 
                                  foreground="blue", font=("Segoe UI", 9))
            count_label.pack(side=tk.RIGHT)
            
            self.actor_checkboxes[actor['id']] = var
            
            # Mettre à jour l'état si l'acteur est déjà sélectionné
            if actor['id'] in self.selected_actor_ids:
                var.set(True)
    
    def _on_actor_toggle(self, actor_id: int, var: tk.BooleanVar):
        """Gestionnaire de changement d'état d'un acteur."""
        if var.get():
            self.selected_actor_ids.add(actor_id)
        else:
            self.selected_actor_ids.discard(actor_id)
    
    def set_selected_actors(self, actor_ids: list[int]):
        """Définit les acteurs sélectionnés."""
        self.selected_actor_ids = set(actor_ids)
        
        # Mettre à jour les checkboxes
        for actor_id, var in self.actor_checkboxes.items():
            var.set(actor_id in self.selected_actor_ids)
    
    def get_selected_actors(self) -> list[int]:
        """Retourne la liste des acteurs sélectionnés."""
        return list(self.selected_actor_ids)
    
    def open_actor_manager(self):
        """Ouvre la fenêtre de gestion des acteurs."""
        open_actor_manager(self.winfo_toplevel(), self.db_path)
        # Rafraîchir après fermeture de la fenêtre
        self.after(500, self.refresh_actors)

class ActorExportDialog:
    """Dialogue pour exporter les cartes par acteur."""
    
    def __init__(self, parent, db_path: str, actor_manager=None, single_actor_mode=False):
        self.parent = parent
        self.db_path = db_path
        self.actor_manager = actor_manager or ActorManager(db_path)
        self.single_actor_mode = single_actor_mode
        
        self.window = tk.Toplevel(parent)
        if single_actor_mode:
            self.window.title("🎭 Exporter un Acteur")
            self.window.geometry("500x400")
        else:
            self.window.title("📤 Export par Acteur")
            self.window.geometry("600x500")
        self.window.resizable(True, True)
        
        self.build_ui()
        self.refresh_actors()
        
        # Centrer et modaliser
        self.window.transient(parent)
        self.window.grab_set()
    
    def build_ui(self):
        """Construit l'interface d'export."""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Titre
        if self.single_actor_mode:
            title_text = "🎭 Export d'un Acteur Spécifique"
            instructions_text = "Sélectionnez l'acteur dont vous voulez exporter les cartes.\nUn fichier .lua sera créé pour cet acteur."
        else:
            title_text = "📤 Export des Cartes par Acteur"
            instructions_text = "Sélectionnez les acteurs dont vous voulez exporter les cartes.\nUn fichier .lua sera créé pour chaque acteur sélectionné."
        
        title = ttk.Label(main_frame, text=title_text, 
                         font=("Segoe UI", 14, "bold"))
        title.pack(pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                                text=instructions_text,
                                justify=tk.CENTER, foreground="gray")
        instructions.pack(pady=(0, 15))
        
        # Liste des acteurs avec checkboxes
        list_frame = ttk.LabelFrame(main_frame, text="🎭 Acteurs Disponibles")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Treeview pour les acteurs
        self.actors_tree = ttk.Treeview(list_frame, columns=("select", "name", "cards", "description"), 
                                       show="tree headings", height=12)
        
        self.actors_tree.heading("#0", text="")
        self.actors_tree.heading("select", text="Exporter")
        self.actors_tree.heading("name", text="Acteur")
        self.actors_tree.heading("cards", text="Cartes")
        self.actors_tree.heading("description", text="Description")
        
        self.actors_tree.column("#0", width=30)
        self.actors_tree.column("select", width=80)
        self.actors_tree.column("name", width=150)
        self.actors_tree.column("cards", width=80)
        self.actors_tree.column("description", width=250)
        
        self.actors_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Variables pour les sélections
        self.selected_exports = {}
        
        # Boutons d'action
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        if not self.single_actor_mode:
            ttk.Button(button_frame, text="✅ Tout Sélectionner", 
                      command=self.select_all).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="❌ Tout Désélectionner", 
                      command=self.deselect_all).pack(side=tk.LEFT, padx=(0, 20))
            export_text = "📤 Exporter Sélection"
        else:
            export_text = "🎭 Exporter cet Acteur"
        
        ttk.Button(button_frame, text=export_text, 
                  command=self.export_selected).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="🚫 Annuler", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
    
    def refresh_actors(self):
        """Rafraîchit la liste des acteurs."""
        # Vider la liste
        for item in self.actors_tree.get_children():
            self.actors_tree.delete(item)
        
        self.selected_exports.clear()
        
        # Charger les acteurs
        actors = self.actor_manager.list_actors()
        
        for actor in actors:
            cards = self.actor_manager.get_actor_cards(actor['id'])
            card_count = len(cards)
            
            # Ajouter à la liste
            item_id = self.actors_tree.insert("", "end", 
                                             text=actor['icon'],
                                             values=("☐", actor['name'], f"{card_count}", actor['description']))
            
            self.selected_exports[item_id] = {'actor_id': actor['id'], 'selected': False, 'actor': actor}
        
        # Bind pour toggle
        self.actors_tree.bind("<Button-1>", self.on_click)
    
    def on_click(self, event):
        """Gestionnaire de clic sur la liste."""
        item = self.actors_tree.identify('item', event.x, event.y)
        column = self.actors_tree.identify('column', event.x, event.y)
        
        if item and column == "#1":  # Colonne "select"
            self.toggle_selection(item)
    
    def toggle_selection(self, item_id):
        """Bascule la sélection d'un acteur."""
        if item_id in self.selected_exports:
            if self.single_actor_mode:
                # Mode single : désélectionner tous les autres
                for other_id in self.selected_exports:
                    self.selected_exports[other_id]['selected'] = False
                    values = list(self.actors_tree.item(other_id, 'values'))
                    values[0] = "☐"
                    self.actors_tree.item(other_id, values=values)
                
                # Sélectionner celui-ci
                self.selected_exports[item_id]['selected'] = True
                values = list(self.actors_tree.item(item_id, 'values'))
                values[0] = "☑"
                self.actors_tree.item(item_id, values=values)
            else:
                # Mode multiple : basculer la sélection
                current = self.selected_exports[item_id]['selected']
                self.selected_exports[item_id]['selected'] = not current
                
                # Mettre à jour l'affichage
                values = list(self.actors_tree.item(item_id, 'values'))
                values[0] = "☑" if not current else "☐"
                self.actors_tree.item(item_id, values=values)
    
    def select_all(self):
        """Sélectionne tous les acteurs."""
        for item_id in self.selected_exports:
            self.selected_exports[item_id]['selected'] = True
            values = list(self.actors_tree.item(item_id, 'values'))
            values[0] = "☑"
            self.actors_tree.item(item_id, values=values)
    
    def deselect_all(self):
        """Désélectionne tous les acteurs."""
        for item_id in self.selected_exports:
            self.selected_exports[item_id]['selected'] = False
            values = list(self.actors_tree.item(item_id, 'values'))
            values[0] = "☐"
            self.actors_tree.item(item_id, values=values)
    
    def export_selected(self):
        """Exporte les acteurs sélectionnés."""
        selected = [data for data in self.selected_exports.values() if data['selected']]
        
        if not selected:
            if self.single_actor_mode:
                messagebox.showwarning("Attention", "Veuillez sélectionner un acteur à exporter.")
            else:
                messagebox.showwarning("Attention", "Veuillez sélectionner au moins un acteur à exporter.")
            return
        
        from tkinter import filedialog
        from lib.actors import export_lua_for_actor
        from lib.database import CardRepo
        
        try:
            repo = CardRepo(self.db_path)
            
            if self.single_actor_mode:
                # Mode single : demander le nom du fichier
                data = selected[0]
                actor = data['actor']
                safe_name = actor['name'].lower().replace(' ', '_').replace('/', '_')
                initial_filename = f"cards_{safe_name}.lua"
                
                filepath = filedialog.asksaveasfilename(
                    title=f"Exporter les cartes de {actor['name']}",
                    initialfile=initial_filename,
                    defaultextension='.lua',
                    filetypes=[('Fichier Lua', '*.lua')]
                )
                
                if not filepath:
                    return
                
                # Effectuer l'export
                export_lua_for_actor(repo, self.actor_manager, data['actor_id'], filepath)
                messagebox.showinfo("Export Réussi", 
                                  f"Export terminé avec succès !\n\n"
                                  f"Fichier : {actor['icon']} {actor['name']}\n"
                                  f"Destination : {filepath}")
                
                self.window.destroy()
                
            else:
                # Mode multiple : demander le dossier de destination
                folder = filedialog.askdirectory(title="Choisir le dossier de destination")
                if not folder:
                    return
                
                exported_files = []
                
                for data in selected:
                    actor = data['actor']
                    actor_id = data['actor_id']
                    
                    # Nom de fichier sécurisé
                    safe_name = actor['name'].lower().replace(' ', '_').replace('/', '_')
                    filename = f"cards_{safe_name}.lua"
                    filepath = f"{folder}/{filename}"
                    
                    # Export
                    export_lua_for_actor(repo, self.actor_manager, actor_id, filepath)
                    exported_files.append(f"{actor['icon']} {actor['name']} → {filename}")
                
                # Message de succès
                files_text = "\n".join(exported_files)
                messagebox.showinfo("Export Réussi", 
                                  f"Export terminé avec succès !\n\n"
                                  f"Fichiers créés :\n{files_text}\n\n"
                                  f"Dossier : {folder}")
                
                self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export :\n{e}")

def open_actor_export_dialog(parent, db_path: str):
    """Ouvre le dialogue d'export par acteur."""
    ActorExportDialog(parent, db_path)
