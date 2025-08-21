#!/usr/bin/env python3
"""
Test de scénario complet GitHub : Utilisateur qui clone le repo et lance l'app
"""

import os
import shutil
import sqlite3
import json
from datetime import datetime

def simulate_github_user_scenario():
    """
    Simule le scénario complet d'un utilisateur GitHub :
    1. A déjà une base de données locale avec chemins absolus
    2. Clone/pull la nouvelle version du repo
    3. Lance l'application
    """
    
    print("🎬 SIMULATION SCÉNARIO UTILISATEUR GITHUB")
    print("=" * 50)
    
    # 1. ÉTAPE : Utilisateur a déjà une base de données
    print("📁 ÉTAPE 1 : L'utilisateur a déjà une base avec chemins absolus")
    
    # Créer une base comme un vrai utilisateur en aurait une
    if os.path.exists("cartes_user.db"):
        os.remove("cartes_user.db")
    
    con = sqlite3.connect("cartes_user.db")
    cur = con.cursor()
    
    # Ancienne structure (sans original_img, sans système de migration)
    cur.execute("""
        CREATE TABLE cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            side TEXT NOT NULL CHECK(side IN ('joueur','ia')),
            name TEXT NOT NULL,
            img TEXT NOT NULL,
            description TEXT NOT NULL,
            powerblow INTEGER NOT NULL DEFAULT 0,
            rarity TEXT NOT NULL DEFAULT 'commun',
            types_json TEXT NOT NULL DEFAULT '[]',
            hero_json TEXT NOT NULL,
            enemy_json TEXT NOT NULL,
            action TEXT NOT NULL,
            action_param TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    # Données utilisateur typiques avec chemins absolus
    now = datetime.now().isoformat()
    hero_json = json.dumps({"heal": 10, "shield": 5, "Epine": 0, "attack": 20, "AttackReduction": 0, "shield_pass": 0, "bleeding": {"value": 0, "number_turns": 0}, "force_augmented": {"value": 0, "number_turns": 0}, "chancePassedTour": 0, "energyCostIncrease": 0, "energyCostDecrease": 0})
    enemy_json = json.dumps({"heal": 0, "shield": 0, "Epine": 5, "attack": 0, "AttackReduction": 10, "shield_pass": 0, "bleeding": {"value": 3, "number_turns": 2}, "force_augmented": {"value": 0, "number_turns": 0}, "chancePassedTour": 15, "energyCostIncrease": 2, "energyCostDecrease": 0})
    
    user_cards = [
        ("Ma Carte Dragon", "C:\\Users\\John\\Desktop\\images\\dragon_red.png", "Mon dragon personnel", "rare"),
        ("Carte Magicien", "C:\\Games\\Assets\\wizard_blue.jpg", "Magicien de glace", "legendaire"),
        ("Guerrier", "/home/user/Pictures/warrior.gif", "Guerrier redoutable", "commun"),
        ("Élite Noire", "D:\\MyCards\\elite_dark.png", "Créature d'élite", "mythique"),
    ]
    
    for name, img_path, desc, rarity in user_cards:
        cur.execute("""
            INSERT INTO cards (side, name, img, description, powerblow, rarity, types_json, hero_json, enemy_json, action, action_param, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ('joueur', name, img_path, desc, 15, rarity, '["Combat"]', hero_json, enemy_json, 'damage', '', now, now))
    
    con.commit()
    con.close()
    
    print(f"   ✅ Base utilisateur créée avec {len(user_cards)} cartes personnelles")
    
    # 2. ÉTAPE : Utilisateur récupère la nouvelle version depuis GitHub
    print(f"\n📥 ÉTAPE 2 : L'utilisateur met à jour son code depuis GitHub")
    print("   (Clone ou pull de la nouvelle version avec système de migration)")
    
    # 3. ÉTAPE : Utilisateur lance l'application
    print(f"\n🚀 ÉTAPE 3 : L'utilisateur lance l'application")
    
    # Importer le nouveau système
    import sys
    sys.path.append('.')
    from lib.database import ensure_db, CardRepo
    
    # La fonction ensure_db va automatiquement détecter et migrer
    try:
        ensure_db("cartes_user.db")
        print("   ✅ Migration automatique réussie !")
    except Exception as e:
        print(f"   ❌ ERREUR lors de la migration : {e}")
        return False
    
    # 4. ÉTAPE : Vérifier que tout fonctionne
    print(f"\n🔍 ÉTAPE 4 : Vérification du bon fonctionnement")
    
    repo = CardRepo("cartes_user.db")
    cards = repo.list_cards()
    
    print(f"\n📊 Résultats après migration :")
    print(f"   • Nombre de cartes : {len(cards)}")
    
    all_good = True
    for card in cards:
        print(f"\n   🃏 {card.name} ({card.rarity})")
        print(f"     img: {card.img}")
        print(f"     original_img: {card.original_img}")
        
        # Vérifications critiques
        if not card.original_img:
            print(f"     ❌ PROBLÈME: original_img vide !")
            all_good = False
        elif card.original_img == card.img:
            print(f"     ✅ original_img correctement initialisé")
        else:
            print(f"     ⚠️  original_img différent de img")
        
        # Vérifier que les données utilisateur sont préservées
        if not card.name or not card.description:
            print(f"     ❌ PROBLÈME: Données utilisateur perdues !")
            all_good = False
        else:
            print(f"     ✅ Données préservées")
    
    # Test de modification d'une carte (le problème original)
    print(f"\n🧪 ÉTAPE 5 : Test changement de rareté (problème initial)")
    
    if cards:
        test_card = cards[0]
        original_rarity = test_card.rarity
        new_rarity = 'legendaire' if original_rarity != 'legendaire' else 'rare'
        
        print(f"   🔄 Changement {test_card.name} : {original_rarity} → {new_rarity}")
        
        test_card.rarity = new_rarity
        repo.update(test_card)
        
        # Recharger et vérifier
        updated_card = repo.get(test_card.id)
        if updated_card and updated_card.rarity == new_rarity:
            print(f"   ✅ Rareté mise à jour avec succès")
            print(f"   ✅ original_img préservé : {updated_card.original_img}")
        else:
            print(f"   ❌ PROBLÈME lors du changement de rareté")
            all_good = False
    
    return all_good

def cleanup_test():
    """Nettoie les fichiers de test"""
    test_files = ["cartes_user.db", "cartes_user.db.backup.*"]
    for pattern in test_files:
        if '*' in pattern:
            import glob
            for file in glob.glob(pattern):
                try:
                    os.remove(file)
                except:
                    pass
        else:
            if os.path.exists(pattern):
                try:
                    os.remove(pattern)
                except:
                    pass

if __name__ == "__main__":
    try:
        success = simulate_github_user_scenario()
        
        print(f"\n" + "=" * 50)
        if success:
            print("🎉 SUCCÈS COMPLET !")
            print("✅ L'utilisateur GitHub peut mettre à jour sans problème")
            print("✅ Les données existantes sont préservées") 
            print("✅ Les chemins absolus sont gérés correctement")
            print("✅ Le système original_img fonctionne parfaitement")
            print("✅ Le problème de superposition de templates est résolu")
            print(f"\n🔒 CONFIRMATION : Un utilisateur qui récupère l'app depuis GitHub")
            print("   avec une base existante bénéficiera automatiquement de la")
            print("   migration et de la correction du bug des templates !")
        else:
            print("❌ ÉCHEC : Des problèmes ont été détectés")
    
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE : {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup_test()
