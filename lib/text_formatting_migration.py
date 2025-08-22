#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration pour ajouter les fonctionnalités de formatage de texte
"""
import sqlite3
import json
from pathlib import Path

def migrate_database_for_text_formatting():
    """Ajoute les colonnes pour le formatage de texte"""
    db_path = Path(__file__).parent.parent / "cartes.db"
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Vérifier si les colonnes existent déjà
        cursor.execute("PRAGMA table_info(cards)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Ajouter les nouvelles colonnes si elles n'existent pas
        new_columns = [
            ("title_x", "INTEGER DEFAULT 50"),
            ("title_y", "INTEGER DEFAULT 30"),
            ("title_font", "TEXT DEFAULT 'Arial'"),
            ("title_size", "INTEGER DEFAULT 16"),
            ("title_color", "TEXT DEFAULT '#000000'"),
            ("text_x", "INTEGER DEFAULT 50"),
            ("text_y", "INTEGER DEFAULT 100"),
            ("text_width", "INTEGER DEFAULT 200"),
            ("text_height", "INTEGER DEFAULT 150"),
            ("text_font", "TEXT DEFAULT 'Arial'"),
            ("text_size", "INTEGER DEFAULT 12"),
            ("text_color", "TEXT DEFAULT '#000000'"),
            ("text_align", "TEXT DEFAULT 'left'"),
            ("line_spacing", "REAL DEFAULT 1.2"),
            ("text_wrap", "INTEGER DEFAULT 1")
        ]
        
        modifications = []
        for col_name, col_def in new_columns:
            if col_name not in columns:
                cursor.execute(f"ALTER TABLE cards ADD COLUMN {col_name} {col_def}")
                modifications.append(col_name)
        
        conn.commit()
        
        if modifications:
            print(f"✅ Migration réussie - Colonnes ajoutées: {', '.join(modifications)}")
        else:
            print("✅ Base de données déjà à jour")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur migration: {e}")
        return False

if __name__ == "__main__":
    migrate_database_for_text_formatting()
