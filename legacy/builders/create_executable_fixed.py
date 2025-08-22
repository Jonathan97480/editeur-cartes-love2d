#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création d'exécutable CORRIGÉ pour l'Éditeur de Cartes Love2D
Résout le problème du python310.dll
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

def create_fixed_spec_file():
    """Crée un fichier .spec corrigé pour résoudre les problèmes de DLL."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Configuration PyInstaller corrigée
block_cipher = None

a = Analysis(
    ['app_final.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('lib', 'lib'),
        ('README.md', '.'),
        ('GUIDE.md', '.'),
        ('GUIDE_ACTEURS.md', '.'),
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
    [],
    exclude_binaries=True,
    name='EditeurCartesLove2D',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Interface graphique pure
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EditeurCartesLove2D',
)
'''
    
    print("📝 Création du fichier EditeurCartesLove2D_Fixed.spec...")
    with open("EditeurCartesLove2D_Fixed.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("✅ Fichier .spec corrigé créé")

def build_executable_fixed():
    """Processus de création avec corrections."""
    print("🚀 CRÉATION D'EXÉCUTABLE CORRIGÉE - ÉDITEUR DE CARTES LOVE2D")
    print("=" * 70)
    
    # Vérifications préliminaires
    print_step("VÉRIFICATIONS PRÉLIMINAIRES")
    
    if not os.path.exists("app_final.py"):
        print("❌ Erreur : app_final.py non trouvé")
        return False
    
    if not os.path.exists("lib"):
        print("❌ Erreur : dossier lib/ non trouvé")
        return False
    
    print("✅ Fichiers du projet trouvés")
    
    # Nettoyer les builds précédents
    print_step("NETTOYAGE COMPLET")
    
    folders_to_clean = ["build", "dist", "__pycache__"]
    for folder in folders_to_clean:
        if os.path.exists(folder):
            print(f"🗑️  Suppression du dossier {folder}/")
            shutil.rmtree(folder, ignore_errors=True)
    
    # Supprimer les anciens fichiers .spec
    for spec_file in Path(".").glob("*.spec"):
        print(f"🗑️  Suppression de {spec_file}")
        spec_file.unlink()
    
    print("✅ Nettoyage complet terminé")
    
    # Créer le fichier .spec corrigé
    print_step("CONFIGURATION PYINSTALLER CORRIGÉE")
    create_fixed_spec_file()
    
    # Build avec paramètres spéciaux
    print_step("CRÉATION DE L'EXÉCUTABLE (VERSION CORRIGÉE)")
    
    # Commande PyInstaller avec options spéciales pour résoudre les problèmes de DLL
    build_command = (
        "pyinstaller "
        "--clean "
        "--noconfirm "
        "--log-level=INFO "
        "EditeurCartesLove2D_Fixed.spec"
    )
    
    if not run_command(build_command, "Création de l'exécutable corrigé"):
        print("\n❌ ÉCHEC DE LA CRÉATION DE L'EXÉCUTABLE")
        return False
    
    # Vérifier le résultat
    print_step("VÉRIFICATION DU RÉSULTAT")
    
    exe_path = Path("dist/EditeurCartesLove2D/EditeurCartesLove2D.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Exécutable créé avec succès !")
        print(f"   📁 Chemin : {exe_path}")
        print(f"   📏 Taille : {size_mb:.1f} MB")
        
        # Vérifier la présence des DLL critiques
        internal_path = Path("dist/EditeurCartesLove2D/_internal")
        critical_dlls = ["python310.dll", "python3.dll", "_tkinter.pyd"]
        
        print(f"\n🔍 Vérification des fichiers critiques :")
        for dll in critical_dlls:
            dll_path = internal_path / dll
            if dll_path.exists():
                print(f"   ✅ {dll} présent")
            else:
                print(f"   ❌ {dll} MANQUANT")
        
        return True
    else:
        print("❌ Exécutable non trouvé dans dist/EditeurCartesLove2D/")
        return False

def create_debug_launcher():
    """Crée un lanceur avec debug pour diagnostiquer les problèmes."""
    launcher_content = '''@echo off
title Editeur de Cartes Love2D - Debug
echo.
echo ==========================================
echo   Editeur de Cartes Love2D - MODE DEBUG
echo ==========================================
echo.

REM Afficher le répertoire courant
echo 📁 Répertoire courant : %CD%
echo.

REM Vérifier les fichiers critiques
echo 🔍 Vérification des fichiers critiques :
if exist "EditeurCartesLove2D.exe" (
    echo ✅ EditeurCartesLove2D.exe présent
) else (
    echo ❌ EditeurCartesLove2D.exe MANQUANT
    goto :error
)

if exist "_internal" (
    echo ✅ Dossier _internal présent
) else (
    echo ❌ Dossier _internal MANQUANT
    goto :error
)

if exist "_internal\\python310.dll" (
    echo ✅ python310.dll présent
) else (
    echo ❌ python310.dll MANQUANT dans _internal
)

if exist "_internal\\python3.dll" (
    echo ✅ python3.dll présent
) else (
    echo ❌ python3.dll MANQUANT dans _internal
)

echo.
echo 🚀 Tentative de lancement...
echo.

REM Définir les variables d'environnement
set PATH=%CD%\\_internal;%PATH%

REM Lancer l'exécutable
"EditeurCartesLove2D.exe"

REM Capturer le code de retour
set EXIT_CODE=%ERRORLEVEL%

echo.
echo ==========================================
echo   RÉSULTAT DU LANCEMENT
echo ==========================================
echo Code de retour : %EXIT_CODE%

if %EXIT_CODE% equ 0 (
    echo ✅ Application fermée normalement
) else (
    echo ❌ Application fermée avec erreur
    echo.
    echo 🔧 Solutions possibles :
    echo - Installer Visual C++ Redistributable
    echo - Lancer en tant qu'administrateur
    echo - Vérifier l'antivirus
    echo - Consulter les logs Windows
)

echo.
pause
goto :end

:error
echo.
echo ❌ ERREUR : Fichiers manquants
echo.
echo 📋 Vérifiez que vous avez :
echo - Le fichier EditeurCartesLove2D.exe
echo - Le dossier _internal avec tous les fichiers
echo - Les permissions de lecture/exécution
echo.
pause

:end
'''
    
    launcher_path = Path("dist/EditeurCartesLove2D/Debug-Launcher.bat")
    print(f"📋 Création du lanceur debug : {launcher_path}")
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    print("✅ Lanceur debug créé")

def main():
    """Fonction principale."""
    try:
        success = build_executable_fixed()
        
        if success:
            # Copier la documentation
            print_step("FINALISATION DU PACKAGE")
            
            exe_folder = Path("dist/EditeurCartesLove2D")
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
            
            # Créer les lanceurs
            create_debug_launcher()
            
            print("\n" + "=" * 70)
            print("🎉 EXÉCUTABLE CORRIGÉ CRÉÉ AVEC SUCCÈS !")
            print("=" * 70)
            
            print("\n📂 FICHIERS GÉNÉRÉS :")
            print("   📁 dist/EditeurCartesLove2D/ - Application complète")
            print("   📄 EditeurCartesLove2D.exe - Exécutable principal")
            print("   📄 Debug-Launcher.bat - Lanceur avec diagnostic")
            
            print("\n🧪 POUR TESTER :")
            print("   1. Allez dans dist/EditeurCartesLove2D/")
            print("   2. Lancez Debug-Launcher.bat pour diagnostiquer")
            print("   3. Si ça marche, utilisez EditeurCartesLove2D.exe")
            
            print("\n🔧 EN CAS DE PROBLÈME :")
            print("   • Utilisez Debug-Launcher.bat pour voir les erreurs")
            print("   • Installez Visual C++ Redistributable 2019-2022")
            print("   • Lancez en tant qu'administrateur")
            
        else:
            print("\n❌ ÉCHEC DE LA CRÉATION")
            
    except KeyboardInterrupt:
        print("\n⚠️  Création interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")

if __name__ == "__main__":
    main()
