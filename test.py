#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Éditeur de cartes Love2D (Lua) – Interface FR sans dépendances externes
======================================================================

- UI **tkinter/ttk** (stdlib) → aucun besoin de conda ni de PySide6.
- **Rareté** par carte (Commun, Rare, Légendaire, Mythique):
  * champ stocké en DB et exporté dans Lua → `Rarete = '...'` (ASCII sans accents)
  * onglets à droite pour **voir les cartes par rareté** : Toutes | Commun | Rare | Légendaire | Mythique
- **Types de carte** multiples (cases à cocher) : Attaque, Défense, Soin, Soutien, Carte jumelle, Cimetière
  * stockés en DB et exportés dans Lua → `Type = { 'attaque', 'soin', ... }`
- **Aperçu visuel** de l'image (onglet "Types & Image").
- Export Lua **strict** : `local Cards = { ... }  return Cards`.
- Scripts Windows: `--write-bats` génère `run.bat` et `build.bat`.
- Construction d'exécutable PyInstaller documentée ci-dessous.
- **Tests** inclus (`--test`).
"""
from __future__ import annotations
import argparse
import sys
import tkinter as tk
from pathlib import Path

# Import des modules de l'application
from lib.main_app import MainApp
from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE, APP_TITLE, load_settings
from lib.utils import write_bat_scripts
from lib.tests import run_tests


def default_db_path() -> str:
    """Retourne le chemin par défaut de la base de données."""
    return str(Path(__file__).parent / DB_FILE)


def main(argv=None):
    """Point d'entrée principal de l'application."""
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument('--test', action='store_true', help='Exécuter la suite de tests et quitter')
    parser.add_argument('--write-bats', action='store_true', help='Générer run.bat et build.bat dans le dossier du script')
    parser.add_argument('--force-advanced', action='store_true', help='Forcer l\'utilisation des thèmes avancés')
    args = parser.parse_args(argv)

    if args.test:
        print("Exécution des tests...")
        success = run_tests()
        sys.exit(0 if success else 1)

    if getattr(args, 'write_bats', False):
        paths = write_bat_scripts()
        print("Scripts générés :", paths)
        sys.exit(0)

    # Initialisation de la base de données
    db_path = default_db_path()
    ensure_db(db_path)
    repo = CardRepo(db_path)
    
    # Charge les paramètres de l'application
    load_settings()

    # Essayer d'abord le mode avancé, puis fallback vers compatibilité
    if args.force_advanced:
        print("Mode avancé forcé...")
        try:
            from lib.main_app import MainApp
            app = MainApp(repo)
            app.mainloop()
        except Exception as e:
            print(f"[ERREUR] Mode avancé échoué: {e}")
            sys.exit(1)
    else:
        # Mode par défaut : essayer avancé, puis compatibilité
        try:
            print("Tentative de lancement en mode avancé...")
            from lib.main_app import MainApp
            app = MainApp(repo)
            app.mainloop()
        except Exception as e:
            print(f"[INFO] Mode avancé non disponible: {e}")
            print("Basculement vers le mode compatibilité...")
            
            try:
                # Mode compatibilité
                from test_compat import SimpleMainApp
                print("Lancement en mode compatibilité...")
                app = SimpleMainApp(repo)
                app.mainloop()
            except Exception as e2:
                print(f"[ERREUR] Échec du mode compatibilité: {e2}")
                print("Aucun mode d'interface disponible.")
                sys.exit(1)


if __name__ == '__main__':
    main()
