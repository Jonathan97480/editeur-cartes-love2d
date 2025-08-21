#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de vérification de l'export Lua avec images fusionnées
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE
from lib.lua_export import export_lua
from lib.utils import get_fused_card_image_path, get_card_image_for_export, ensure_images_subfolders

def default_db_path():
    return str(Path(__file__).parent / DB_FILE)

def test_lua_export_with_fused_images():
    """Test que l'export Lua utilise bien les images fusionnées."""
    print("🧪 Test de l'export Lua avec images fusionnées")
    print("=" * 50)
    
    # Initialiser la base de données
    db_path = default_db_path()
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    ensure_db(db_path)
    repo = CardRepo(db_path)
    
    # Récupérer toutes les cartes
    cards = repo.list_cards()
    
    if not cards:
        print("⚠️  Aucune carte trouvée pour le test")
        return True
    
    print(f"📊 {len(cards)} cartes trouvées")
    
    # Créer la structure de dossiers
    subfolders = ensure_images_subfolders()
    print(f"📁 Dossiers créés :")
    for name, path in subfolders.items():
        print(f"   - {name}: {path}")
    
    # Tester la logique de sélection d'image pour chaque carte
    print("\n🔍 Analyse des images pour chaque carte :")
    
    for card in cards:
        print(f"\n📋 Carte : '{card.name}'")
        print(f"   Image originale : {card.img}")
        
        # Vérifier si une image fusionnée existe
        fused_path = get_fused_card_image_path(card.name)
        if fused_path:
            print(f"   ✅ Image fusionnée trouvée : {fused_path}")
        else:
            print(f"   ⚠️  Aucune image fusionnée trouvée")
        
        # Tester la fonction de sélection d'image pour export
        export_image = get_card_image_for_export(card)
        print(f"   📤 Image pour export : {export_image}")
        
        if fused_path and export_image == fused_path.replace('\\', '/'):
            print(f"   ✅ Utilise correctement l'image fusionnée")
        elif not fused_path and export_image == card.img:
            print(f"   ✅ Utilise correctement l'image originale (pas de fusion)")
        else:
            print(f"   ❌ Problème de sélection d'image")
            return False
    
    # Test de l'export complet
    print(f"\n📤 Test d'export Lua...")
    test_export_path = "test_export_cards.lua"
    
    try:
        export_lua(repo, 'joueur', test_export_path)
        print(f"✅ Export réussi : {test_export_path}")
        
        # Vérifier le contenu du fichier exporté
        with open(test_export_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📊 Taille du fichier exporté : {len(content)} caractères")
        
        # Vérifier que les images fusionnées sont bien référencées
        for card in cards:
            fused_path = get_fused_card_image_path(card.name)
            if fused_path:
                expected_path = fused_path.replace('\\', '/')
                if expected_path in content:
                    print(f"   ✅ Image fusionnée '{card.name}' référencée dans l'export")
                else:
                    print(f"   ⚠️  Image fusionnée '{card.name}' non trouvée dans l'export")
        
        # Nettoyer le fichier de test
        try:
            os.remove(test_export_path)
            print(f"🗑️  Fichier de test supprimé")
        except:
            pass
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export : {e}")
        return False
    
    print("\n🎉 Test terminé avec succès !")
    return True

if __name__ == "__main__":
    try:
        success = test_lua_export_with_fused_images()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Appuyez sur Entrée pour fermer...")
    input()
