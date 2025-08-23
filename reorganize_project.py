#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de réorganisation complète du projet
Déplace tous les fichiers temporaires, tests et démos dans des dossiers appropriés
"""

import os
import shutil
import sys
from pathlib import Path

def reorganize_project():
    """Réorganise complètement la structure du projet"""
    
    # Définir les règles de déplacement
    move_rules = {
        'scripts/tests/': [
            'test_',
            'validation_',
            'verification_',
            'check_',
            'analyser_tests.py',
            'run_tests.py',
            'test.py'
        ],
        'scripts/demos/': [
            'demo_',
            'guide_',
            'app_simple.py',
            'app_text_icons.py'
        ],
        'scripts/maintenance/': [
            'audit_',
            'cleanup_',
            'nettoyer_',
            'organiser_',
            'finaliser_',
            'reorganiser_',
            'fix_',
            'migrate_',
            'reset_',
            'maintenance.py',
            'manage_',
            'db_tools.py'
        ],
        'scripts/setup/': [
            'install_',
            'configure_',
            'setup_',
            'create_',
            'add_energy_columns.py'
        ],
        'scripts/utils/': [
            'export_',
            'generate_',
            'generation_',
            'monitor_',
            'smart_',
            'sync_',
            'standardize_',
            'convert_',
            'package_',
            'path_fix_',
            'auto_',
            'lua_',
            'game_package_exporter.py',
            'quick_export.py',
            'comparaison_export_lua.py',
            'amelioration_interface_position.py',
            'diagnostic_images.py',
            'debug_image.py',
            'deck_viewer_summary.py',
            'organize_fonts.py',
            'restart_editor_300px.py'
        ],
        'tools/': [
            '.bat',
            'commit_',
            'git_manager.py',
            'secure_',
            'pre_commit_',
            'quick_commit.bat',
            'simple_commit.bat',
            'publish_github.bat',
            'git_status.bat',
            'git_push.bat',
            'git.bat'
        ],
        'docs/deprecated/': [
            '.md',
            'rapport_',
            'bilan_',
            'documentation_',
            'corrections_',
            'resume_',
            'confirmation_',
            'SOLUTION_',
            'AMELIORATIONS_',
            'PROBLEME_',
            'CORRECTION_',
            'RESUMÉ_',
            'RÉSUMÉ_',
            'TOUTES_',
            'RAPPORT_',
            'GUIDE_',
            'UPDATE_',
            'TECHNICAL_',
            'MODES.md',
            'BUILD_SUCCESS.md',
            'COMMIT_REUSSI.md',
            'GIT_INFO.md',
            'README_GITHUB.md',
            'README_NEW.md'
        ]
    }
    
    # Fichiers à garder à la racine
    keep_at_root = {
        'app_final.py',
        'README.md',
        'CHANGELOG.md',
        'cartes.db',
        'reorganize_project.py'
    }
    
    # Obtenir la liste de tous les fichiers à la racine
    root_files = []
    for file in os.listdir('.'):
        if os.path.isfile(file):
            root_files.append(file)
    
    print(f"📁 Trouvé {len(root_files)} fichiers à la racine")
    
    # Créer les dossiers de destination
    for folder in move_rules.keys():
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Dossier créé : {folder}")
    
    moved_count = 0
    errors = []
    
    # Déplacer les fichiers selon les règles
    for target_folder, patterns in move_rules.items():
        print(f"\n📂 Traitement du dossier : {target_folder}")
        
        for pattern in patterns:
            for file in root_files[:]:  # Copie de la liste pour modification
                if file in keep_at_root:
                    continue
                    
                # Vérifier si le fichier correspond au pattern
                matches = False
                if pattern.endswith('.py') or pattern.endswith('.bat') or pattern.endswith('.md'):
                    # Fichier exact
                    if file == pattern:
                        matches = True
                elif pattern.startswith('.'):
                    # Extension
                    if file.endswith(pattern):
                        matches = True
                else:
                    # Préfixe
                    if file.startswith(pattern):
                        matches = True
                
                if matches:
                    try:
                        source_path = file
                        dest_path = os.path.join(target_folder, file)
                        shutil.move(source_path, dest_path)
                        print(f"  ➡️  {file} → {target_folder}")
                        root_files.remove(file)
                        moved_count += 1
                    except Exception as e:
                        errors.append(f"Erreur avec {file}: {e}")
    
    # Gérer les fichiers non catégorisés
    remaining_files = []
    for file in os.listdir('.'):
        if os.path.isfile(file) and file not in keep_at_root and file != 'reorganize_project.py':
            remaining_files.append(file)
    
    if remaining_files:
        print(f"\n⚠️  {len(remaining_files)} fichiers non catégorisés restants :")
        for file in remaining_files[:10]:  # Montrer seulement les 10 premiers
            print(f"  - {file}")
        if len(remaining_files) > 10:
            print(f"  ... et {len(remaining_files) - 10} autres")
    
    # Résumé
    print(f"\n✅ Réorganisation terminée !")
    print(f"📦 {moved_count} fichiers déplacés")
    print(f"🏠 {len(keep_at_root)} fichiers gardés à la racine")
    
    if errors:
        print(f"\n❌ {len(errors)} erreurs :")
        for error in errors:
            print(f"  - {error}")
    
    # Vérifier les dossiers créés
    print(f"\n📋 Structure créée :")
    for folder in move_rules.keys():
        count = len([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])
        print(f"  {folder}: {count} fichiers")
    
    return moved_count, len(errors)

if __name__ == "__main__":
    print("🧹 Début de la réorganisation du projet...")
    print("=" * 60)
    
    try:
        moved, errors = reorganize_project()
        
        if errors == 0:
            print("\n🎉 Réorganisation réussie sans erreur !")
            sys.exit(0)
        else:
            print(f"\n⚠️  Réorganisation terminée avec {errors} erreurs")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Erreur critique : {e}")
        sys.exit(1)
