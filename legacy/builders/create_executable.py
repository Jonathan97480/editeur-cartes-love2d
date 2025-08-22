#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création d'exécutable pour l'Éditeur de Cartes Love2D
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step_name):
    """Affiche une étape avec style."""
    print(f"\n{'='*60}")
    print(f"🔧 {step_name}")
    print(f"{'='*60}")

def run_command(command, description):
    """Exécute une commande et gère les erreurs."""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} réussi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description.lower()} :")
        print(f"   Commande : {command}")
        print(f"   Code de retour : {e.returncode}")
        if e.stdout:
            print(f"   Sortie : {e.stdout}")
        if e.stderr:
            print(f"   Erreur : {e.stderr}")
        return False

def create_requirements():
    """Crée un fichier requirements.txt s'il n'existe pas."""
    requirements_content = """Pillow>=10.0.0
pyinstaller>=6.0.0
"""
    
    if not os.path.exists("requirements.txt"):
        print("📝 Création du fichier requirements.txt...")
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements_content)
        print("✅ requirements.txt créé")
    else:
        print("ℹ️  requirements.txt existe déjà")

def create_spec_file():
    """Crée un fichier .spec personnalisé pour PyInstaller."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['app_final.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('lib', 'lib'),
        ('README.md', '.'),
        ('GUIDE.md', '.'),
        ('GUIDE_ACTEURS.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'sqlite3',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'json',
        'datetime',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='EditeurCartesLove2D',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EditeurCartesLove2D',
)
'''
    
    print("📝 Création du fichier EditeurCartesLove2D.spec...")
    with open("EditeurCartesLove2D.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("✅ Fichier .spec créé")

def build_executable():
    """Processus principal de création de l'exécutable."""
    print("🚀 CRÉATION D'EXÉCUTABLE - ÉDITEUR DE CARTES LOVE2D")
    print("=" * 65)
    
    # Vérifications préliminaires
    print_step("VÉRIFICATIONS PRÉLIMINAIRES")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("app_final.py"):
        print("❌ Erreur : app_final.py non trouvé")
        print("   Assurez-vous d'être dans le répertoire du projet")
        return False
    
    if not os.path.exists("lib"):
        print("❌ Erreur : dossier lib/ non trouvé")
        return False
    
    print("✅ Fichiers du projet trouvés")
    
    # Vérifier Python
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python détecté : {result.stdout.strip()}")
    except:
        print("❌ Python non trouvé")
        return False
    
    # Créer requirements.txt
    print_step("PRÉPARATION DES DÉPENDANCES")
    create_requirements()
    
    # Installer les dépendances
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Mise à jour de pip"):
        return False
    
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installation des dépendances"):
        return False
    
    # Nettoyer les builds précédents
    print_step("NETTOYAGE")
    
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            print(f"🗑️  Suppression du dossier {folder}/")
            shutil.rmtree(folder, ignore_errors=True)
    
    # Supprimer les anciens fichiers .spec
    for spec_file in Path(".").glob("*.spec"):
        if spec_file.name != "EditeurCartesLove2D.spec":
            print(f"🗑️  Suppression de {spec_file}")
            spec_file.unlink()
    
    print("✅ Nettoyage terminé")
    
    # Créer le fichier .spec
    print_step("CONFIGURATION PYINSTALLER")
    create_spec_file()
    
    # Build avec PyInstaller
    print_step("CRÉATION DE L'EXÉCUTABLE")
    
    if not run_command("pyinstaller EditeurCartesLove2D.spec", "Création de l'exécutable"):
        print("\n❌ ÉCHEC DE LA CRÉATION DE L'EXÉCUTABLE")
        print("Vérifiez les erreurs ci-dessus et réessayez.")
        return False
    
    # Vérifier le résultat
    print_step("VÉRIFICATION DU RÉSULTAT")
    
    exe_path = Path("dist/EditeurCartesLove2D/EditeurCartesLove2D.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Exécutable créé avec succès !")
        print(f"   📁 Chemin : {exe_path}")
        print(f"   📏 Taille : {size_mb:.1f} MB")
        
        # Lister les fichiers dans le dossier dist
        print(f"\n📂 Contenu du dossier dist/EditeurCartesLove2D/ :")
        dist_folder = Path("dist/EditeurCartesLove2D")
        for item in sorted(dist_folder.iterdir()):
            if item.is_file():
                size_kb = item.stat().st_size / 1024
                print(f"   📄 {item.name} ({size_kb:.1f} KB)")
            elif item.is_dir():
                print(f"   📁 {item.name}/")
        
        return True
    else:
        print("❌ Exécutable non trouvé dans dist/EditeurCartesLove2D/")
        return False

def create_portable_package():
    """Crée un package portable avec documentation."""
    print_step("CRÉATION DU PACKAGE PORTABLE")
    
    exe_folder = Path("dist/EditeurCartesLove2D")
    if not exe_folder.exists():
        print("❌ Dossier de l'exécutable non trouvé")
        return False
    
    # Copier la documentation
    docs_to_copy = [
        "README.md",
        "GUIDE.md", 
        "GUIDE_ACTEURS.md",
        "CHANGELOG.md"
    ]
    
    for doc in docs_to_copy:
        if os.path.exists(doc):
            print(f"📋 Copie de {doc}...")
            shutil.copy2(doc, exe_folder)
    
    # Créer un fichier de lancement simple
    launcher_content = '''@echo off
title Editeur de Cartes Love2D
echo.
echo ==========================================
echo   Editeur de Cartes Love2D
echo ==========================================
echo.
echo Lancement de l'application...
echo.

REM Lancer l'executable
"EditeurCartesLove2D.exe"

REM Si erreur, afficher message et attendre
if errorlevel 1 (
    echo.
    echo ==========================================
    echo   Erreur de lancement
    echo ==========================================
    echo.
    echo L'application s'est fermee de maniere inattendue.
    echo.
    echo Solutions possibles :
    echo - Verifiez que tous les fichiers sont presents
    echo - Lancez en tant qu'administrateur
    echo - Consultez le fichier README.md pour plus d'aide
    echo.
    pause
)
'''
    
    launcher_path = exe_folder / "Lancer.bat"
    print(f"📋 Création du fichier de lancement : {launcher_path}")
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("✅ Package portable créé")
    return True

def main():
    """Fonction principale."""
    try:
        success = build_executable()
        
        if success:
            create_portable_package()
            
            print("\n" + "=" * 65)
            print("🎉 CRÉATION D'EXÉCUTABLE TERMINÉE AVEC SUCCÈS !")
            print("=" * 65)
            
            print("\n📂 FICHIERS GÉNÉRÉS :")
            print("   📁 dist/EditeurCartesLove2D/ - Dossier de l'application")
            print("   📄 dist/EditeurCartesLove2D/EditeurCartesLove2D.exe - Exécutable principal")
            print("   📄 dist/EditeurCartesLove2D/Lancer.bat - Lanceur facile")
            print("   📚 Documentation copiée dans le dossier")
            
            print("\n🚀 UTILISATION :")
            print("   1. Allez dans le dossier dist/EditeurCartesLove2D/")
            print("   2. Double-cliquez sur Lancer.bat ou EditeurCartesLove2D.exe")
            print("   3. L'application se lance directement !")
            
            print("\n📦 DISTRIBUTION :")
            print("   • Compressez le dossier dist/EditeurCartesLove2D/")
            print("   • Partagez l'archive ZIP")
            print("   • Aucune installation requise pour l'utilisateur final")
            
        else:
            print("\n❌ ÉCHEC DE LA CRÉATION DE L'EXÉCUTABLE")
            print("Consultez les erreurs ci-dessus pour diagnostiquer le problème.")
            
    except KeyboardInterrupt:
        print("\n⚠️  Création interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")

if __name__ == "__main__":
    main()
