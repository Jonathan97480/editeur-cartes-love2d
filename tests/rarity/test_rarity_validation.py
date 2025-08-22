#!/usr/bin/env python3
"""
Test du système de changement de rareté avec validation de la suppression des anciennes images.
"""

import os
import sqlite3
import time
from datetime import datetime

def test_rarity_change_with_validation():
    """Teste le changement de rareté en surveillant les fichiers."""
    print("🧪 Test du changement de rareté avec validation\n")
    
    if not os.path.exists("cartes.db"):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect("cartes.db")
    cursor = conn.cursor()
    
    # Sélectionner une carte pour le test
    cursor.execute("SELECT id, name, rarity, img FROM cards WHERE img IS NOT NULL LIMIT 1")
    card = cursor.fetchone()
    
    if not card:
        print("❌ Aucune carte avec image trouvée")
        return
    
    card_id, name, current_rarity, img_path = card
    print(f"📋 Carte de test : {name}")
    print(f"   ID : {card_id}")
    print(f"   Rareté actuelle : {current_rarity}")
    print(f"   Image : {img_path}")
    
    # Vérifier l'état initial du fichier image
    if os.path.exists(img_path):
        initial_size = os.path.getsize(img_path)
        initial_mtime = os.path.getmtime(img_path)
        print(f"   ✅ Fichier initial : {initial_size} bytes")
        print(f"   📅 Modifié le : {datetime.fromtimestamp(initial_mtime)}")
    else:
        print(f"   ❌ Fichier image manquant")
        return
    
    print(f"\n🔧 Instructions pour le test :")
    print(f"1. Ouvrez l'application principale")
    print(f"2. Sélectionnez la carte '{name}' (ID: {card_id})")
    print(f"3. Changez sa rareté de '{current_rarity}' vers une autre (ex: 'rare')")
    print(f"4. Cliquez sur 'Sauvegarder'")
    print(f"5. Revenez ici et appuyez sur Entrée pour vérifier le résultat")
    
    input("\n⏸️ Appuyez sur Entrée après avoir effectué le changement de rareté...")
    
    # Vérification après changement
    print(f"\n🔍 Vérification après changement...")
    
    # Recharger les données de la carte
    cursor.execute("SELECT rarity, img FROM cards WHERE id = ?", (card_id,))
    new_data = cursor.fetchone()
    
    if new_data:
        new_rarity, new_img_path = new_data
        print(f"   Nouvelle rareté : {new_rarity}")
        print(f"   Nouveau chemin image : {new_img_path}")
        
        # Vérifier si le fichier a été modifié
        if os.path.exists(new_img_path):
            new_size = os.path.getsize(new_img_path)
            new_mtime = os.path.getmtime(new_img_path)
            
            print(f"   ✅ Nouveau fichier : {new_size} bytes")
            print(f"   📅 Modifié le : {datetime.fromtimestamp(new_mtime)}")
            
            # Comparer les timestamps pour voir si l'image a été régénérée
            if new_mtime > initial_mtime:
                print(f"   ✅ L'image a été régénérée (nouveau timestamp)")
            else:
                print(f"   ⚠️ L'image n'a pas été modifiée (même timestamp)")
            
            # Comparer les tailles
            if new_size != initial_size:
                print(f"   📊 Taille différente : {initial_size} → {new_size} bytes")
            else:
                print(f"   📊 Même taille : {new_size} bytes")
                
        else:
            print(f"   ❌ Fichier image manquant après changement")
    
    conn.close()

def check_image_consistency():
    """Vérifie la cohérence entre la base de données et les fichiers."""
    print(f"\n🔍 Vérification de cohérence des images")
    
    if not os.path.exists("cartes.db"):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect("cartes.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, rarity, img FROM cards WHERE img IS NOT NULL")
    cards = cursor.fetchall()
    
    print(f"📊 Vérification de {len(cards)} cartes avec images...")
    
    issues_found = 0
    for card_id, name, rarity, img_path in cards:
        if not os.path.exists(img_path):
            print(f"   ❌ {name} (ID:{card_id}) : fichier manquant {img_path}")
            issues_found += 1
        else:
            # Vérifier si le nom du fichier correspond au nom de la carte
            expected_filename = f"images/cards/{name.replace(' ', '_')}.png"
            if img_path != expected_filename:
                print(f"   ⚠️ {name} (ID:{card_id}) : nom incohérent")
                print(f"      Attendu : {expected_filename}")
                print(f"      Actuel  : {img_path}")
    
    if issues_found == 0:
        print(f"   ✅ Toutes les images sont cohérentes")
    else:
        print(f"   ⚠️ {issues_found} problème(s) détecté(s)")
    
    conn.close()

if __name__ == "__main__":
    test_rarity_change_with_validation()
    check_image_consistency()
