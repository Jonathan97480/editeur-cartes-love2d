"""
Module de gestion de la base de données simplifiée pour les cartes avec formatage de texte.
"""
import sqlite3
import os
from typing import List, Optional

class Card:
    def __init__(self, row=None):
        # Champs de base
        self.id = None
        self.nom = ''
        self.type = ''
        self.rarete = ''
        self.cout = 0
        self.description = ''
        self.image_path = ''
        
        # Champs de formatage du titre
        self.title_x = 50
        self.title_y = 30
        self.title_font = 'Arial'
        self.title_size = 16
        self.title_color = '#000000'
        
        # Champs de formatage du texte
        self.text_x = 50
        self.text_y = 100
        self.text_width = 200
        self.text_height = 150
        self.text_font = 'Arial'
        self.text_size = 12
        self.text_color = '#000000'
        self.text_align = 'left'
        self.line_spacing = 1.2
        self.text_wrap = True
        
        if row:
            self.from_row(row)

    def from_row(self, row):
        """Initialize card from database row."""
        if row is None:
            return
        
        # Champs de base
        self.id = row['id'] if 'id' in row.keys() else None
        self.nom = row['nom'] if 'nom' in row.keys() else ''
        self.type = row['type'] if 'type' in row.keys() else ''
        self.rarete = row['rarete'] if 'rarete' in row.keys() else ''
        self.cout = row['cout'] if 'cout' in row.keys() else 0
        self.description = row['description'] if 'description' in row.keys() else ''
        self.image_path = row['image_path'] if 'image_path' in row.keys() else ''
        
        # Champs de formatage du titre
        self.title_x = row['title_x'] if 'title_x' in row.keys() else 50
        self.title_y = row['title_y'] if 'title_y' in row.keys() else 30
        self.title_font = row['title_font'] if 'title_font' in row.keys() else 'Arial'
        self.title_size = row['title_size'] if 'title_size' in row.keys() else 16
        self.title_color = row['title_color'] if 'title_color' in row.keys() else '#000000'
        
        # Champs de formatage du texte
        self.text_x = row['text_x'] if 'text_x' in row.keys() else 50
        self.text_y = row['text_y'] if 'text_y' in row.keys() else 100
        self.text_width = row['text_width'] if 'text_width' in row.keys() else 200
        self.text_height = row['text_height'] if 'text_height' in row.keys() else 150
        self.text_font = row['text_font'] if 'text_font' in row.keys() else 'Arial'
        self.text_size = row['text_size'] if 'text_size' in row.keys() else 12
        self.text_color = row['text_color'] if 'text_color' in row.keys() else '#000000'
        self.text_align = row['text_align'] if 'text_align' in row.keys() else 'left'
        self.line_spacing = row['line_spacing'] if 'line_spacing' in row.keys() else 1.2
        self.text_wrap = bool(row['text_wrap']) if 'text_wrap' in row.keys() else True

    def to_db_tuple(self):
        """Convert card to database tuple for insertion/update."""
        return (
            self.nom,
            self.type,
            self.rarete,
            self.cout,
            self.description,
            self.image_path,
            self.title_x,
            self.title_y,
            self.title_font,
            self.title_size,
            self.title_color,
            self.text_x,
            self.text_y,
            self.text_width,
            self.text_height,
            self.text_font,
            self.text_size,
            self.text_color,
            self.text_align,
            self.line_spacing,
            int(self.text_wrap)
        )

    def to_dict(self):
        """Convert card to dictionary for export."""
        return {
            'id': self.id,
            'nom': self.nom,
            'type': self.type,
            'rarete': self.rarete,
            'cout': self.cout,
            'description': self.description,
            'image_path': self.image_path,
            'title_x': self.title_x,
            'title_y': self.title_y,
            'title_font': self.title_font,
            'title_size': self.title_size,
            'title_color': self.title_color,
            'text_x': self.text_x,
            'text_y': self.text_y,
            'text_width': self.text_width,
            'text_height': self.text_height,
            'text_font': self.text_font,
            'text_size': self.text_size,
            'text_color': self.text_color,
            'text_align': self.text_align,
            'line_spacing': self.line_spacing,
            'text_wrap': self.text_wrap
        }

    @property
    def img(self):
        """Propriété de compatibilité pour image_path."""
        return self.image_path
    
    @img.setter
    def img(self, value):
        """Setter pour la propriété de compatibilité."""
        self.image_path = value

class CardRepo:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.init_database()

    def connect(self):
        """Create database connection with Row factory."""
        con = sqlite3.connect(self.db_file)
        con.row_factory = sqlite3.Row
        return con

    def init_database(self):
        """Initialize database with basic structure if needed."""
        if not os.path.exists(self.db_file):
            self.create_tables()

    def create_tables(self):
        """Create the cards table with all formatting fields."""
        con = self.connect()
        cursor = con.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                type TEXT NOT NULL,
                rarete TEXT NOT NULL,
                cout INTEGER NOT NULL,
                description TEXT NOT NULL,
                image_path TEXT,
                title_x INTEGER DEFAULT 50,
                title_y INTEGER DEFAULT 30,
                title_font TEXT DEFAULT 'Arial',
                title_size INTEGER DEFAULT 16,
                title_color TEXT DEFAULT '#000000',
                text_x INTEGER DEFAULT 50,
                text_y INTEGER DEFAULT 100,
                text_width INTEGER DEFAULT 200,
                text_height INTEGER DEFAULT 150,
                text_font TEXT DEFAULT 'Arial',
                text_size INTEGER DEFAULT 12,
                text_color TEXT DEFAULT '#000000',
                text_align TEXT DEFAULT 'left',
                line_spacing REAL DEFAULT 1.2,
                text_wrap INTEGER DEFAULT 1
            )
        ''')
        
        con.commit()
        con.close()

    def list_cards(self, side: str = None, search_text: str = None, rarity: str = None) -> List[Card]:
        """List all cards with optional filtering."""
        con = self.connect()
        cursor = con.cursor()
        
        query = "SELECT * FROM cards"
        params = []
        where_clauses = []
        
        if search_text:
            where_clauses.append("(nom LIKE ? OR description LIKE ?)")
            params.extend([f"%{search_text}%", f"%{search_text}%"])
        
        if rarity:
            where_clauses.append("rarete = ?")
            params.append(rarity)
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " ORDER BY nom"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        con.close()
        
        return [Card(row) for row in rows]

    def get_card(self, card_id: int) -> Optional[Card]:
        """Get a specific card by ID."""
        con = self.connect()
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
        row = cursor.fetchone()
        con.close()
        
        return Card(row) if row else None

    def save_card(self, card: Card) -> int:
        """Save a card (insert or update)."""
        con = self.connect()
        cursor = con.cursor()
        
        if card.id:
            # Update existing card
            cursor.execute('''
                UPDATE cards SET 
                    nom = ?, type = ?, rarete = ?, cout = ?, description = ?, image_path = ?,
                    title_x = ?, title_y = ?, title_font = ?, title_size = ?, title_color = ?,
                    text_x = ?, text_y = ?, text_width = ?, text_height = ?, text_font = ?,
                    text_size = ?, text_color = ?, text_align = ?, line_spacing = ?, text_wrap = ?
                WHERE id = ?
            ''', card.to_db_tuple() + (card.id,))
        else:
            # Insert new card
            cursor.execute('''
                INSERT INTO cards (
                    nom, type, rarete, cout, description, image_path,
                    title_x, title_y, title_font, title_size, title_color,
                    text_x, text_y, text_width, text_height, text_font,
                    text_size, text_color, text_align, line_spacing, text_wrap
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', card.to_db_tuple())
            card.id = cursor.lastrowid
        
        con.commit()
        con.close()
        return card.id

    def delete_card(self, card_id: int) -> bool:
        """Delete a card by ID."""
        con = self.connect()
        cursor = con.cursor()
        
        cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        deleted = cursor.rowcount > 0
        
        con.commit()
        con.close()
        return deleted

    def get_rarites(self) -> List[str]:
        """Get all unique rarities."""
        con = self.connect()
        cursor = con.cursor()
        
        cursor.execute("SELECT DISTINCT rarete FROM cards ORDER BY rarete")
        rows = cursor.fetchall()
        con.close()
        
        return [row[0] for row in rows]

    def get_types(self) -> List[str]:
        """Get all unique types."""
        con = self.connect()
        cursor = con.cursor()
        
        cursor.execute("SELECT DISTINCT type FROM cards ORDER BY type")
        rows = cursor.fetchall()
        con.close()
        
        return [row[0] for row in rows]

    def export_all_cards(self) -> List[dict]:
        """Export all cards as dictionaries."""
        cards = self.list_cards()
        return [card.to_dict() for card in cards]
