#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SCRIPT DE PRÉVENTION DES CHEMINS ABSOLUS
============================================

Script qui s'exécute après chaque sauvegarde pour détecter
et corriger automatiquement les nouveaux chemins absolus.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Ajouter le chemin lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

try:
    from config import DB_FILE
except ImportError:
    DB_FILE = 'data/cartes.db'

def check_and_fix_new_absolute_paths():
    """Vérifie et corrige les nouveaux chemins absolus"""
    
    if not os.path.exists(DB_FILE):
        return
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Chercher les chemins absolus récents
        cursor.execute("""
            SELECT id, img FROM cards 
            WHERE (img LIKE 'c:%' OR img LIKE 'C:%' OR 
                   img LIKE 'd:%' OR img LIKE 'D:%') 
            AND datetime(updated_at) > datetime('now', '-1 hour')
        """)
        
        recent_issues = cursor.fetchall()
        
        if recent_issues:
            print(f"🚨 {len(recent_issues)} nouveaux chemins absolus détectés!")
            
            for card_id, bad_path in recent_issues:
                # Convertir en relatif
                if 'images/' in bad_path:
                    relative_path = bad_path[bad_path.find('images/'):]
                else:
                    filename = bad_path.split('/')[-1]
                    relative_path = f"images/cards/{filename}"
                
                # Corriger en base
                cursor.execute('UPDATE cards SET img = ? WHERE id = ?', 
                             (relative_path, card_id))
                
                print(f"✅ Corrigé ID {card_id}: {bad_path} → {relative_path}")
            
            conn.commit()
            print("💾 Corrections sauvegardées")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == '__main__':
    check_and_fix_new_absolute_paths()
