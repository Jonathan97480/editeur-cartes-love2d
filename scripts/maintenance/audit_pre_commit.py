#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT PRÉ-COMMIT - FONCTIONNALITÉ FAVORIS
=========================================
Audit complet avant commit de la fonctionnalité favoris
"""

import os
import sys
import sqlite3
import importlib.util
from pathlib import Path

def audit_pre_commit():
    """Effectue un audit complet avant commit."""
    print("🔍 AUDIT PRÉ-COMMIT - FONCTIONNALITÉ FAVORIS")
    print("=" * 60)
    
    errors = []
    warnings = []
    success_count = 0
    
    # 1. Vérification de la structure des fichiers
    print("\n1️⃣ VÉRIFICATION DE LA STRUCTURE")
    print("-" * 40)
    
    essential_files = {
        "app_final.py": "Application principale",
        "lib/database.py": "Module base de données",
        "lib/favorites_manager.py": "Gestionnaire de favoris",
        "lib/text_formatting_editor.py": "Éditeur de formatage",
        "tests/test_formatting_favorites.py": "Tests des favoris",
        "data/cartes.db": "Base de données"
    }
    
    for file_path, description in essential_files.items():
        if Path(file_path).exists():
            print(f"   ✅ {file_path} - {description}")
            success_count += 1
        else:
            error_msg = f"Fichier manquant: {file_path}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
    
    # 2. Vérification de la base de données
    print("\n2️⃣ VÉRIFICATION DE LA BASE DE DONNÉES")
    print("-" * 40)
    
    try:
        db_path = "data/cartes.db"
        if Path(db_path).exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Vérifier la table formatting_favorites
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formatting_favorites'")
            if cursor.fetchone():
                print("   ✅ Table formatting_favorites existe")
                success_count += 1
                
                # Vérifier les colonnes
                cursor.execute("PRAGMA table_info(formatting_favorites)")
                columns = cursor.fetchall()
                expected_columns = 25  # 1 id + 1 title + 23 paramètres de formatage
                
                if len(columns) >= expected_columns:
                    print(f"   ✅ Structure de table correcte ({len(columns)} colonnes)")
                    success_count += 1
                else:
                    error_msg = f"Structure de table incorrecte: {len(columns)} colonnes (attendu: {expected_columns})"
                    print(f"   ❌ {error_msg}")
                    errors.append(error_msg)
            else:
                error_msg = "Table formatting_favorites manquante"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
            
            conn.close()
        else:
            error_msg = "Base de données manquante"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
            
    except Exception as e:
        error_msg = f"Erreur base de données: {str(e)}"
        print(f"   ❌ {error_msg}")
        errors.append(error_msg)
    
    # 3. Vérification des imports Python
    print("\n3️⃣ VÉRIFICATION DES IMPORTS")
    print("-" * 40)
    
    modules_to_test = [
        ("lib.database", "Module database"),
        ("lib.favorites_manager", "Gestionnaire favoris"),
        ("lib.text_formatting_editor", "Éditeur formatage")
    ]
    
    sys.path.insert(0, 'lib')
    
    for module_name, description in modules_to_test:
        try:
            if module_name.startswith('lib.'):
                module_name = module_name[4:]  # Enlever 'lib.'
            
            spec = importlib.util.spec_from_file_location(module_name, f"lib/{module_name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            print(f"   ✅ {module_name} - {description}")
            success_count += 1
        except Exception as e:
            error_msg = f"Erreur import {module_name}: {str(e)}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
    
    # 4. Vérification du gestionnaire de favoris
    print("\n4️⃣ VÉRIFICATION DU GESTIONNAIRE DE FAVORIS")
    print("-" * 40)
    
    try:
        from favorites_manager import FavoritesManager
        
        # Test d'instanciation
        fm = FavoritesManager("data/cartes.db")
        print("   ✅ Instanciation du FavoritesManager")
        success_count += 1
        
        # Test des méthodes principales
        methods_to_test = ['save_favorite', 'load_favorite', 'get_all_favorites_status']
        for method_name in methods_to_test:
            if hasattr(fm, method_name):
                print(f"   ✅ Méthode {method_name} présente")
                success_count += 1
            else:
                error_msg = f"Méthode manquante: {method_name}"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
                
    except Exception as e:
        error_msg = f"Erreur gestionnaire favoris: {str(e)}"
        print(f"   ❌ {error_msg}")
        errors.append(error_msg)
    
    # 5. Vérification des tests
    print("\n5️⃣ VÉRIFICATION DES TESTS")
    print("-" * 40)
    
    test_file = "tests/test_formatting_favorites.py"
    if Path(test_file).exists():
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier la présence des classes de test
            test_classes = [
                'TestFormattingFavoritesDatabase',
                'TestFavoritesManager', 
                'TestIntegrationFormattingFavorites'
            ]
            
            for test_class in test_classes:
                if test_class in content:
                    print(f"   ✅ Classe de test {test_class}")
                    success_count += 1
                else:
                    warning_msg = f"Classe de test manquante: {test_class}"
                    print(f"   ⚠️ {warning_msg}")
                    warnings.append(warning_msg)
            
            # Compter les méthodes de test
            test_methods = content.count('def test_')
            if test_methods >= 10:
                print(f"   ✅ {test_methods} méthodes de test trouvées")
                success_count += 1
            else:
                warning_msg = f"Peu de méthodes de test: {test_methods}"
                print(f"   ⚠️ {warning_msg}")
                warnings.append(warning_msg)
                
        except Exception as e:
            error_msg = f"Erreur lecture tests: {str(e)}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
    else:
        error_msg = "Fichier de tests manquant"
        print(f"   ❌ {error_msg}")
        errors.append(error_msg)
    
    # 6. Vérification de l'éditeur de texte
    print("\n6️⃣ VÉRIFICATION DE L'ÉDITEUR DE TEXTE")
    print("-" * 40)
    
    editor_file = "lib/text_formatting_editor.py"
    if Path(editor_file).exists():
        try:
            with open(editor_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier la présence des méthodes de favoris
            favorites_methods = [
                'add_to_favorites',
                'load_favorite', 
                'update_favorite_buttons'
            ]
            
            for method in favorites_methods:
                if method in content:
                    print(f"   ✅ Méthode {method} présente")
                    success_count += 1
                else:
                    error_msg = f"Méthode manquante dans l'éditeur: {method}"
                    print(f"   ❌ {error_msg}")
                    errors.append(error_msg)
            
            # Vérifier la présence des boutons favoris
            if '"★ Ajouter Favoris"' in content:
                print("   ✅ Bouton 'Ajouter aux Favoris' présent")
                success_count += 1
            else:
                error_msg = "Bouton 'Ajouter aux Favoris' manquant"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
            
            # Vérifier les 3 boutons de favoris
            if 'self.favorite_buttons' in content and 'for i in [1, 2, 3]:' in content:
                print("   ✅ Boutons Favoris 1, 2, 3 présents")
                success_count += 3
            else:
                error_msg = "Boutons Favoris manquants"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
                    
        except Exception as e:
            error_msg = f"Erreur lecture éditeur: {str(e)}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
    else:
        error_msg = "Fichier éditeur manquant"
        print(f"   ❌ {error_msg}")
        errors.append(error_msg)
    
    # 7. Vérification de la documentation
    print("\n7️⃣ VÉRIFICATION DE LA DOCUMENTATION")
    print("-" * 40)
    
    doc_files = [
        "docs/FAVORIS_FORMATAGE_IMPLEMENTATION.md",
        "docs/GUIDE_LANCEMENT.md",
        "docs/RAPPORT_AUDIT_FINAL.md",
        "RAPPORT_FINAL_COMMIT.md"
    ]
    
    for doc_file in doc_files:
        if Path(doc_file).exists():
            print(f"   ✅ {doc_file}")
            success_count += 1
        else:
            warning_msg = f"Documentation manquante: {doc_file}"
            print(f"   ⚠️ {warning_msg}")
            warnings.append(warning_msg)
    
    # 8. Vérification des fichiers de lancement
    print("\n8️⃣ VÉRIFICATION DES FICHIERS DE LANCEMENT")
    print("-" * 40)
    
    launch_files = [
        "START.bat",
        "launch_simple.bat",
        "app_final.py"
    ]
    
    for launch_file in launch_files:
        if Path(launch_file).exists():
            print(f"   ✅ {launch_file}")
            success_count += 1
        else:
            warning_msg = f"Fichier de lancement manquant: {launch_file}"
            print(f"   ⚠️ {warning_msg}")
            warnings.append(warning_msg)
    
    # RÉSUMÉ FINAL
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE L'AUDIT PRÉ-COMMIT")
    print("=" * 60)
    
    total_checks = success_count + len(errors)
    success_rate = (success_count / total_checks * 100) if total_checks > 0 else 0
    
    print(f"✅ Vérifications réussies: {success_count}")
    print(f"❌ Erreurs critiques: {len(errors)}")
    print(f"⚠️ Avertissements: {len(warnings)}")
    print(f"📈 Taux de réussite: {success_rate:.1f}%")
    
    if errors:
        print(f"\n🚨 ERREURS CRITIQUES À CORRIGER:")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
    
    if warnings:
        print(f"\n⚠️ AVERTISSEMENTS:")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    
    # Verdict final
    print(f"\n{'=' * 60}")
    if len(errors) == 0:
        if len(warnings) == 0:
            print("🎉 AUDIT PARFAIT - PRÊT POUR LE COMMIT!")
            verdict = "PARFAIT"
        else:
            print("✅ AUDIT RÉUSSI - PRÊT POUR LE COMMIT (avec avertissements mineurs)")
            verdict = "RÉUSSI"
    else:
        print("❌ AUDIT ÉCHOUÉ - CORRIGER LES ERREURS AVANT LE COMMIT")
        verdict = "ÉCHOUÉ"
    
    print(f"{'=' * 60}")
    
    return {
        'verdict': verdict,
        'success_count': success_count,
        'errors': errors,
        'warnings': warnings,
        'success_rate': success_rate
    }

if __name__ == "__main__":
    try:
        result = audit_pre_commit()
        
        # Code de sortie
        if result['verdict'] == "ÉCHOUÉ":
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"\n💥 ERREUR FATALE DANS L'AUDIT: {str(e)}")
        sys.exit(2)
