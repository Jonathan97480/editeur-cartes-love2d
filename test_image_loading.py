#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du chargement d'image dans l'éditeur de formatage
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_card_image_loading():
    """Test le chargement d'images de cartes"""
    print("🧪 Test du chargement d'images dans l'éditeur")
    print("=" * 50)
    
    try:
        from lib.database import CardRepo, ensure_db
        from lib.config import DB_FILE
        
        # Configurer la base de données
        db_path = str(Path(__file__).parent / DB_FILE)
        ensure_db(db_path)
        repo = CardRepo(db_path)
        
        cards = repo.list_cards()
        if not cards:
            print("❌ Aucune carte trouvée")
            return False
        
        # Prendre les premières cartes et vérifier leurs images
        for i, card in enumerate(cards[:3]):
            print(f"\n📋 Carte {i+1}: {card.name}")
            print(f"   Image: {card.img}")
            
            # Vérifier si le fichier image existe
            if card.img:
                image_path = Path(__file__).parent / card.img.strip()
                if image_path.exists():
                    print(f"   ✅ Image trouvée: {image_path}")
                    print(f"   📏 Taille: {image_path.stat().st_size} octets")
                else:
                    print(f"   ❌ Image non trouvée: {image_path}")
                    
                    # Chercher dans le dossier images
                    images_dir = Path(__file__).parent / "images"
                    if images_dir.exists():
                        print(f"   🔍 Recherche dans images/...")
                        image_files = list(images_dir.glob("**/*"))
                        image_files = [f for f in image_files if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif']]
                        print(f"   📁 {len(image_files)} images trouvées dans images/:")
                        for img_file in image_files[:5]:
                            print(f"      - {img_file.relative_to(Path(__file__).parent)}")
                        if len(image_files) > 5:
                            print(f"      ... et {len(image_files) - 5} autres")
            else:
                print(f"   ⚠️ Pas de chemin d'image défini")
        
        print(f"\n✅ Test terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_card_image_loading()
    if success:
        print("\n🎉 Test réussi ! Vérifiez les chemins d'images ci-dessus.")
    else:
        print("\n❌ Test échoué.")
