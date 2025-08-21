#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création d'exécutable ONEFILE pour l'Éditeur de Cartes Love2D
Version qui fonctionne en double-clic
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

def create_onefile_spec():
    """Crée un fichier .spec pour un exécutable monofichier."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Configuration pour exécutable monofichier
block_cipher = None

a = Analysis(
    ['app_final.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('lib', 'lib'),
        ('cartes.db', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'sqlite3',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'json',
        'datetime',
        'pathlib',
        'os',
        'sys',
        'shutil',
        'glob',
        're',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'numpy',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EditeurCartesLove2D_Portable',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)
'''
    
    print("📝 Création du fichier EditeurCartesLove2D_OneFile.spec...")
    with open("EditeurCartesLove2D_OneFile.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("✅ Fichier .spec monofichier créé")

def build_onefile_executable():
    """Crée un exécutable monofichier."""
    print("🚀 CRÉATION D'EXÉCUTABLE MONOFICHIER")
    print("=" * 60)
    
    # Vérifications
    print_step("VÉRIFICATIONS")
    
    if not os.path.exists("app_final.py"):
        print("❌ app_final.py non trouvé")
        return False
    
    print("✅ Fichiers trouvés")
    
    # Nettoyer
    print_step("NETTOYAGE")
    
    if os.path.exists("dist/EditeurCartesLove2D_Portable.exe"):
        os.remove("dist/EditeurCartesLove2D_Portable.exe")
        print("🗑️ Ancien exécutable supprimé")
    
    # Créer le .spec
    print_step("CONFIGURATION MONOFICHIER")
    create_onefile_spec()
    
    # Build
    print_step("CRÉATION MONOFICHIER")
    
    build_command = (
        "pyinstaller "
        "--clean "
        "--noconfirm "
        "EditeurCartesLove2D_OneFile.spec"
    )
    
    if not run_command(build_command, "Création exécutable monofichier"):
        return False
    
    # Vérifier
    print_step("VÉRIFICATION")
    
    exe_path = Path("dist/EditeurCartesLove2D_Portable.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Exécutable monofichier créé !")
        print(f"   📁 Chemin : {exe_path}")
        print(f"   📏 Taille : {size_mb:.1f} MB")
        return True
    else:
        print("❌ Exécutable monofichier non trouvé")
        return False

def create_launcher_wrapper():
    """Crée un wrapper qui configure l'environnement."""
    wrapper_content = '''@echo off
REM Wrapper pour EditeurCartesLove2D - Configure l'environnement
setlocal

REM Se placer dans le répertoire du script
cd /d "%~dp0"

REM Configuration des variables d'environnement
set "TEMP=%~dp0temp"
set "TMP=%~dp0temp"
if not exist "%TEMP%" mkdir "%TEMP%"

REM Lancer l'exécutable principal
if exist "EditeurCartesLove2D_Portable.exe" (
    "EditeurCartesLove2D_Portable.exe"
) else if exist "EditeurCartesLove2D.exe" (
    "EditeurCartesLove2D.exe"
) else (
    echo ❌ Aucun exécutable trouvé
    pause
)

REM Nettoyer le dossier temp
if exist "%TEMP%" rmdir /s /q "%TEMP%" 2>nul

endlocal
'''
    
    print("📋 Création du wrapper launcher...")
    with open("dist/Wrapper-Launcher.bat", "w", encoding="utf-8") as f:
        f.write(wrapper_content)
    print("✅ Wrapper créé")

def main():
    """Fonction principale."""
    print("🎯 CRÉATION D'EXÉCUTABLE PORTABLE")
    print("Objectif : Fonctionne en double-clic direct")
    print("=" * 60)
    
    try:
        # Option 1 : Exécutable monofichier
        print("\n📦 OPTION 1 : EXÉCUTABLE MONOFICHIER")
        success_onefile = build_onefile_executable()
        
        if success_onefile:
            print("\n✅ EXÉCUTABLE MONOFICHIER CRÉÉ")
            print("   📄 dist/EditeurCartesLove2D_Portable.exe")
            print("   🎯 Double-clic direct fonctionnel")
        
        # Option 2 : Wrapper pour l'exécutable existant
        print("\n📦 OPTION 2 : WRAPPER POUR EXÉCUTABLE EXISTANT")
        create_launcher_wrapper()
        
        print("\n" + "=" * 60)
        print("🎉 SOLUTIONS CRÉÉES !")
        print("=" * 60)
        
        print("\n📋 FICHIERS DISPONIBLES :")
        
        if success_onefile:
            print("   🥇 EditeurCartesLove2D_Portable.exe (RECOMMANDÉ)")
            print("      → Monofichier, double-clic direct")
        
        if os.path.exists("dist/EditeurCartesLove2D"):
            print("   📁 dist/EditeurCartesLove2D/ (Version dossier)")
            print("      → Utiliser Lancer-Fixe.bat")
        
        print("   🔧 dist/Wrapper-Launcher.bat (Alternative)")
        
        print("\n🚀 RECOMMANDATION :")
        if success_onefile:
            print("   Utilisez EditeurCartesLove2D_Portable.exe")
            print("   → Un seul fichier, fonctionne partout")
        else:
            print("   Utilisez Lancer-Fixe.bat dans le dossier")
            print("   → Configure l'environnement automatiquement")
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}")

if __name__ == "__main__":
    main()
