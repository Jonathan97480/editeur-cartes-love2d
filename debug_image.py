#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic du problème d'image dans l'éditeur
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def debug_image_loading():
    """Debug le chargement d'image dans l'éditeur"""
    print("🔍 Diagnostic du problème d'image")
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
        
        # Trouver une carte avec une image
        card_with_image = None
        for card in cards:
            if card.img and card.img.strip():
                card_with_image = card
                break
        
        if not card_with_image:
            print("❌ Aucune carte avec image trouvée")
            return False
        
        print(f"✅ Carte sélectionnée: {card_with_image.name}")
        print(f"📷 Chemin image brut: '{card_with_image.img}'")
        
        # Simuler ce que fait l'éditeur
        card_image_path = card_with_image.img
        
        print(f"\n🔍 Test de chargement d'image...")
        print(f"   Chemin brut: '{card_image_path}'")
        
        if not card_image_path:
            print("❌ Pas de chemin d'image")
            return False
            
        # Test chemin absolu
        if Path(card_image_path).is_absolute():
            print("📍 Chemin absolu détecté")
            image_path = Path(card_image_path.strip())
        else:
            print("📍 Chemin relatif détecté")
            base_path = Path(__file__).parent
            image_path = base_path / card_image_path.strip()
        
        print(f"   Chemin final: {image_path}")
        print(f"   Existe? {image_path.exists()}")
        
        if image_path.exists():
            print(f"   Taille: {image_path.stat().st_size} octets")
            
            # Test de chargement PIL
            try:
                from PIL import Image
                img = Image.open(image_path)
                print(f"   Format: {img.format}")
                print(f"   Taille: {img.size}")
                print("✅ Image chargeable avec PIL")
            except Exception as e:
                print(f"❌ Erreur PIL: {e}")
                
        else:
            print("❌ Fichier non trouvé")
            
            # Rechercher des fichiers similaires
            print("\n🔍 Recherche de fichiers similaires...")
            base_dir = Path(__file__).parent
            
            # Chercher dans images/
            images_dir = base_dir / "images"
            if images_dir.exists():
                image_files = list(images_dir.glob("**/*.png"))
                image_files.extend(list(images_dir.glob("**/*.jpg")))
                image_files.extend(list(images_dir.glob("**/*.jpeg")))
                
                print(f"   📁 {len(image_files)} images trouvées dans images/")
                for img_file in image_files[:5]:
                    print(f"      - {img_file.relative_to(base_dir)}")
                    
                # Chercher un nom similaire
                card_name = card_with_image.name.replace(" ", "_")
                for img_file in image_files:
                    if card_name.lower() in img_file.name.lower():
                        print(f"   🎯 Fichier similaire trouvé: {img_file.relative_to(base_dir)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_image_loading()
