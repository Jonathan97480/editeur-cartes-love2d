#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script utilitaire pour migrer les images existantes vers la nouvelle structure
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import CardRepo, ensure_db
from lib.utils import ensure_images_subfolders, copy_image_to_originals, sanitize_filename
from lib.config import default_db_path

def migrate_images():
    """Migre toutes les images de cartes vers la nouvelle structure organisée."""
    
    print("=== Migration des Images vers Structure Organisée ===")
    print()
    
    # Vérifier la base de données
    db_path = default_db_path()
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée. Lancez l'application d'abord.")
        return
    
    # Créer la structure de dossiers
    subfolders = ensure_images_subfolders()
    print(f"✅ Structure de dossiers créée :")
    for name, path in subfolders.items():
        print(f"   - {name}: {path}")
    print()
    
    # Connecter à la base de données
    ensure_db(db_path)
    repo = CardRepo(db_path)
    
    # Récupérer toutes les cartes
    cards = repo.list_cards()
    print(f"📊 Trouvé {len(cards)} cartes en base de données")
    print()
    
    migrated_count = 0
    error_count = 0
    
    for card in cards:
        if not card.img:
            continue
            
        print(f"🔍 Traitement de '{card.name}'...")
        
        # Vérifier si l'image existe
        if not os.path.exists(card.img):
            print(f"   ⚠️  Image non trouvée : {card.img}")
            error_count += 1
            continue
            
        # Vérifier si l'image est déjà dans originals
        if subfolders['originals'] in card.img:
            print(f"   ✅ Déjà dans originals")
            continue
            
        # Copier l'image vers originals
        new_path = copy_image_to_originals(card.img, card.name)
        
        if new_path:
            # Mettre à jour le chemin en base de données
            card.img = new_path.replace('\\', '/')
            repo.update(card)
            print(f"   ✅ Migrée vers : {new_path}")
            migrated_count += 1
        else:
            print(f"   ❌ Échec de migration")
            error_count += 1
    
    print()
    print("=== Résumé de la Migration ===")
    print(f"✅ Images migrées : {migrated_count}")
    print(f"❌ Erreurs : {error_count}")
    print(f"📁 Dossier originals : {subfolders['originals']}")
    print(f"📁 Dossier cards : {subfolders['cards']}")
    print(f"📁 Dossier templates : {subfolders['templates']}")
    print()
    
    if migrated_count > 0:
        print("🎉 Migration terminée ! Vos images sont maintenant organisées.")
        print("   Les cartes utilisent désormais les copies locales.")
    else:
        print("ℹ️  Aucune migration nécessaire.")

if __name__ == "__main__":
    try:
        migrate_images()
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        import traceback
        traceback.print_exc()
    
    input("\nAppuyez sur Entrée pour fermer...")
