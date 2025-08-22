#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide pour vérifier la correction de l'erreur d'import
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test des imports qui causaient l'erreur."""
    print("🧪 Test des imports corrigés")
    print("=" * 40)
    
    try:
        print("📦 Test import actor_selector...")
        from lib.actor_selector import ActorExportDialog
        print("✅ ActorExportDialog importé avec succès")
        
        print("📦 Test import config...")
        from lib.config import DB_FILE
        print(f"✅ DB_FILE importé : {DB_FILE}")
        
        print("📦 Test import actors...")
        from lib.actors import ActorManager, export_all_actors_lua
        print("✅ ActorManager et export_all_actors_lua importés")
        
        print("📦 Test création ActorManager...")
        actor_manager = ActorManager(DB_FILE)
        print("✅ ActorManager créé avec succès")
        
        print("📦 Test liste des acteurs...")
        actors = actor_manager.list_actors()
        print(f"✅ {len(actors)} acteurs trouvés")
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 Tous les imports fonctionnent correctement !")
    return True

if __name__ == "__main__":
    success = test_imports()
    if not success:
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("Les boutons d'export devraient maintenant fonctionner !")
    print("Vous pouvez tester '🎭 Exporter Acteur' et '📤 Exporter Tout'")
    print("=" * 40)
