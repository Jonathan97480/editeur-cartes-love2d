#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour tester les chemins d'images exportés
"""
import sqlite3

def test_export_paths():
    """Teste que les chemins sont corrects pour l'export"""
    print("🧪 Test des chemins pour l'export Lua")
    print("=" * 40)
    
    conn = sqlite3.connect('cartes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, img FROM cards WHERE img IS NOT NULL AND img != "" LIMIT 5')
    rows = cursor.fetchall()
    
    print("Chemins d'images qui seront utilisés dans l'export :")
    print("-" * 40)
    
    for name, img_path in rows:
        print(f"🃏 {name}")
        print(f"   img = '{img_path}'")
        
        # Vérifier que c'est un chemin relatif
        if img_path.startswith('images/'):
            print("   ✅ Format relatif correct")
        elif '/' in img_path and 'images' in img_path:
            print("   ⚠️  Pourrait être converti en relatif")
        else:
            print("   ❓ Format non standard")
        print()
    
    conn.close()
    
    print("=" * 40)
    print("✅ Test terminé")

if __name__ == "__main__":
    test_export_paths()
