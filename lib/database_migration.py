#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de migration et de vérification de la base de données
"""
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any
from .config import RARITY_VALUES

# ======================= Constantes =======================

# Version actuelle de la base de données
CURRENT_DB_VERSION = 3

# Schéma requis pour la table cards
REQUIRED_SCHEMA = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'side': 'TEXT NOT NULL CHECK(side IN (\'joueur\',\'ia\'))',
    'name': 'TEXT NOT NULL',
    'img': 'TEXT NOT NULL',
    'description': 'TEXT NOT NULL',
    'powerblow': 'INTEGER NOT NULL DEFAULT 0',
    'rarity': 'TEXT NOT NULL DEFAULT \'commun\'',
    'types_json': 'TEXT NOT NULL DEFAULT \'[]\'',
    'hero_json': 'TEXT NOT NULL',
    'enemy_json': 'TEXT NOT NULL',
    'action': 'TEXT NOT NULL',
    'action_param': 'TEXT NOT NULL DEFAULT \'\'',
    'created_at': 'TEXT NOT NULL',
    'updated_at': 'TEXT NOT NULL'
}

# ======================= Fonctions de migration =======================

def get_db_version(db_path: str) -> int:
    """Récupère la version actuelle de la base de données."""
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Vérifier si la table de version existe
        cur.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='db_version'
        """)
        
        if not cur.fetchone():
            # Pas de table de version, c'est une ancienne DB
            con.close()
            return 1
            
        cur.execute("SELECT version FROM db_version ORDER BY id DESC LIMIT 1")
        result = cur.fetchone()
        con.close()
        
        return result[0] if result else 1
        
    except Exception:
        return 1

def set_db_version(db_path: str, version: int) -> None:
    """Met à jour la version de la base de données."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Créer la table de version si elle n'existe pas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS db_version (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version INTEGER NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    # Insérer la nouvelle version
    now = datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO db_version (version, updated_at) VALUES (?, ?)",
        (version, now)
    )
    
    con.commit()
    con.close()

def get_table_schema(db_path: str, table_name: str) -> Dict[str, str]:
    """Récupère le schéma actuel d'une table."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = cur.fetchall()
    con.close()
    
    schema = {}
    for col in columns:
        col_name = col[1]
        col_type = col[2]
        not_null = col[3]
        default_value = col[4]
        is_pk = col[5]
        
        # Reconstruire la définition de colonne
        definition = col_type
        if is_pk:
            definition += " PRIMARY KEY"
            if col_type == "INTEGER":
                definition += " AUTOINCREMENT"
        elif not_null:
            definition += " NOT NULL"
            if default_value is not None:
                if isinstance(default_value, str):
                    definition += f" DEFAULT '{default_value}'"
                else:
                    definition += f" DEFAULT {default_value}"
        
        schema[col_name] = definition
    
    return schema

def migrate_v1_to_v2(db_path: str) -> None:
    """Migration de la version 1 à la version 2 - Ajout rarity et types_json."""
    print("🔄 Migration v1 → v2 : Ajout des colonnes rarity et types_json...")
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Vérifier les colonnes existantes
    cur.execute("PRAGMA table_info(cards)")
    existing_cols = [row[1] for row in cur.fetchall()]
    
    # Ajouter rarity si manquante
    if 'rarity' not in existing_cols:
        cur.execute("ALTER TABLE cards ADD COLUMN rarity TEXT NOT NULL DEFAULT 'commun'")
        print("   ✅ Colonne 'rarity' ajoutée")
    
    # Ajouter types_json si manquante
    if 'types_json' not in existing_cols:
        cur.execute("ALTER TABLE cards ADD COLUMN types_json TEXT NOT NULL DEFAULT '[]'")
        print("   ✅ Colonne 'types_json' ajoutée")
    
    con.commit()
    con.close()

def migrate_v2_to_v3(db_path: str) -> None:
    """Migration de la version 2 à la version 3 - Validation et nettoyage des données."""
    print("🔄 Migration v2 → v3 : Validation et nettoyage des données...")
    
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    # Récupérer toutes les cartes
    cur.execute("SELECT * FROM cards")
    cards = cur.fetchall()
    
    fixed_count = 0
    
    for card in cards:
        card_id = card['id']
        updates = []
        params = []
        needs_update = False
        
        # Vérifier et corriger la rareté
        if card['rarity'] not in RARITY_VALUES:
            updates.append("rarity = ?")
            params.append('commun')
            needs_update = True
            print(f"   🔧 Carte {card_id} '{card['name']}': rareté '{card['rarity']}' → 'commun'")
        
        # Vérifier et corriger types_json
        try:
            types = json.loads(card['types_json'])
            if not isinstance(types, list):
                raise ValueError("types_json doit être une liste")
        except (json.JSONDecodeError, ValueError):
            updates.append("types_json = ?")
            params.append('[]')
            needs_update = True
            print(f"   🔧 Carte {card_id} '{card['name']}': types_json corrigé")
        
        # Vérifier et corriger hero_json
        try:
            hero = json.loads(card['hero_json'])
            if not isinstance(hero, dict):
                raise ValueError("hero_json doit être un dictionnaire")
        except (json.JSONDecodeError, ValueError):
            default_hero = {
                "heal": 0, "shield": 0, "Epine": 0, "attack": 0,
                "AttackReduction": 0, "shield_pass": 0,
                "bleeding": {"value": 0, "number_turns": 0},
                "force_augmented": {"value": 0, "number_turns": 0},
                "chancePassedTour": 0, "energyCostIncrease": 0, "energyCostDecrease": 0
            }
            updates.append("hero_json = ?")
            params.append(json.dumps(default_hero, ensure_ascii=False))
            needs_update = True
            print(f"   🔧 Carte {card_id} '{card['name']}': hero_json corrigé")
        
        # Vérifier et corriger enemy_json
        try:
            enemy = json.loads(card['enemy_json'])
            if not isinstance(enemy, dict):
                raise ValueError("enemy_json doit être un dictionnaire")
        except (json.JSONDecodeError, ValueError):
            default_enemy = {
                "heal": 0, "shield": 0, "Epine": 0, "attack": 0,
                "AttackReduction": 0, "shield_pass": 0,
                "bleeding": {"value": 0, "number_turns": 0},
                "force_augmented": {"value": 0, "number_turns": 0},
                "chancePassedTour": 0, "energyCostIncrease": 0, "energyCostDecrease": 0
            }
            updates.append("enemy_json = ?")
            params.append(json.dumps(default_enemy, ensure_ascii=False))
            needs_update = True
            print(f"   🔧 Carte {card_id} '{card['name']}': enemy_json corrigé")
        
        # Vérifier les timestamps
        if not card['created_at']:
            updates.append("created_at = ?")
            params.append(datetime.utcnow().isoformat())
            needs_update = True
        
        if not card['updated_at']:
            updates.append("updated_at = ?")
            params.append(datetime.utcnow().isoformat())
            needs_update = True
        
        # Appliquer les mises à jour si nécessaire
        if needs_update:
            query = f"UPDATE cards SET {', '.join(updates)} WHERE id = ?"
            params.append(card_id)
            cur.execute(query, params)
            fixed_count += 1
    
    con.commit()
    con.close()
    
    if fixed_count > 0:
        print(f"   ✅ {fixed_count} cartes corrigées")
    else:
        print("   ✅ Toutes les données sont valides")

def verify_database_integrity(db_path: str) -> bool:
    """Vérifie l'intégrité de la base de données."""
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Vérification de l'intégrité SQLite
        cur.execute("PRAGMA integrity_check")
        integrity_result = cur.fetchone()[0]
        
        if integrity_result != "ok":
            print(f"❌ Échec de vérification d'intégrité : {integrity_result}")
            con.close()
            return False
        
        # Vérification du schéma
        current_schema = get_table_schema(db_path, "cards")
        
        # Vérifier que toutes les colonnes requises existent
        for col_name in REQUIRED_SCHEMA:
            if col_name not in current_schema:
                print(f"❌ Colonne manquante : {col_name}")
                con.close()
                return False
        
        con.close()
        print("✅ Intégrité de la base de données vérifiée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {e}")
        return False

def migrate_database(db_path: str) -> bool:
    """Effectue toutes les migrations nécessaires."""
    print("🚀 Vérification et migration de la base de données...")
    
    try:
        current_version = get_db_version(db_path)
        print(f"📊 Version actuelle : {current_version}")
        print(f"📊 Version cible : {CURRENT_DB_VERSION}")
        
        if current_version == CURRENT_DB_VERSION:
            print("✅ Base de données à jour")
            return verify_database_integrity(db_path)
        
        # Sauvegarder la base avant migration
        backup_path = f"{db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"💾 Sauvegarde créée : {backup_path}")
        
        # Appliquer les migrations
        if current_version < 2:
            migrate_v1_to_v2(db_path)
            set_db_version(db_path, 2)
        
        if current_version < 3:
            migrate_v2_to_v3(db_path)
            set_db_version(db_path, 3)
        
        print(f"✅ Migration terminée ! Version {current_version} → {CURRENT_DB_VERSION}")
        
        # Vérifier l'intégrité après migration
        return verify_database_integrity(db_path)
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        import traceback
        traceback.print_exc()
        return False

def ensure_db_with_migration(db_path: str) -> bool:
    """Assure que la base de données existe et est à jour."""
    import os
    
    # Créer la base si elle n'existe pas
    if not os.path.exists(db_path):
        print("📂 Création de la nouvelle base de données...")
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Créer la table cards avec le schéma complet
        columns_def = ", ".join([f"{name} {definition}" for name, definition in REQUIRED_SCHEMA.items()])
        cur.execute(f"CREATE TABLE cards ({columns_def})")
        
        con.commit()
        con.close()
        
        # Marquer comme version actuelle
        set_db_version(db_path, CURRENT_DB_VERSION)
        print("✅ Base de données créée avec le schéma actuel")
        return True
    
    # Migrer la base existante
    return migrate_database(db_path)
