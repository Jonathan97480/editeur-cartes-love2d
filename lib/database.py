#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle de données et gestion de la base de données
"""
import json
import sqlite3
from datetime import datetime

# Pattern try/except pour imports relatifs/absolus
try:
    from .config import RARITY_VALUES
except ImportError:
    from config import RARITY_VALUES

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
            
            # Champs de formatage de texte (avec valeurs par défaut)
            self.title_x = row['title_x'] if 'title_x' in row.keys() else 50
            self.title_y = row['title_y'] if 'title_y' in row.keys() else 30
            self.title_font = row['title_font'] if 'title_font' in row.keys() else 'Arial'
            self.title_size = row['title_size'] if 'title_size' in row.keys() else 16
            self.title_color = row['title_color'] if 'title_color' in row.keys() else '#000000'
            self.text_x = row['text_x'] if 'text_x' in row.keys() else 50
            self.text_y = row['text_y'] if 'text_y' in row.keys() else 100
            self.text_width = row['text_width'] if 'text_width' in row.keys() else 200
            self.text_height = row['text_height'] if 'text_height' in row.keys() else 150
            self.text_font = row['text_font'] if 'text_font' in row.keys() else 'Arial'
            self.text_size = row['text_size'] if 'text_size' in row.keys() else 12
            self.text_color = row['text_color'] if 'text_color' in row.keys() else '#000000'
            self.text_align = row['text_align'] if 'text_align' in row.keys() else 'left'
            self.line_spacing = row['line_spacing'] if 'line_spacing' in row.keys() else 1.2
            self.text_wrap = row['text_wrap'] if 'text_wrap' in row.keys() else 1
            
            # Champs de formatage du coût en énergie (avec valeurs par défaut)
            self.energy_x = row['energy_x'] if 'energy_x' in row.keys() else 25
            self.energy_y = row['energy_y'] if 'energy_y' in row.keys() else 25
            self.energy_font = row['energy_font'] if 'energy_font' in row.keys() else 'Arial'
            self.energy_size = row['energy_size'] if 'energy_size' in row.keys() else 14
            self.energy_color = row['energy_color'] if 'energy_color' in row.keys() else '#FFFFFF'
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
    try:
        from .database_migration import ensure_db_with_migration
    except ImportError:
        from database_migration import ensure_db_with_migration
    
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
    
    # Migration pour la table des favoris de formatage
    ensure_formatting_favorites_table(cur)
    
    con.commit()
    con.close()


def ensure_formatting_favorites_table(cursor):
    """Crée la table des favoris de formatage si elle n'existe pas."""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS formatting_favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot_number INTEGER NOT NULL CHECK(slot_number IN (1,2,3)),
                name TEXT NOT NULL DEFAULT '',
                -- Données du titre
                title_x REAL DEFAULT 50,
                title_y REAL DEFAULT 30,
                title_font TEXT DEFAULT 'Arial',
                title_size INTEGER DEFAULT 16,
                title_color TEXT DEFAULT '#000000',
                -- Données du texte
                text_x REAL DEFAULT 50,
                text_y REAL DEFAULT 100,
                text_width REAL DEFAULT 200,
                text_height REAL DEFAULT 150,
                text_font TEXT DEFAULT 'Arial',
                text_size INTEGER DEFAULT 12,
                text_color TEXT DEFAULT '#000000',
                text_align TEXT DEFAULT 'left',
                line_spacing REAL DEFAULT 1.2,
                text_wrap INTEGER DEFAULT 1,
                -- Données de l'énergie
                energy_x REAL DEFAULT 25,
                energy_y REAL DEFAULT 25,
                energy_font TEXT DEFAULT 'Arial',
                energy_size INTEGER DEFAULT 14,
                energy_color TEXT DEFAULT '#FFFFFF',
                -- Métadonnées
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(slot_number)
            )
        """)
        
        # Vérifier si la table existe vraiment
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formatting_favorites'")
        if cursor.fetchone():
            print("🔧 Migration: Table formatting_favorites créée/vérifiée avec succès")
        else:
            print("⚠️  Migration: Impossible de créer la table formatting_favorites")
            
    except Exception as e:
        print(f"❌ Erreur migration formatting_favorites: {e}")


def save_formatting_favorite(db_path: str, slot_number: int, data: dict, name: str = ""):
    """Sauvegarde un favori de formatage dans un slot."""
    if slot_number not in [1, 2, 3]:
        raise ValueError(f"Slot invalide: {slot_number}. Doit être 1, 2 ou 3.")
    
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Vérifier que la table existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formatting_favorites'")
        if not cur.fetchone():
            ensure_formatting_favorites_table(cur)
        
        from datetime import datetime
        now = datetime.now().isoformat()
        
        # Utiliser INSERT OR REPLACE pour mettre à jour ou créer
        cur.execute("""
            INSERT OR REPLACE INTO formatting_favorites (
                slot_number, name,
                title_x, title_y, title_font, title_size, title_color,
                text_x, text_y, text_width, text_height, text_font, text_size, 
                text_color, text_align, line_spacing, text_wrap,
                energy_x, energy_y, energy_font, energy_size, energy_color,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            slot_number, name or f"Favori {slot_number}",
            data.get('title_x', 50), data.get('title_y', 30), 
            data.get('title_font', 'Arial'), data.get('title_size', 16), 
            data.get('title_color', '#000000'),
            data.get('text_x', 50), data.get('text_y', 100),
            data.get('text_width', 200), data.get('text_height', 150),
            data.get('text_font', 'Arial'), data.get('text_size', 12),
            data.get('text_color', '#000000'), data.get('text_align', 'left'),
            data.get('line_spacing', 1.2), data.get('text_wrap', 1),
            data.get('energy_x', 25), data.get('energy_y', 25),
            data.get('energy_font', 'Arial'), data.get('energy_size', 14),
            data.get('energy_color', '#FFFFFF'),
            now, now
        ))
        
        con.commit()
        con.close()
        
        display_name = name or f"Favori {slot_number}"
        print(f"✅ Favori '{display_name}' sauvegardé dans slot {slot_number}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde favori slot {slot_number}: {e}")
        return False


def get_formatting_favorite(db_path: str, slot_number: int):
    """Récupère un favori de formatage depuis un slot."""
    if slot_number not in [1, 2, 3]:
        raise ValueError(f"Slot invalide: {slot_number}. Doit être 1, 2 ou 3.")
    
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Vérifier que la table existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formatting_favorites'")
        if not cur.fetchone():
            con.close()
            return None
        
        cur.execute("SELECT * FROM formatting_favorites WHERE slot_number = ?", (slot_number,))
        row = cur.fetchone()
        con.close()
        
        if not row:
            return None
        
        # Convertir en dictionnaire
        columns = [
            'id', 'slot_number', 'name',
            'title_x', 'title_y', 'title_font', 'title_size', 'title_color',
            'text_x', 'text_y', 'text_width', 'text_height', 'text_font', 
            'text_size', 'text_color', 'text_align', 'line_spacing', 'text_wrap',
            'energy_x', 'energy_y', 'energy_font', 'energy_size', 'energy_color',
            'created_at', 'updated_at'
        ]
        
        favorite = dict(zip(columns, row))
        print(f"🟢 Favori '{favorite['name']}' chargé depuis slot {slot_number}")
        return favorite
        
    except Exception as e:
        print(f"❌ Erreur chargement favori slot {slot_number}: {e}")
        return None


def list_formatting_favorites(db_path: str):
    """Liste tous les favoris de formatage."""
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Vérifier que la table existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formatting_favorites'")
        if not cur.fetchone():
            con.close()
            return {}
        
        cur.execute("SELECT slot_number, name FROM formatting_favorites ORDER BY slot_number")
        rows = cur.fetchall()
        con.close()
        
        favorites = {}
        for slot, name in rows:
            favorites[slot] = name
            
        return favorites
        
    except Exception as e:
        print(f"❌ Erreur listage favoris: {e}")
        return {}


def delete_formatting_favorite(db_path: str, slot_number: int):
    """Supprime un favori de formatage."""
    if slot_number not in [1, 2, 3]:
        raise ValueError(f"Slot invalide: {slot_number}. Doit être 1, 2 ou 3.")
    
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Vérifier que la table existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formatting_favorites'")
        if not cur.fetchone():
            con.close()
            return False
        
        cur.execute("DELETE FROM formatting_favorites WHERE slot_number = ?", (slot_number,))
        deleted = cur.rowcount > 0
        con.commit()
        con.close()
        
        if deleted:
            print(f"🗑️ Favori slot {slot_number} supprimé")
        else:
            print(f"⚠️ Aucun favori trouvé dans slot {slot_number}")
            
        return deleted
        
    except Exception as e:
        print(f"❌ Erreur suppression favori slot {slot_number}: {e}")
        return False


def validate_formatting_data(data):
    """Valide les données de formatage avant sauvegarde."""
    try:
        # Vérifier les types et valeurs
        required_fields = [
            'title_x', 'title_y', 'title_size',
            'text_x', 'text_y', 'text_width', 'text_height', 'text_size',
            'energy_x', 'energy_y', 'energy_size'
        ]
        
        for field in required_fields:
            if field not in data:
                return False, f"Champ manquant: {field}"
            
            value = data[field]
            if not isinstance(value, (int, float)):
                return False, f"Valeur invalide pour {field}: {value}"
            
            # Vérifier les limites raisonnables
            if field.endswith('_size') and (value < 1 or value > 100):
                return False, f"Taille invalide pour {field}: {value}"
        
        return True, "Données valides"
        
    except Exception as e:
        return False, f"Erreur validation: {e}"
