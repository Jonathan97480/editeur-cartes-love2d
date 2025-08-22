#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour convertir tous les chemins absolus en chemins relatifs dans la base de données
"""
import sqlite3
import os
import sys

# Ajouter le dossier lib au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

try:
    from utils import convert_to_relative_path
except ImportError:
    # Fonction de fallback si l'import échoue
    def convert_to_relative_path(absolute_path: str) -> str:
        if not absolute_path:
            return ''
        normalized_path = absolute_path.replace('\\', '/')
        if 'images' in normalized_path:
            parts = normalized_path.split('/')
            try:
                idx = parts.index('images')
                relative_path = '/'.join(parts[idx:])
                return relative_path
            except ValueError:
                pass
        return normalized_path

def convert_paths_to_relative():
    """Convertit tous les chemins absolus en chemins relatifs dans la base de données"""
    conn = sqlite3.connect('cartes.db')
    cursor = conn.cursor()
    
    # Récupérer toutes les cartes avec des images
    cursor.execute('SELECT id, name, img FROM cards WHERE img IS NOT NULL AND img != ""')
    cards = cursor.fetchall()
    
    print(f"Trouvé {len(cards)} cartes avec des images")
    print("=" * 60)
    
    updated_count = 0
    
    for card_id, name, img_path in cards:
        if img_path:
            # Convertir en chemin relatif
            relative_path = convert_to_relative_path(img_path)
            
            # Mettre à jour seulement si le chemin a changé
            if relative_path != img_path:
                cursor.execute('UPDATE cards SET img = ? WHERE id = ?', (relative_path, card_id))
                print(f"✅ {name}:")
                print(f"   Ancien: {img_path}")
                print(f"   Nouveau: {relative_path}")
                print()
                updated_count += 1
            else:
                print(f"⏭️  {name}: déjà en format relatif")
    
    # Sauvegarder les changements
    conn.commit()
    conn.close()
    
    print("=" * 60)
    print(f"✅ Conversion terminée ! {updated_count} cartes mises à jour.")
    
    return updated_count

if __name__ == "__main__":
    convert_paths_to_relative()
