#!/usr/bin/env python3
"""
Test pour vérifier le comportement lors du changement de rareté d'une carte.
"""

import os
import sqlite3

def check_existing_cards():
    """Vérifie les cartes existantes et leurs images."""
    if not os.path.exists("cartes.db"):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect("cartes.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, rarity, img FROM cards ORDER BY name")
    cards = cursor.fetchall()
    
    print("📋 Cartes existantes :")
    for card_id, name, rarity, img_path in cards:
        img_exists = "✅" if img_path and os.path.exists(img_path) else "❌"
        print(f"   {card_id:2d}. {name:<20} | {rarity:<10} | {img_exists} {img_path}")
    
    conn.close()
    
    # Vérifier le dossier images/cards pour les images fusionnées
    cards_dir = "images/cards"
    if os.path.exists(cards_dir):
        print(f"\n📁 Contenu du dossier {cards_dir} :")
        files = os.listdir(cards_dir)
        for file in sorted(files):
            if file.endswith(('.png', '.jpg', '.jpeg')):
                print(f"   - {file}")
    else:
        print(f"\n❌ Dossier {cards_dir} non trouvé")

def simulate_rarity_change():
    """Simule un changement de rareté pour voir les fichiers générés."""
    print("\n🔧 Pour tester le changement de rareté :")
    print("1. Ouvrez l'application")
    print("2. Sélectionnez une carte existante")
    print("3. Changez sa rareté")
    print("4. Sauvegardez")
    print("5. Vérifiez si l'ancienne image est supprimée")

if __name__ == "__main__":
    print("🧪 Test du changement de rareté\n")
    check_existing_cards()
    simulate_rarity_change()
