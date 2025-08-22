#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT COMPLET DE L'ÉDITEUR DE CARTES LOVE2D
============================================

Script d'audit automatisé pour évaluer tous les aspects du projet :
- Structure des fichiers
- Imports et modules
- Base de données
- Export Love2D
- Tests unitaires
- Intégration système
"""

import os
import sys
import sqlite3
import tempfile
from datetime import datetime
import unittest
import io
from contextlib import redirect_stderr

# Ajouter les chemins nécessaires
sys.path.insert(0, 'lib')
sys.path.insert(0, '.')

class AuditComplet:
    def __init__(self):
        self.scores = {}
        self.details = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def audit_structure_fichiers(self):
        """Test de la structure des fichiers essentiels"""
        print("1. AUDIT STRUCTURE DES FICHIERS")
        print("-" * 40)
        
        fichiers_essentiels = [
            "app_final.py",
            "data/cartes.db",
            "lib/config.py",
            "lib/database.py",
            "lib/ui_components.py", 
            "lib/utils.py",
            "lib/text_formatting_editor.py",
            "lib/lua_export.py",
            "lib/tests.py"
        ]
        
        fichiers_presents = []
        tailles = {}
        
        for fichier in fichiers_essentiels:
            if os.path.exists(fichier):
                fichiers_presents.append(fichier)
                taille = os.path.getsize(fichier)
                tailles[fichier] = taille
                print(f"✅ {fichier}: {taille:,} octets")
            else:
                print(f"❌ {fichier}: MANQUANT")
        
        pourcentage = (len(fichiers_presents) / len(fichiers_essentiels)) * 100
        
        if pourcentage == 100:
            print("✅ Structure: PARFAITE")
            score = 100
        elif pourcentage >= 90:
            print("⚠️ Structure: EXCELLENTE")
            score = 95
        elif pourcentage >= 80:
            print("⚠️ Structure: BONNE")
            score = 85
        else:
            print("❌ Structure: PROBLÉMATIQUE")
            score = 60
            
        self.scores['structure'] = score
        self.details['structure'] = {
            'fichiers_presents': len(fichiers_presents),
            'fichiers_total': len(fichiers_essentiels),
            'pourcentage': pourcentage,
            'tailles': tailles
        }
        
        print(f"Score structure: {score}%\n")
        return score
    
    def audit_imports_modules(self):
        """Test des imports et modules"""
        print("2. AUDIT IMPORTS ET MODULES")
        print("-" * 40)
        
        modules_a_tester = [
            'config',
            'utils', 
            'database',
            'ui_components',
            'text_formatting_editor',
            'lua_export',
            'tests',
            'database_migration',
            'game_package_exporter'
        ]
        
        modules_ok = []
        modules_erreur = []
        
        for module in modules_a_tester:
            try:
                __import__(module)
                modules_ok.append(module)
                print(f"✅ {module}: Import réussi")
            except Exception as e:
                modules_erreur.append((module, str(e)))
                print(f"❌ {module}: {e}")
        
        pourcentage = (len(modules_ok) / len(modules_a_tester)) * 100
        
        if pourcentage == 100:
            print("✅ Imports: PARFAITS")
            score = 100
        elif pourcentage >= 90:
            print("⚠️ Imports: EXCELLENTS")
            score = 95
        elif pourcentage >= 80:
            print("⚠️ Imports: BONS")
            score = 85
        else:
            print("❌ Imports: PROBLÉMATIQUES")
            score = 60
            
        self.scores['imports'] = score
        self.details['imports'] = {
            'modules_ok': len(modules_ok),
            'modules_total': len(modules_a_tester),
            'pourcentage': pourcentage,
            'erreurs': modules_erreur
        }
        
        print(f"Score imports: {score}%\n")
        return score
    
    def audit_base_donnees(self):
        """Test de la base de données"""
        print("3. AUDIT BASE DE DONNÉES")
        print("-" * 40)
        
        try:
            from database import CardRepo
            from config import DB_FILE
            
            # Test connexion
            repo = CardRepo(DB_FILE)
            cards = repo.list_cards()
            nb_cartes = len(cards)
            
            print(f"📊 Cartes dans la base: {nb_cartes}")
            
            # Test structure de la base
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(cards)")
            colonnes = cursor.fetchall()
            nb_colonnes = len(colonnes)
            
            # Compter les colonnes de formatage
            colonnes_formatage = [col for col in colonnes if any(fmt in col[1] for fmt in ['title_', 'text_', 'line_spacing', 'text_wrap'])]
            nb_formatage = len(colonnes_formatage)
            
            print(f"📊 Colonnes totales: {nb_colonnes}")
            print(f"📊 Colonnes formatage: {nb_formatage}")
            
            conn.close()
            
            # Calcul du score
            if nb_cartes >= 5 and nb_colonnes >= 30 and nb_formatage >= 15:
                print("✅ Base de données: PARFAITE")
                score = 100
            elif nb_cartes >= 3 and nb_colonnes >= 25:
                print("⚠️ Base de données: EXCELLENTE")
                score = 90
            elif nb_cartes >= 1 and nb_colonnes >= 20:
                print("⚠️ Base de données: BONNE")
                score = 80
            else:
                print("❌ Base de données: PROBLÉMATIQUE")
                score = 60
                
        except Exception as e:
            print(f"❌ Erreur base de données: {e}")
            score = 0
            nb_cartes = 0
            nb_colonnes = 0
            nb_formatage = 0
            
        self.scores['database'] = score
        self.details['database'] = {
            'nb_cartes': nb_cartes,
            'nb_colonnes': nb_colonnes,
            'nb_formatage': nb_formatage
        }
        
        print(f"Score base de données: {score}%\n")
        return score
    
    def audit_export_love2d(self):
        """Test de l'export Love2D"""
        print("4. AUDIT EXPORT LOVE2D")
        print("-" * 40)
        
        try:
            from lua_exporter_love2d import Love2DLuaExporter
            from database import CardRepo
            from config import DB_FILE
            
            repo = CardRepo(DB_FILE)
            exporter = Love2DLuaExporter(repo)
            
            # Générer export
            content = exporter.export_all_cards_love2d()
            taille = len(content)
            
            print(f"📄 Export généré: {taille:,} caractères")
            
            # Vérifications
            has_textformatting = 'TextFormatting' in content
            has_cards_data = 'cards =' in content  # Format corrigé
            has_return = 'return cards' in content  # Format corrigé
            has_local_cards = 'local cards' in content  # Format corrigé
            
            print(f"✅ TextFormatting: {'OUI' if has_textformatting else 'NON'}")
            print(f"✅ Format cards: {'OUI' if has_cards_data else 'NON'}")
            print(f"✅ Return cards: {'OUI' if has_return else 'NON'}")
            print(f"✅ Local cards: {'OUI' if has_local_cards else 'NON'}")
            
            # Score
            if has_textformatting and has_cards_data and has_return and has_local_cards and taille > 20000:
                print("✅ Export Love2D: PARFAIT")
                score = 100
            elif has_textformatting and taille > 15000:
                print("⚠️ Export Love2D: EXCELLENT")
                score = 90
            elif taille > 10000:
                print("⚠️ Export Love2D: BON")
                score = 80
            else:
                print("❌ Export Love2D: PROBLÉMATIQUE")
                score = 60
                
        except Exception as e:
            print(f"❌ Erreur export: {e}")
            score = 0
            taille = 0
            has_textformatting = False
            
        self.scores['export'] = score
        self.details['export'] = {
            'taille': taille,
            'textformatting': has_textformatting,
            'format_correct': has_cards_data if 'has_cards_data' in locals() else False
        }
        
        print(f"Score export: {score}%\n")
        return score
    
    def audit_tests_unitaires(self):
        """Test des tests unitaires"""
        print("5. AUDIT TESTS UNITAIRES")
        print("-" * 40)
        
        try:
            import tests
            
            # Créer et lancer les tests
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(tests)
            
            # Capturer les résultats
            test_output = io.StringIO()
            with redirect_stderr(test_output):
                runner = unittest.TextTestRunner(stream=test_output, verbosity=0)
                result = runner.run(suite)
            
            tests_run = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)
            success = tests_run - failures - errors
            
            print(f"📊 Tests exécutés: {tests_run}")
            print(f"✅ Réussis: {success}")
            print(f"❌ Échecs: {failures}")
            print(f"⚠️ Erreurs: {errors}")
            
            success_rate = (success / tests_run * 100) if tests_run > 0 else 0
            print(f"📈 Taux de réussite: {success_rate:.1f}%")
            
            if success_rate == 100:
                print("✅ Tests unitaires: PARFAITS")
                score = 100
            elif success_rate >= 90:
                print("⚠️ Tests unitaires: EXCELLENTS")
                score = 90
            elif success_rate >= 80:
                print("⚠️ Tests unitaires: BONS")
                score = 80
            else:
                print("❌ Tests unitaires: PROBLÉMATIQUES")
                score = 60
                
        except Exception as e:
            print(f"❌ Erreur tests: {e}")
            score = 0
            success_rate = 0
            tests_run = 0
            
        self.scores['tests'] = score
        self.details['tests'] = {
            'success_rate': success_rate,
            'tests_run': tests_run
        }
        
        print(f"Score tests: {score}%\n")
        return score
    
    def audit_integration_systeme(self):
        """Test d'intégration système"""
        print("6. AUDIT INTÉGRATION SYSTÈME")
        print("-" * 40)
        
        try:
            # Test intégration complète
            from database import CardRepo
            from config import DB_FILE
            from lua_exporter_love2d import Love2DLuaExporter
            
            repo = CardRepo(DB_FILE)
            cards = repo.list_cards()
            
            if cards:
                # Test export intégré
                exporter = Love2DLuaExporter(repo)
                output_path = os.path.join(tempfile.gettempdir(), 'audit_integration.lua')
                size = exporter.export_to_file(output_path)
                
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifications intégration
                has_all_features = all([
                    'TextFormatting' in content,
                    'local cards' in content,
                    'return cards' in content,
                    size > 20000
                ])
                
                print(f"🎴 Cartes disponibles: {len(cards)}")
                print(f"📄 Export intégré: {size:,} caractères")
                print(f"✅ Intégration complète: {'OUI' if has_all_features else 'NON'}")
                
                if has_all_features:
                    print("✅ Intégration système: PARFAITE")
                    score = 100
                else:
                    print("⚠️ Intégration système: BONNE")
                    score = 85
            else:
                print("❌ Aucune carte pour test intégration")
                score = 60
                
        except Exception as e:
            print(f"❌ Erreur intégration: {e}")
            score = 0
            
        self.scores['integration'] = score
        self.details['integration'] = {
            'integration_complete': has_all_features if 'has_all_features' in locals() else False
        }
        
        print(f"Score intégration: {score}%\n")
        return score
    
    def calculer_score_final(self):
        """Calcul du score final pondéré"""
        print("7. CALCUL SCORE FINAL")
        print("=" * 40)
        
        # Pondération des scores
        weights = {
            'structure': 0.15,    # 15%
            'imports': 0.20,      # 20%
            'database': 0.25,     # 25%
            'export': 0.15,       # 15%
            'tests': 0.15,        # 15%
            'integration': 0.10   # 10%
        }
        
        # Calcul pondéré
        score_final = sum(
            self.scores.get(category, 0) * weight 
            for category, weight in weights.items()
        )
        
        print("📊 DÉTAIL DES SCORES:")
        for category, weight in weights.items():
            score = self.scores.get(category, 0)
            print(f"   {category.capitalize()}: {score}% (poids {weight*100:.0f}%)")
        
        print(f"\n🎯 SCORE FINAL: {score_final:.1f}/100")
        
        # Classification
        if score_final >= 98:
            grade = "PARFAIT"
            emoji = "🏆"
        elif score_final >= 95:
            grade = "EXCELLENT"
            emoji = "🥇"
        elif score_final >= 85:
            grade = "TRÈS BON"
            emoji = "🥈"
        elif score_final >= 75:
            grade = "BON"
            emoji = "🥉"
        elif score_final >= 65:
            grade = "MOYEN"
            emoji = "⚠️"
        else:
            grade = "PROBLÉMATIQUE"
            emoji = "❌"
        
        print(f"{emoji} ÉVALUATION: {grade}")
        
        self.scores['final'] = score_final
        self.details['grade'] = grade
        
        return score_final, grade
    
    def generer_rapport(self):
        """Génère un rapport complet d'audit"""
        print("\n" + "=" * 60)
        print("🏆 RAPPORT D'AUDIT COMPLET")
        print("=" * 60)
        print(f"Date: {self.timestamp}")
        print(f"Projet: Éditeur de cartes Love2D")
        print()
        
        score_final = self.scores.get('final', 0)
        grade = self.details.get('grade', 'INCONNU')
        
        print(f"🎯 SCORE GLOBAL: {score_final:.1f}/100 - {grade}")
        print()
        
        # Détails par catégorie
        if self.details.get('structure'):
            details = self.details['structure']
            print(f"📁 STRUCTURE: {details['fichiers_presents']}/{details['fichiers_total']} fichiers ({details['pourcentage']:.1f}%)")
        
        if self.details.get('imports'):
            details = self.details['imports']
            print(f"📦 IMPORTS: {details['modules_ok']}/{details['modules_total']} modules ({details['pourcentage']:.1f}%)")
        
        if self.details.get('database'):
            details = self.details['database']
            print(f"🗄️ BASE DE DONNÉES: {details['nb_cartes']} cartes, {details['nb_colonnes']} colonnes, {details['nb_formatage']} formatage")
        
        if self.details.get('export'):
            details = self.details['export']
            print(f"📤 EXPORT LOVE2D: {details['taille']:,} caractères, TextFormatting: {'✅' if details['textformatting'] else '❌'}")
        
        if self.details.get('tests'):
            details = self.details['tests']
            print(f"🧪 TESTS: {details['success_rate']:.1f}% de réussite sur {details['tests_run']} tests")
        
        print()
        print("🎉 AUDIT TERMINÉ")
        
        return {
            'score_final': score_final,
            'grade': grade,
            'scores': self.scores,
            'details': self.details,
            'timestamp': self.timestamp
        }
    
    def executer_audit_complet(self):
        """Exécute l'audit complet"""
        print("🔍 DÉMARRAGE AUDIT COMPLET")
        print("=" * 60)
        print(f"Date: {self.timestamp}")
        print()
        
        # Exécuter tous les audits
        self.audit_structure_fichiers()
        self.audit_imports_modules()
        self.audit_base_donnees()
        self.audit_export_love2d()
        self.audit_tests_unitaires()
        self.audit_integration_systeme()
        
        # Calcul final
        self.calculer_score_final()
        
        # Rapport final
        return self.generer_rapport()

def main():
    """Fonction principale d'audit"""
    audit = AuditComplet()
    resultat = audit.executer_audit_complet()
    
    # Sauvegarder le rapport
    with open('rapport_audit.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(resultat, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport sauvegardé: rapport_audit.json")
    
    return resultat

if __name__ == "__main__":
    main()
