#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide d'export Lua direct
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE
from lib.lua_export import export_lua

def default_db_path():
    return str(Path(__file__).parent / DB_FILE)

def quick_export_test():
    """Test rapide d'export Lua."""
    print("⚡ Test rapide d'export Lua")
    print("=" * 30)
    
    # Initialiser la base de données
    db_path = default_db_path()
    ensure_db(db_path)
    repo = CardRepo(db_path)
    
    # Export cartes joueur
    print("📤 Export cartes joueur...")
    try:
        export_lua(repo, 'joueur', 'cards_player_test.lua')
        print("✅ Export joueur réussi : cards_player_test.lua")
    except Exception as e:
        print(f"❌ Erreur export joueur : {e}")
        return False
    
    # Export cartes IA
    print("📤 Export cartes IA...")
    try:
        export_lua(repo, 'ia', 'cards_ai_test.lua')
        print("✅ Export IA réussi : cards_ai_test.lua")
    except Exception as e:
        print(f"❌ Erreur export IA : {e}")
        return False
    
    print("\n🎉 Exports terminés !")
    print("Fichiers générés :")
    print("- cards_player_test.lua")
    print("- cards_ai_test.lua")
    
    return True

if __name__ == "__main__":
    try:
        quick_export_test()
    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)
    
    input("\nAppuyez sur Entrée pour fermer...")
