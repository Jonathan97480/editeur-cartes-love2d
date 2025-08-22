#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outils de diagnostic et maintenance de la base de données
"""
import argparse
import os
import sys
from pathlib import Path

# Configuration pour éviter les problèmes d'encodage Unicode
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database_migration import (
    migrate_database, get_db_version, verify_database_integrity,
    get_table_schema, REQUIRED_SCHEMA, CURRENT_DB_VERSION
)
from lib.config import DB_FILE

def default_db_path():
    """Retourne le chemin par défaut de la base de données."""
    return str(Path(__file__).parent / DB_FILE)

def diagnose_database():
    """Diagnostic complet de la base de données."""
    print("🔍 Diagnostic de la base de données")
    print("=" * 50)
    
    db_path = default_db_path()
    
    # Vérifier l'existence
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    print(f"📁 Fichier : {db_path}")
    print(f"📊 Taille : {os.path.getsize(db_path)} octets")
    
    # Version
    try:
        version = get_db_version(db_path)
        print(f"📊 Version : {version} (cible: {CURRENT_DB_VERSION})")
    except Exception as e:
        print(f"❌ Erreur lecture version : {e}")
        return False
    
    # Schéma actuel
    try:
        schema = get_table_schema(db_path, "cards")
        print(f"📋 Colonnes présentes : {len(schema)}")
        
        missing_cols = []
        for col_name in REQUIRED_SCHEMA:
            if col_name not in schema:
                missing_cols.append(col_name)
        
        if missing_cols:
            print(f"⚠️  Colonnes manquantes : {', '.join(missing_cols)}")
        else:
            print("✅ Toutes les colonnes requises sont présentes")
            
    except Exception as e:
        print(f"❌ Erreur lecture schéma : {e}")
        return False
    
    # Intégrité
    try:
        integrity_ok = verify_database_integrity(db_path)
        if integrity_ok:
            print("✅ Intégrité vérifiée")
        else:
            print("❌ Problème d'intégrité détecté")
            return False
    except Exception as e:
        print(f"❌ Erreur vérification intégrité : {e}")
        return False
    
    # Compter les cartes
    try:
        import sqlite3
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM cards")
        count = cur.fetchone()[0]
        con.close()
        print(f"📊 Nombre de cartes : {count}")
    except Exception as e:
        print(f"⚠️  Impossible de compter les cartes : {e}")
    
    print("\n🎉 Diagnostic terminé")
    return True

def force_migration():
    """Force une migration complète."""
    print("🔄 Migration forcée de la base de données")
    print("=" * 50)
    
    db_path = default_db_path()
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    try:
        success = migrate_database(db_path)
        if success:
            print("✅ Migration forcée réussie")
            return True
        else:
            print("❌ Échec de la migration forcée")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        import traceback
        traceback.print_exc()
        return False

def backup_database():
    """Crée une sauvegarde de la base de données."""
    print("💾 Sauvegarde de la base de données")
    print("=" * 50)
    
    db_path = default_db_path()
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    try:
        from datetime import datetime
        import shutil
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Créer le dossier dbBackup s'il n'existe pas
        backup_dir = "dbBackup"
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_filename = f"{os.path.basename(db_path)}.backup.manual.{timestamp}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        shutil.copy2(db_path, backup_path)
        print(f"✅ Sauvegarde créée : {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        return False

def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Outils de maintenance base de données")
    parser.add_argument('--diagnose', action='store_true', help='Diagnostic complet')
    parser.add_argument('--migrate', action='store_true', help='Migration forcée')
    parser.add_argument('--backup', action='store_true', help='Sauvegarde manuelle')
    parser.add_argument('--validate', action='store_true', help='Validation rapide intégrité')
    parser.add_argument('--all', action='store_true', help='Exécuter toutes les opérations')
    
    args = parser.parse_args()
    
    if not any([args.diagnose, args.migrate, args.backup, args.validate, args.all]):
        # Par défaut, faire un diagnostic
        args.diagnose = True
    
    success = True
    
    # Validation rapide pour les tests de sécurité
    if args.validate:
        print("Validation rapide de la base de donnees...")
        try:
            if not os.path.exists(default_db_path()):
                print("Erreur: Base de donnees non trouvee")
                return False
            
            # Test de connexion basique
            import sqlite3
            conn = sqlite3.connect(default_db_path())
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            conn.close()
            
            if table_count > 0:
                print(f"Succes: Base de donnees valide ({table_count} tables)")
                return True
            else:
                print("Erreur: Base de donnees vide ou corrompue")
                return False
                
        except Exception as e:
            print(f"Erreur validation: {e}")
            return False
    
    if args.all or args.backup:
        print()
        if not backup_database():
            success = False
    
    if args.all or args.diagnose:
        print()
        if not diagnose_database():
            success = False
    
    if args.all or args.migrate:
        print()
        if not force_migration():
            success = False
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Opération interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Appuyez sur Entrée pour fermer...")
    input()
