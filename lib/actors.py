#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 SYSTÈME D'ACTEURS - Migration du système IA/Joueur vers Acteurs

Ce module gère la transition du système binaire IA/Joueur 
vers un système flexible d'acteurs personnalisés.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class ActorManager:
    """Gestionnaire des acteurs et de leurs liaisons avec les cartes."""
    
    def __init__(self, db_path: str):
        """
        Initialise le gestionnaire d'acteurs.
        
        Args:
            db_path: Chemin vers la base de données SQLite
        """
        self.db_path = db_path
        self.ensure_actors_table()
        self.migrate_legacy_data()
    
    def ensure_actors_table(self):
        """Crée les tables nécessaires pour les acteurs si elles n'existent pas."""
        with sqlite3.connect(self.db_path) as conn:
            # Table des acteurs
            conn.execute("""
                CREATE TABLE IF NOT EXISTS actors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT DEFAULT '',
                    color TEXT DEFAULT '#2196F3',
                    icon TEXT DEFAULT '🎭',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Table de liaison cartes-acteurs (many-to-many)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS card_actors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_id INTEGER NOT NULL,
                    actor_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (card_id) REFERENCES cards (id) ON DELETE CASCADE,
                    FOREIGN KEY (actor_id) REFERENCES actors (id) ON DELETE CASCADE,
                    UNIQUE(card_id, actor_id)
                )
            """)
            
            # Index pour optimiser les requêtes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_card_actors_card_id ON card_actors(card_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_card_actors_actor_id ON card_actors(actor_id)")
            
            conn.commit()
    
    def migrate_legacy_data(self):
        """Migre les données de l'ancien système IA/Joueur vers les acteurs."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Vérifier si des acteurs par défaut existent déjà
            cursor = conn.execute("SELECT COUNT(*) as count FROM actors")
            if cursor.fetchone()['count'] > 0:
                return  # Migration déjà effectuée
            
            # Créer les acteurs par défaut
            now = datetime.utcnow().isoformat()
            default_actors = [
                ('Joueur', 'Cartes du joueur principal', '#4CAF50', '🎮'),
                ('IA', 'Cartes de l\'intelligence artificielle', '#F44336', '🤖'),
                ('Boss', 'Cartes des boss et ennemis principaux', '#9C27B0', '👹'),
                ('PNJ', 'Cartes des personnages non-joueurs', '#FF9800', '👤'),
                ('Marchand', 'Cartes liées aux échanges', '#607D8B', '🛒')
            ]
            
            actor_ids = {}
            for name, description, color, icon in default_actors:
                cursor = conn.execute("""
                    INSERT INTO actors (name, description, color, icon, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, description, color, icon, now, now))
                actor_ids[name] = cursor.lastrowid
            
            # Migrer les cartes existantes
            cursor = conn.execute("SELECT id, side FROM cards")
            cards = cursor.fetchall()
            
            for card in cards:
                if card['side'] == 'joueur':
                    target_actor_id = actor_ids['Joueur']
                elif card['side'] == 'ia':
                    target_actor_id = actor_ids['IA']
                else:
                    target_actor_id = actor_ids['Joueur']  # Par défaut
                
                conn.execute("""
                    INSERT OR IGNORE INTO card_actors (card_id, actor_id, created_at)
                    VALUES (?, ?, ?)
                """, (card['id'], target_actor_id, now))
            
            conn.commit()
            print(f"✅ Migration réussie : {len(default_actors)} acteurs créés, {len(cards)} cartes migrées")

    def list_actors(self):
        """Liste tous les acteurs actifs."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM actors 
                WHERE is_active = 1 
                ORDER BY name
            """)
            return cursor.fetchall()

    def create_actor(self, name: str, description: str = '', color: str = '#2196F3', icon: str = '🎭'):
        """Crée un nouvel acteur."""
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO actors (name, description, color, icon, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, description, color, icon, now, now))
            return cursor.lastrowid

    def delete_actor(self, actor_id: int):
        """Supprime un acteur (désactive)."""
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            # Marquer comme inactif au lieu de supprimer physiquement
            conn.execute("""
                UPDATE actors 
                SET is_active = 0, updated_at = ?
                WHERE id = ?
            """, (now, actor_id))
            
            # Supprimer les liaisons avec les cartes
            conn.execute("DELETE FROM card_actors WHERE actor_id = ?", (actor_id,))
            conn.commit()

    def update_actor(self, actor_id: int, name: str = None, description: str = None, 
                    color: str = None, icon: str = None):
        """Met à jour un acteur."""
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if color is not None:
            updates.append("color = ?")
            params.append(color)
        if icon is not None:
            updates.append("icon = ?")
            params.append(icon)
        
        if updates:
            now = datetime.utcnow().isoformat()
            updates.append("updated_at = ?")
            params.append(now)
            params.append(actor_id)
            
            with sqlite3.connect(self.db_path) as conn:
                query = f"UPDATE actors SET {', '.join(updates)} WHERE id = ?"
                conn.execute(query, params)
                conn.commit()

    def get_actor_cards(self, actor_id: int):
        """Récupère toutes les cartes liées à un acteur."""
        from .database import CardRepo
        
        # Récupérer les IDs des cartes liées à cet acteur
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT card_id FROM card_actors
                WHERE actor_id = ?
                ORDER BY card_id
            """, (actor_id,))
            card_ids = [row[0] for row in cursor.fetchall()]
        
        # Récupérer les objets Card complets
        if not card_ids:
            return []
        
        repo = CardRepo(self.db_path)
        cards = []
        for card_id in card_ids:
            card = repo.get(card_id)
            if card:
                cards.append(card)
        
        return cards

    def get_card_actors(self, card_id: int):
        """Récupère tous les acteurs liés à une carte."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT a.* FROM actors a
                JOIN card_actors ca ON a.id = ca.actor_id
                WHERE ca.card_id = ? AND a.is_active = 1
                ORDER BY a.name
            """, (card_id,))
            return cursor.fetchall()

    def link_card_to_actor(self, card_id: int, actor_id: int):
        """Lie une carte à un acteur."""
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR IGNORE INTO card_actors (card_id, actor_id, created_at)
                VALUES (?, ?, ?)
            """, (card_id, actor_id, now))
            conn.commit()

    def unlink_card_from_actor(self, card_id: int, actor_id: int):
        """Retire le lien entre une carte et un acteur."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                DELETE FROM card_actors 
                WHERE card_id = ? AND actor_id = ?
            """, (card_id, actor_id))
            conn.commit()

    def get_actor_by_id(self, actor_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un acteur par son ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM actors 
                WHERE id = ? AND is_active = 1
            """, (actor_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_actors_stats(self) -> Dict[str, Any]:
        """Récupère des statistiques sur les acteurs."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Nombre total d'acteurs
            cursor = conn.execute("SELECT COUNT(*) as count FROM actors WHERE is_active = 1")
            total_actors = cursor.fetchone()['count']
            
            # Nombre de cartes par acteur
            cursor = conn.execute("""
                SELECT a.name, a.icon, COUNT(ca.card_id) as card_count
                FROM actors a
                LEFT JOIN card_actors ca ON a.id = ca.actor_id
                WHERE a.is_active = 1
                GROUP BY a.id, a.name, a.icon
                ORDER BY card_count DESC, a.name
            """)
            actors_cards = cursor.fetchall()
            
            return {
                'total_actors': total_actors,
                'actors_cards': actors_cards
            }


def generate_lua_content(cards):
    """Génère le contenu Lua pour une liste de cartes."""
    if not cards:
        return "-- Aucune carte disponible\nlocal cards = {}\nreturn cards"
    
    lua_content = []
    lua_content.append("-- Cartes générées automatiquement")
    lua_content.append("local cards = {")
    
    for i, card in enumerate(cards, 1):
        lua_content.append(f"    -- Carte {i}: {card.name}")
        lua_content.append("    {")
        lua_content.append(f'        name = "{card.name}",')
        lua_content.append(f'        description = "{card.description}",')
        lua_content.append(f'        rarity = "{card.rarity}",')
        lua_content.append(f'        powerblow = {card.powerblow},')
        types_str = ", ".join(f'"{t}"' for t in card.types)
        lua_content.append(f'        types = {{{types_str}}},')
        lua_content.append("    },")
    
    lua_content.append("}")
    lua_content.append("return cards")
    
    return "\n".join(lua_content)


def export_lua_for_actor(card_repo, actor_manager: ActorManager, actor_id: int, filename: str = None):
    """
    Exporte les cartes d'un acteur spécifique vers un fichier Lua.
    
    Args:
        card_repo: Instance de CardRepo
        actor_manager: Instance d'ActorManager
        actor_id: ID de l'acteur
        filename: Nom du fichier (optionnel, généré automatiquement si non fourni)
    """
    actor = actor_manager.get_actor_by_id(actor_id)
    if not actor:
        raise ValueError(f"Acteur avec ID {actor_id} introuvable")
    
    cards = actor_manager.get_actor_cards(actor_id)
    
    if filename is None:
        # Générer un nom de fichier basé sur le nom de l'acteur
        safe_name = actor['name'].lower().replace(' ', '_').replace("'", "")
        filename = f"cards_{safe_name}.lua"
    
    # Créer le contenu Lua directement
    content = generate_lua_content(cards)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📤 Export {actor['icon']} {actor['name']} : {len(cards)} cartes → {filename}")
    return filename


def demo_actors_system():
    """Fonction de démonstration du système d'acteurs."""
    print("🎭 DÉMONSTRATION DU SYSTÈME D'ACTEURS")
    print("=" * 50)
    
    from .config import DB_FILE
    from .database import CardRepo
    
    # Initialiser le système
    actor_manager = ActorManager(DB_FILE)
    repo = CardRepo(DB_FILE)
    
    # Afficher les acteurs
    actors = actor_manager.list_actors()
    print(f"\n📋 Acteurs disponibles ({len(actors)}) :")
    for actor in actors:
        cards = actor_manager.get_actor_cards(actor['id'])
        print(f"   {actor['icon']} {actor['name']} : {len(cards)} cartes")
    
    # Test d'export pour chaque acteur ayant des cartes
    print(f"\n📤 Test d'export pour chaque acteur :")
    for actor in actors:
        cards = actor_manager.get_actor_cards(actor['id'])
        if cards:
            try:
                filename = export_lua_for_actor(repo, actor_manager, actor['id'])
                print(f"   ✅ {actor['icon']} {actor['name']} : {len(cards)} cartes → {filename}")
            except Exception as e:
                print(f"   ❌ {actor['icon']} {actor['name']} : Erreur - {e}")
        else:
            print(f"   ⚠️  {actor['icon']} {actor['name']} : Aucune carte")
    
    # Statistiques
    stats = actor_manager.get_actors_stats()
    print(f"\n📊 Statistiques :")
    print(f"   Total acteurs : {stats['total_actors']}")
    print(f"   Répartition des cartes :")
    for stat in stats['actors_cards']:
        print(f"      {stat['icon']} {stat['name']} : {stat['card_count']} cartes")


if __name__ == "__main__":
    demo_actors_system()
