#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NETTOYAGE FINAL DU PROJET - FONCTIONNALITÉ FAVORIS
================================================
Nettoie le projet après l'implémentation des favoris de formatage
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Nettoie le projet après l'implémentation des favoris."""
    print("🧹 NETTOYAGE FINAL DU PROJET")
    print("=" * 50)
    
    project_root = Path(".")
    files_removed = 0
    dirs_removed = 0
    
    # 1. Fichiers temporaires de test
    temp_files = [
        "test_energy_formatting.py",
        "test_favorites_quick.py", 
        "NETTOYAGE_PROJET.py",
        "audit_simple.py"
    ]
    
    print("\n1️⃣ Suppression des fichiers de test temporaires...")
    for file_name in temp_files:
        file_path = project_root / file_name
        if file_path.exists():
            file_path.unlink()
            print(f"   🗑️ Supprimé: {file_name}")
            files_removed += 1
    
    # 2. Fichiers de cache Python
    print("\n2️⃣ Nettoyage des caches Python...")
    for pycache_dir in project_root.rglob('__pycache__'):
        if pycache_dir.is_dir():
            shutil.rmtree(pycache_dir)
            print(f"   🗑️ Supprimé: {pycache_dir}")
            dirs_removed += 1
    
    for pyc_file in project_root.rglob('*.pyc'):
        pyc_file.unlink()
        print(f"   🗑️ Supprimé: {pyc_file}")
        files_removed += 1
    
    # 3. Fichiers de logs temporaires
    print("\n3️⃣ Nettoyage des logs temporaires...")
    log_patterns = ["*.log", "*.tmp", "debug_*.txt"]
    for pattern in log_patterns:
        for file_path in project_root.glob(pattern):
            if file_path.is_file():
                file_path.unlink()
                print(f"   🗑️ Supprimé: {file_path}")
                files_removed += 1
    
    # 4. Vérification des fichiers essentiels
    print("\n4️⃣ Vérification des fichiers essentiels...")
    essential_files = [
        "app_final.py",
        "lib/database.py",
        "lib/favorites_manager.py", 
        "lib/text_formatting_editor.py",
        "tests/test_formatting_favorites.py",
        "data/cartes.db"
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not (project_root / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("   ❌ Fichiers manquants:")
        for file_path in missing_files:
            print(f"      - {file_path}")
    else:
        print("   ✅ Tous les fichiers essentiels sont présents")
    
    # 5. Vérification de la structure des tests
    print("\n5️⃣ Vérification de la structure des tests...")
    tests_dir = project_root / "tests"
    if tests_dir.exists():
        test_files = list(tests_dir.rglob("test_*.py"))
        print(f"   📊 {len(test_files)} fichiers de test trouvés")
        
        # Vérifier le test des favoris
        favorites_test = tests_dir / "test_formatting_favorites.py"
        if favorites_test.exists():
            print("   ✅ Test des favoris de formatage présent")
        else:
            print("   ❌ Test des favoris de formatage manquant")
    
    # 6. Organisation des fichiers de documentation
    print("\n6️⃣ Organisation de la documentation...")
    doc_files = [
        "FAVORIS_FORMATAGE_IMPLEMENTATION.md",
        "GUIDE_LANCEMENT.md",
        "RAPPORT_AUDIT_FINAL.md"
    ]
    
    docs_dir = project_root / "docs"
    if not docs_dir.exists():
        docs_dir.mkdir()
        print(f"   📁 Dossier docs/ créé")
    
    moved_docs = 0
    for doc_file in doc_files:
        source = project_root / doc_file
        target = docs_dir / doc_file
        
        if source.exists() and not target.exists():
            shutil.move(str(source), str(target))
            print(f"   📄 Déplacé: {doc_file} → docs/")
            moved_docs += 1
    
    # 7. Résumé final
    print("\n" + "=" * 50)
    print("✅ NETTOYAGE TERMINÉ")
    print(f"📊 Statistiques:")
    print(f"   - Fichiers supprimés: {files_removed}")
    print(f"   - Dossiers supprimés: {dirs_removed}")
    print(f"   - Documents organisés: {moved_docs}")
    
    if missing_files:
        print(f"\n⚠️ Attention: {len(missing_files)} fichiers essentiels manquants")
    else:
        print(f"\n🎯 Projet prêt pour le commit!")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    success = cleanup_project()
    if not success:
        print("\n❌ Nettoyage incomplet. Vérifiez les fichiers manquants.")
        exit(1)
    else:
        print("\n✅ Nettoyage réussi. Projet prêt!")
        exit(0)
