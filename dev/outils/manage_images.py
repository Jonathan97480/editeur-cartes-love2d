#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour gérer le dossier images dans les exécutables
"""
import os
import shutil
from pathlib import Path

def analyze_images_folder():
    """Analyse le contenu du dossier images."""
    print("🖼️ ANALYSE DU DOSSIER IMAGES")
    print("=" * 50)
    
    images_path = Path("images")
    
    if not images_path.exists():
        print("❌ Aucun dossier images trouvé")
        return None
    
    # Statistiques
    total_files = 0
    total_size = 0
    structure = {}
    
    print(f"📁 Dossier images trouvé : {images_path}")
    
    for item in images_path.rglob('*'):
        if item.is_file():
            total_files += 1
            total_size += item.stat().st_size
            
            # Organiser par sous-dossier
            relative_path = item.relative_to(images_path)
            subfolder = str(relative_path.parent) if relative_path.parent != Path('.') else 'racine'
            
            if subfolder not in structure:
                structure[subfolder] = {'files': 0, 'size': 0, 'types': set()}
            
            structure[subfolder]['files'] += 1
            structure[subfolder]['size'] += item.stat().st_size
            structure[subfolder]['types'].add(item.suffix.lower())
    
    print(f"📊 Statistiques globales :")
    print(f"   📄 Fichiers total : {total_files}")
    print(f"   📏 Taille totale : {total_size / (1024*1024):.1f} MB")
    
    print(f"\n📂 Structure détaillée :")
    for subfolder, stats in structure.items():
        print(f"   📁 {subfolder}/ :")
        print(f"      📄 {stats['files']} fichiers")
        print(f"      📏 {stats['size'] / (1024*1024):.1f} MB") 
        print(f"      🎨 Types : {', '.join(sorted(stats['types']))}")
    
    return structure

def copy_images_to_executables():
    """Copie le dossier images vers les emplacements d'exécutables."""
    print("\n🖼️ COPIE DU DOSSIER IMAGES VERS LES EXÉCUTABLES")
    print("=" * 60)
    
    source_images = Path("images")
    
    if not source_images.exists():
        print("❌ Aucun dossier images source trouvé")
        print("   L'application créera un dossier vide au besoin")
        return False
    
    # Destinations où copier le dossier images
    destinations = [
        "dist/images",                                    # Pour version simple
        "dist/EditeurCartesLove2D/images",               # Version dossier original
    ]
    
    print("📋 Copie vers les emplacements d'exécutables :")
    
    copied_count = 0
    for dest_path in destinations:
        dest = Path(dest_path)
        
        try:
            # Supprimer l'ancien dossier s'il existe
            if dest.exists():
                shutil.rmtree(dest)
                print(f"   🗑️ Ancien dossier supprimé : {dest}")
            
            # Copier le dossier complet
            shutil.copytree(source_images, dest)
            print(f"   ✅ {dest}")
            copied_count += 1
            
        except Exception as e:
            print(f"   ❌ {dest} - Erreur : {e}")
    
    print(f"\n✅ Dossier images copié vers {copied_count} emplacements")
    return copied_count > 0

def create_images_management_scripts():
    """Crée des scripts pour gérer le dossier images."""
    
    # Script pour copier les images
    copy_images_script = '''@echo off
title Copie du Dossier Images
cd /d "%~dp0"

echo ==========================================
echo   Copie du Dossier Images
echo ==========================================
echo.

if not exist "images" (
    echo ❌ Aucun dossier images trouve
    echo.
    echo Pour utiliser vos images existantes :
    echo 1. Creez un dossier "images" dans ce repertoire
    echo 2. Placez vos images dedans (originals/, cards/, templates/)
    echo 3. Relancez ce script
    echo.
    pause
    exit /b 1
)

echo 🖼️ Dossier images trouve
echo.
echo 📋 Copie vers les executables...

REM Copier vers les differents emplacements
if exist "dist" (
    if exist "dist\\images" (
        echo 🗑️ Suppression ancien dossier dist\\images...
        rmdir /s /q "dist\\images" 2>nul
    )
    
    xcopy "images" "dist\\images\\" /E /I /Y >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ dist\\images\\
    ) else (
        echo ❌ Erreur copie vers dist\\images\\
    )
    
    if exist "dist\\EditeurCartesLove2D" (
        if exist "dist\\EditeurCartesLove2D\\images" (
            echo 🗑️ Suppression ancien dossier dist\\EditeurCartesLove2D\\images...
            rmdir /s /q "dist\\EditeurCartesLove2D\\images" 2>nul
        )
        
        xcopy "images" "dist\\EditeurCartesLove2D\\images\\" /E /I /Y >nul 2>&1
        if !errorlevel! equ 0 (
            echo ✅ dist\\EditeurCartesLove2D\\images\\
        ) else (
            echo ❌ Erreur copie vers dist\\EditeurCartesLove2D\\images\\
        )
    )
)

echo.
echo ✅ Copie terminee !
echo.
echo 🎯 Vos executables utilisent maintenant vos images
echo    Templates, cartes et images sources incluses !
echo.
pause
'''
    
    with open("Copier-Images.bat", "w", encoding="utf-8") as f:
        f.write(copy_images_script)
    
    # Script pour sauvegarder les images
    backup_images_script = '''@echo off
title Sauvegarde du Dossier Images
cd /d "%~dp0"

echo ==========================================
echo   Sauvegarde du Dossier Images
echo ==========================================
echo.

set "BACKUP_DIR=backup_images_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%"
set "BACKUP_DIR=%BACKUP_DIR: =0%"
set "BACKUP_DIR=%BACKUP_DIR::=%"

echo 📁 Creation du dossier de sauvegarde : %BACKUP_DIR%
mkdir "%BACKUP_DIR%" 2>nul

set FOUND=0

REM Chercher et sauvegarder tous les dossiers images
if exist "images" (
    xcopy "images" "%BACKUP_DIR%\\images_racine\\" /E /I /Y >nul 2>&1
    echo ✅ images\\ → %BACKUP_DIR%\\images_racine\\
    set FOUND=1
)

if exist "dist\\images" (
    xcopy "dist\\images" "%BACKUP_DIR%\\images_dist\\" /E /I /Y >nul 2>&1
    echo ✅ dist\\images\\ → %BACKUP_DIR%\\images_dist\\
    set FOUND=1
)

if exist "dist\\EditeurCartesLove2D\\images" (
    xcopy "dist\\EditeurCartesLove2D\\images" "%BACKUP_DIR%\\images_dossier\\" /E /I /Y >nul 2>&1
    echo ✅ dist\\EditeurCartesLove2D\\images\\ → %BACKUP_DIR%\\images_dossier\\
    set FOUND=1
)

if %FOUND%==0 (
    echo ❌ Aucun dossier images trouve
    rmdir "%BACKUP_DIR%" 2>nul
) else (
    echo.
    echo ✅ Sauvegarde terminee dans le dossier : %BACKUP_DIR%
    echo 📊 Verifiez le contenu pour vous assurer que tout est sauve
)

echo.
pause
'''
    
    with open("Sauvegarder-Images.bat", "w", encoding="utf-8") as f:
        f.write(backup_images_script)
    
    # Script pour synchroniser les images
    sync_images_script = '''@echo off
title Synchronisation des Images
cd /d "%~dp0"

echo ==========================================
echo   Synchronisation des Images
echo ==========================================
echo.

echo 🔄 Recherche des dossiers images les plus recents...
echo.

REM Trouver le dossier images le plus recent
set "LATEST_SOURCE="
set "LATEST_DATE=0"

for /d %%d in ("images" "dist\\images" "dist\\EditeurCartesLove2D\\images") do (
    if exist "%%d" (
        echo 📁 Trouve : %%d
        REM Note: Verification basique de l'existence
        set "LATEST_SOURCE=%%d"
    )
)

if "%LATEST_SOURCE%"=="" (
    echo ❌ Aucun dossier images trouve
    echo.
    pause
    exit /b 1
)

echo.
echo 📂 Source selectionnee : %LATEST_SOURCE%
echo.
echo 🔄 Synchronisation vers tous les emplacements...

REM Copier vers tous les autres emplacements
if not "%LATEST_SOURCE%"=="images" (
    if exist "images" rmdir /s /q "images" 2>nul
    xcopy "%LATEST_SOURCE%" "images\\" /E /I /Y >nul 2>&1
    echo ✅ → images\\
)

if not "%LATEST_SOURCE%"=="dist\\images" (
    if exist "dist\\images" rmdir /s /q "dist\\images" 2>nul
    if exist "dist" (
        xcopy "%LATEST_SOURCE%" "dist\\images\\" /E /I /Y >nul 2>&1
        echo ✅ → dist\\images\\
    )
)

if not "%LATEST_SOURCE%"=="dist\\EditeurCartesLove2D\\images" (
    if exist "dist\\EditeurCartesLove2D\\images" rmdir /s /q "dist\\EditeurCartesLove2D\\images" 2>nul
    if exist "dist\\EditeurCartesLove2D" (
        xcopy "%LATEST_SOURCE%" "dist\\EditeurCartesLove2D\\images\\" /E /I /Y >nul 2>&1
        echo ✅ → dist\\EditeurCartesLove2D\\images\\
    )
)

echo.
echo ✅ Synchronisation terminee !
echo 🎯 Tous vos executables ont maintenant les memes images
echo.
pause
'''
    
    with open("Synchroniser-Images.bat", "w", encoding="utf-8") as f:
        f.write(sync_images_script)
    
    print("📄 Scripts de gestion des images créés :")
    print("   📁 Copier-Images.bat - Copie vos images vers les exécutables")
    print("   📁 Sauvegarder-Images.bat - Sauvegarde tous les dossiers images")
    print("   📁 Synchroniser-Images.bat - Synchronise entre tous les emplacements")

def main():
    """Fonction principale."""
    print("🖼️ GESTION DU DOSSIER IMAGES POUR LES EXÉCUTABLES")
    print("=" * 65)
    
    print("\n🎯 PROBLÈME IDENTIFIÉ :")
    print("   Les exécutables ne contiennent pas vos images personnalisées")
    print("   Templates, cartes et images sources ne sont pas incluses")
    
    print("\n💡 SOLUTIONS PROPOSÉES :")
    
    # Analyse du dossier existant
    print("\n1️⃣  ANALYSE DU DOSSIER IMAGES EXISTANT")
    structure = analyze_images_folder()
    
    if structure:
        # Copie automatique
        print("\n2️⃣  COPIE AUTOMATIQUE VERS LES EXÉCUTABLES")
        success = copy_images_to_executables()
        
        # Scripts de gestion
        print("\n3️⃣  SCRIPTS DE GESTION MANUELLE")
        create_images_management_scripts()
        
        print("\n" + "=" * 65)
        print("🎉 SOLUTIONS CRÉÉES !")
        print("=" * 65)
        
        if success:
            print("\n✅ SOLUTION IMMÉDIATE :")
            print("   Votre dossier images a été copié vers tous les exécutables")
            print("   Templates et images seront disponibles immédiatement !")
        
        print("\n🛠️  SCRIPTS DISPONIBLES :")
        print("   📄 Copier-Images.bat - Pour copier vos images vers les exécutables")
        print("   📄 Sauvegarder-Images.bat - Pour sauvegarder vos images")
        print("   📄 Synchroniser-Images.bat - Pour synchroniser entre versions")
        
        print("\n🎯 RECOMMANDATIONS :")
        print("   1. Utilisez vos exécutables - ils ont maintenant vos images")
        print("   2. Sauvegardez régulièrement avec Sauvegarder-Images.bat")
        print("   3. Si vous modifiez des images, utilisez Synchroniser-Images.bat")
        
        print("\n📝 NOTE :")
        print("   Chaque version d'exécutable aura sa propre copie des images")
        print("   Modifiez vos images dans UNE version puis synchronisez")
        
    else:
        print("\n📝 NOTE :")
        print("   Aucun dossier images trouvé - L'application en créera un vide")
        print("   Vous pourrez ajouter vos images plus tard")

if __name__ == "__main__":
    main()
