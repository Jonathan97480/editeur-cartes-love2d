#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE NETTOYAGE COMPLET DU PROJET
=====================================

Ce script nettoie automatiquement le projet en supprimant :
- Les fichiers temporaires de développement
- Les fichiers de test isolés (hors dossier tests/)
- Les sauvegardes redondantes
- Les exports de démonstration
- Les fichiers de configuration temporaires
- Les dossiers de cache

Préserve :
- Le dossier tests/ organisé
- Les fichiers de configuration essentiels
- Les modules principaux (lib/)
- La documentation importante
- Les assets (images, fonts)
"""

import os
import shutil
import sys
from pathlib import Path

class ProjectCleaner:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.preserved_files = set()
        self.deleted_files = set()
        self.deleted_dirs = set()
        
    def log_action(self, action, path, reason=""):
        """Log des actions de nettoyage"""
        print(f"📋 {action}: {path}")
        if reason:
            print(f"   Raison: {reason}")
    
    def is_essential_file(self, file_path):
        """Vérifie si un fichier est essentiel au projet"""
        essential_patterns = [
            # Fichiers système et configuration
            '.git', '.github', '.gitignore', 'README', 'LICENSE',
            'requirements.txt', 'setup.py', 'pyproject.toml',
            
            # Scripts principaux
            'START.bat', 'run.bat', 'UPDATE.bat',
            
            # Modules principaux
            'lib/', 'app_final.py', 'main.py',
            
            # Documentation organisée
            'docs/', 'guides/',
            
            # Assets
            'images/', 'fonts/', 'data/',
            
            # Tests organisés
            'tests/',
            
            # Exports organisés
            'exports/', 'result_export_lua/',
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in essential_patterns)
    
    def clean_temporary_files(self):
        """Nettoie les fichiers temporaires de développement"""
        temp_patterns = [
            # Tests isolés (pas dans tests/)
            'test_*.py',
            # Fichiers temporaires
            '*_temp*', 'temp_*', '*.tmp', '*.temp',
            # Fichiers de démonstration
            'demo_*.py', '*_demo.py',
            # Fichiers de correction temporaires
            'fix_*.py', 'correction_*.py', 'repair_*.py',
            # Fichiers d'audit et maintenance
            'audit_*.py', 'maintenance_*.py', 'nettoyer_*.py',
            # Fichiers de validation temporaires
            'validate_*.py', 'verification_*.py',
            # Rapports temporaires
            'RAPPORT_*.md', 'CORRECTION_*.md', 'RÉSUMÉ_*.txt',
        ]
        
        for pattern in temp_patterns:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file() and not self.is_essential_file(file_path):
                    self.log_action("SUPPRESSION", file_path, f"Fichier temporaire ({pattern})")
                    file_path.unlink()
                    self.deleted_files.add(str(file_path))
    
    def clean_backup_directories(self):
        """Nettoie les dossiers de sauvegarde redondants"""
        backup_dirs = [
            'backups/', 'dbBackup/', 'imagesBackup/', 'luaBackup/', 'lua_backup/',
            '__pycache__/', '.pytest_cache/', 'build/', 'dist/',
            'dev_temp/', 'temp/', 'legacy/',
            'commit_reports/', 'rapports/', 'test_correction/', 'test_output/',
            'test_packages/', 'test_features/', 'demo_exports/', 'lua_tests/',
            'love2d_test/'
        ]
        
        for dir_name in backup_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.log_action("SUPPRESSION DOSSIER", dir_path, "Dossier de sauvegarde/temporaire")
                shutil.rmtree(dir_path)
                self.deleted_dirs.add(str(dir_path))
    
    def clean_duplicate_configs(self):
        """Nettoie les fichiers de configuration dupliqués"""
        config_duplicates = [
            '.gitignore_new', 'README_NEW.md', 'README_GITHUB.md',
            'START_NEW.bat', 'settings.json', 'test_config.json',
            'commit_message.txt', 'commit_message_temp.txt', 'commit_msg.txt'
        ]
        
        for config_file in config_duplicates:
            file_path = self.project_root / config_file
            if file_path.exists():
                self.log_action("SUPPRESSION", file_path, "Configuration dupliquée")
                file_path.unlink()
                self.deleted_files.add(str(file_path))
    
    def clean_export_files(self):
        """Nettoie les fichiers d'export temporaires"""
        export_patterns = [
            '*.lua',  # Fichiers Lua temporaires à la racine
            'cards_*.lua', 'test_*.lua', 'audit_*.lua'
        ]
        
        for pattern in export_patterns:
            for file_path in self.project_root.glob(pattern):
                # Garder seulement les exports dans les dossiers organisés
                if (file_path.is_file() and 
                    file_path.parent == self.project_root and
                    not str(file_path.name).startswith('main') and
                    not str(file_path.name).startswith('app')):
                    self.log_action("SUPPRESSION", file_path, f"Export temporaire ({pattern})")
                    file_path.unlink()
                    self.deleted_files.add(str(file_path))
    
    def clean_documentation_duplicates(self):
        """Nettoie la documentation dupliquée"""
        doc_duplicates = [
            'INSTALLATION_GUIDE.md', 'NOUVEAU_SYSTEME_EXPORT.md',
            'ORGANISATION_COMPLETE_PROJET.md', 'LUA_ORGANISATION_INDEX.md',
            'VALIDATION_EXPORTS_ENERGIE.md'
        ]
        
        for doc_file in doc_duplicates:
            file_path = self.project_root / doc_file
            if file_path.exists():
                self.log_action("SUPPRESSION", file_path, "Documentation dupliquée")
                file_path.unlink()
                self.deleted_files.add(str(file_path))
    
    def clean_development_scripts(self):
        """Nettoie les scripts de développement temporaires"""
        dev_scripts = [
            'amelioration_interface_position.py', 'auto_prevent_absolute_paths.py',
            'check_database_paths.py', 'commit_organisation.py',
            'export_package.py', 'finaliser_organisation_tests.py',
            'fix_absolute_path_sources.py', 'fix_database_paths.py',
            'fix_imports.py', 'install_fonts.py', 'organiser_documentation.py',
            'organize_fonts.py', 'package_export_ui.py', 'path_fix_documentation.py',
            'prevent_absolute_paths.py', 'restart_editor_300px.py',
            'secure_commit_system.py', 'standardize_sliders.py',
            'DIAGNOSTIC.bat', 'LAUNCH_PORTABLE.bat', 'LAUNCH_WITH_RESIZABLE_PANEL.bat',
            'RESTART_WITH_300PX_SLIDERS.bat', 'check_paths_at_startup.bat'
        ]
        
        for script_file in dev_scripts:
            file_path = self.project_root / script_file
            if file_path.exists():
                self.log_action("SUPPRESSION", file_path, "Script de développement temporaire")
                file_path.unlink()
                self.deleted_files.add(str(file_path))
    
    def clean_python_cache(self):
        """Nettoie les caches Python"""
        for pycache_dir in self.project_root.rglob('__pycache__'):
            if pycache_dir.is_dir():
                self.log_action("SUPPRESSION CACHE", pycache_dir, "Cache Python")
                shutil.rmtree(pycache_dir)
                self.deleted_dirs.add(str(pycache_dir))
        
        for pyc_file in self.project_root.rglob('*.pyc'):
            if pyc_file.is_file():
                self.log_action("SUPPRESSION", pyc_file, "Fichier bytecode Python")
                pyc_file.unlink()
                self.deleted_files.add(str(pyc_file))
    
    def generate_cleanup_report(self):
        """Génère un rapport de nettoyage"""
        report_path = self.project_root / 'RAPPORT_NETTOYAGE.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🧹 RAPPORT DE NETTOYAGE DU PROJET\n\n")
            f.write(f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## 📊 Statistiques\n\n")
            f.write(f"- **Fichiers supprimés**: {len(self.deleted_files)}\n")
            f.write(f"- **Dossiers supprimés**: {len(self.deleted_dirs)}\n\n")
            
            if self.deleted_files:
                f.write("## 📄 Fichiers supprimés\n\n")
                for file_path in sorted(self.deleted_files):
                    f.write(f"- `{file_path}`\n")
                f.write("\n")
            
            if self.deleted_dirs:
                f.write("## 📁 Dossiers supprimés\n\n")
                for dir_path in sorted(self.deleted_dirs):
                    f.write(f"- `{dir_path}/`\n")
                f.write("\n")
            
            f.write("## ✅ Structure finale préservée\n\n")
            f.write("- `lib/` - Modules principaux\n")
            f.write("- `tests/` - Tests organisés\n")
            f.write("- `docs/` et `guides/` - Documentation\n")
            f.write("- `images/` et `fonts/` - Assets\n")
            f.write("- `data/` - Base de données\n")
            f.write("- `exports/` et `result_export_lua/` - Exports organisés\n")
            f.write("- Scripts essentiels (`START.bat`, `app_final.py`, etc.)\n")
        
        print(f"\n📋 Rapport de nettoyage sauvegardé: {report_path}")
    
    def run_cleanup(self):
        """Exécute le nettoyage complet"""
        print("🧹 DÉBUT DU NETTOYAGE COMPLET DU PROJET")
        print("=" * 50)
        
        print("\n1️⃣ Nettoyage des fichiers temporaires...")
        self.clean_temporary_files()
        
        print("\n2️⃣ Nettoyage des dossiers de sauvegarde...")
        self.clean_backup_directories()
        
        print("\n3️⃣ Nettoyage des configurations dupliquées...")
        self.clean_duplicate_configs()
        
        print("\n4️⃣ Nettoyage des exports temporaires...")
        self.clean_export_files()
        
        print("\n5️⃣ Nettoyage de la documentation dupliquée...")
        self.clean_documentation_duplicates()
        
        print("\n6️⃣ Nettoyage des scripts de développement...")
        self.clean_development_scripts()
        
        print("\n7️⃣ Nettoyage des caches Python...")
        self.clean_python_cache()
        
        print("\n8️⃣ Génération du rapport...")
        self.generate_cleanup_report()
        
        print(f"\n✅ NETTOYAGE TERMINÉ!")
        print(f"📊 Statistiques finales:")
        print(f"   - Fichiers supprimés: {len(self.deleted_files)}")
        print(f"   - Dossiers supprimés: {len(self.deleted_dirs)}")
        print(f"\n🎯 Le projet est maintenant propre et organisé!")

def main():
    """Point d'entrée principal"""
    project_root = Path(__file__).parent
    
    print("🧹 SCRIPT DE NETTOYAGE COMPLET DU PROJET")
    print("=" * 50)
    print(f"📂 Dossier du projet: {project_root}")
    
    response = input("\n⚠️  Voulez-vous continuer le nettoyage ? (oui/non): ").lower().strip()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("❌ Nettoyage annulé.")
        return
    
    cleaner = ProjectCleaner(project_root)
    cleaner.run_cleanup()

if __name__ == "__main__":
    main()
