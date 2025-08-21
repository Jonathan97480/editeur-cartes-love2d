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
from .lua_export import export_lua
from .utils import to_int, create_card_image

class CardForm(ttk.Frame):
    def __init__(self, master, repo: CardRepo, on_saved, **kw):
        super().__init__(master, **kw)
        self.repo = repo
        self.on_saved = on_saved
        self.current_id: int | None = None
        self.generated_image_path: str | None = None  # Chemin de l'image générée
        self._build_ui()

    # ---------- Build Tabs ----------
    def _build_ui(self):
        pad = dict(padx=8, pady=4)
        # Ligne 1 : côté, nom, power, rareté
        row = ttk.Frame(self); row.pack(fill='x', **pad)
        ttk.Label(row, text="Côté :").pack(side='left')
        self.side_var = tk.StringVar(value='Joueur')
        ttk.Combobox(row, textvariable=self.side_var, values=['Joueur', 'IA'], width=8, state='readonly').pack(side='left', padx=6)

        ttk.Label(row, text="Nom de la carte :").pack(side='left', padx=(12,4))
        self.name_var = tk.StringVar(); ttk.Entry(row, textvariable=self.name_var, width=32).pack(side='left')

        ttk.Label(row, text="Coût (PowerBlow) :").pack(side='left', padx=(12,4))
        self.power_var = tk.IntVar(value=0)
        ttk.Spinbox(row, from_=0, to=999, textvariable=self.power_var, width=6).pack(side='left')

        ttk.Label(row, text="Rareté :").pack(side='left', padx=(12,4))
        self.rarity_var = tk.StringVar(value='Commun')
        ttk.Combobox(row, textvariable=self.rarity_var, values=['Commun','Rare','Légendaire','Mythique'], width=12, state='readonly').pack(side='left')

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
        original_path = None
        generated_path = getattr(self, 'generated_image_path', None)
        
        try:
            path = self.img_var.get().strip()
        except Exception:
            path = ''
        if path and os.path.exists(path):
            original_path = path
        
        if generated_path and os.path.exists(generated_path):
            generated_path = generated_path
        else:
            generated_path = None
        
        # Choisir quelle image afficher selon le mode
        preview_path = None
        if hasattr(self, 'show_generated') and self.show_generated and generated_path:
            preview_path = generated_path
        elif original_path:
            preview_path = original_path
        elif generated_path:  # Fallback sur l'image générée si pas d'original
            preview_path = generated_path
        
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
        if preview_path == getattr(self, 'generated_image_path', None):
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
            if preview_path == getattr(self, 'generated_image_path', None):
                self.toggle_image_btn.config(text="Voir original", state='normal')
            else:
                if getattr(self, 'generated_image_path', None) and os.path.exists(getattr(self, 'generated_image_path', '')):
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
            from .utils import copy_image_to_originals
            
            # Copier l'image vers le dossier originals
            local_image_path = copy_image_to_originals(path, card_name)
            
            if local_image_path:
                # Utiliser la copie locale au lieu du fichier original
                self.img_var.set(local_image_path.replace('\\', '/'))
                messagebox.showinfo("Image copiée", 
                    f"Image copiée dans :\n{local_image_path}\n\nLa carte utilisera maintenant cette copie locale.")
            else:
                # En cas d'échec de copie, utiliser le chemin original (fallback)
                self.img_var.set(path.replace('\\', '/'))
                messagebox.showwarning("Copie échouée", 
                    "La copie de l'image a échoué. Le chemin original sera utilisé.")
            
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
        self.side_var.set('Joueur')
        self.name_var.set('')
        self.img_var.set('')
        self.desc_txt.delete('1.0', 'end')
        self.power_var.set(0)
        self.rarity_var.set('Commun')
        
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

    def load_card(self, card: Card):
        self.current_id = card.id
        self.generated_image_path = None  # Réinitialiser l'image générée lors du chargement
        self.side_var.set('Joueur' if card.side == 'joueur' else 'IA')
        self.name_var.set(card.name)
        self.img_var.set(card.img)
        self.desc_txt.delete('1.0', 'end'); self.desc_txt.insert('1.0', card.description)
        self.power_var.set(int(card.powerblow))
        self.rarity_var.set(RARITY_LABELS.get(getattr(card, 'rarity', 'commun'), 'Commun'))
        
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
        c.side = 'joueur' if self.side_var.get() == 'Joueur' else 'ia'
        c.name = self.name_var.get().strip()
        c.img = self.img_var.get().strip()
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

    # ---------- Commands ----------
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
        
        # Génère l'image fusionnée si possible
        generated_image = self.generate_card_image()
        if generated_image:
            self.generated_image_path = generated_image
            # Mettre à jour le chemin de l'image en base de données
            c.img = generated_image.replace('\\', '/')
            self.repo.update(c)
            # Actualiser l'aperçu pour montrer l'image générée
            self._update_preview()
        
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

    # ---------- Card Image Generation ----------
    def generate_card_image(self):
        """Génère l'image fusionnée de la carte selon sa rareté."""
        if not self.img_var.get().strip():
            return None
        
        card_name = self.name_var.get().strip() or "carte_sans_nom"
        card_image_path = self.img_var.get().strip()
        
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
            return None
        
        return create_card_image(card_image_path, template_path, card_name)


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
        ttk.Label(top, text='Côté :').pack(side='left')
        self.side_filter = tk.StringVar(value='Tous')
        ttk.Combobox(top, textvariable=self.side_filter, values=['Tous', 'Joueur', 'IA'], width=8, state='readonly').pack(side='left', padx=6)
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
        cols = ('id','cote','rarete','nom','power','desc','maj')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=20)
        self.tree.heading('id', text='ID'); self.tree.column('id', width=50, anchor='center')
        self.tree.heading('cote', text='Côté'); self.tree.column('cote', width=70, anchor='center')
        self.tree.heading('rarete', text='Rareté'); self.tree.column('rarete', width=110, anchor='center')
        self.tree.heading('nom', text='Nom'); self.tree.column('nom', width=200)
        self.tree.heading('power', text='Power'); self.tree.column('power', width=60, anchor='center')
        self.tree.heading('desc', text='Description'); self.tree.column('desc', width=300)
        self.tree.heading('maj', text='MAJ'); self.tree.column('maj', width=140, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=8, pady=4)
        self.tree.bind('<Double-1>', self._on_double)

        # Exports
        exp = ttk.Frame(self); exp.pack(fill='x', **pad)
        ttk.Button(exp, text='Exporter LUA (Joueur)', command=lambda: self.export_side('joueur')).pack(side='left')
        ttk.Button(exp, text='Exporter LUA (IA)', command=lambda: self.export_side('ia')).pack(side='left', padx=6)
        ttk.Button(exp, text='Terminer (Exporter les deux)', command=self.export_both).pack(side='right')

    def _side_value(self):
        v = self.side_filter.get()
        if v == 'Joueur': return 'joueur'
        if v == 'IA': return 'ia'
        return None

    def refresh(self):
        side = self._side_value()
        text = self.search_var.get().strip() or None
        if self.fixed_rarity_label:
            rarity = RARITY_FROM_LABEL.get(self.fixed_rarity_label)
        else:
            rarity_label = self.rarity_filter.get() if self.rarity_filter else 'Toutes'
            rarity = RARITY_FROM_LABEL.get(rarity_label) if rarity_label != 'Toutes' else None
        cards = self.repo.list_cards(side=side, search_text=text, rarity=rarity)
        for i in self.tree.get_children(): self.tree.delete(i)
        for c in cards:
            maj = c.updated_at.split('T')[0] if c.updated_at else ''
            self.tree.insert('', 'end', values=(
                c.id,
                'Joueur' if c.side=='joueur' else 'IA',
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
