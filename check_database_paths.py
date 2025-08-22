#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des chemins absolus dans la base de données
Recherche les chemins Windows (c:/) qui pourraient causer des problèmes de portabilité
"""

import sqlite3
import os
import sys

# Ajouter le chemin lib pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from config import DB_FILE

def check_database_paths():
    """Vérifier s'il y a des chemins absolus Windows dans la base de données"""
    
    print('🔍 VÉRIFICATION DES CHEMINS DANS LA BASE DE DONNÉES')
    print('=' * 60)
    
    if not os.path.exists(DB_FILE):
        print(f'❌ Base de données non trouvée: {DB_FILE}')
        return []
    
    problematic_entries = []
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Vérifier la structure de la table cards
        cursor.execute('PRAGMA table_info(cards)')
        columns = cursor.fetchall()
        print('📋 Colonnes dans la table cards:')
        for col in columns:
            print(f'   - {col[1]}: {col[2]}')
        
        print('\n🔍 Recherche de chemins absolus Windows (c:/)...')
        
        # Colonnes qui peuvent contenir des chemins
        path_columns = ['img', 'original_img', 'image_path']
        
        for col_info in columns:
            col_name = col_info[1]
            col_type = col_info[2]
            
            # Vérifier les colonnes de type TEXT qui pourraient contenir des chemins
            if 'TEXT' in col_type.upper() or col_name in path_columns:
                # Rechercher les chemins Windows absolus
                cursor.execute(f'''
                    SELECT id, {col_name} FROM cards 
                    WHERE {col_name} LIKE "c:%" OR {col_name} LIKE "C:%" 
                    OR {col_name} LIKE "d:%" OR {col_name} LIKE "D:%"
                    OR {col_name} LIKE "e:%" OR {col_name} LIKE "E:%"
                ''')
                results = cursor.fetchall()
                
                if results:
                    print(f'\n❌ Problèmes trouvés dans la colonne "{col_name}":')
                    for row in results:
                        card_id, path_value = row
                        if path_value:  # Ignorer les valeurs NULL
                            print(f'   - ID {card_id}: {path_value}')
                            problematic_entries.append({
                                'table': 'cards',
                                'id': card_id,
                                'column': col_name,
                                'old_path': path_value
                            })
        
        # Vérifier aussi dans la table templates si elle existe
        try:
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="templates"')
            if cursor.fetchone():
                print('\n🔍 Vérification de la table templates...')
                cursor.execute('PRAGMA table_info(templates)')
                template_columns = cursor.fetchall()
                
                for col_info in template_columns:
                    col_name = col_info[1]
                    col_type = col_info[2]
                    
                    if 'TEXT' in col_type.upper():
                        cursor.execute(f'''
                            SELECT id, {col_name} FROM templates 
                            WHERE {col_name} LIKE "c:%" OR {col_name} LIKE "C:%" 
                            OR {col_name} LIKE "d:%" OR {col_name} LIKE "D:%"
                            OR {col_name} LIKE "e:%" OR {col_name} LIKE "E:%"
                        ''')
                        results = cursor.fetchall()
                        
                        if results:
                            print(f'❌ Problèmes dans templates.{col_name}:')
                            for row in results:
                                template_id, path_value = row
                                if path_value:
                                    print(f'   - ID {template_id}: {path_value}')
                                    problematic_entries.append({
                                        'table': 'templates',
                                        'id': template_id,
                                        'column': col_name,
                                        'old_path': path_value
                                    })
        except Exception as e:
            print(f'ℹ️  Erreur lors de la vérification des templates: {e}')
        
        conn.close()
        
    except Exception as e:
        print(f'❌ Erreur lors de la vérification: {e}')
        return []
    
    print(f'\n📊 RÉSUMÉ:')
    print(f'   Entrées problématiques: {len(problematic_entries)}')
    
    if not problematic_entries:
        print('✅ Aucun chemin absolu Windows trouvé dans la base de données!')
    else:
        print('⚠️  Des chemins absolus ont été trouvés et doivent être corrigés')
        print('\n📝 Détails des problèmes:')
        for entry in problematic_entries:
            print(f'   - Table: {entry["table"]}, ID: {entry["id"]}, '
                  f'Colonne: {entry["column"]}, Chemin: {entry["old_path"]}')
    
    return problematic_entries

if __name__ == '__main__':
    problematic_entries = check_database_paths()
    
    if problematic_entries:
        print('\n🔧 Pour corriger ces problèmes, lancez: python fix_database_paths.py')
        sys.exit(1)  # Code d'erreur pour indiquer qu'il y a des problèmes
    else:
        sys.exit(0)  # Tout va bien
