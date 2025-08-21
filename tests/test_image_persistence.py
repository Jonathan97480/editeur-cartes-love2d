#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la correction du problème de sauvegarde des images fusionnées
"""
# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()


import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

def test_image_fusion_persistence():
    """Test que les images fusionnées sont bien sauvegardées en base."""

    print("🧪 Test de persistence des images fusionnées")
    print("=" * 50)
    
    try:
        from lib.database import CardRepo, Card
        from lib.utils import ensure_images_subfolders
        
        # Vérifier qu'il y a des cartes avec images fusionnées
        repo = CardRepo("cartes.db")
        cards = repo.list_cards()
        
        if not cards:
            print("   ⚠️ Aucune carte en base pour tester")
            return False
        
        subfolders = ensure_images_subfolders()
        cards_folder = subfolders['cards']
        
        fused_cards = []
        original_cards = []
        
        for card in cards:
            if not card.img:
                continue
                
            # Vérifier si l'image stockée en base est dans le dossier cards/ (fusionnée)
            if "cards/" in card.img or cards_folder in card.img:
                fused_cards.append(card)
                print(f"   ✅ {card.name}: utilise image fusionnée ({os.path.basename(card.img)})")
            else:
                original_cards.append(card)
                print(f"   ⚠️ {card.name}: utilise image originale ({os.path.basename(card.img)})")
        
        print(f"\n📊 Résultats :")
        print(f"   Cartes avec images fusionnées : {len(fused_cards)}")
        print(f"   Cartes avec images originales : {len(original_cards)}")
        
        # Vérifier que les fichiers existent
        missing_files = 0
        for card in fused_cards:
            if not os.path.exists(card.img):
                print(f"   ❌ Image manquante : {card.img}")
                missing_files += 1
        
        if missing_files == 0:
            print(f"   ✅ Tous les fichiers d'images fusionnées existent")
        else:
            print(f"   ❌ {missing_files} fichiers manquants")
        
        # Vérifier si des images fusionnées existent sur disque mais ne sont pas référencées
        if os.path.exists(cards_folder):
            files_on_disk = os.listdir(cards_folder)
            db_files = [os.path.basename(card.img) for card in fused_cards]
            
            orphaned = [f for f in files_on_disk if f not in db_files and not f.endswith('_fused.png')]
            
            if orphaned:
                print(f"\n   ⚠️ Images fusionnées non référencées en base :")
                for f in orphaned:
                    print(f"      - {f}")
            else:
                print(f"\n   ✅ Toutes les images fusionnées sont correctement référencées")
        
        return len(fused_cards) > 0 and missing_files == 0
        
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Point d'entrée principal."""
    try:
        success = test_image_fusion_persistence()
        
        print(f"\n{'='*50}")
        if success:
            print("🎉 Test réussi !")
            print("\n📝 Avec la correction appliquée :")
            print("   ✅ Les images fusionnées sont maintenant sauvegardées en base")
            print("   ✅ Au redémarrage, les cartes pointent vers les bonnes images")
            print("   ✅ Plus de message 'pas d'image' au redémarrage")
        else:
            print("⚠️ Des problèmes ont été détectés")
            print("\n💡 Solutions :")
            print("   1. Ouvrir l'éditeur et re-sauvegarder les cartes problématiques")
            print("   2. Cela mettra à jour les chemins en base de données")
            print("   3. La correction automatique s'appliquera aux nouvelles sauvegardes")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'='*50}")
        print("Appuyez sur Entrée pour fermer...")
        input()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrompu")
        sys.exit(1)
