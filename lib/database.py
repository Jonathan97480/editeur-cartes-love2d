#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle de données et gestion de la base de données
"""
import json
import sqlite3
from datetime import datetime
from .config import RARITY_VALUES

# ======================= Modèle de données =======================

class Card:
    def __init__(self, row=None):
        self.id: int | None = None
        self.side = 'joueur'  # 'joueur' | 'ia'
        self.name = ''
        self.img = ''  # Image fusionnée (pour affichage)
        self.original_img = ''  # Image originale (pour fusion)
        self.description = ''
        self.powerblow = 0
        self.rarity = 'commun'
        self.types: list[str] = []
        self.hero = {
            "heal": 0,
            "shield": 0,
            "Epine": 0,
            "attack": 0,
            "AttackReduction": 0,
            "shield_pass": 0,
            "bleeding": {"value": 0, "number_turns": 0},
            "force_augmented": {"value": 0, "number_turns": 0},
            "chancePassedTour": 0,
            "energyCostIncrease": 0,
            "energyCostDecrease": 0
        }
        self.enemy = {
            "heal": 0,
            "shield": 0,
            "Epine": 0,
            "attack": 0,
            "AttackReduction": 0,
            "shield_pass": 0,
            "bleeding": {"value": 0, "number_turns": 0},
            "force_augmented": {"value": 0, "number_turns": 0},
            "chancePassedTour": 0,
            "energyCostIncrease": 0,
            "energyCostDecrease": 0
        }
        self.action = ''
        self.action_param = ''  # '' ou '_user'
        self.created_at = ''
        self.updated_at = ''
        if row:
            self.from_row(row)

    def from_row(self, row):
        # Support sqlite3.Row (nommé) ou tuple ancien schéma
        if isinstance(row, sqlite3.Row):
            self.id = row['id']
            self.side = row['side']
            self.name = row['name']
            self.img = row['img']
            # Gestion du champ original_img avec fallback
            if 'original_img' in row.keys() and row['original_img']:
                self.original_img = row['original_img']
            else:
                self.original_img = row['img']  # Fallback vers img si pas de original_img
            self.description = row['description']
            self.powerblow = row['powerblow']
            self.rarity = row['rarity']
            self.types = json.loads(row['types_json']) if 'types_json' in row.keys() else []
            self.hero = json.loads(row['hero_json'])
            self.enemy = json.loads(row['enemy_json'])
            self.action = row['action']
            self.action_param = row['action_param']
            self.created_at = row['created_at']
            self.updated_at = row['updated_at']
        else:
            (
                self.id,
                self.side,
                self.name,
                self.img,
                self.description,
                self.powerblow,
                hero_json,
                enemy_json,
                self.action,
                self.action_param,
                self.created_at,
                self.updated_at,
            ) = row
            self.hero = json.loads(hero_json)
            self.enemy = json.loads(enemy_json)
            self.types = []  # ancien schéma

    def to_db_tuple(self):
        now = datetime.utcnow().isoformat()
        return (
            self.side,
            self.name,
            self.img,
            self.original_img,
            self.description,
            int(self.powerblow),
            self.rarity,
            json.dumps(self.types, ensure_ascii=False),
            json.dumps(self.hero, ensure_ascii=False),
            json.dumps(self.enemy, ensure_ascii=False),
            self.action,
            self.action_param,
            now,
            now,
        )

# ======================= Repository =======================

class CardRepo:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def connect(self):
        con = sqlite3.connect(self.db_file)
        con.row_factory = sqlite3.Row
        return con

    def list_cards(self, side: str | None = None, search_text: str | None = None, rarity: str | None = None):
        con = self.connect(); cur = con.cursor()
        q = "SELECT * FROM cards"; params = []; where = []
        if side in ('joueur', 'ia'):
            where.append("side = ?"); params.append(side)
        if rarity in RARITY_VALUES:
            where.append("rarity = ?"); params.append(rarity)
        if search_text:
            where.append("(name LIKE ? OR description LIKE ?)")
            params.extend([f"%{search_text}%", f"%{search_text}%"])
        if where:
            q += " WHERE " + " AND ".join(where)
        q += (
            " ORDER BY CASE rarity "
            "WHEN 'commun' THEN 1 WHEN 'rare' THEN 2 WHEN 'legendaire' THEN 3 WHEN 'mythique' THEN 4 ELSE 5 END, "
            "updated_at DESC, id DESC"
        )
        cur.execute(q, params); rows = cur.fetchall(); con.close()
        return [Card(row) for row in rows]

    def get(self, card_id: int) -> Card | None:
        con = self.connect(); cur = con.cursor()
        cur.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
        row = cur.fetchone(); con.close()
        return Card(row) if row else None

    def insert(self, card: Card) -> int:
        con = self.connect(); cur = con.cursor()
        cur.execute(
            """
            INSERT INTO cards (
                side, name, img, original_img, description, powerblow,
                rarity, types_json,
                hero_json, enemy_json, action, action_param,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            card.to_db_tuple(),
        )
        con.commit(); card.id = cur.lastrowid; con.close()
        return int(card.id)

    def update(self, card: Card) -> int:
        if card.id is None:
            return self.insert(card)
        con = self.connect(); cur = con.cursor()
        now = datetime.utcnow().isoformat()
        cur.execute(
            """
            UPDATE cards SET
              side=?, name=?, img=?, original_img=?, description=?, powerblow=?,
              rarity=?, types_json=?,
              hero_json=?, enemy_json=?, action=?, action_param=?,
              updated_at=?
            WHERE id=?
            """,
            (
                card.side,
                card.name,
                card.img,
                card.original_img,
                card.description,
                int(card.powerblow),
                card.rarity,
                json.dumps(card.types, ensure_ascii=False),
                json.dumps(card.hero, ensure_ascii=False),
                json.dumps(card.enemy, ensure_ascii=False),
                card.action,
                card.action_param,
                now,
                card.id,
            ),
        )
        con.commit(); con.close()
        return int(card.id)

    def delete(self, card_id: int) -> None:
        con = self.connect(); cur = con.cursor()
        cur.execute("DELETE FROM cards WHERE id=?", (card_id,))
        con.commit(); con.close()

# ======================= Database Setup =======================

def ensure_db(db_path: str) -> None:
    """Assure que la base de données existe et est à jour avec le système de migration."""
    from .database_migration import ensure_db_with_migration
    
    success = ensure_db_with_migration(db_path)
    if not success:
        raise RuntimeError(f"Échec de la migration de la base de données : {db_path}")

def ensure_db_legacy(db_path: str) -> None:
    """Version legacy de ensure_db pour compatibilité."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cards (
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
        """
    )
    # Migration si nécessaire
    cur.execute("PRAGMA table_info(cards)")
    cols = [r[1] for r in cur.fetchall()]
    if 'rarity' not in cols:
        cur.execute("ALTER TABLE cards ADD COLUMN rarity TEXT NOT NULL DEFAULT 'commun'")
    if 'types_json' not in cols:
        cur.execute("ALTER TABLE cards ADD COLUMN types_json TEXT NOT NULL DEFAULT '[]'")
    if 'original_img' not in cols:
        cur.execute("ALTER TABLE cards ADD COLUMN original_img TEXT NOT NULL DEFAULT ''")
        # Initialiser original_img avec la valeur actuelle de img pour les cartes existantes
        cur.execute("UPDATE cards SET original_img = img WHERE original_img = ''")
        print("✅ Migration: Ajout du champ original_img et initialisation avec les images actuelles")
    con.commit()
    con.close()
