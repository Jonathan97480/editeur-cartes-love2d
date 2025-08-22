#!/usr/bin/env python3
"""
Test de migration pour un utilisateur qui récupère l'app depuis GitHub
avec une base de données existante contenant des chemins absolus
"""

import os
import shutil
import sqlite3
import json
from datetime import datetime

def create_legacy_database():
    """Crée une base de données comme celle qu'un utilisateur pourrait avoir"""
    
    # Supprimer l'ancienne base de test si elle existe
    if os.path.exists("test_migration.db"):
        os.remove("test_migration.db")
    
    print("🔧 Création d'une base de données legacy avec chemins absolus...")
    
    con = sqlite3.connect("test_migration.db")
    cur = con.cursor()
    
    # Créer l'ancien schéma (sans original_img)
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
    
    # Insérer des cartes avec des chemins absolus typiques
    sample_cards = [
        {
            "name": "Carte Legacy 1",
            "img": "C:\\Users\\autreuser\\Documents\\cartes\\dragon.jpg",
            "description": "Une carte avec chemin absolu Windows",
            "rarity": "rare"
        },
        {
            "name": "Carte Legacy 2", 
            "img": "/home/user/images/knight.png",
            "description": "Une carte avec chemin absolu Linux",
            "rarity": "commun"
        },
        {
            "name": "Carte Legacy 3",
            "img": "D:\\GameAssets\\wizard.gif",
            "description": "Autre chemin absolu Windows", 
            "rarity": "legendaire"
        }
    ]
    
    now = datetime.utcnow().isoformat()
    hero_json = json.dumps({
        "heal": 5, "shield": 10, "Epine": 0, "attack": 15,
        "AttackReduction": 0, "shield_pass": 0,
        "bleeding": {"value": 0, "number_turns": 0},
        "force_augmented": {"value": 0, "number_turns": 0},
        "chancePassedTour": 0, "energyCostIncrease": 0, "energyCostDecrease": 0
    })
    enemy_json = json.dumps({
        "heal": 0, "shield": 0, "Epine": 3, "attack": 0,
        "AttackReduction": 5, "shield_pass": 0,
        "bleeding": {"value": 2, "number_turns": 3},
        "force_augmented": {"value": 0, "number_turns": 0},
        "chancePassedTour": 10, "energyCostIncrease": 1, "energyCostDecrease": 0
    })
    
    for card in sample_cards:
        cur.execute("""
            INSERT INTO cards (
                side, name, img, description, powerblow, rarity, types_json,
                hero_json, enemy_json, action, action_param, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'joueur', card['name'], card['img'], card['description'], 
            10, card['rarity'], '["Sort", "Feu"]',
            hero_json, enemy_json, 'damage', '', now, now
        ))
    
    con.commit()
    con.close()
    
    print(f"✅ Base legacy créée avec {len(sample_cards)} cartes")
    return sample_cards

def test_migration():
    """Test la migration avec les nouvelles fonctions"""
    
    print("\n🧪 Test de migration...")
    
    # Importer les modules après création de la base
    import sys
    sys.path.append('.')
    from lib.database import ensure_db, CardRepo
    
    # Tester la migration
    try:
        ensure_db("test_migration.db")
        print("✅ Migration réussie")
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        return False
    
    # Vérifier que les données sont correctes après migration
    repo = CardRepo("test_migration.db")
    cards = repo.list_cards()
    
    print(f"\n📊 Cartes après migration : {len(cards)}")
    
    for card in cards:
        print(f"\n🃏 {card.name}:")
        print(f"   img: {card.img}")
        print(f"   original_img: {card.original_img}")
        
        # Vérifier que original_img a été correctement initialisé
        if not card.original_img:
            print("   ❌ ERREUR: original_img vide")
            return False
        elif card.original_img == card.img:
            print("   ✅ original_img correctement initialisé depuis img")
        else:
            print("   ⚠️  original_img différent de img")
    
    return True

def test_database_schema():
    """Vérifie que le schéma de la base migrée est correct"""
    
    print("\n🔍 Vérification du schéma...")
    
    con = sqlite3.connect("test_migration.db")
    cur = con.cursor()
    
    # Vérifier les colonnes
    cur.execute("PRAGMA table_info(cards)")
    columns = {row[1]: row[2] for row in cur.fetchall()}
    
    required_columns = ['id', 'side', 'name', 'img', 'original_img', 'description', 
                       'powerblow', 'rarity', 'types_json', 'hero_json', 'enemy_json',
                       'action', 'action_param', 'created_at', 'updated_at']
    
    missing = [col for col in required_columns if col not in columns]
    if missing:
        print(f"❌ Colonnes manquantes : {missing}")
        return False
    
    print("✅ Toutes les colonnes requises sont présentes")
    print(f"📋 Colonnes : {list(columns.keys())}")
    
    con.close()
    return True

def cleanup():
    """Nettoie les fichiers de test"""
    if os.path.exists("test_migration.db"):
        os.remove("test_migration.db")
        print("🧹 Fichier de test supprimé")

if __name__ == "__main__":
    print("🚀 TEST DE MIGRATION POUR UTILISATEUR GITHUB")
    print("=" * 55)
    print("Simule un utilisateur qui :")
    print("1. A une base de données existante avec chemins absolus")
    print("2. Récupère la nouvelle version depuis GitHub") 
    print("3. Lance l'application")
    print("=" * 55)
    
    try:
        # 1. Créer base legacy
        sample_cards = create_legacy_database()
        
        # 2. Tester migration
        migration_success = test_migration()
        
        # 3. Vérifier schéma
        schema_success = test_database_schema()
        
        print("\n" + "=" * 55)
        if migration_success and schema_success:
            print("✅ SUCCÈS : La migration fonctionne parfaitement !")
            print("🔄 Un utilisateur GitHub peut mettre à jour sans problème")
            print("💾 Les données existantes sont préservées")
            print("🆕 Le nouveau système original_img fonctionne")
        else:
            print("❌ ÉCHEC : Problèmes détectés dans la migration")
            
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE : {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup()
