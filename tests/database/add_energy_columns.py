#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajout des colonnes de formatage pour le coût en énergie
"""

import sqlite3
from lib.config import DB_FILE

def add_energy_formatting_columns():
    """Ajoute les colonnes de formatage pour le coût en énergie"""
    print('⚡ AJOUT DES COLONNES DE FORMATAGE COÛT ÉNERGIE')
    print('=' * 60)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Colonnes à ajouter pour le coût en énergie
    energy_columns = [
        ('energy_x', 'INTEGER', 25, 'Position X du coût énergie'),
        ('energy_y', 'INTEGER', 25, 'Position Y du coût énergie'),
        ('energy_font', 'TEXT', 'Arial', 'Police du coût énergie'),
        ('energy_size', 'INTEGER', 14, 'Taille police coût énergie'),
        ('energy_color', 'TEXT', '#FFFFFF', 'Couleur du coût énergie')
    ]

    added_columns = []

    for col_name, col_type, default_value, description in energy_columns:
        try:
            if col_type == 'TEXT':
                cursor.execute(f'ALTER TABLE cards ADD COLUMN {col_name} {col_type} DEFAULT "{default_value}"')
            else:
                cursor.execute(f'ALTER TABLE cards ADD COLUMN {col_name} {col_type} DEFAULT {default_value}')
            added_columns.append((col_name, description))
            print(f'✅ Ajouté: {col_name} ({description})')
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e):
                print(f'⚡ Existe déjà: {col_name}')
            else:
                print(f'❌ Erreur pour {col_name}: {e}')

    conn.commit()

    # Vérifier l'ajout
    cursor.execute('PRAGMA table_info(cards)')
    columns = cursor.fetchall()

    energy_cols = [col for col in columns if 'energy' in col[1].lower()]
    print(f'\n📊 Colonnes énergie disponibles: {len(energy_cols)}')
    for col in energy_cols:
        print(f'   - {col[1]}: {col[2]} (default: {col[4]})')

    conn.close()

    print(f'\n✅ Migration terminée - {len(added_columns)} nouvelles colonnes ajoutées')
    return len(added_columns) > 0

if __name__ == "__main__":
    add_energy_formatting_columns()
