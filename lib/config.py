#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration et constantes pour l'éditeur de cartes Love2D
"""
import json
import os

# ======================= Constantes =======================

DB_FILE = "cartes.db"
APP_TITLE = "Éditeur de Cartes Love2D"
SETTINGS_FILE = "settings.json"
IMAGES_FOLDER = "images"

# ---------- Rareté ----------
RARITY_VALUES = ['commun', 'rare', 'legendaire', 'mythique']
RARITY_LABELS = {
    'commun': 'Commun',
    'rare': 'Rare',
    'legendaire': 'Légendaire',
    'mythique': 'Mythique',
}
RARITY_FROM_LABEL = {v: k for k, v in RARITY_LABELS.items()}

# ---------- Types (ASCII pour le Lua/DB) ----------
TYPE_LABELS = {
    'attaque': 'Attaque',
    'defense': 'Défense',
    'soin': 'Soin',
    'soutien': 'Soutien',
    'carte_jumelle': 'Carte jumelle',
    'cimetiere': 'Cimetière',
}
TYPE_FROM_LABEL = {v: k for k, v in TYPE_LABELS.items()}
TYPE_ORDER = ['attaque','defense','soin','soutien','carte_jumelle','cimetiere']

# ---------- Configuration globale ----------
APP_SETTINGS = {
    "template_image": "",
    "output_folder": IMAGES_FOLDER,
    "theme": "auto"  # "auto", "light", "dark"
}

# ======================= Fonctions de configuration =======================

def load_settings() -> dict:
    """Charge les paramètres depuis le fichier JSON."""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                APP_SETTINGS.update(settings)
    except Exception:
        pass
    return APP_SETTINGS

def save_settings() -> None:
    """Sauvegarde les paramètres dans le fichier JSON."""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(APP_SETTINGS, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
