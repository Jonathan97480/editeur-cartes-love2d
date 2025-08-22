#!/usr/bin/env python3
"""
Test avancé pour détecter les problèmes lors du changement de rareté.
"""

import os
import sqlite3
import shutil
from datetime import datetime

def backup_current_state():
    """Fait une sauvegarde de l'état actuel pour pouvoir le restaurer."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sauvegarde de la base de données
    if os.path.exists("cartes.db"):
        shutil.copy("cartes.db", f"cartes_backup_{timestamp}.db")
        print(f"✅ DB sauvegardée : cartes_backup_{timestamp}.db")
    
    # Sauvegarde du dossier images/cards
    if os.path.exists("images/cards"):
        backup_dir = f"images_backup_{timestamp}"
        shutil.copytree("images/cards", backup_dir)
        print(f"✅ Images sauvegardées : {backup_dir}")

def test_rarity_change_scenario():
    """Teste un scénario de changement de rareté."""
    print("\n🧪 Test du scénario de changement de rareté")
    
    if not os.path.exists("cartes.db"):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect("cartes.db")
    cursor = conn.cursor()
    
    # Prendre la première carte comme test
    cursor.execute("SELECT id, name, rarity, img FROM cards LIMIT 1")
    card = cursor.fetchone()
    
    if not card:
        print("❌ Aucune carte trouvée")
        return
    
    card_id, name, current_rarity, img_path = card
    print(f"📋 Carte de test : {name}")
    print(f"   Rareté actuelle : {current_rarity}")
    print(f"   Image actuelle : {img_path}")
    
    # Vérifier si l'image existe
    if img_path and os.path.exists(img_path):
        print(f"   ✅ Image existe : {os.path.getsize(img_path)} bytes")
        file_time = os.path.getmtime(img_path)
        print(f"   📅 Modifiée le : {datetime.fromtimestamp(file_time)}")
    else:
        print(f"   ❌ Image manquante")
    
    print(f"\n💡 Pour tester :")
    print(f"1. Changez la rareté de '{name}' vers 'rare' ou 'legendaire'")
    print(f"2. Sauvegardez la carte")
    print(f"3. Vérifiez que l'image {img_path} a été mise à jour")
    print(f"4. Exécutez ce script à nouveau pour comparer les timestamps")
    
    conn.close()

def check_orphaned_images():
    """Vérifie s'il y a des images orphelines dans le dossier cards."""
    print("\n🔍 Vérification des images orphelines")
    
    if not os.path.exists("cartes.db"):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect("cartes.db")
    cursor = conn.cursor()
    
    # Récupérer toutes les images référencées en base
    cursor.execute("SELECT DISTINCT img FROM cards WHERE img IS NOT NULL AND img != ''")
    db_images = {row[0] for row in cursor.fetchall()}
    
    # Lister toutes les images dans le dossier
    cards_dir = "images/cards"
    if not os.path.exists(cards_dir):
        print(f"❌ Dossier {cards_dir} non trouvé")
        return
    
    file_images = set()
    for file in os.listdir(cards_dir):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            file_images.add(os.path.join(cards_dir, file).replace('\\', '/'))
    
    # Trouver les orphelines
    orphaned = file_images - db_images
    missing = db_images - file_images
    
    print(f"📊 Statistiques :")
    print(f"   Images en base : {len(db_images)}")
    print(f"   Images sur disque : {len(file_images)}")
    print(f"   Images orphelines : {len(orphaned)}")
    print(f"   Images manquantes : {len(missing)}")
    
    if orphaned:
        print(f"\n🗑️ Images orphelines (présentes sur disque mais pas en base) :")
        for img in sorted(orphaned):
            print(f"   - {img}")
    
    if missing:
        print(f"\n❌ Images manquantes (référencées en base mais absentes du disque) :")
        for img in sorted(missing):
            print(f"   - {img}")
    
    conn.close()

if __name__ == "__main__":
    print("🧪 Test avancé du changement de rareté\n")
    backup_current_state()
    test_rarity_change_scenario()
    check_orphaned_images()
