#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier que les chemins relatifs sont utilisés dans les exports
"""
import sqlite3
import os

def check_export_compatibility():
    """Vérifie que les exports utiliseront les bons chemins"""
    print("🔍 VÉRIFICATION DE LA COMPATIBILITÉ DES EXPORTS")
    print("=" * 60)
    
    # Vérifier dans le dossier principal
    print("📂 Vérification dans le dossier principal...")
    check_database_and_images(".")
    
    # Vérifier dans le dossier de l'exécutable
    executable_path = os.path.join("dist", "EditeurCartesLove2D")
    if os.path.exists(executable_path):
        print(f"\n📂 Vérification dans {executable_path}...")
        check_database_and_images(executable_path)
    
    print("\n" + "=" * 60)
    print("✅ Vérification terminée !")

def check_database_and_images(folder_path):
    """Vérifie la base et les images dans un dossier donné"""
    db_path = os.path.join(folder_path, "cartes.db")
    images_path = os.path.join(folder_path, "images")
    
    # Vérifier la base de données
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM cards WHERE img LIKE "images/%" AND img IS NOT NULL AND img != ""')
        relative_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM cards WHERE img IS NOT NULL AND img != ""')
        total_count = cursor.fetchone()[0]
        
        print(f"   🗄️ Base de données : {total_count} cartes avec images")
        print(f"   ✅ Chemins relatifs : {relative_count}/{total_count}")
        
        # Montrer quelques exemples
        cursor.execute('SELECT name, img FROM cards WHERE img IS NOT NULL AND img != "" LIMIT 3')
        for name, img_path in cursor.fetchall():
            print(f"      🃏 {name}: {img_path}")
        
        conn.close()
    else:
        print(f"   ❌ Base non trouvée : {db_path}")
    
    # Vérifier le dossier images
    if os.path.exists(images_path):
        cards_folder = os.path.join(images_path, "cards")
        originals_folder = os.path.join(images_path, "originals")
        
        cards_count = len(os.listdir(cards_folder)) if os.path.exists(cards_folder) else 0
        originals_count = len(os.listdir(originals_folder)) if os.path.exists(originals_folder) else 0
        
        print(f"   🖼️ Dossier images trouvé")
        print(f"      📁 cards/ : {cards_count} fichiers")
        print(f"      📁 originals/ : {originals_count} fichiers")
    else:
        print(f"   ❌ Dossier images non trouvé : {images_path}")

if __name__ == "__main__":
    check_export_compatibility()
