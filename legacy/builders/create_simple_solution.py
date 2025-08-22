#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer un dossier _internal COMPLET mais organisé
Solution robuste pour le double-clic
"""
import os
import shutil
from pathlib import Path

def create_complete_minimal_internal():
    """Crée un dossier _internal complet mais bien organisé."""
    print("🔧 CRÉATION D'UN DOSSIER _INTERNAL COMPLET")
    print("=" * 60)
    
    # Dossiers
    source_internal = Path("dist/EditeurCartesLove2D/_internal")
    dest_dir = Path("dist")
    dest_internal = dest_dir / "_internal"
    
    if not source_internal.exists():
        print("❌ Dossier source _internal non trouvé")
        return False
    
    # Supprimer l'ancien et recréer
    if dest_internal.exists():
        print("🗑️ Suppression de l'ancien _internal...")
        shutil.rmtree(dest_internal)
    
    print("📁 Copie complète du dossier _internal...")
    shutil.copytree(source_internal, dest_internal)
    
    # Copier aussi l'exécutable
    source_exe = Path("dist/EditeurCartesLove2D/EditeurCartesLove2D.exe") 
    dest_exe = dest_dir / "EditeurCartesLove2D_Simple.exe"
    
    if source_exe.exists():
        shutil.copy2(source_exe, dest_exe)
        print(f"📄 Exécutable copié : {dest_exe}")
    
    return True

def create_robust_launcher():
    """Crée un lanceur robuste qui gère tous les cas."""
    launcher_content = '''@echo off
title Editeur de Cartes Love2D - Solution Simple
setlocal enabledelayedexpansion

REM Se placer dans le répertoire du script
cd /d "%~dp0"

echo ==========================================
echo   Editeur de Cartes Love2D
echo   Solution Simple avec _internal complet
echo ==========================================
echo.

REM Configuration robuste de l'environnement
set "APP_DIR=%~dp0"
set "INTERNAL_DIR=%APP_DIR%_internal"

REM Ajouter _internal au PATH (en premier)
set "PATH=%INTERNAL_DIR%;%PATH%"

REM Variables Python
set "PYTHONHOME="
set "PYTHONPATH="
set "PYTHONDLLPATH=%INTERNAL_DIR%"

REM Variables Tcl/Tk
set "TCL_LIBRARY=%INTERNAL_DIR%\tcl8\tcl8.6"
set "TK_LIBRARY=%INTERNAL_DIR%\tcl8\tk8.6"

echo 📁 Repertoire application : %APP_DIR%
echo 📁 Repertoire _internal : %INTERNAL_DIR%
echo 🔧 Configuration des variables d'environnement...

REM Vérifications
if not exist "EditeurCartesLove2D_Simple.exe" (
    echo ❌ ERREUR : EditeurCartesLove2D_Simple.exe non trouve
    echo    Assurez-vous que le fichier est present dans ce dossier
    pause
    exit /b 1
)

if not exist "_internal" (
    echo ❌ ERREUR : Dossier _internal non trouve
    echo    Le dossier _internal doit etre present a cote de l'executable
    pause
    exit /b 1
)

if not exist "_internal\python310.dll" (
    echo ❌ ERREUR : python310.dll non trouve dans _internal
    echo    Verifiez que le dossier _internal est complet
    pause
    exit /b 1
)

echo ✅ Tous les fichiers sont presents
echo 🚀 Lancement de l'application...
echo.

REM Lancer l'application
"%APP_DIR%EditeurCartesLove2D_Simple.exe"

REM Vérifier le résultat
set EXIT_CODE=!ERRORLEVEL!

if !EXIT_CODE! neq 0 (
    echo.
    echo ==========================================
    echo   DIAGNOSTIC D'ERREUR
    echo ==========================================
    echo Code d'erreur : !EXIT_CODE!
    echo.
    echo 🔧 Solutions possibles :
    echo.
    echo 1. PERMISSIONS :
    echo    - Clic droit sur ce fichier → "Executer en tant qu'administrateur"
    echo.
    echo 2. ANTIVIRUS :
    echo    - Ajouter une exception pour ce dossier
    echo    - Desactiver temporairement la protection temps reel
    echo.
    echo 3. DEPENDANCES :
    echo    - Installer Microsoft Visual C++ Redistributable 2019-2022
    echo    - URL : https://aka.ms/vs/17/release/vc_redist.x64.exe
    echo.
    echo 4. SYSTEME :
    echo    - Redemarrer l'ordinateur
    echo    - Verifier les mises a jour Windows
    echo.
    echo Appuyez sur une touche pour fermer...
    pause >nul
) else (
    echo ✅ Application fermee normalement
)

endlocal
'''
    
    launcher_path = Path("dist/Lancer-Simple.bat")
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    print(f"📄 Lanceur robuste créé : {launcher_path}")

def create_direct_launcher():
    """Crée un lanceur ultra-simple pour double-clic."""
    simple_launcher = '''@echo off
cd /d "%~dp0"
set "PATH=%~dp0_internal;%PATH%"
"EditeurCartesLove2D_Simple.exe"
'''
    
    launcher_path = Path("dist/Double-Clic.bat")
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(simple_launcher)
    print(f"📄 Lanceur ultra-simple créé : {launcher_path}")

def main():
    """Fonction principale."""
    print("🎯 SOLUTION SIMPLE : EXÉCUTABLE + _INTERNAL COMPLET")
    print("Approche : Copier tout le _internal pour garantir le fonctionnement")
    print("=" * 75)
    
    try:
        # Créer la structure
        success = create_complete_minimal_internal()
        
        if success:
            # Créer les lanceurs
            create_robust_launcher()
            create_direct_launcher()
            
            print("\n" + "=" * 75)
            print("🎉 SOLUTION SIMPLE CRÉÉE !")
            print("=" * 75)
            
            print("\n📂 STRUCTURE FINALE :")
            print("   📁 dist/")
            print("   ├── 📄 EditeurCartesLove2D_Simple.exe      (Application)")
            print("   ├── 📄 Double-Clic.bat                     (Ultra-simple)")
            print("   ├── 📄 Lancer-Simple.bat                   (Avec diagnostic)")
            print("   ├── 📄 EditeurCartesLove2D_Portable.exe    (Monofichier)")
            print("   └── 📁 _internal/                          (DLL complètes)")
            
            print("\n🧪 TESTS À EFFECTUER (par ordre de priorité) :")
            print("   1️⃣  Double-clic sur Double-Clic.bat")
            print("   2️⃣  Double-clic sur EditeurCartesLove2D_Simple.exe")
            print("   3️⃣  Double-clic sur Lancer-Simple.bat (diagnostic)")
            
            print("\n🎯 CETTE SOLUTION DEVRAIT FONCTIONNER CAR :")
            print("   ✅ _internal complet (toutes les DLL)")
            print("   ✅ PATH configuré correctement")
            print("   ✅ Variables d'environnement définies")
            print("   ✅ Structure identique à la version qui marche en terminal")
            
            # Afficher les tailles
            internal_size = sum(f.stat().st_size for f in Path("dist/_internal").rglob('*') if f.is_file()) / (1024*1024)
            exe_size = Path("dist/EditeurCartesLove2D_Simple.exe").stat().st_size / (1024*1024)
            total_size = internal_size + exe_size
            
            print(f"\n📏 TAILLES :")
            print(f"   📄 Exécutable : {exe_size:.1f} MB")
            print(f"   📁 _internal : {internal_size:.1f} MB")
            print(f"   📦 Total : {total_size:.1f} MB")
            
        else:
            print("\n❌ Échec de la création")
            
    except Exception as e:
        print(f"\n❌ Erreur : {e}")

if __name__ == "__main__":
    main()
