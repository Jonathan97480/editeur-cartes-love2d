#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer un dossier _internal minimal avec les DLL essentielles
Solution simple pour le problème de double-clic
"""
import os
import shutil
from pathlib import Path

def create_minimal_internal():
    """Crée un dossier _internal minimal avec les DLL critiques."""
    print("🔧 CRÉATION D'UN DOSSIER _INTERNAL MINIMAL")
    print("=" * 60)
    
    # Dossiers source et destination
    source_internal = Path("dist/EditeurCartesLove2D/_internal")
    dest_dir = Path("dist")
    dest_internal = dest_dir / "_internal"
    
    # Vérifications
    if not source_internal.exists():
        print("❌ Dossier source _internal non trouvé")
        return False
    
    # Créer le dossier de destination
    if dest_internal.exists():
        print("🗑️ Suppression de l'ancien _internal minimal...")
        shutil.rmtree(dest_internal)
    
    dest_internal.mkdir(exist_ok=True)
    print(f"📁 Création du dossier : {dest_internal}")
    
    # DLL essentielles à copier
    essential_dlls = [
        # DLL Python critiques
        "python310.dll",
        "python3.dll",
        
        # Runtime Visual C++
        "VCRUNTIME140.dll",
        "VCRUNTIME140_1.dll",
        
        # SQLite pour la base de données
        "sqlite3.dll",
        
        # Tkinter (interface graphique)
        "tcl86t.dll",
        "tk86t.dll",
        
        # Runtime C
        "ucrtbase.dll",
        
        # SSL/Crypto
        "libcrypto-1_1.dll",
        "libssl-1_1.dll",
        "libffi-7.dll",
        
        # Runtime Windows essentiels
        "api-ms-win-crt-runtime-l1-1-0.dll",
        "api-ms-win-crt-stdio-l1-1-0.dll",
        "api-ms-win-crt-heap-l1-1-0.dll",
        "api-ms-win-crt-string-l1-1-0.dll",
        "api-ms-win-crt-math-l1-1-0.dll",
        "api-ms-win-crt-convert-l1-1-0.dll",
        "api-ms-win-crt-environment-l1-1-0.dll",
        "api-ms-win-crt-filesystem-l1-1-0.dll",
        "api-ms-win-crt-process-l1-1-0.dll",
        "api-ms-win-crt-time-l1-1-0.dll",
        "api-ms-win-crt-utility-l1-1-0.dll",
    ]
    
    # Fichiers Python essentiels (.pyd)
    essential_pyds = [
        "_tkinter.pyd",
        "_sqlite3.pyd",
        "sqlite3.dll",
        "select.pyd",
        "_socket.pyd",
        "_ssl.pyd",
        "_hashlib.pyd",
        "unicodedata.pyd",
    ]
    
    # Copier les DLL
    print("\n📋 Copie des DLL essentielles :")
    copied_count = 0
    
    for dll in essential_dlls:
        source_file = source_internal / dll
        if source_file.exists():
            dest_file = dest_internal / dll
            shutil.copy2(source_file, dest_file)
            print(f"   ✅ {dll}")
            copied_count += 1
        else:
            print(f"   ⚠️  {dll} (non trouvé)")
    
    # Copier les fichiers .pyd
    print("\n📋 Copie des modules Python (.pyd) :")
    
    for pyd in essential_pyds:
        source_file = source_internal / pyd
        if source_file.exists():
            dest_file = dest_internal / pyd
            shutil.copy2(source_file, dest_file)
            print(f"   ✅ {pyd}")
            copied_count += 1
        else:
            print(f"   ⚠️  {pyd} (non trouvé)")
    
    # Copier base_library.zip (essentiel)
    base_lib = source_internal / "base_library.zip"
    if base_lib.exists():
        shutil.copy2(base_lib, dest_internal / "base_library.zip")
        print(f"   ✅ base_library.zip")
        copied_count += 1
    
    # Copier les dossiers essentiels
    essential_dirs = ["tcl8", "_tcl_data", "_tk_data"]
    print("\n📋 Copie des dossiers essentiels :")
    
    for dir_name in essential_dirs:
        source_dir = source_internal / dir_name
        if source_dir.exists():
            dest_dir_path = dest_internal / dir_name
            shutil.copytree(source_dir, dest_dir_path, dirs_exist_ok=True)
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ⚠️  {dir_name}/ (non trouvé)")
    
    # Copier les données du projet
    print("\n📋 Copie des données du projet :")
    project_files = ["cartes.db", "lib"]
    
    for item in project_files:
        source_item = source_internal / item
        if source_item.exists():
            dest_item = dest_internal / item
            if source_item.is_dir():
                shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
                print(f"   ✅ {item}/")
            else:
                shutil.copy2(source_item, dest_item)
                print(f"   ✅ {item}")
    
    print(f"\n✅ Dossier _internal minimal créé avec {copied_count} fichiers copiés")
    return True

def copy_executable_to_root():
    """Copie l'exécutable à la racine du dossier dist."""
    source_exe = Path("dist/EditeurCartesLove2D/EditeurCartesLove2D.exe")
    dest_exe = Path("dist/EditeurCartesLove2D_Minimal.exe")
    
    if source_exe.exists():
        shutil.copy2(source_exe, dest_exe)
        print(f"📄 Exécutable copié : {dest_exe}")
        return True
    else:
        print("❌ Exécutable source non trouvé")
        return False

def create_simple_launcher():
    """Crée un lanceur simple qui utilise le _internal minimal."""
    launcher_content = '''@echo off
title Editeur de Cartes Love2D - Version Minimale
cd /d "%~dp0"

echo ==========================================
echo   Editeur de Cartes Love2D
echo   Version avec _internal minimal
echo ==========================================
echo.

REM Configurer l'environnement
set "PATH=%~dp0_internal;%PATH%"
set "PYTHONDLLPATH=%~dp0_internal"

echo 📁 Repertoire : %~dp0
echo 🔧 PATH configure avec _internal minimal

REM Verifier les fichiers
if not exist "EditeurCartesLove2D_Minimal.exe" (
    echo ❌ EditeurCartesLove2D_Minimal.exe non trouve
    pause
    exit /b 1
)

if not exist "_internal\\python310.dll" (
    echo ❌ python310.dll non trouve dans _internal
    pause
    exit /b 1
)

echo ✅ Fichiers presents
echo 🚀 Lancement...
echo.

REM Lancer l'application
"EditeurCartesLove2D_Minimal.exe"

if errorlevel 1 (
    echo.
    echo ❌ Erreur de lancement
    echo Essayez en tant qu'administrateur
    pause
)
'''
    
    launcher_path = Path("dist/Lancer-Minimal.bat")
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    print(f"📄 Lanceur créé : {launcher_path}")

def main():
    """Fonction principale."""
    print("🎯 CRÉATION D'UNE SOLUTION _INTERNAL MINIMALE")
    print("Objectif : DLL essentielles à côté de l'exécutable")
    print("=" * 70)
    
    try:
        # Créer le dossier _internal minimal
        success = create_minimal_internal()
        
        if success:
            # Copier l'exécutable
            copy_executable_to_root()
            
            # Créer le lanceur
            create_simple_launcher()
            
            print("\n" + "=" * 70)
            print("🎉 SOLUTION _INTERNAL MINIMALE CRÉÉE !")
            print("=" * 70)
            
            print("\n📂 STRUCTURE CRÉÉE :")
            print("   📁 dist/")
            print("   ├── 📄 EditeurCartesLove2D_Minimal.exe")
            print("   ├── 📄 Lancer-Minimal.bat")
            print("   ├── 📄 EditeurCartesLove2D_Portable.exe (monofichier)")
            print("   └── 📁 _internal/ (DLL essentielles uniquement)")
            
            print("\n🧪 TESTS À EFFECTUER :")
            print("   1. Double-clic sur EditeurCartesLove2D_Minimal.exe")
            print("   2. Double-clic sur Lancer-Minimal.bat")
            print("   3. Vérifier que l'interface se lance")
            
            print("\n🎯 AVANTAGES DE CETTE SOLUTION :")
            print("   ✅ Structure simple et claire")
            print("   ✅ Seulement les DLL nécessaires")
            print("   ✅ Plus petit que la version complète")
            print("   ✅ Même efficacité que le monofichier")
            
            # Afficher la taille
            internal_size = sum(f.stat().st_size for f in Path("dist/_internal").rglob('*') if f.is_file()) / (1024*1024)
            print(f"\n📏 Taille du _internal minimal : {internal_size:.1f} MB")
            
        else:
            print("\n❌ Échec de la création")
            
    except Exception as e:
        print(f"\n❌ Erreur : {e}")

if __name__ == "__main__":
    main()
