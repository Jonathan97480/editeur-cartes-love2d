#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire Git avec environnement Python configuré
Évite les erreurs "Python est introuvable" dans les hooks Git
"""

import os
import sys
import subprocess
from pathlib import Path

def get_python_executable():
    """Retourne le chemin vers l'exécutable Python correct"""
    conda_python = r"C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe"
    if os.path.exists(conda_python):
        return conda_python
    return sys.executable

def run_git_command(git_args, cwd=None):
    """Exécute une commande git avec gestion d'erreur"""
    try:
        result = subprocess.run(
            ["git"] + git_args,
            cwd=cwd or os.getcwd(),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result
    except Exception as e:
        print(f"Erreur lors de l'exécution git: {e}")
        return None

def run_tests():
    """Lance les tests avec le bon environnement Python"""
    python_exe = get_python_executable()
    print(f"🧪 Lancement des tests avec {python_exe}")
    
    result = subprocess.run([
        python_exe, "app_final.py", "--test"
    ], capture_output=True, text=True, encoding='utf-8', errors='replace')
    
    return result.returncode == 0, result.stdout, result.stderr

def git_status():
    """Affiche le statut Git"""
    print("📊 STATUT GIT")
    print("=" * 40)
    
    result = run_git_command(["status"])
    if result:
        print(result.stdout)
    
    print("\n📋 Derniers commits:")
    result = run_git_command(["log", "--oneline", "-5"])
    if result:
        print(result.stdout)

def git_add_all():
    """Ajoute tous les fichiers modifiés"""
    print("📝 Ajout de tous les fichiers modifiés...")
    result = run_git_command(["add", "."])
    if result and result.returncode == 0:
        print("✅ Fichiers ajoutés")
        return True
    else:
        print("❌ Erreur lors de l'ajout des fichiers")
        return False

def git_commit_with_validation(message):
    """Fait un commit avec validation préalable et sécurité"""
    print("� VALIDATION PRE-COMMIT AVEC SÉCURITÉ")
    print("=" * 50)
    
    # Étape 1: Tests rapides
    print("🧪 Tests rapides...")
    success, stdout, stderr = run_tests()
    if not success:
        print("❌ Tests rapides échoués - Commit annulé")
        print("Sortie des tests:")
        print(stdout)
        if stderr:
            print("Erreurs:")
            print(stderr)
        return False
    
    print("✅ Tests rapides OK")
    
    # Étape 2: Test de sécurité rapide (éviter les timeouts)
    print("\n🔒 Test de sécurité rapide...")
    python_exe = get_python_executable()
    
    # Test simple et rapide
    quick_security = subprocess.run([
        "dev\\test_quick_security.bat"
    ], capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
    
    if quick_security.returncode != 0:
        print("❌ TEST DE SÉCURITÉ ÉCHOUÉ - Commit bloqué")
        print("\n📋 Rapport de sécurité:")
        print(quick_security.stdout)
        if quick_security.stderr:
            print("\nErreurs:")
            print(quick_security.stderr)
        
        print(f"\n📄 Consultez les rapports détaillés dans: commit_reports/")
        return False
    
    print("✅ Audit de sécurité réussi - Commit autorisé")
    
    # Étape 3: Faire le commit
    print(f"\n💾 Création du commit: '{message}'")
    result = run_git_command(["commit", "-m", message])
    if result and result.returncode == 0:
        print("✅ Commit créé avec succès !")
        print(result.stdout)
        
        # Afficher les rapports générés
        import glob
        from datetime import datetime
        today = datetime.now().strftime("%Y%m%d")
        recent_reports = glob.glob(f"commit_reports/commit_report_{today}*.md")
        if recent_reports:
            latest_report = max(recent_reports)
            print(f"\n📄 Rapport de sécurité: {latest_report}")
        
        return True
    else:
        print("❌ Erreur lors du commit")
        if result:
            print(result.stderr)
        return False

def git_push_with_validation():
    """Push avec validation préalable"""
    print("📤 PUSH AVEC VALIDATION")
    print("=" * 40)
    
    # Tests préalables
    success, stdout, stderr = run_tests()
    if not success:
        print("❌ Tests échoués - Push annulé")
        return False
    
    print("✅ Tests OK - Proceeding avec le push")
    
    # Push
    result = run_git_command(["push", "origin", "main"])
    if result and result.returncode == 0:
        print("✅ Push réussi !")
        return True
    else:
        print("❌ Erreur lors du push")
        if result:
            print(result.stderr)
        return False

def interactive_menu():
    """Menu interactif pour Git"""
    while True:
        print("\n🔧 GESTIONNAIRE GIT")
        print("=" * 30)
        print("1. Voir le statut")
        print("2. Ajouter tous les fichiers")
        print("3. Faire un commit")
        print("4. Push vers origin")
        print("5. Commit + Push")
        print("6. Lancer les tests")
        print("0. Quitter")
        
        choice = input("\nChoisissez une option: ").strip()
        
        if choice == "1":
            git_status()
        elif choice == "2":
            git_add_all()
        elif choice == "3":
            message = input("💬 Message de commit: ").strip()
            if message:
                git_commit_with_validation(message)
            else:
                print("❌ Message de commit requis")
        elif choice == "4":
            git_push_with_validation()
        elif choice == "5":
            message = input("💬 Message de commit: ").strip()
            if message:
                if git_add_all() and git_commit_with_validation(message):
                    git_push_with_validation()
            else:
                print("❌ Message de commit requis")
        elif choice == "6":
            success, stdout, stderr = run_tests()
            print("\n📊 Résultats des tests:")
            print(stdout)
            if stderr:
                print("Erreurs:")
                print(stderr)
        elif choice == "0":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Option invalide")

def main():
    """Fonction principale"""
    python_exe = get_python_executable()
    print(f"🐍 GESTIONNAIRE GIT - Python: {python_exe}")
    print("🎯 Évite les erreurs 'Python est introuvable'")
    
    if len(sys.argv) > 1:
        # Mode ligne de commande
        command = sys.argv[1].lower()
        
        if command == "status":
            git_status()
        elif command == "add":
            git_add_all()
        elif command == "commit":
            if len(sys.argv) > 2:
                message = " ".join(sys.argv[2:])
                git_add_all()
                git_commit_with_validation(message)
            else:
                print("❌ Message de commit requis")
        elif command == "push":
            git_push_with_validation()
        elif command == "test":
            success, stdout, stderr = run_tests()
            print(stdout)
            if stderr:
                print(stderr)
        else:
            print(f"❌ Commande inconnue: {command}")
    else:
        # Mode interactif
        interactive_menu()

if __name__ == "__main__":
    main()
