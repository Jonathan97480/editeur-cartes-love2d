#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composants de l'interface utilisateur pour l'éditeur de cartes
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .config import (APP_TITLE, RARITY_LABELS, RARITY_FROM_LABEL, 
                     TYPE_LABELS, TYPE_FROM_LABEL, TYPE_ORDER, APP_SETTINGS)
from .database import Card, CardRepo
# from .lua_export import export_lua  # Ancien système SANS TextFormatting
# CORRECTION: Utiliser directement Love2DLuaExporter
def export_lua(repo, side, filepath):
    """Export avec Love2DLuaExporter - garantit TextFormatting"""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from lua_exporter_love2d import Love2DLuaExporter
    exporter = Love2DLuaExporter(repo)
    exporter.export_to_file(filepath)
    print(f"✅ Export Love2D avec TextFormatting: {filepath}")

from .utils import to_int, create_card_image, sanitize_filename

def get_available_actors():
    """Récupère la liste des acteurs disponibles pour les interfaces."""
    try:
        from .actors import ActorManager
        from .config import DB_FILE
        
        manager = ActorManager(DB_FILE)
        actors = manager.list_actors()
        
        # Retourner les noms des acteurs
        return [actor['name'] for actor in actors]
    except Exception as e:
        print(f"Erreur lors de la récupération des acteurs : {e}")
        # Fallback vers l'ancien système
        return ['Joueur', 'IA']

class CardForm(ttk.Frame):
    def __init__(self, master, repo: CardRepo, on_saved, **kw):
        super().__init__(master, **kw)
        self.repo = repo
        self.on_saved = on_saved
        self.current_id: int | None = None
        self.generated_image_path: str | None = None  # Chemin de l'image générée
        self.previous_rarity: str | None = None  # Pour tracker les changements de rareté
        self._build_ui()

    # ---------- Build Tabs ----------
    def _build_ui(self):
        pad = dict(padx=8, pady=4)
        # Ligne 1 : acteurs, nom, power, rareté
        row = ttk.Frame(self); row.pack(fill='x', **pad)
        
        # Sélection multiple d'acteurs
        actors_frame = ttk.LabelFrame(row, text="Acteurs (Ctrl+clic pour sélection multiple)", padding=5)
        actors_frame.pack(side='left', padx=(0,12), fill='y')
        
        available_actors = get_available_actors()
        self.actors_listbox = tk.Listbox(actors_frame, height=3, width=15, selectmode='extended')
        self.actors_listbox.pack(side='left')
        
        # Ajouter une scrollbar pour la liste des acteurs
        actors_scrollbar = ttk.Scrollbar(actors_frame, orient='vertical', command=self.actors_listbox.yview)
        actors_scrollbar.pack(side='right', fill='y')
        self.actors_listbox.config(yscrollcommand=actors_scrollbar.set)
        
        # Remplir la liste des acteurs
        for actor in available_actors:
            self.actors_listbox.insert('end', actor)
        
        # Sélectionner 'Joueur' par défaut s'il existe
        try:
            joueur_index = available_actors.index('Joueur')
            self.actors_listbox.selection_set(joueur_index)
        except ValueError:
            # Si 'Joueur' n'existe pas, sélectionner le premier
            if available_actors:
                self.actors_listbox.selection_set(0)
        
        # Conteneur pour nom, power, rareté
        info_frame = ttk.Frame(row)
        info_frame.pack(side='left', fill='x', expand=True)

        # Conteneur pour nom, power, rareté
        info_frame = ttk.Frame(row)
        info_frame.pack(side='left', fill='x', expand=True)

        ttk.Label(info_frame, text="Nom de la carte :").pack(side='left', padx=(0,4))
        self.name_var = tk.StringVar(); ttk.Entry(info_frame, textvariable=self.name_var, width=25).pack(side='left', padx=(0,8))

        ttk.Label(info_frame, text="Coût (PowerBlow) :").pack(side='left', padx=(8,4))
        self.power_var = tk.IntVar(value=0)
        ttk.Spinbox(info_frame, from_=0, to=999, textvariable=self.power_var, width=6).pack(side='left', padx=(0,8))

        ttk.Label(info_frame, text="Rareté :").pack(side='left', padx=(8,4))
        self.rarity_var = tk.StringVar(value='Commun')
        ttk.Combobox(info_frame, textvariable=self.rarity_var, values=['Commun','Rare','Légendaire','Mythique'], width=12, state='readonly').pack(side='left')

        # Ligne 2 : illustration (chemin) + bouton
        r2 = ttk.Frame(self); r2.pack(fill='x', **pad)
        ttk.Label(r2, text="Illustration (chemin) :").pack(side='left')
        self.img_var = tk.StringVar()
        ttk.Entry(r2, textvariable=self.img_var).pack(side='left', fill='x', expand=True, padx=6)
        ttk.Button(r2, text="Parcourir…", command=self._browse_img).pack(side='left')

        # Description
        ttk.Label(self, text="Description (utilisez \\n pour nouvelle ligne) :").pack(anchor='w', **pad)
        self.desc_txt = tk.Text(self, height=5, wrap='word'); self.desc_txt.pack(fill='x', padx=8)
        self.desc_txt.configure(font=('TkFixedFont', 10))

        # Notebook : Héros / Ennemi / Types&Image / Action
        nb = ttk.Notebook(self); nb.pack(fill='both', expand=True, **pad)
        nb.add(self._tab_hero(), text='Effets Héros')
        nb.add(self._tab_enemy(), text='Effets Ennemi')
        nb.add(self._tab_types_image(), text='Types & Image')
        nb.add(self._tab_action(), text='Action (Lua)')

        # Boutons bas
        b = ttk.Frame(self); b.pack(fill='x', **pad)
        ttk.Button(b, text="🆕Nouveau", command=self.clear_form, width=12).pack(side='left', padx=(0,5))
        ttk.Button(b, text="💾Sauvegarder", command=self.save, width=14).pack(side='left', padx=(0,5))
        ttk.Button(b, text="🎨Format Text", command=self.open_text_formatter, width=14).pack(side='left', padx=(0,5))
        ttk.Button(b, text="🗑️Supprimer", command=self.delete_current, width=14).pack(side='left')

    def _tab_hero(self):
        c = ttk.Frame(self)
        pad = dict(padx=10, pady=6)
        
        # Variables pour tous les champs héros
        self.h_heal = tk.IntVar(value=0)
        self.h_shield = tk.IntVar(value=0)
        self.h_epine = tk.IntVar(value=0)
        self.h_attack = tk.IntVar(value=0)
        self.h_areduc = tk.IntVar(value=0)
        self.h_shield_pass = tk.IntVar(value=0)
        self.h_chpass = tk.IntVar(value=0)
        self.h_energy_cost = tk.IntVar(value=0)
        self.h_energy_decrease = tk.IntVar(value=0)
        self.h_b_value = tk.IntVar(value=0)
        self.h_b_turns = tk.IntVar(value=0)
        self.h_f_value = tk.IntVar(value=0)
        self.h_f_turns = tk.IntVar(value=0)

        labels = [
            ("Soin (heal)", self.h_heal),
            ("Bouclier (shield)", self.h_shield),
            ("Épine (Epine)", self.h_epine),
            ("Dégâts (attack)", self.h_attack),
            ("Réduc. attaque (%)", self.h_areduc),
            ("Ignore bouclier (0/1)", self.h_shield_pass),
            ("% passer le tour", self.h_chpass),
            ("Augmente coût énergie", self.h_energy_cost),
            ("Réduit coût énergie", self.h_energy_decrease),
            ("Saignement valeur", self.h_b_value),
            ("Saignement tours", self.h_b_turns),
            ("Dégâts augmentés valeur", self.h_f_value),
            ("Dégâts augmentés tours", self.h_f_turns),
        ]
        
        for i, (txt, var) in enumerate(labels):
            ttk.Label(c, text=txt).grid(row=i, column=0, sticky='w', **pad)
            ttk.Spinbox(c, from_=0, to=999, textvariable=var, width=8).grid(row=i, column=1, **pad)
        
        for i in range(2): c.grid_columnconfigure(i, weight=1)
        return c

    def _tab_enemy(self):
        c = ttk.Frame(self)
        pad = dict(padx=10, pady=6)
        
        # Variables pour tous les champs ennemi
        self.e_heal = tk.IntVar(value=0)
        self.e_attack = tk.IntVar(value=0)
        self.e_areduc = tk.IntVar(value=0)
        self.e_epine = tk.IntVar(value=0)
        self.e_shield = tk.IntVar(value=0)
        self.e_shield_pass = tk.IntVar(value=0)
        self.e_chpass = tk.IntVar(value=0)
        self.e_energy_cost = tk.IntVar(value=0)
        self.e_energy_decrease = tk.IntVar(value=0)
        self.e_b_value = tk.IntVar(value=0)
        self.e_b_turns = tk.IntVar(value=0)
        self.e_f_value = tk.IntVar(value=0)
        self.e_f_turns = tk.IntVar(value=0)

        labels = [
            ("Soin (heal)", self.e_heal),
            ("Dégâts (attack)", self.e_attack),
            ("Réduc. attaque (%)", self.e_areduc),
            ("Épine (Epine)", self.e_epine),
            ("Bouclier (shield)", self.e_shield),
            ("Ignore bouclier (0/1)", self.e_shield_pass),
            ("% passer le tour", self.e_chpass),
            ("Augmente coût énergie", self.e_energy_cost),
            ("Réduit coût énergie", self.e_energy_decrease),
            ("Saignement valeur", self.e_b_value),
            ("Saignement tours", self.e_b_turns),
            ("Dégâts augmentés valeur", self.e_f_value),
            ("Dégâts augmentés tours", self.e_f_turns),
        ]
        
        for i, (txt, var) in enumerate(labels):
            ttk.Label(c, text=txt).grid(row=i, column=0, sticky='w', **pad)
            ttk.Spinbox(c, from_=0, to=999, textvariable=var, width=8).grid(row=i, column=1, **pad)
        
        for i in range(2): c.grid_columnconfigure(i, weight=1)
        return c

    def _tab_types_image(self):
        c = ttk.Frame(self); pad = dict(padx=10, pady=6)
        # Types (checkbox)
        types_frame = ttk.LabelFrame(c, text='Types de carte')
        types_frame.pack(fill='x', padx=10, pady=6)
        self.type_vars = {}
        row = 0; col = 0
        for key in TYPE_ORDER:
            var = tk.BooleanVar(value=False); self.type_vars[key] = var
            ttk.Checkbutton(types_frame, text=TYPE_LABELS[key], variable=var).grid(row=row, column=col, sticky='w', padx=8, pady=4)
            col += 1
            if col >= 3: col = 0; row += 1
        for i in range(3): types_frame.grid_columnconfigure(i, weight=1)

        # Aperçu image
        prev_group = ttk.LabelFrame(c, text="Aperçu de l'image")
        prev_group.pack(fill='both', expand=True, padx=10, pady=6)
        
        # Frame pour les contrôles d'aperçu
        preview_controls = ttk.Frame(prev_group)
        preview_controls.pack(fill='x', pady=(5, 0))
        
        # Indicateur du type d'image
        self.image_type_label = ttk.Label(preview_controls, text="", 
                                         font=('TkDefaultFont', 8), 
                                         foreground='blue')
        self.image_type_label.pack(side='left')
        
        # Bouton pour basculer entre les images
        self.toggle_image_btn = ttk.Button(preview_controls, text="Voir original", 
                                          command=self._toggle_preview_image, width=12)
        self.toggle_image_btn.pack(side='right')
        self.show_generated = True  # Par défaut, montrer l'image générée si disponible
        
        self.preview_label = ttk.Label(prev_group, anchor='center')
        self.preview_label.pack(fill='both', expand=True, padx=10, pady=10)
        self._preview_img = None
        self.img_var.trace_add('write', lambda *_: self._update_preview())
        self._update_preview()
        return c

    def _update_preview(self):
        # Définir les chemins disponibles
        current_img_path = None
        generated_path = getattr(self, 'generated_image_path', None)
        
        try:
            current_img_path = self.img_var.get().strip()
        except Exception:
            current_img_path = ''
        
        # Résoudre le chemin relatif en absolu pour les vérifications d'existence
        from .utils import resolve_relative_path
        resolved_img_path = resolve_relative_path(current_img_path) if current_img_path else ''
        
        # Déterminer si l'image actuelle est fusionnée ou originale
        is_fused_image = False
        if current_img_path:
            # Une image est considérée comme fusionnée si elle est dans le dossier cards/
            is_fused_image = ("cards/" in current_img_path or 
                            os.path.sep + "cards" + os.path.sep in current_img_path or
                            current_img_path.endswith(os.path.join("cards", os.path.basename(current_img_path))))
        
        # Si on a une image fusionnée chargée depuis la base, l'utiliser comme image générée
        if is_fused_image and not generated_path:
            generated_path = current_img_path
            self.generated_image_path = current_img_path
        
        # Chercher l'image originale correspondante
        original_path = None
        if current_img_path and os.path.exists(resolved_img_path):
            if is_fused_image:
                # Chercher l'image originale correspondante
                from .utils import ensure_images_subfolders
                subfolders = ensure_images_subfolders()
                filename = os.path.basename(resolved_img_path)
                potential_original = os.path.join(subfolders['originals'], filename)
                if os.path.exists(potential_original):
                    original_path = potential_original
                else:
                    # Si pas d'original trouvé, utiliser l'image fusionnée comme original pour l'affichage
                    original_path = resolved_img_path
            else:
                original_path = resolved_img_path
        
        # Résoudre aussi le chemin généré s'il existe
        resolved_generated_path = resolve_relative_path(generated_path) if generated_path else ''
        
        if generated_path and os.path.exists(resolved_generated_path):
            generated_path = generated_path
        else:
            generated_path = None
        
        # Choisir quelle image afficher selon le mode
        preview_path = None
        if hasattr(self, 'show_generated') and self.show_generated and generated_path:
            preview_path = resolve_relative_path(generated_path)
        elif original_path:
            preview_path = original_path
        elif generated_path:  # Fallback sur l'image générée si pas d'original
            preview_path = resolve_relative_path(generated_path)
        
        # Afficher l'image
        if not preview_path:
            self.preview_label.config(text="(aucune image)", image='')
            if hasattr(self, 'image_type_label'):
                self.image_type_label.config(text="")
            self._preview_img = None
            return
            
        try:
            img = tk.PhotoImage(file=preview_path)
        except Exception:
            self.preview_label.config(text="Aperçu non disponible (format non supporté sans Pillow)", image='')
            if hasattr(self, 'image_type_label'):
                self.image_type_label.config(text="")
            self._preview_img = None
            return
            
        max_w, max_h = 360, 220
        w, h = img.width(), img.height()
        factor = max(1, int(max(w / max_w, h / max_h)))
        if factor > 1:
            img = img.subsample(factor, factor)
        self._preview_img = img
        
        # Indiquer quel type d'image est affiché
        if preview_path and generated_path and preview_path == generated_path:
            image_type = "✅ Image finale avec template"
            type_color = 'green'
        elif preview_path and is_fused_image and preview_path == current_img_path:
            image_type = "✅ Image finale avec template"
            type_color = 'green'
        else:
            image_type = "📷 Image d'origine"
            type_color = 'blue'
            
        self.preview_label.config(image=self._preview_img, text='')
        if hasattr(self, 'image_type_label'):
            self.image_type_label.config(text=image_type, foreground=type_color)
        
        # Mettre à jour le bouton de basculement
        if hasattr(self, 'toggle_image_btn'):
            if preview_path and generated_path and preview_path == generated_path:
                # On affiche l'image finale, proposer de voir l'original
                if original_path and original_path != generated_path:
                    self.toggle_image_btn.config(text="Voir original", state='normal')
                else:
                    self.toggle_image_btn.config(text="Image unique", state='disabled')
            else:
                # On affiche l'original, proposer de voir la finale
                if generated_path and os.path.exists(resolved_generated_path):
                    self.toggle_image_btn.config(text="Voir finale", state='normal')
                else:
                    self.toggle_image_btn.config(text="Pas de finale", state='disabled')
    
    def _toggle_preview_image(self):
        """Bascule entre l'image d'origine et l'image générée."""
        if not hasattr(self, 'show_generated'):
            self.show_generated = True
        
        self.show_generated = not self.show_generated
        self._update_preview()

    def _tab_action(self):
        c = ttk.Frame(self)
        pad = dict(padx=10, pady=6)
        top = ttk.Frame(c); top.pack(fill='x', **pad)
        ttk.Label(top, text="Paramètre de la fonction action :").pack(side='left')
        self.param_var = tk.StringVar(value='(aucun)')
        ttk.Combobox(top, textvariable=self.param_var, values=['(aucun)', '_user'], width=10, state='readonly').pack(side='left', padx=6)

        self.action_txt = tk.Text(c, height=10, wrap='none')
        self.action_txt.configure(font=('TkFixedFont', 10))
        self.action_txt.pack(fill='both', expand=True, padx=10, pady=4)

        btns = ttk.Frame(c); btns.pack(fill='x', **pad)
        ttk.Button(btns, text="Insérer graveyardPioche('Nom')", command=lambda: self._insert_action("graveyardPioche('NomCarte')")).pack(side='left')
        ttk.Button(btns, text="Insérer findCard('Nom')", command=lambda: self._insert_action("findCard('NomCarte')")).pack(side='left', padx=6)
        return c

    def _insert_action(self, text: str):
        self.action_txt.insert('insert', text)

    def _browse_img(self):
        path = filedialog.askopenfilename(title="Choisir une image", filetypes=[
            ("Images", "*.png *.gif *.jpg *.jpeg *.webp *.bmp"), ("Tous les fichiers", "*.*")
        ])
        if path:
            # Copier l'image dans le dossier originals avec le nom de la carte
            card_name = self.name_var.get().strip() or "carte_sans_nom"
            from .utils import copy_image_to_originals, convert_to_relative_path
            
            # Copier l'image vers le dossier originals
            local_image_path = copy_image_to_originals(path, card_name)
            
            if local_image_path:
                # Convertir en chemin relatif pour la sauvegarde
                relative_path = convert_to_relative_path(local_image_path)
                self.img_var.set(relative_path)
                # Stocker comme image originale pour les futures fusions
                self._original_image_path = relative_path
                messagebox.showinfo("Image copiée", 
                    f"Image copiée dans :\n{local_image_path}\n\nChemin sauvegardé : {relative_path}")
            else:
                # En cas d'échec de copie, essayer de convertir le chemin original en relatif
                relative_path = convert_to_relative_path(path)
                self.img_var.set(relative_path)
                # Stocker comme image originale pour les futures fusions
                self._original_image_path = relative_path
                messagebox.showwarning("Copie échouée", 
                    f"La copie de l'image a échoué. Chemin sauvegardé : {relative_path}")
            
            self._update_preview()

    def _update_image_name_if_needed(self):
        """Met à jour le nom de l'image dans originals si le nom de la carte a changé."""
        current_image_path = self.img_var.get().strip()
        current_card_name = self.name_var.get().strip()
        
        if not current_image_path or not current_card_name:
            return
            
        # Vérifier si l'image est dans le dossier originals
        from .utils import ensure_images_subfolders, sanitize_filename
        subfolders = ensure_images_subfolders()
        
        if subfolders['originals'] in current_image_path:
            # Générer le nouveau nom de fichier basé sur le nom de carte actuel
            _, ext = os.path.splitext(current_image_path)
            new_filename = f"{sanitize_filename(current_card_name)}{ext}"
            new_path = os.path.join(subfolders['originals'], new_filename)
            
            # Renommer le fichier si nécessaire
            if current_image_path != new_path and os.path.exists(current_image_path):
                try:
                    import shutil
                    shutil.move(current_image_path, new_path)
                    self.img_var.set(new_path.replace('\\', '/'))
                    self._update_preview()
                except Exception as e:
                    print(f"Erreur lors du renommage de l'image : {e}")

    # ---------- Populate / Clear ----------
    def clear_form(self):
        self.current_id = None
        self.generated_image_path = None  # Réinitialiser l'image générée
        self.previous_rarity = None  # Réinitialiser le tracker de rareté
        self._original_image_path = None  # Réinitialiser l'image originale
        
        # Réinitialiser la sélection des acteurs
        self.actors_listbox.selection_clear(0, 'end')
        available_actors = get_available_actors()
        try:
            joueur_index = available_actors.index('Joueur')
            self.actors_listbox.selection_set(joueur_index)
            print("✅ Acteur 'Joueur' sélectionné par défaut")
        except ValueError:
            if available_actors:
                self.actors_listbox.selection_set(0)
                print(f"✅ Premier acteur sélectionné par défaut : {available_actors[0]}")
            else:
                print("⚠️ Aucun acteur disponible")
        
        self.name_var.set('')
        self.img_var.set('')
        self.desc_txt.delete('1.0', 'end')
        self.power_var.set(0)
        self.rarity_var.set('Commun')
        self.previous_rarity = 'Commun'  # Initialiser le tracker
        
        # Tous les champs héros
        self.h_heal.set(0); self.h_shield.set(0); self.h_epine.set(0)
        self.h_attack.set(0); self.h_areduc.set(0); self.h_shield_pass.set(0)
        self.h_chpass.set(0); self.h_energy_cost.set(0); self.h_energy_decrease.set(0)
        self.h_b_value.set(0); self.h_b_turns.set(0)
        self.h_f_value.set(0); self.h_f_turns.set(0)
        
        # Tous les champs ennemi
        self.e_heal.set(0); self.e_attack.set(0); self.e_areduc.set(0); self.e_epine.set(0)
        self.e_shield.set(0); self.e_shield_pass.set(0); self.e_chpass.set(0)
        self.e_energy_cost.set(0); self.e_energy_decrease.set(0)
        self.e_b_value.set(0); self.e_b_turns.set(0)
        self.e_f_value.set(0); self.e_f_turns.set(0)
        
        # types
        if hasattr(self, 'type_vars'):
            for v in self.type_vars.values(): v.set(False)
        # action
        self.param_var.set('(aucun)')
        self.action_txt.delete('1.0', 'end')
        if callable(self.on_saved):
            self.on_saved()

    def _get_card_actors(self, card_id):
        """Récupère la liste des acteurs liés à cette carte."""
        try:
            from .actors import ActorManager
            from .config import DB_FILE
            
            manager = ActorManager(DB_FILE)
            actors = manager.get_card_actors(card_id)
            
            if actors:
                # Retourner les noms des acteurs liés
                return [actor['name'] for actor in actors]
            else:
                # Fallback : utiliser le système legacy side
                return ['Joueur']  # Valeur par défaut
                
        except Exception as e:
            print(f"Erreur lors de la récupération des acteurs : {e}")
            return ['Joueur']

    def load_card(self, card: Card):
        self.current_id = card.id
        self.generated_image_path = None  # Réinitialiser l'image générée lors du chargement
        
        # Récupérer les acteurs liés à cette carte
        actor_names = self._get_card_actors(card.id)
        
        # Sélectionner les acteurs dans la listbox
        self.actors_listbox.selection_clear(0, 'end')
        available_actors = get_available_actors()
        
        for actor_name in actor_names:
            try:
                actor_index = available_actors.index(actor_name)
                self.actors_listbox.selection_set(actor_index)
            except ValueError:
                print(f"Acteur '{actor_name}' non trouvé dans la liste disponible")
        
        self.name_var.set(card.name)
        self.img_var.set(card.img)
        
        # Stocker l'image originale pour la fusion
        self._original_image_path = getattr(card, 'original_img', card.img)
        
        self.desc_txt.delete('1.0', 'end'); self.desc_txt.insert('1.0', card.description)
        self.power_var.set(int(card.powerblow))
        
        # Charger la rareté et tracker l'ancienne valeur
        current_rarity = RARITY_LABELS.get(getattr(card, 'rarity', 'commun'), 'Commun')
        self.rarity_var.set(current_rarity)
        self.previous_rarity = current_rarity  # Tracker pour détecter les changements
        
        # Tous les champs héros
        self.h_heal.set(to_int(card.hero.get('heal', 0)))
        self.h_shield.set(to_int(card.hero.get('shield', 0)))
        self.h_epine.set(to_int(card.hero.get('Epine', 0)))
        self.h_attack.set(to_int(card.hero.get('attack', 0)))
        self.h_areduc.set(to_int(card.hero.get('AttackReduction', 0)))
        self.h_shield_pass.set(to_int(card.hero.get('shield_pass', 0)))
        self.h_chpass.set(to_int(card.hero.get('chancePassedTour', 0)))
        self.h_energy_cost.set(to_int(card.hero.get('energyCostIncrease', 0)))
        self.h_energy_decrease.set(to_int(card.hero.get('energyCostDecrease', 0)))
        h_b = card.hero.get('bleeding', {}) or {}
        self.h_b_value.set(to_int(h_b.get('value', 0)))
        self.h_b_turns.set(to_int(h_b.get('number_turns', 0)))
        h_f = card.hero.get('force_augmented', {}) or {}
        self.h_f_value.set(to_int(h_f.get('value', 0)))
        self.h_f_turns.set(to_int(h_f.get('number_turns', 0)))
        
        # Tous les champs ennemi
        self.e_heal.set(to_int(card.enemy.get('heal', 0)))
        self.e_attack.set(to_int(card.enemy.get('attack', 0)))
        self.e_areduc.set(to_int(card.enemy.get('AttackReduction', 0)))
        self.e_epine.set(to_int(card.enemy.get('Epine', 0)))
        self.e_shield.set(to_int(card.enemy.get('shield', 0)))
        self.e_shield_pass.set(to_int(card.enemy.get('shield_pass', 0)))
        self.e_chpass.set(to_int(card.enemy.get('chancePassedTour', 0)))
        self.e_energy_cost.set(to_int(card.enemy.get('energyCostIncrease', 0)))
        self.e_energy_decrease.set(to_int(card.enemy.get('energyCostDecrease', 0)))
        e_b = card.enemy.get('bleeding', {}) or {}
        self.e_b_value.set(to_int(e_b.get('value', 0)))
        self.e_b_turns.set(to_int(e_b.get('number_turns', 0)))
        e_f = card.enemy.get('force_augmented', {}) or {}
        self.e_f_value.set(to_int(e_f.get('value', 0)))
        self.e_f_turns.set(to_int(e_f.get('number_turns', 0)))
        
        # types
        if hasattr(self, 'type_vars'):
            for k, v in self.type_vars.items():
                v.set(k in (card.types or []))
        # action
        self.param_var.set('(aucun)' if not card.action_param else '_user')
        self.action_txt.delete('1.0', 'end'); self.action_txt.insert('1.0', card.action)

    def _form_to_card(self) -> Card:
        c = Card()
        c.id = self.current_id
        
        # Récupérer les acteurs sélectionnés pour déterminer le side (compatibilité legacy)
        selected_actors = self._get_selected_actors()
        if 'Joueur' in selected_actors:
            c.side = 'joueur'
        elif 'IA' in selected_actors:
            c.side = 'ia'
        else:
            c.side = 'joueur'  # Par défaut
            
        c.name = self.name_var.get().strip()
        c.img = self.img_var.get().strip()
        # Gérer l'image originale
        c.original_img = getattr(self, '_original_image_path', c.img)
        c.description = self.desc_txt.get('1.0', 'end').rstrip('\n').strip()
        c.powerblow = int(self.power_var.get())
        c.rarity = RARITY_FROM_LABEL.get(self.rarity_var.get(), 'commun')
        
        # Tous les champs héros
        c.hero = {
            "heal": int(self.h_heal.get()),
            "shield": int(self.h_shield.get()),
            "Epine": int(self.h_epine.get()),
            "attack": int(self.h_attack.get()),
            "AttackReduction": int(self.h_areduc.get()),
            "shield_pass": int(self.h_shield_pass.get()),
            "bleeding": {"value": int(self.h_b_value.get()), "number_turns": int(self.h_b_turns.get())},
            "force_augmented": {"value": int(self.h_f_value.get()), "number_turns": int(self.h_f_turns.get())},
            "chancePassedTour": int(self.h_chpass.get()),
            "energyCostIncrease": int(self.h_energy_cost.get()),
            "energyCostDecrease": int(self.h_energy_decrease.get())
        }
        
        # Tous les champs ennemi
        c.enemy = {
            "heal": int(self.e_heal.get()),
            "attack": int(self.e_attack.get()),
            "AttackReduction": int(self.e_areduc.get()),
            "Epine": int(self.e_epine.get()),
            "shield": int(self.e_shield.get()),
            "shield_pass": int(self.e_shield_pass.get()),
            "bleeding": {"value": int(self.e_b_value.get()), "number_turns": int(self.e_b_turns.get())},
            "force_augmented": {"value": int(self.e_f_value.get()), "number_turns": int(self.e_f_turns.get())},
            "chancePassedTour": int(self.e_chpass.get()),
            "energyCostIncrease": int(self.e_energy_cost.get()),
            "energyCostDecrease": int(self.e_energy_decrease.get())
        }
        
        c.action_param = '' if self.param_var.get() == '(aucun)' else '_user'
        c.action = self.action_txt.get('1.0', 'end').rstrip('\n')
        # types
        if hasattr(self, 'type_vars'):
            c.types = [k for k, var in self.type_vars.items() if bool(var.get())]
        return c

    def _get_selected_actors(self):
        """Récupère la liste des acteurs sélectionnés dans la listbox."""
        selected_indices = self.actors_listbox.curselection()
        available_actors = get_available_actors()
        return [available_actors[i] for i in selected_indices if i < len(available_actors)]

    # ---------- Commands ----------
    def _update_actor_linkage(self, card_id):
        """Met à jour la liaison entre la carte et les acteurs sélectionnés."""
        try:
            from .actors import ActorManager
            from .config import DB_FILE
            
            manager = ActorManager(DB_FILE)
            selected_actor_names = self._get_selected_actors()
            
            # Supprimer toutes les anciennes liaisons de cette carte
            all_actors = manager.list_actors()
            for actor in all_actors:
                manager.unlink_card_from_actor(card_id, actor['id'])
            
            # Créer les nouvelles liaisons pour chaque acteur sélectionné
            for actor_name in selected_actor_names:
                # Trouver l'ID de l'acteur sélectionné
                selected_actor_id = None
                for actor in all_actors:
                    if actor['name'] == actor_name:
                        selected_actor_id = actor['id']
                        break
                
                if selected_actor_id:
                    manager.link_card_to_actor(card_id, selected_actor_id)
                    print(f"✅ Carte {card_id} liée à l'acteur '{actor_name}'")
            
            if selected_actor_names:
                print(f"🎯 Carte {card_id} maintenant liée à {len(selected_actor_names)} acteur(s)")
            
        except Exception as e:
            print(f"Erreur lors de la liaison avec les acteurs : {e}")

    def save(self):
        # Mettre à jour le nom de l'image si nécessaire avant la sauvegarde
        self._update_image_name_if_needed()
        
        c = self._form_to_card()
        # validations minimales
        if not c.name:
            messagebox.showwarning(APP_TITLE, "Le nom de la carte est requis.")
            return
        if not c.img:
            messagebox.showwarning(APP_TITLE, "Le chemin d'illustration est requis.")
            return
        if not c.description:
            messagebox.showwarning(APP_TITLE, "La description est requise.")
            return
        
        # Sauvegarde en base
        if c.id is None:
            new_id = self.repo.insert(c); self.current_id = new_id
        else:
            self.repo.update(c)
        
        # Gérer la liaison avec l'acteur sélectionné
        self._update_actor_linkage(c.id if c.id else self.current_id)
        
        # Détecter si la rareté a changé
        current_rarity = self.rarity_var.get()
        rarity_changed = (self.previous_rarity is not None and 
                         self.previous_rarity != current_rarity)
        
        if rarity_changed:
            print(f"🔄 Changement de rareté détecté : {self.previous_rarity} → {current_rarity}")
        
        # Génère l'image fusionnée si possible
        old_image_path = c.img  # Sauvegarder l'ancien chemin pour nettoyage si nécessaire
        generated_image = self.generate_card_image()
        if generated_image:
            self.generated_image_path = generated_image
            # Mettre à jour le chemin de l'image en base de données
            c.img = generated_image.replace('\\', '/')
            self.repo.update(c)
            # Actualiser l'aperçu pour montrer l'image générée
            self._update_preview()
            
            # Valider que l'image a été correctement mise à jour après changement de rareté
            if rarity_changed:
                if self.validate_image_after_rarity_change(
                    self.previous_rarity or 'Commun', 
                    current_rarity, 
                    c.name
                ):
                    print(f"✅ Image fusionnée mise à jour avec succès pour la nouvelle rareté")
                else:
                    print(f"⚠️ Problème détecté lors de la mise à jour de l'image fusionnée")
            
        elif old_image_path and old_image_path.startswith('images/cards/'):
            # Si la génération échoue mais qu'on avait une image fusionnée avant,
            # on garde l'ancienne référence mais on avertit l'utilisateur
            print(f"⚠️ Impossible de générer la nouvelle image fusionnée pour la rareté {current_rarity}")
            print(f"   L'ancienne image fusionnée est conservée : {old_image_path}")
            
            if rarity_changed:
                messagebox.showwarning(
                    APP_TITLE, 
                    f"Attention !\n\nLa rareté a été changée de '{self.previous_rarity}' vers '{current_rarity}', "
                    f"mais l'image fusionnée n'a pas pu être mise à jour.\n\n"
                    f"Vérifiez la configuration des templates de rareté dans les paramètres."
                )
        
        # Mettre à jour le tracker de rareté
        self.previous_rarity = current_rarity
        
        if callable(self.on_saved):
            self.on_saved()
        
        success_msg = "Carte enregistrée avec succès !"
        if generated_image:
            success_msg += f"\nImage générée : {os.path.basename(generated_image)}"
        
        messagebox.showinfo(APP_TITLE, success_msg)

    def delete_current(self):
        if self.current_id is None:
            messagebox.showinfo(APP_TITLE, "Aucune carte sélectionnée.")
            return
        if messagebox.askyesno(APP_TITLE, "Supprimer cette carte ?"):
            self.repo.delete(self.current_id)
            self.clear_form()
            if callable(self.on_saved):
                self.on_saved()

    def open_text_formatter(self):
        """Ouvre l'éditeur de formatage de texte"""
        if self.current_id is None:
            # Proposer de sauvegarder d'abord
            if messagebox.askyesno(APP_TITLE, 
                "Vous devez sauvegarder la carte avant de formater le texte.\n"
                "Voulez-vous sauvegarder maintenant ?"):
                self.save()
                if self.current_id is None:  # Si la sauvegarde a échoué
                    return
            else:
                return
        
        # Récupérer les données actuelles de la carte
        card = self.repo.get(self.current_id)
        if not card:
            messagebox.showerror(APP_TITLE, "Erreur : impossible de récupérer les données de la carte.")
            return
        
        # Ouvrir l'éditeur de formatage
        try:
            # Utiliser le système principal unifié
            from .text_formatting_editor import TextFormattingEditor
            import sqlite3
            
            # Récupérer les données de formatage depuis la base principale
            conn = sqlite3.connect(self.repo.db_file)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT title_x, title_y, title_font, title_size, title_color,
                       text_x, text_y, text_width, text_height, text_font,
                       text_size, text_color, text_align, line_spacing, text_wrap
                FROM cards WHERE id = ?
            """, (self.current_id,))
            
            formatting_data = cursor.fetchone()
            conn.close()
            
            if formatting_data:
                # Adapter les données pour l'éditeur
                card_data = {
                    'id': self.current_id,
                    'nom': card.name,
                    'description': card.description,
                    'img': card.img,
                    'title_x': formatting_data[0] or 50,
                    'title_y': formatting_data[1] or 30,
                    'title_font': formatting_data[2] or 'Arial',
                    'title_size': formatting_data[3] or 16,
                    'title_color': formatting_data[4] or '#000000',
                    'text_x': formatting_data[5] or 50,
                    'text_y': formatting_data[6] or 100,
                    'text_width': formatting_data[7] or 200,
                    'text_height': formatting_data[8] or 150,
                    'text_font': formatting_data[9] or 'Arial',
                    'text_size': formatting_data[10] or 12,
                    'text_color': formatting_data[11] or '#000000',
                    'text_align': formatting_data[12] or 'left',
                    'line_spacing': formatting_data[13] or 1.2,
                    'text_wrap': bool(formatting_data[14]) if formatting_data[14] is not None else True
                }
            else:
                # Données par défaut si pas de formatage
                card_data = {
                    'id': self.current_id,
                    'nom': card.name,
                    'description': card.description,
                    'img': card.img,
                    'title_x': 50, 'title_y': 30, 'title_font': 'Arial', 'title_size': 16, 'title_color': '#000000',
                    'text_x': 50, 'text_y': 100, 'text_width': 200, 'text_height': 150, 'text_font': 'Arial',
                    'text_size': 12, 'text_color': '#000000', 'text_align': 'left', 'line_spacing': 1.2, 'text_wrap': True
                }
            
            # Créer un repo de formatage personnalisé
            class FormattingRepo:
                def __init__(self, main_repo):
                    self.main_repo = main_repo
                
                def get_card(self, card_id):
                    # Retourner une pseudo-carte avec les bonnes données
                    card = self.main_repo.get(card_id)
                    if card:
                        # Simuler l'objet database_simple Card
                        class FormattingCard:
                            pass
                        
                        fc = FormattingCard()
                        fc.id = card.id
                        fc.nom = card.name
                        fc.description = card.description
                        fc.img = card.img
                        return fc
                    return None
                
                def save_card(self, card_data):
                    # Sauvegarder dans le système principal
                    conn = sqlite3.connect(self.main_repo.db_file)
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        UPDATE cards SET 
                            title_x=?, title_y=?, title_font=?, title_size=?, title_color=?,
                            text_x=?, text_y=?, text_width=?, text_height=?, text_font=?,
                            text_size=?, text_color=?, text_align=?, line_spacing=?, text_wrap=?
                        WHERE id=?
                    """, (
                        card_data.title_x, card_data.title_y, card_data.title_font,
                        card_data.title_size, card_data.title_color,
                        card_data.text_x, card_data.text_y, card_data.text_width,
                        card_data.text_height, card_data.text_font, card_data.text_size,
                        card_data.text_color, card_data.text_align, card_data.line_spacing,
                        int(card_data.text_wrap), card_data.id
                    ))
                    
                    conn.commit()
                    conn.close()
            
            formatting_repo = FormattingRepo(self.repo)
            
            # Créer l'éditeur avec le repo personnalisé
            editor = TextFormattingEditor(self.winfo_toplevel(), self.current_id, card_data, formatting_repo)
            
            # Rafraîchir les données après fermeture de l'éditeur
            if callable(self.on_saved):
                self.on_saved()
                
        except ImportError as e:
            messagebox.showerror(APP_TITLE, f"Erreur : Impossible de charger l'éditeur de formatage.\n{e}")
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Erreur : {e}")

    # ---------- Card Image Generation ----------
    def generate_card_image(self):
        """Génère l'image fusionnée de la carte selon sa rareté."""
        # Utiliser l'image originale pour la fusion, pas l'image actuelle qui peut être déjà fusionnée
        original_image_path = getattr(self, '_original_image_path', None) or self.img_var.get().strip()
        
        if not original_image_path:
            return None
        
        card_name = self.name_var.get().strip() or "carte_sans_nom"
        
        # Récupérer la rareté de la carte
        rarity_label = self.rarity_var.get()
        from .config import RARITY_FROM_LABEL
        rarity_key = RARITY_FROM_LABEL.get(rarity_label, 'commun')
        
        # Récupérer le template pour cette rareté
        rarity_templates = APP_SETTINGS.get("rarity_templates", {})
        template_path = rarity_templates.get(rarity_key, "")
        
        # Si pas de template pour cette rareté, essayer le template par défaut (legacy)
        if not template_path:
            template_path = APP_SETTINGS.get("template_image", "")
        
        # Si toujours pas de template, retourner None
        if not template_path:
            print(f"⚠️ Aucun template trouvé pour la rareté '{rarity_label}' ({rarity_key})")
            return None
        
        print(f"🎨 Génération d'image fusionnée pour '{card_name}' (rareté: {rarity_label})")
        print(f"   📁 Image originale : {original_image_path}")
        print(f"   🎨 Template : {template_path}")
        
        return create_card_image(original_image_path, template_path, card_name)

    def validate_image_after_rarity_change(self, old_rarity: str, new_rarity: str, card_name: str) -> bool:
        """Valide que l'image a été correctement mise à jour après un changement de rareté."""
        if old_rarity == new_rarity:
            return True  # Pas de changement nécessaire
        
        expected_path = f"images/cards/{sanitize_filename(card_name)}.png"
        
        if not os.path.exists(expected_path):
            print(f"⚠️ Image attendue manquante après changement de rareté : {expected_path}")
            return False
        
        # Vérifier que l'image a été modifiée récemment (dans les 10 dernières secondes)
        import time
        file_mtime = os.path.getmtime(expected_path)
        time_diff = time.time() - file_mtime
        
        if time_diff > 10:  # Plus de 10 secondes
            print(f"⚠️ L'image n'a pas été mise à jour récemment (modifiée il y a {time_diff:.1f}s)")
            return False
        
        print(f"✅ Image validée pour la nouvelle rareté '{new_rarity}'")
        return True


class CardList(ttk.Frame):
    def __init__(self, master, repo: CardRepo, on_select, fixed_rarity_label: str | None = None, **kw):
        super().__init__(master, **kw)
        self.repo = repo
        self.on_select = on_select
        self.fixed_rarity_label = fixed_rarity_label  # Si défini, le tab est fixé sur cette rareté
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        pad = dict(padx=8, pady=6)
        top = ttk.Frame(self); top.pack(fill='x', **pad)
        ttk.Label(top, text='Acteur :').pack(side='left')
        self.side_filter = tk.StringVar(value='Tous')
        available_actors = ['Tous'] + get_available_actors()
        ttk.Combobox(top, textvariable=self.side_filter, values=available_actors, width=12, state='readonly').pack(side='left', padx=6)
        self.side_filter.trace_add('write', lambda *_: self.refresh())

        # Rareté (fixée par l'onglet ou modifiable)
        if self.fixed_rarity_label:
            ttk.Label(top, text=f"Rareté : {self.fixed_rarity_label}").pack(side='left', padx=(10,4))
            self.rarity_filter = None
        else:
            ttk.Label(top, text='Rareté :').pack(side='left', padx=(10,4))
            self.rarity_filter = tk.StringVar(value='Toutes')
            ttk.Combobox(top, textvariable=self.rarity_filter, values=['Toutes','Commun','Rare','Légendaire','Mythique'], width=12, state='readonly').pack(side='left')
            self.rarity_filter.trace_add('write', lambda *_: self.refresh())

        self.search_var = tk.StringVar()
        ent = ttk.Entry(top, textvariable=self.search_var); ent.pack(side='left', fill='x', expand=True, padx=6)
        self.search_var.trace_add('write', lambda *_: self.refresh())

        # Treeview
        cols = ('id','acteurs','rarete','nom','power','desc','maj')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=20)
        self.tree.heading('id', text='ID'); self.tree.column('id', width=50, anchor='center')
        self.tree.heading('acteurs', text='Acteurs'); self.tree.column('acteurs', width=120, anchor='center')
        self.tree.heading('rarete', text='Rareté'); self.tree.column('rarete', width=110, anchor='center')
        self.tree.heading('nom', text='Nom'); self.tree.column('nom', width=200)
        self.tree.heading('power', text='Power'); self.tree.column('power', width=60, anchor='center')
        self.tree.heading('desc', text='Description'); self.tree.column('desc', width=280)
        self.tree.heading('maj', text='MAJ'); self.tree.column('maj', width=140, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=8, pady=4)
        self.tree.bind('<Double-1>', self._on_double)

        # Exports
        exp = ttk.Frame(self); exp.pack(fill='x', **pad)
        ttk.Button(exp, text='🎭 Exporter Acteur', command=self.export_actor_selection).pack(side='left')
        ttk.Button(exp, text='📤 Exporter Tout', command=self.export_all_actors).pack(side='left', padx=6)
        ttk.Button(exp, text='🎮 Export Love2D+Format', command=self.export_love2d_with_formatting).pack(side='left', padx=6)
        ttk.Button(exp, text='📦 Package Complet', command=self.export_game_package).pack(side='left', padx=6)

    def _side_value(self):
        v = self.side_filter.get()
        if v == 'Joueur': return 'joueur'
        if v == 'IA': return 'ia'
        return None

    def _get_card_actors_display(self, card_id):
        """Récupère l'affichage des acteurs liés à une carte."""
        try:
            from .actors import ActorManager
            from .config import DB_FILE
            
            manager = ActorManager(DB_FILE)
            actors = manager.get_card_actors(card_id)
            
            if actors:
                # Si plusieurs acteurs, afficher le nombre
                if len(actors) == 1:
                    return actors[0]['name']
                else:
                    actor_names = [actor['name'] for actor in actors]
                    return f"{len(actors)} acteurs: {', '.join(actor_names[:2])}" + ("..." if len(actors) > 2 else "")
            else:
                # Fallback vers l'ancien système side
                return 'Aucun acteur'
                
        except Exception as e:
            print(f"Erreur lors de la récupération des acteurs pour la carte {card_id} : {e}")
            return 'Erreur acteurs'

    def refresh(self):
        side = self._side_value()
        text = self.search_var.get().strip() or None
        if self.fixed_rarity_label:
            rarity = RARITY_FROM_LABEL.get(self.fixed_rarity_label)
        else:
            rarity_label = self.rarity_filter.get() if self.rarity_filter else 'Toutes'
            rarity = RARITY_FROM_LABEL.get(rarity_label) if rarity_label != 'Toutes' else None
        
        # Obtenir toutes les cartes (sans filtre side pour l'instant)
        cards = self.repo.list_cards(side=None, search_text=text, rarity=rarity)
        
        # Filtrer par acteur si nécessaire
        if side:
            filtered_cards = []
            try:
                from .actors import ActorManager
                from .config import DB_FILE
                
                manager = ActorManager(DB_FILE)
                
                for card in cards:
                    card_actors = manager.get_card_actors(card.id)
                    
                    # Vérifier si la carte a l'acteur recherché
                    if side == 'joueur':
                        has_joueur = any(actor['name'] == 'Joueur' for actor in card_actors)
                        if has_joueur:
                            filtered_cards.append(card)
                    elif side == 'ia':
                        has_ia = any(actor['name'] == 'IA' for actor in card_actors)
                        if has_ia:
                            filtered_cards.append(card)
                
                cards = filtered_cards
                
            except Exception as e:
                print(f"Erreur filtrage par acteur : {e}")
                # Fallback vers l'ancien système
                cards = self.repo.list_cards(side=side, search_text=text, rarity=rarity)
        
        # Afficher les cartes avec leurs acteurs
        for i in self.tree.get_children(): 
            self.tree.delete(i)
            
        for c in cards:
            maj = c.updated_at.split('T')[0] if c.updated_at else ''
            
            # Obtenir l'affichage des acteurs pour cette carte
            actors_display = self._get_card_actors_display(c.id)
            
            self.tree.insert('', 'end', values=(
                c.id,
                actors_display,  # Remplacer l'ancien système Joueur/IA
                RARITY_LABELS.get(getattr(c,'rarity','commun'),'Commun'),
                c.name,
                c.powerblow,
                (c.description or '')[:80],
                maj
            ))

    def _on_double(self, _event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], 'values')
        try:
            card_id = int(vals[0])
        except Exception:
            return
        if callable(self.on_select):
            self.on_select(card_id)

    def export_side(self, side: str):
        default_name = 'cards_player.lua' if side == 'joueur' else 'cards_ai.lua'
        path = filedialog.asksaveasfilename(title='Emplacement du fichier LUA', initialfile=default_name, defaultextension='.lua', filetypes=[('Fichier Lua','*.lua')])
        if not path: return
        try:
            export_lua(self.repo, side, path)
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Échec export : {e}")
            return
        messagebox.showinfo(APP_TITLE, f"Export réussi :\n{path}")

    def export_both(self):
        folder = filedialog.askdirectory(title="Choisir un dossier pour l'export")
        if not folder: return
        p1 = os.path.join(folder, 'cards_player.lua')
        p2 = os.path.join(folder, 'cards_ai.lua')
        try:
            export_lua(self.repo, 'joueur', p1)
            export_lua(self.repo, 'ia', p2)
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Échec export : {e}")
            return
        messagebox.showinfo(APP_TITLE, f"Exports réussis :\n- {p1}\n- {p2}")

    def export_actor_selection(self):
        """Ouvre un dialogue pour sélectionner un acteur spécifique à exporter."""
        try:
            from .actor_selector import ActorExportDialog
            from .config import DB_FILE
            from .actors import ActorManager
            
            # Créer le gestionnaire d'acteurs
            db_path = DB_FILE
            actor_manager = ActorManager(db_path)
            
            # Ouvrir le dialogue de sélection d'acteur unique
            dialog = ActorExportDialog(
                parent=self,
                db_path=db_path,
                actor_manager=actor_manager,
                single_actor_mode=True
            )
            
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Erreur lors de l'ouverture de la sélection d'acteur :\n{e}")
    
    def export_all_actors(self):
        """Exporte tous les acteurs en un seul fichier."""
        try:
            from .actors import ActorManager, export_all_actors_lua
            from .config import DB_FILE
            
            # Créer le gestionnaire d'acteurs  
            db_path = DB_FILE
            actor_manager = ActorManager(db_path)
            
            # Demander le fichier de destination
            filepath = filedialog.asksaveasfilename(
                title='Export de tous les acteurs',
                initialfile='cards_all_actors.lua',
                defaultextension='.lua',
                filetypes=[('Fichier Lua', '*.lua')]
            )
            
            if not filepath:
                return
            
            # Effectuer l'export
            export_all_actors_lua(self.repo, actor_manager, filepath)
            messagebox.showinfo(APP_TITLE, f"Export réussi :\n{filepath}")
            
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Erreur lors de l'export de tous les acteurs :\n{e}")

    def export_love2d_with_formatting(self):
        """Exporte toutes les cartes au format Love2D avec formatage de texte."""
        try:
            # Import du nouvel exporteur
            from lua_exporter_love2d import Love2DLuaExporter
            
            # Demander le fichier de destination
            filepath = filedialog.asksaveasfilename(
                title='Export Love2D avec formatage',
                initialfile='cards_joueur_with_formatting.lua',
                defaultextension='.lua',
                filetypes=[('Fichier Lua', '*.lua')]
            )
            
            if not filepath:
                return
            
            # Créer l'exporteur et effectuer l'export
            exporter = Love2DLuaExporter(self.repo)
            size = exporter.export_to_file(filepath)
            
            # Compter les cartes exportées
            cards = self.repo.list_cards()
            card_count = len(cards)
            
            messagebox.showinfo(
                APP_TITLE, 
                f"Export Love2D réussi !\n\n"
                f"📁 Fichier: {filepath}\n"
                f"📊 Cartes exportées: {card_count}\n"
                f"📝 Taille: {size:,} caractères\n\n"
                f"✅ Inclut les données de formatage de texte\n"
                f"   (position titre, position texte, polices, etc.)"
            )
            
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Erreur lors de l'export Love2D :\n{e}")

    def export_game_package(self):
        """Exporte un package complet de jeu avec fichier Lua, images fusionnées et polices."""
        try:
            # Vérifier qu'il y a des cartes
            cards = self.repo.list_cards()
            if not cards:
                messagebox.showwarning(APP_TITLE, "Aucune carte à exporter!")
                return
            
            # Dialog pour le nom du package
            from tkinter import simpledialog
            package_name = simpledialog.askstring(
                "Export Package", 
                "Nom du package de jeu:",
                initialvalue="mon_jeu_cartes"
            )
            
            if not package_name:
                return
            
            # Nettoyer le nom du package
            package_name = package_name.strip().replace(' ', '_')
            
            # Choisir le dossier de destination
            output_dir = filedialog.askdirectory(
                title="Choisir le dossier de destination",
                initialdir="exports"
            )
            
            if not output_dir:
                return
            
            # Créer une fenêtre de progression
            progress_window = tk.Toplevel(self)
            progress_window.title("Export en cours...")
            progress_window.geometry("400x150")
            progress_window.resizable(False, False)
            progress_window.transient(self)
            progress_window.grab_set()
            
            # Centrer la fenêtre
            progress_window.geometry("+%d+%d" % (
                progress_window.winfo_toplevel().winfo_x() + 50,
                progress_window.winfo_toplevel().winfo_y() + 50))
            
            # Contenu de la fenêtre de progression
            ttk.Label(progress_window, text="🎮 Export du package en cours...", 
                     font=("Arial", 12, "bold")).pack(pady=10)
            
            status_var = tk.StringVar(value="Initialisation...")
            status_label = ttk.Label(progress_window, textvariable=status_var)
            status_label.pack(pady=5)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(fill='x', padx=20, pady=10)
            progress_bar.start(10)
            
            # Effectuer l'export en arrière-plan
            def do_export():
                try:
                    # Import de l'exporteur
                    status_var.set("Chargement de l'exporteur...")
                    from game_package_exporter import GamePackageExporter
                    
                    # Créer l'exporteur
                    status_var.set("Analyse des ressources...")
                    exporter = GamePackageExporter(self.repo, output_dir)
                    
                    # Effectuer l'export
                    status_var.set("Création du package...")
                    package_path = exporter.export_complete_package(package_name)
                    
                    # Succès
                    progress_window.after(0, lambda: export_success(package_path))
                    
                except Exception as e:
                    progress_window.after(0, lambda: export_error(str(e)))
            
            def export_success(package_path):
                progress_bar.stop()
                progress_window.destroy()
                
                # Calculer les statistiques
                import os
                import zipfile
                
                size = os.path.getsize(package_path)
                
                with zipfile.ZipFile(package_path, 'r') as zipf:
                    files = zipf.namelist()
                    image_files = [f for f in files if f.endswith('.png')]
                    font_files = [f for f in files if f.endswith(('.ttf', '.otf'))]
                
                # Message de succès
                message = (
                    f"🎉 Package créé avec succès!\n\n"
                    f"📁 Fichier: {os.path.basename(package_path)}\n"
                    f"📏 Taille: {size:,} octets ({size/1024:.1f} KB)\n\n"
                    f"📦 Contenu:\n"
                    f"   • {len(cards)} cartes avec données complètes\n"
                    f"   • {len(image_files)} images fusionnées\n"
                    f"   • {len(font_files)} polices incluses\n"
                    f"   • Documentation Love2D\n\n"
                    f"✨ Prêt pour intégration dans votre jeu!\n\n"
                    f"Ouvrir le dossier contenant le package?"
                )
                
                if messagebox.askyesno(APP_TITLE, message):
                    # Ouvrir le dossier
                    folder_path = os.path.dirname(package_path)
                    os.startfile(folder_path)  # Windows
            
            def export_error(error_message):
                progress_bar.stop()
                progress_window.destroy()
                messagebox.showerror(APP_TITLE, f"Erreur lors de l'export du package:\n\n{error_message}")
            
            # Lancer l'export en thread
            import threading
            thread = threading.Thread(target=do_export)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Erreur lors de l'export du package :\n{e}")
            import traceback
            traceback.print_exc()
