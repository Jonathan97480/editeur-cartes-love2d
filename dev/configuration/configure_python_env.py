#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration de l'environnement Python pour le projet
Évite l'erreur "Python est introuvable" en utilisant le bon environnement
"""

import os
import sys
import subprocess

# Configuration pour éviter les problèmes d'encodage Unicode
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from pathlib import Path

def get_python_executable():
    """Retourne le chemin vers l'exécutable Python correct"""
    # Chemin vers l'environnement Conda configuré
    conda_python = r"C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe"
    
    if os.path.exists(conda_python):
        return conda_python
    
    # Fallback vers l'exécutable Python actuel
    return sys.executable

def run_python_command(command_args, cwd=None):
    """Exécute une commande Python avec le bon environnement"""
    python_exe = get_python_executable()
    
    if isinstance(command_args, str):
        # Si c'est une chaîne, on l'ajoute après l'exécutable
        full_command = [python_exe] + command_args.split()
    else:
        # Si c'est déjà une liste
        full_command = [python_exe] + list(command_args)
    
    try:
        result = subprocess.run(
            full_command,
            cwd=cwd or os.getcwd(),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        return None

def test_environment():
    """Teste que l'environnement Python fonctionne"""
    print("🔍 Test de l'environnement Python...")
    
    python_exe = get_python_executable()
    print(f"📍 Exécutable Python: {python_exe}")
    
    # Test version
    result = run_python_command(["--version"])
    if result and result.returncode == 0:
        print(f"✅ Version: {result.stdout.strip()}")
    else:
        print("❌ Impossible de récupérer la version")
        return False
    
    # Test import basique
    result = run_python_command(["-c", "import sys; print('Python OK')"])
    if result and result.returncode == 0:
        print("✅ Import basique: OK")
    else:
        print("❌ Problème avec les imports")
        return False
    
    # Test du projet
    if os.path.exists("app_final.py"):
        result = run_python_command(["app_final.py", "--test"])
        if result and result.returncode == 0:
            print("✅ Tests du projet: OK")
        else:
            print("⚠️  Tests du projet: Quelques problèmes détectés")
    
    return True

def create_run_script():
    """Crée un script pour lancer l'application avec le bon Python"""
    python_exe = get_python_executable()
    
    # Script Windows (.bat)
    script_content_bat = f'''@echo off
echo Lancement de l'editeur de cartes Love2D...
"{python_exe}" app_final.py %*
pause
'''
    
    with open("run_app.bat", "w", encoding="utf-8") as f:
        f.write(script_content_bat)
    
    # Script PowerShell (.ps1)
    script_content_ps1 = f'''# Lancement de l'editeur de cartes Love2D
Write-Host "Lancement de l'editeur de cartes Love2D..." -ForegroundColor Green
& "{python_exe}" app_final.py $args
Read-Host "Appuyez sur Entree pour fermer"
'''
    
    with open("run_app.ps1", "w", encoding="utf-8") as f:
        f.write(script_content_ps1)
    
    print("✅ Scripts de lancement créés:")
    print("   - run_app.bat (Windows)")
    print("   - run_app.ps1 (PowerShell)")

def create_test_script():
    """Crée un script pour lancer les tests avec le bon Python"""
    python_exe = get_python_executable()
    
    script_content = f'''@echo off
echo Lancement des tests...
"{python_exe}" app_final.py --test
pause
'''
    
    with open("run_tests.bat", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ Script de tests créé: run_tests.bat")

def create_organize_script():
    """Crée un script pour l'organisation avec le bon Python"""
    python_exe = get_python_executable()
    
    script_content = f'''@echo off
echo Organisation automatique du projet...
"{python_exe}" organiser_projet.py
pause
'''
    
    with open("run_organize.bat", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ Script d'organisation créé: run_organize.bat")

def main():
    """Fonction principale"""
    # Gérer l'argument --validate pour les tests de sécurité
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        print("Validation environnement Python...")
        if test_environment():
            print("✅ Environnement Python valide")
            return True
        else:
            print("❌ Problème environnement Python")
            return False
    
    print("Configuration de l'environnement Python")
    print("=" * 50)
    
    if test_environment():
        print("\n🛠️  Création des scripts de lancement...")
        create_run_script()
        create_test_script()
        create_organize_script()
        
        print("\n🎉 Configuration terminée avec succès !")
        print("\n💡 Utilisation:")
        print("   • Double-cliquez sur run_app.bat pour lancer l'application")
        print("   • Double-cliquez sur run_tests.bat pour lancer les tests")
        print("   • Double-cliquez sur run_organize.bat pour organiser le projet")
        print("\n📝 Note: Ces scripts utilisent le bon environnement Python")
        print("   et évitent l'erreur 'Python est introuvable'")
        return True
    else:
        print("\n❌ Problème avec l'environnement Python")
        print("Veuillez vérifier votre installation Python/Conda")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
