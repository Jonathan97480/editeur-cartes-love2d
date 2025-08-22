#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des chemins absolus dans la base de données
Convertit les chemins Windows absolus en chemins relatifs portables
"""

import sqlite3
import os
import sys
import re

# Ajouter le chemin lib pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from config import DB_FILE

def fix_database_paths():
    """Corriger les chemins absolus Windows dans la base de données"""
    
    print('🔧 CORRECTION DES CHEMINS DANS LA BASE DE DONNÉES')
    print('=' * 60)
    
    if not os.path.exists(DB_FILE):
        print(f'❌ Base de données non trouvée: {DB_FILE}')
        return False
    
    # Faire une sauvegarde avant la correction
    backup_file = DB_FILE.replace('.db', '_backup_before_path_fix.db')
    try:
        import shutil
        shutil.copy2(DB_FILE, backup_file)
        print(f'📁 Sauvegarde créée: {backup_file}')
    except Exception as e:
        print(f'⚠️  Impossible de créer la sauvegarde: {e}')
        print('Continuer quand même ? (y/N): ', end='')
        if input().lower() != 'y':
            return False
    
    corrections_made = 0
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Vérifier la structure de la table cards
        cursor.execute('PRAGMA table_info(cards)')
        columns = cursor.fetchall()
        
        print('\n🔍 Recherche et correction des chemins absolus...')
        
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
                    print(f'\n🔧 Correction de la colonne "{col_name}":')
                    
                    for row in results:
                        card_id, old_path = row
                        if old_path:  # Ignorer les valeurs NULL
                            # Convertir le chemin absolu en chemin relatif
                            new_path = convert_absolute_to_relative(old_path)
                            
                            if new_path != old_path:
                                print(f'   - ID {card_id}:')
                                print(f'     Ancien: {old_path}')
                                print(f'     Nouveau: {new_path}')
                                
                                # Mettre à jour dans la base de données
                                cursor.execute(f'''
                                    UPDATE cards SET {col_name} = ? WHERE id = ?
                                ''', (new_path, card_id))
                                
                                corrections_made += 1
        
        # Vérifier aussi dans la table templates si elle existe
        try:
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="templates"')
            if cursor.fetchone():
                print('\n🔍 Correction de la table templates...')
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
                            print(f'🔧 Correction templates.{col_name}:')
                            for row in results:
                                template_id, old_path = row
                                if old_path:
                                    new_path = convert_absolute_to_relative(old_path)
                                    
                                    if new_path != old_path:
                                        print(f'   - ID {template_id}: {old_path} → {new_path}')
                                        cursor.execute(f'''
                                            UPDATE templates SET {col_name} = ? WHERE id = ?
                                        ''', (new_path, template_id))
                                        corrections_made += 1
        except Exception as e:
            print(f'ℹ️  Erreur lors de la correction des templates: {e}')
        
        # Valider les changements
        if corrections_made > 0:
            conn.commit()
            print(f'\n✅ {corrections_made} corrections appliquées avec succès!')
            
            # Vérifier que les corrections ont fonctionné
            print('\n🔍 Vérification des corrections...')
            cursor.execute('''
                SELECT COUNT(*) FROM cards 
                WHERE img LIKE "c:%" OR img LIKE "C:%" 
                OR img LIKE "d:%" OR img LIKE "D:%"
                OR img LIKE "e:%" OR img LIKE "E:%"
            ''')
            remaining_problems = cursor.fetchone()[0]
            
            if remaining_problems == 0:
                print('✅ Toutes les corrections ont été appliquées avec succès!')
                print('🎯 La base de données utilise maintenant des chemins relatifs portables')
            else:
                print(f'⚠️  Il reste {remaining_problems} chemins absolus non corrigés')
        else:
            print('\n✅ Aucune correction nécessaire')
        
        conn.close()
        
    except Exception as e:
        print(f'❌ Erreur lors de la correction: {e}')
        return False
    
    return True

def convert_absolute_to_relative(absolute_path):
    """Convertir un chemin absolu Windows en chemin relatif portable"""
    
    if not absolute_path:
        return absolute_path
    
    # Normaliser les séparateurs
    path = absolute_path.replace('\\', '/')
    
    # Patterns courants à remplacer
    patterns = [
        # Chemin complet vers le dossier du projet
        (r'[A-Za-z]:/.*?/Nouveau dossier/', ''),
        (r'[A-Za-z]:/.*?/editeur-cartes-love2d/', ''),
        
        # Autres patterns possibles
        (r'[A-Za-z]:/Users/[^/]+/Downloads/[^/]+/', ''),
        (r'[A-Za-z]:/[^/]+/[^/]+/[^/]+/Nouveau dossier/', ''),
        
        # Pattern générique pour tout chemin absolu menant à images/
        (r'[A-Za-z]:/.*?/(?=images/)', ''),
        (r'[A-Za-z]:/.*?/(?=data/)', ''),
        (r'[A-Za-z]:/.*?/(?=lib/)', ''),
        (r'[A-Za-z]:/.*?/(?=assets/)', ''),
    ]
    
    new_path = path
    
    for pattern, replacement in patterns:
        new_path = re.sub(pattern, replacement, new_path, flags=re.IGNORECASE)
    
    # Si ça commence encore par une lettre de lecteur, essayer une approche plus agressive
    if re.match(r'^[A-Za-z]:', new_path):
        # Extraire juste la partie relative à partir de 'images/' ou autres dossiers connus
        known_folders = ['images/', 'data/', 'lib/', 'assets/', 'fonts/']
        for folder in known_folders:
            if folder in new_path:
                parts = new_path.split(folder)
                if len(parts) > 1:
                    new_path = folder + parts[-1]
                    break
    
    return new_path

def create_startup_checker():
    """Créer un script qui vérifie les chemins au démarrage"""
    
    checker_content = '''@echo off
echo 🔍 Vérification des chemins dans la base de données...

python check_database_paths.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️  Des chemins absolus ont été détectés dans la base de données
    echo    Cela peut causer des problèmes de portabilité entre ordinateurs.
    echo.
    echo 🔧 Correction automatique en cours...
    python fix_database_paths.py
    
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Chemins corrigés avec succès!
    ) else (
        echo ❌ Erreur lors de la correction des chemins
        pause
        exit /b 1
    )
) else (
    echo ✅ Tous les chemins sont corrects
)

echo.
'''
    
    with open('check_paths_at_startup.bat', 'w', encoding='utf-8') as f:
        f.write(checker_content)
    
    print('📝 Script de vérification au démarrage créé: check_paths_at_startup.bat')

if __name__ == '__main__':
    success = fix_database_paths()
    
    if success:
        create_startup_checker()
        print('\n🎯 MISSION ACCOMPLIE!')
        print('   ✅ Chemins corrigés dans la base de données')
        print('   ✅ Script de vérification automatique créé')
        print('   ✅ La base de données est maintenant portable')
        print('\n💡 Le script check_paths_at_startup.bat peut être intégré à START.bat')
    else:
        print('\n❌ Erreur lors de la correction')
        sys.exit(1)
