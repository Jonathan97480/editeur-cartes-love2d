#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système de migration de la base de données
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database_migration import migrate_database, get_db_version, ensure_db_with_migration
from lib.config import DB_FILE

def default_db_path():
    """Retourne le chemin par défaut de la base de données."""
    return str(Path(__file__).parent / DB_FILE)

def test_migration():
    """Test du système de migration."""
    print("🧪 Test du système de migration de la base de données")
    print("=" * 60)
    
    db_path = default_db_path()
    
    # Afficher l'état actuel
    if os.path.exists(db_path):
        version = get_db_version(db_path)
        print(f"📊 Base de données trouvée")
        print(f"📊 Version actuelle : {version}")
    else:
        print("📊 Aucune base de données trouvée")
    
    print()
    
    # Tester la migration
    print("🔄 Test de la migration...")
    success = ensure_db_with_migration(db_path)
    
    if success:
        new_version = get_db_version(db_path)
        print(f"✅ Migration réussie !")
        print(f"📊 Nouvelle version : {new_version}")
    else:
        print("❌ Échec de la migration")
        return False
    
    print()
    print("🎉 Test terminé avec succès !")
    return True

if __name__ == "__main__":
    try:
        success = test_migration()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    input("\nAppuyez sur Entrée pour fermer...")
