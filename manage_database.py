#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour résoudre le problème de la base de données dans l'exécutable
"""
import os
import shutil
from pathlib import Path

def copy_database_to_executables():
    """Copie la base de données existante vers les dossiers d'exécutables."""
    print("🗄️ GESTION DE LA BASE DE DONNÉES POUR LES EXÉCUTABLES")
    print("=" * 65)
    
    # Base de données source
    source_db = Path("cartes.db")
    
    if not source_db.exists():
        print("⚠️  Aucune base de données cartes.db trouvée dans le dossier source")
        print("   L'application créera une base vide au premier lancement")
        return
    
    print(f"📊 Base de données source trouvée : {source_db}")
    
    # Afficher les statistiques de la base existante
    import sqlite3
    try:
        with sqlite3.connect(source_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cards")
            card_count = cursor.fetchone()[0]
            print(f"   📝 Nombre de cartes : {card_count}")
    except Exception as e:
        print(f"   ⚠️  Impossible de lire la base : {e}")
    
    # Destinations où copier la base
    destinations = [
        "dist/cartes.db",                                    # Pour version simple
        "dist/_internal/cartes.db",                          # Dans _internal
        "dist/EditeurCartesLove2D/cartes.db",               # Version dossier original
        "dist/EditeurCartesLove2D/_internal/cartes.db",     # Dans _internal du dossier
    ]
    
    print("\n📋 Copie vers les emplacements d'exécutables :")
    
    copied_count = 0
    for dest_path in destinations:
        dest = Path(dest_path)
        
        # Créer le dossier parent si nécessaire
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(source_db, dest)
            print(f"   ✅ {dest}")
            copied_count += 1
        except Exception as e:
            print(f"   ❌ {dest} - Erreur : {e}")
    
    print(f"\n✅ Base de données copiée vers {copied_count} emplacements")
    
    return copied_count > 0

def create_database_management_options():
    """Crée des options pour gérer la base de données."""
    
    # Option 1 : Script pour copier la base existante
    copy_script = '''@echo off
title Copie de la Base de Donnees
cd /d "%~dp0"

echo ==========================================
echo   Copie de la Base de Donnees
echo ==========================================
echo.

if not exist "cartes.db" (
    echo ❌ Aucune base de donnees cartes.db trouvee
    echo.
    echo Pour utiliser vos donnees existantes :
    echo 1. Copiez votre fichier cartes.db dans ce dossier
    echo 2. Relancez ce script
    echo.
    pause
    exit /b 1
)

echo 📊 Base de donnees trouvee : cartes.db
echo.
echo 📋 Copie vers les executables...

REM Copier vers les differents emplacements
if exist "dist" (
    copy "cartes.db" "dist\\" 2>nul
    echo ✅ dist\\cartes.db
    
    if exist "dist\\_internal" (
        copy "cartes.db" "dist\\_internal\\" 2>nul
        echo ✅ dist\\_internal\\cartes.db
    )
    
    if exist "dist\\EditeurCartesLove2D" (
        copy "cartes.db" "dist\\EditeurCartesLove2D\\" 2>nul
        echo ✅ dist\\EditeurCartesLove2D\\cartes.db
        
        if exist "dist\\EditeurCartesLove2D\\_internal" (
            copy "cartes.db" "dist\\EditeurCartesLove2D\\_internal\\" 2>nul
            echo ✅ dist\\EditeurCartesLove2D\\_internal\\cartes.db
        )
    )
)

echo.
echo ✅ Copie terminee !
echo.
echo 🎯 Vos executables utiliseront maintenant votre base existante
echo    avec toutes vos cartes personnalisees !
echo.
pause
'''
    
    with open("Copier-Base-Donnees.bat", "w", encoding="utf-8") as f:
        f.write(copy_script)
    
    # Option 2 : Script pour sauvegarder la base depuis l'exécutable
    backup_script = '''@echo off
title Sauvegarde de la Base de Donnees
cd /d "%~dp0"

echo ==========================================
echo   Sauvegarde de la Base de Donnees
echo ==========================================
echo.

set "BACKUP_DIR=backup_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%"
set "BACKUP_DIR=%BACKUP_DIR: =0%"
set "BACKUP_DIR=%BACKUP_DIR::=%"

echo 📁 Creation du dossier de sauvegarde : %BACKUP_DIR%
mkdir "%BACKUP_DIR%" 2>nul

set FOUND=0

REM Chercher et sauvegarder toutes les bases de donnees
if exist "cartes.db" (
    copy "cartes.db" "%BACKUP_DIR%\\cartes_racine.db" 2>nul
    echo ✅ cartes.db → %BACKUP_DIR%\\cartes_racine.db
    set FOUND=1
)

if exist "dist\\cartes.db" (
    copy "dist\\cartes.db" "%BACKUP_DIR%\\cartes_dist.db" 2>nul
    echo ✅ dist\\cartes.db → %BACKUP_DIR%\\cartes_dist.db
    set FOUND=1
)

if exist "dist\\_internal\\cartes.db" (
    copy "dist\\_internal\\cartes.db" "%BACKUP_DIR%\\cartes_internal.db" 2>nul
    echo ✅ dist\\_internal\\cartes.db → %BACKUP_DIR%\\cartes_internal.db
    set FOUND=1
)

if exist "dist\\EditeurCartesLove2D\\cartes.db" (
    copy "dist\\EditeurCartesLove2D\\cartes.db" "%BACKUP_DIR%\\cartes_dossier.db" 2>nul
    echo ✅ dist\\EditeurCartesLove2D\\cartes.db → %BACKUP_DIR%\\cartes_dossier.db
    set FOUND=1
)

if %FOUND%==0 (
    echo ❌ Aucune base de donnees trouvee
    rmdir "%BACKUP_DIR%" 2>nul
) else (
    echo.
    echo ✅ Sauvegarde terminee dans le dossier : %BACKUP_DIR%
)

echo.
pause
'''
    
    with open("Sauvegarder-Base-Donnees.bat", "w", encoding="utf-8") as f:
        f.write(backup_script)
    
    print("📄 Scripts de gestion créés :")
    print("   📁 Copier-Base-Donnees.bat - Copie votre base vers les exécutables")
    print("   📁 Sauvegarder-Base-Donnees.bat - Sauvegarde les bases existantes")

def main():
    """Fonction principale."""
    print("🗄️ GESTION DE LA BASE DE DONNÉES POUR LES EXÉCUTABLES")
    print("=" * 70)
    
    print("\n🎯 PROBLÈME IDENTIFIÉ :")
    print("   Les exécutables créent une nouvelle base vide au premier lancement")
    print("   Vos cartes existantes ne sont pas incluses automatiquement")
    
    print("\n💡 SOLUTIONS PROPOSÉES :")
    
    # Solution 1 : Copier la base existante
    print("\n1️⃣  COPIE AUTOMATIQUE DE LA BASE EXISTANTE")
    success = copy_database_to_executables()
    
    # Solution 2 : Scripts de gestion
    print("\n2️⃣  SCRIPTS DE GESTION MANUELLE")
    create_database_management_options()
    
    print("\n" + "=" * 70)
    print("🎉 SOLUTIONS CRÉÉES !")
    print("=" * 70)
    
    if success:
        print("\n✅ SOLUTION IMMÉDIATE :")
        print("   Votre base de données a été copiée vers tous les exécutables")
        print("   Vos cartes seront disponibles immédiatement !")
    
    print("\n🛠️  SCRIPTS DISPONIBLES :")
    print("   📄 Copier-Base-Donnees.bat - Pour copier votre base vers les exécutables")
    print("   📄 Sauvegarder-Base-Donnees.bat - Pour sauvegarder vos données")
    
    print("\n🎯 RECOMMANDATIONS :")
    print("   1. Utilisez vos exécutables - ils ont maintenant vos données")
    print("   2. Sauvegardez régulièrement avec Sauvegarder-Base-Donnees.bat")
    print("   3. Si vous ajoutez des cartes, utilisez Copier-Base-Donnees.bat")
    
    print("\n📝 NOTE :")
    print("   Chaque version d'exécutable aura sa propre copie de la base")
    print("   Modifiez vos cartes dans UNE version puis copiez si nécessaire")

if __name__ == "__main__":
    main()
