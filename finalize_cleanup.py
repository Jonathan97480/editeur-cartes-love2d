#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de finalisation de la réorganisation
Traite les fichiers restants
"""

import os
import shutil

def finalize_cleanup():
    """Finalise le nettoyage des fichiers restants"""
    
    # Fichiers à déplacer vers tools/
    tools_files = [
        'ANALYSER_EXPORT_LUA.bat',
        'DEMO_ANALYSER.bat', 
        'DIAGNOSTIC.bat',
        'commit.bat',
        'commit.ps1',
        'git_commit.bat',
        'LAUNCH_PORTABLE.bat',
        'launch_simple.bat',
        'LAUNCH_WITH_RESIZABLE_PANEL.bat',
        'launch.bat',
        'run_final.bat',
        'run.bat',
        'RESTART_WITH_300PX_SLIDERS.bat',
        'START_NEW.bat',
        'START.bat',
        'UPDATE.bat',
        'validate_all.bat'
    ]
    
    # Fichiers à déplacer vers scripts/utils/
    utils_files = [
        'diagnostic.py',
        'solution_finale.py',
        'correction_confirmee.py',
        'MIGRATION_TESTS_SUMMARY.py',
        'validate_tests_auto.py',
        'verify_db_protection.py',
        'verify_relative_paths.py'
    ]
    
    # Fichiers à déplacer vers docs/deprecated/
    docs_files = [
        'DIMENSIONS_INTERFACE.md',
        'DOCUMENTATION_MISE_A_JOUR.md',
        'DOSSIER_IMAGES_RESOLU.md',
        'GESTION_DONNEES_COMPLETE.md',
        'GRANDE_REORGANISATION_COMPLETE.md',
        'GUIDE.md',
        'INSTALLATION_GUIDE.md',
        'MODIFICATION_START_BAT.md',
        'NOUVEAU_SYSTEME_EXPORT.md',
        'REORGANISATION_COMPLETE.md',
        'SECURITE_BDD.md',
        'VALIDATION_EXPORTS_ENERGIE.md'
    ]
    
    # Fichiers à déplacer vers legacy/
    legacy_files = [
        'AUDIT_DATA.json',
        'cards_player_test.lua',
        'exemple_love2d.lua',
        '.gitignore_new'
    ]
    
    moved_count = 0
    
    # Créer le dossier legacy s'il n'existe pas
    os.makedirs('legacy', exist_ok=True)
    
    # Déplacer vers tools/
    print("📂 Finalisation tools/")
    for file in tools_files:
        if os.path.exists(file):
            try:
                shutil.move(file, f'tools/{file}')
                print(f"  ➡️  {file} → tools/")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Erreur avec {file}: {e}")
    
    # Déplacer vers scripts/utils/
    print("\n📂 Finalisation scripts/utils/")
    for file in utils_files:
        if os.path.exists(file):
            try:
                shutil.move(file, f'scripts/utils/{file}')
                print(f"  ➡️  {file} → scripts/utils/")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Erreur avec {file}: {e}")
    
    # Déplacer vers docs/deprecated/
    print("\n📂 Finalisation docs/deprecated/")
    for file in docs_files:
        if os.path.exists(file):
            try:
                shutil.move(file, f'docs/deprecated/{file}')
                print(f"  ➡️  {file} → docs/deprecated/")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Erreur avec {file}: {e}")
    
    # Déplacer vers legacy/
    print("\n📂 Finalisation legacy/")
    for file in legacy_files:
        if os.path.exists(file):
            try:
                shutil.move(file, f'legacy/{file}')
                print(f"  ➡️  {file} → legacy/")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Erreur avec {file}: {e}")
    
    print(f"\n✅ Finalisation terminée ! {moved_count} fichiers déplacés")
    
    # Afficher les fichiers restants à la racine
    remaining = []
    for item in os.listdir('.'):
        if os.path.isfile(item) and item not in [
            'app_final.py', 'README.md', 'CHANGELOG.md', 'cartes.db', 
            'reorganize_project.py', 'finalize_cleanup.py', 'requirements.txt',
            'LICENSE'
        ]:
            remaining.append(item)
    
    if remaining:
        print(f"\n📋 Fichiers restants à la racine ({len(remaining)}) :")
        for file in remaining:
            print(f"  - {file}")
    else:
        print("\n🎉 Racine complètement nettoyée !")

if __name__ == "__main__":
    finalize_cleanup()
