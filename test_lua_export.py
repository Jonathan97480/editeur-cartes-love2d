#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour tester l'export Lua avec les nouveaux chemins relatifs
"""
import sys
import os

# Ajouter le dossier lib au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from database import get_db_connection, Card
from exports import export_to_lua_with_new_logic

def test_lua_export():
    """Teste l'export Lua avec les chemins relatifs"""
    print("🧪 Test de l'export Lua avec chemins relatifs")
    print("=" * 50)
    
    # Récupérer quelques cartes avec images
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cards WHERE img IS NOT NULL AND img != "" LIMIT 3')
    rows = cursor.fetchall()
    
    if not rows:
        print("❌ Aucune carte avec image trouvée")
        return
    
    cards = []
    for row in rows:
        card = Card(
            id=row[0], name=row[1], img=row[2], description=row[3],
            powerblow=row[4], hero=eval(row[5]) if row[5] else {}
        )
        cards.append(card)
    
    conn.close()
    
    print(f"📊 {len(cards)} cartes trouvées avec images")
    
    # Tester l'export
    try:
        lua_content = export_to_lua_with_new_logic(cards)
        
        # Vérifier les chemins dans le contenu
        print("\n🔍 Vérification des chemins dans l'export Lua :")
        lines = lua_content.split('\n')
        for i, line in enumerate(lines):
            if 'img =' in line and 'images/' in line:
                print(f"Ligne {i+1}: {line.strip()}")
                
        print(f"\n✅ Export réussi ! {len(lua_content)} caractères générés")
        
        # Sauvegarder un échantillon
        with open('test_export_sample.lua', 'w', encoding='utf-8') as f:
            f.write(lua_content)
        print("💾 Échantillon sauvegardé dans test_export_sample.lua")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export : {e}")

if __name__ == "__main__":
    test_lua_export()
