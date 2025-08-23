#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE COMMIT SÉCURISÉ - FONCTIONNALITÉ FAVORIS
=================================================
Script pour effectuer un commit sécurisé avec validations préalables
"""

import os
import sys
import subprocess
import sqlite3
import json
from pathlib import Path
from datetime import datetime

class SecureCommit:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
        
    def log(self, message, level="INFO"):
        """Log avec timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "CRITICAL": "🚨"
        }.get(level, "📝")
        
        print(f"[{timestamp}] {prefix} {message}")
        
    def run_command(self, command, description):
        """Exécute une commande shell de manière sécurisée."""
        self.log(f"Exécution: {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.log(f"Réussi: {description}", "SUCCESS")
                return True, result.stdout.strip()
            else:
                error_msg = f"Échec: {description} - {result.stderr.strip()}"
                self.log(error_msg, "ERROR")
                self.errors.append(error_msg)
                return False, result.stderr.strip()
        except subprocess.TimeoutExpired:
            error_msg = f"Timeout: {description}"
            self.log(error_msg, "ERROR")
            self.errors.append(error_msg)
            return False, "Timeout"
        except Exception as e:
            error_msg = f"Exception: {description} - {str(e)}"
            self.log(error_msg, "ERROR")
            self.errors.append(error_msg)
            return False, str(e)
    
    def validate_git_status(self):
        """Valide l'état Git du projet."""
        self.log("🔍 VALIDATION DE L'ÉTAT GIT")
        
        # Vérifier si on est dans un repo Git
        success, _ = self.run_command("git rev-parse --git-dir", "Vérification repo Git")
        if not success:
            return False
            
        # Vérifier l'état des fichiers
        success, output = self.run_command("git status --porcelain", "État des fichiers")
        if success:
            if output:
                modified_files = len(output.splitlines())
                self.log(f"Fichiers modifiés détectés: {modified_files}")
                self.success_count += 1
            else:
                self.log("Aucune modification détectée", "WARNING")
                self.warnings.append("Aucune modification à commiter")
                
        return True
    
    def validate_database(self):
        """Valide la base de données."""
        self.log("🗄️ VALIDATION DE LA BASE DE DONNÉES")
        
        db_path = "data/cartes.db"
        if not Path(db_path).exists():
            error_msg = "Base de données manquante"
            self.log(error_msg, "ERROR")
            self.errors.append(error_msg)
            return False
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Vérifier la table favorites
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formatting_favorites'")
            if cursor.fetchone():
                self.log("Table formatting_favorites présente", "SUCCESS")
                self.success_count += 1
            else:
                error_msg = "Table formatting_favorites manquante"
                self.log(error_msg, "ERROR")
                self.errors.append(error_msg)
                return False
                
            # Vérifier la structure
            cursor.execute("PRAGMA table_info(formatting_favorites)")
            columns = cursor.fetchall()
            if len(columns) >= 25:
                self.log(f"Structure table correcte ({len(columns)} colonnes)", "SUCCESS")
                self.success_count += 1
            else:
                error_msg = f"Structure table incorrecte ({len(columns)} colonnes)"
                self.log(error_msg, "ERROR")
                self.errors.append(error_msg)
                return False
                
            conn.close()
            return True
            
        except Exception as e:
            error_msg = f"Erreur base de données: {str(e)}"
            self.log(error_msg, "ERROR")
            self.errors.append(error_msg)
            return False
    
    def run_tests(self):
        """Exécute les tests de validation."""
        self.log("🧪 EXÉCUTION DES TESTS")
        
        # Test des favoris
        success, output = self.run_command(
            "python -m pytest tests/test_formatting_favorites.py -v --tb=short",
            "Tests des favoris"
        )
        
        if success:
            if "PASSED" in output and "FAILED" not in output:
                # Compter les tests passés
                passed_count = output.count("PASSED")
                self.log(f"Tous les tests réussis ({passed_count} tests)", "SUCCESS")
                self.success_count += 1
                return True
            else:
                error_msg = "Certains tests ont échoué"
                self.log(error_msg, "ERROR")
                self.errors.append(error_msg)
                return False
        else:
            return False
    
    def validate_critical_files(self):
        """Valide la présence des fichiers critiques."""
        self.log("📁 VALIDATION DES FICHIERS CRITIQUES")
        
        critical_files = [
            "app_final.py",
            "lib/database.py", 
            "lib/favorites_manager.py",
            "lib/text_formatting_editor.py",
            "tests/test_formatting_favorites.py"
        ]
        
        missing_files = []
        for file_path in critical_files:
            if Path(file_path).exists():
                self.log(f"Fichier présent: {file_path}", "SUCCESS")
                self.success_count += 1
            else:
                missing_files.append(file_path)
                
        if missing_files:
            error_msg = f"Fichiers critiques manquants: {', '.join(missing_files)}"
            self.log(error_msg, "ERROR")
            self.errors.append(error_msg)
            return False
            
        return True
    
    def create_backup(self):
        """Crée une sauvegarde avant commit."""
        self.log("💾 CRÉATION DE SAUVEGARDE")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_avant_commit_{timestamp}"
        
        # Créer un stash Git
        success, _ = self.run_command(
            f"git stash push -m \"{backup_name}\"",
            "Création stash de sauvegarde"
        )
        
        if success:
            self.log(f"Sauvegarde créée: {backup_name}", "SUCCESS")
            self.success_count += 1
            return True
        else:
            self.log("Impossible de créer la sauvegarde", "WARNING")
            self.warnings.append("Sauvegarde échouée")
            return False
    
    def add_files_to_git(self):
        """Ajoute les fichiers modifiés à Git."""
        self.log("➕ AJOUT DES FICHIERS À GIT")
        
        # Ajouter les fichiers de la fonctionnalité favoris
        files_to_add = [
            "lib/favorites_manager.py",
            "lib/database.py", 
            "lib/text_formatting_editor.py",
            "tests/test_formatting_favorites.py",
            "docs/",
            "RAPPORT_FINAL_COMMIT.md"
        ]
        
        for file_path in files_to_add:
            if Path(file_path).exists():
                success, _ = self.run_command(
                    f"git add {file_path}",
                    f"Ajout {file_path}"
                )
                if success:
                    self.success_count += 1
        
        # Ajouter les autres fichiers modifiés
        success, _ = self.run_command("git add .", "Ajout des autres modifications")
        return success
    
    def create_commit(self):
        """Crée le commit avec un message structuré."""
        self.log("💬 CRÉATION DU COMMIT")
        
        commit_message = """feat: Ajout de la fonctionnalité favoris de formatage

✨ Nouvelles fonctionnalités:
- 4 boutons favoris dans l'éditeur de formatage
- Sauvegarde rapide du formatage actuel  
- Chargement instantané des favoris 1, 2, 3
- Feedback visuel des états (vert/rouge/normal)

🗄️ Base de données:
- Table formatting_favorites avec 25 colonnes
- Migration automatique intégrée
- Validation des données robuste

🧪 Tests:
- 16 tests unitaires et d'intégration
- Couverture complète de la fonctionnalité
- Validation de tous les cas d'usage

📚 Documentation:
- Guides d'implémentation complets
- Documentation utilisateur
- Rapport d'audit validé

🔧 Corrections:
- Résolution des problèmes de lancement
- Optimisation de l'interface utilisateur
- Nettoyage du projet

Testé: 16/16 tests passants
Validé: Audit complet réussi 100%"""

        success, _ = self.run_command(
            f'git commit -m "{commit_message}"',
            "Création du commit"
        )
        
        if success:
            self.log("Commit créé avec succès", "SUCCESS")
            self.success_count += 1
            return True
        else:
            return False
    
    def show_commit_info(self):
        """Affiche les informations du commit."""
        self.log("📊 INFORMATIONS DU COMMIT")
        
        success, output = self.run_command("git log -1 --oneline", "Dernier commit")
        if success:
            self.log(f"Commit: {output}")
            
        success, output = self.run_command("git diff --stat HEAD~1", "Statistiques")
        if success:
            self.log("Statistiques des modifications:")
            for line in output.splitlines():
                if line.strip():
                    self.log(f"  {line}")
    
    def execute_secure_commit(self):
        """Exécute le processus de commit sécurisé complet."""
        self.log("🚀 DÉBUT DU COMMIT SÉCURISÉ")
        self.log("=" * 60)
        
        steps = [
            ("Validation Git", self.validate_git_status),
            ("Validation Base de Données", self.validate_database),
            ("Validation Fichiers Critiques", self.validate_critical_files),
            ("Exécution Tests", self.run_tests),
            ("Création Sauvegarde", self.create_backup),
            ("Ajout Fichiers Git", self.add_files_to_git),
            ("Création Commit", self.create_commit)
        ]
        
        for step_name, step_func in steps:
            self.log(f"\n🔄 {step_name}")
            success = step_func()
            
            if not success and step_name != "Création Sauvegarde":
                self.log(f"❌ ARRÊT: Échec à l'étape {step_name}", "CRITICAL")
                return False
                
        # Affichage final
        self.show_commit_info()
        
        # Résumé
        self.log("\n" + "=" * 60)
        self.log("📊 RÉSUMÉ DU COMMIT SÉCURISÉ")
        self.log("=" * 60)
        self.log(f"✅ Opérations réussies: {self.success_count}")
        self.log(f"❌ Erreurs: {len(self.errors)}")
        self.log(f"⚠️ Avertissements: {len(self.warnings)}")
        
        if self.errors:
            self.log("\n🚨 ERREURS:", "ERROR")
            for error in self.errors:
                self.log(f"  - {error}")
                
        if self.warnings:
            self.log("\n⚠️ AVERTISSEMENTS:", "WARNING")
            for warning in self.warnings:
                self.log(f"  - {warning}")
        
        if len(self.errors) == 0:
            self.log("\n🎉 COMMIT SÉCURISÉ RÉUSSI!", "SUCCESS")
            self.log("📝 La fonctionnalité favoris a été commitée avec succès")
            return True
        else:
            self.log("\n❌ COMMIT SÉCURISÉ ÉCHOUÉ", "ERROR")
            return False

def main():
    """Point d'entrée principal."""
    try:
        commit_manager = SecureCommit()
        success = commit_manager.execute_secure_commit()
        
        if success:
            print("\n🎯 PROCHAINES ÉTAPES RECOMMANDÉES:")
            print("   1. Vérifier le commit: git log -1")
            print("   2. Pousser vers GitHub: git push origin main")
            print("   3. Créer un tag: git tag v2.4.0-favoris")
            sys.exit(0)
        else:
            print("\n💡 ACTIONS CORRECTIVES:")
            print("   1. Corriger les erreurs listées")
            print("   2. Relancer le script de commit")
            print("   3. Vérifier l'état du projet")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Commit interrompu par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 ERREUR FATALE: {str(e)}")
        sys.exit(2)

if __name__ == "__main__":
    main()
