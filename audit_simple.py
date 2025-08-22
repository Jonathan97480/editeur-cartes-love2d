#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT SIMPLIFIÉ DU PROJET
========================
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

def audit_project():
    project_root = Path(".")
    
    print("🔍 AUDIT SIMPLIFIÉ DU PROJET")
    print("=" * 40)
    
    # 1. Structure du projet
    print("\n📁 STRUCTURE DU PROJET")
    total_files = 0
    python_files = 0
    directories = []
    
    for root, dirs, files in os.walk(project_root):
        relative_root = Path(root).relative_to(project_root)
        if str(relative_root) != '.':
            directories.append(str(relative_root))
        
        for file in files:
            total_files += 1
            if file.endswith('.py'):
                python_files += 1
    
    print(f"   📊 Total des fichiers: {total_files}")
    print(f"   🐍 Fichiers Python: {python_files}")
    print(f"   📁 Dossiers: {len(directories)}")
    
    # Vérifier fichiers essentiels
    essential_files = {
        'README.md': 'README.md',
        'requirements.txt': 'requirements.txt',
        'LICENSE': 'LICENSE',
        'START.bat': 'START.bat',
        'app_final.py': 'app_final.py'
    }
    
    print("   📋 Fichiers essentiels:")
    for name, path in essential_files.items():
        exists = Path(path).exists()
        status = '✅' if exists else '❌'
        print(f"      {status} {name}")
    
    # 2. Base de données
    print("\n💾 BASE DE DONNÉES")
    db_path = Path('data/cartes.db')
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cards")
            card_count = cursor.fetchone()[0]
            conn.close()
            print(f"   ✅ Base de données opérationnelle ({card_count} cartes)")
        except Exception as e:
            print(f"   ❌ Erreur base de données: {e}")
    else:
        print("   ❌ Base de données manquante")
    
    # 3. Modules principaux
    print("\n🔧 MODULES PRINCIPAUX")
    lib_path = Path('lib')
    if lib_path.exists():
        key_modules = [
            'main_app.py',
            'ui_components.py', 
            'database.py',
            'text_formatting_editor.py',
            'lua_export.py'
        ]
        
        for module in key_modules:
            module_path = lib_path / module
            exists = module_path.exists()
            status = '✅' if exists else '❌'
            size = f"({module_path.stat().st_size // 1024} KB)" if exists else ""
            print(f"   {status} {module} {size}")
    
    # 4. Tests
    print("\n🧪 TESTS")
    tests_path = Path('tests')
    if tests_path.exists():
        test_files = list(tests_path.rglob('test_*.py'))
        print(f"   ✅ Dossier tests existe ({len(test_files)} fichiers de test)")
        
        # Catégories de tests
        categories = set()
        for test_file in test_files:
            relative_path = test_file.relative_to(tests_path)
            if len(relative_path.parts) > 1:
                categories.add(relative_path.parts[0])
        
        if categories:
            print(f"   📋 Catégories: {', '.join(sorted(categories))}")
    else:
        print("   ❌ Dossier tests manquant")
    
    # 5. Documentation
    print("\n📚 DOCUMENTATION")
    readme_exists = Path('README.md').exists()
    docs_exists = Path('docs').is_dir()
    guides_exists = Path('guides').is_dir()
    
    print(f"   {'✅' if readme_exists else '❌'} README.md")
    print(f"   {'✅' if docs_exists else '❌'} Dossier docs/")
    print(f"   {'✅' if guides_exists else '❌'} Dossier guides/")
    
    # 6. Exports
    print("\n📦 CAPACITÉS D'EXPORT")
    export_files = [
        'lua_exporter_love2d.py',
        'game_package_exporter.py'
    ]
    
    for export_file in export_files:
        exists = Path(export_file).exists()
        status = '✅' if exists else '❌'
        print(f"   {status} {export_file}")
    
    # 7. Score global simplifié
    print("\n📊 ÉVALUATION GLOBALE")
    
    checks = [
        ('Structure organisée', len(directories) >= 5),
        ('Fichiers essentiels', all(Path(f).exists() for f in essential_files.values())),
        ('Base de données', db_path.exists()),
        ('Modules principaux', lib_path.exists() and len(list(lib_path.glob('*.py'))) >= 5),
        ('Tests organisés', tests_path.exists()),
        ('Documentation', readme_exists),
        ('Capacités export', any(Path(f).exists() for f in export_files))
    ]
    
    passed_checks = sum(1 for _, check in checks if check)
    score = (passed_checks / len(checks)) * 100
    
    print(f"   📈 Score global: {score:.1f}%")
    
    if score >= 80:
        status = "✅ EXCELLENT"
    elif score >= 60:
        status = "⚠️ BON"
    else:
        status = "❌ À AMÉLIORER"
    
    print(f"   🎯 Status: {status}")
    
    # Recommandations rapides
    print("\n💡 RECOMMANDATIONS RAPIDES")
    
    if score < 100:
        for name, check in checks:
            if not check:
                print(f"   ⚠️ Améliorer: {name}")
    else:
        print("   🎉 Projet en excellent état!")
    
    print("\n" + "=" * 40)
    print("✅ AUDIT TERMINÉ")
    
    return score

if __name__ == "__main__":
    audit_project()
