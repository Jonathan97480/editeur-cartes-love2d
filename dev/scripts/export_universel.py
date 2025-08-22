#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EXPORTEUR UNIVERSEL LOVE2D AVEC TEXTFORMATTING
===============================================
Ce fichier remplace TOUS les autres exports pour garantir
que l'application utilise TOUJOURS le bon exporteur.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from lua_exporter_love2d import Love2DLuaExporter
from lib.database import CardRepo
from lib.config import DB_FILE

def export_lua(repo, side, filepath):
    """Export universel - utilise TOUJOURS Love2DLuaExporter"""
    exporter = Love2DLuaExporter(repo)
    exporter.export_to_file(filepath)
    print(f"✅ Export Love2D avec TextFormatting: {filepath}")

# Export direct pour tests
if __name__ == "__main__":
    print("🔧 TEST DE L'EXPORTEUR UNIVERSEL")
    print("=" * 50)
    
    repo = CardRepo(DB_FILE)
    export_lua(repo, 'joueur', 'cards_final_corrected.lua')
    
    # Vérifier le résultat
    with open('cards_final_corrected.lua', 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_textformatting = 'TextFormatting' in content
    has_dimensions = 'width' in content and 'height' in content
    card_count = content.count('--[[ CARTE')
    
    print(f"\n📊 RÉSULTATS:")
    print(f"   TextFormatting: {'✅ OUI' if has_textformatting else '❌ NON'}")
    print(f"   Dimensions: {'✅ OUI' if has_dimensions else '❌ NON'}")
    print(f"   Cartes: {card_count}")
    print(f"   Taille: {len(content)} caractères")
    
    if has_textformatting and has_dimensions:
        print(f"\n🎉 EXPORTEUR UNIVERSEL FONCTIONNE PARFAITEMENT!")
    else:
        print(f"\n❌ Problème avec l'exporteur universel")
