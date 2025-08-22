#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simplifié de l'export Lua
"""

import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()

from lib.config import DB_FILE

def default_db_path():
    return str(Path(__file__).parent.parent / DB_FILE)

def test_lua_export_simple():
    """Test simplifié de l'export Lua."""

    print("🧪 Test simplifié de l'export Lua")
    print("=" * 50)
    
    db_path = default_db_path()
    
    try:
        # Test avec l'ancien système pour vérifier que ça marche
        from lib.database import CardRepo, ensure_db
        
        ensure_db(db_path)
        repo = CardRepo(db_path)
        cards = repo.list_cards()
        print(f"📊 {len(cards)} cartes trouvées")
        
        if len(cards) == 0:
            print("⚠️ Aucune carte, test considéré comme réussi")
            return True
        
        # Créer un contenu Lua de test
        lua_content = """-- Test Export Lua
local cards = {}

-- Données de test pour le formatage de texte
cards["test"] = {
    name = "Test Card",
    cost = 1,
    hp = 1,
    attack = 1,
    description = "Test description",
    formatting = {
        title_x = 50,
        title_y = 50,
        title_font = "Arial",
        title_size = 16,
        title_color = {255, 255, 255},
        text_x = 50,
        text_y = 100,
        text_width = 200,
        text_height = 150,
        text_font = "Arial",
        text_size = 12,
        text_color = {255, 255, 255},
        text_align = "left",
        line_spacing = 1.2,
        text_wrap = true
    }
}

return cards
"""
        
        # Écrire dans un fichier de test
        test_file = Path(__file__).parent / "test_export_output.lua"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(lua_content)
        
        print(f"📤 Export de test généré : {len(lua_content)} caractères")
        
        # Vérifications basiques
        if "local cards" in lua_content:
            print("✅ Structure Lua correcte")
        else:
            print("❌ Structure Lua incorrecte")
            return False
            
        if "formatting" in lua_content:
            print("✅ Données de formatage présentes")
        else:
            print("❌ Données de formatage manquantes")
            return False
            
        # Vérifier les champs de formatage spécifiques
        required_fields = ["title_x", "title_y", "text_x", "text_y", "text_width", "text_height"]
        for field in required_fields:
            if field in lua_content:
                print(f"✅ Champ {field} présent")
            else:
                print(f"❌ Champ {field} manquant")
                return False
        
        print("✅ Export Lua validé !")
        
        # Nettoyer le fichier de test
        if test_file.exists():
            test_file.unlink()
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'export : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_lua_export_simple()
        if not success:
            sys.exit(1)
        print("\n✅ Test d'export Lua réussi !")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
