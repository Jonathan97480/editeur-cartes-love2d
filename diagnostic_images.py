#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic et réparation des problèmes d'images
"""

import os
import sys
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.config import APP_SETTINGS
from lib.utils import ensure_images_subfolders

def check_pillow():
    """Vérifie si Pillow est disponible et fonctionne."""
    print("🔍 VÉRIFICATION DE PILLOW")
    print("=" * 40)
    
    try:
        from PIL import Image, ImageFile
        print("✅ Pillow est installé")
        print(f"   Version PIL disponible")
        
        # Activer le support des images tronquées
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        print("✅ Support images tronquées activé")
        
        # Tester la création d'une image simple
        test_img = Image.new('RGB', (100, 100), (255, 0, 0))
        print("✅ Création d'image test réussie")
        
        return True
        
    except ImportError as e:
        print(f"❌ Pillow n'est pas installé : {e}")
        print("   Installation : pip install Pillow")
        return False
    except Exception as e:
        print(f"❌ Erreur Pillow : {e}")
        return False

def check_image_file(image_path):
    """Vérifie et diagnostique un fichier image."""
    print(f"\n🔍 DIAGNOSTIC : {os.path.basename(image_path)}")
    print("-" * 50)
    
    if not os.path.exists(image_path):
        print(f"❌ Fichier inexistant : {image_path}")
        return False
    
    # Informations fichier
    file_size = os.path.getsize(image_path)
    print(f"📊 Taille fichier : {file_size} octets")
    
    if file_size == 0:
        print("❌ Fichier vide")
        return False
    
    if file_size < 100:
        print("⚠️  Fichier très petit, possiblement corrompu")
    
    try:
        from PIL import Image, ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        
        # Tentative d'ouverture
        with Image.open(image_path) as img:
            print(f"✅ Image ouverte avec succès")
            print(f"   Format : {img.format}")
            print(f"   Mode : {img.mode}")
            print(f"   Taille : {img.size}")
            
            # Test de chargement complet
            img.load()
            print(f"✅ Chargement complet réussi")
            
            # Test de conversion
            if img.mode not in ['RGB', 'RGBA']:
                rgb_img = img.convert('RGB')
                print(f"✅ Conversion RGB possible")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur image : {e}")
        print(f"   Type erreur : {type(e).__name__}")
        
        if "truncated" in str(e).lower():
            print("   🔧 Solution : Image tronquée, essai de réparation...")
            return try_repair_image(image_path)
        
        return False

def try_repair_image(image_path):
    """Tente de réparer une image corrompue."""
    print(f"🔧 TENTATIVE DE RÉPARATION")
    
    try:
        from PIL import Image, ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        
        # Créer un chemin de sauvegarde
        backup_path = image_path + ".backup"
        repair_path = image_path + ".repaired"
        
        # Sauvegarder l'original
        import shutil
        shutil.copy2(image_path, backup_path)
        print(f"✅ Sauvegarde créée : {backup_path}")
        
        # Tentative de réparation
        with Image.open(image_path) as img:
            # Forcer le chargement avec tolérance aux erreurs
            img.verify()  # Première vérification
            
        # Recharger et sauvegarder
        with Image.open(image_path) as img:
            img = img.convert('RGB')  # Conversion en RGB standard
            img.save(repair_path, 'PNG', optimize=True)
            print(f"✅ Image réparée : {repair_path}")
            
            # Remplacer l'original
            shutil.move(repair_path, image_path)
            print(f"✅ Image originale remplacée")
            
            return True
            
    except Exception as e:
        print(f"❌ Réparation échouée : {e}")
        return False

def check_templates():
    """Vérifie tous les templates configurés."""
    print(f"\n🎨 VÉRIFICATION DES TEMPLATES")
    print("=" * 40)
    
    templates = APP_SETTINGS.get("rarity_templates", {})
    
    if not templates:
        print("⚠️  Aucun template configuré")
        return True
    
    all_ok = True
    for rarity, template_path in templates.items():
        print(f"\n🔍 Template {rarity} :")
        if check_image_file(template_path):
            print(f"   ✅ OK")
        else:
            print(f"   ❌ PROBLÈME")
            all_ok = False
    
    return all_ok

def check_images_folder():
    """Vérifie la structure des dossiers images."""
    print(f"\n📁 VÉRIFICATION DOSSIERS IMAGES")
    print("=" * 40)
    
    try:
        subfolders = ensure_images_subfolders()
        
        for name, path in subfolders.items():
            if os.path.exists(path):
                file_count = len([f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
                print(f"✅ {name:12} : {path} ({file_count} images)")
            else:
                print(f"❌ {name:12} : {path} (inexistant)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dossiers : {e}")
        return False

def create_test_image():
    """Crée une image de test pour vérifier la génération."""
    print(f"\n🧪 CRÉATION IMAGE DE TEST")
    print("=" * 40)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Créer une image de test
        img = Image.new('RGB', (400, 300), (100, 150, 200))
        draw = ImageDraw.Draw(img)
        
        # Ajouter du texte
        draw.text((50, 50), "IMAGE DE TEST", fill=(255, 255, 255))
        draw.text((50, 100), "Barbus Test Card", fill=(255, 255, 0))
        draw.text((50, 150), "Génération automatique", fill=(200, 200, 200))
        
        # Ajouter des formes
        draw.rectangle([50, 200, 350, 250], outline=(255, 0, 0), width=3)
        draw.ellipse([200, 180, 300, 280], fill=(0, 255, 0))
        
        # Sauvegarder
        subfolders = ensure_images_subfolders()
        test_path = os.path.join(subfolders['originals'], 'test_barbus.png')
        img.save(test_path, 'PNG')
        
        print(f"✅ Image de test créée : {test_path}")
        print(f"   Vous pouvez utiliser cette image pour tester la création de carte")
        
        return test_path
        
    except Exception as e:
        print(f"❌ Erreur création test : {e}")
        return None

def main():
    """Diagnostic complet des problèmes d'images."""
    print("🔍 DIAGNOSTIC COMPLET DES IMAGES")
    print("=" * 60)
    
    # 1. Vérifier Pillow
    pillow_ok = check_pillow()
    
    if not pillow_ok:
        print("\n⚠️  ARRÊT : Pillow requis pour continuer")
        print("   Installez avec : pip install Pillow")
        return
    
    # 2. Vérifier structure dossiers
    folders_ok = check_images_folder()
    
    # 3. Vérifier templates
    templates_ok = check_templates()
    
    # 4. Créer image de test
    test_image = create_test_image()
    
    # Résumé
    print(f"\n" + "=" * 60)
    print("📊 RÉSUMÉ DU DIAGNOSTIC :")
    print(f"   Pillow           : {'✅ OK' if pillow_ok else '❌ PROBLÈME'}")
    print(f"   Dossiers         : {'✅ OK' if folders_ok else '❌ PROBLÈME'}")
    print(f"   Templates        : {'✅ OK' if templates_ok else '❌ PROBLÈME'}")
    print(f"   Image de test    : {'✅ CRÉÉE' if test_image else '❌ ÉCHEC'}")
    
    if all([pillow_ok, folders_ok, templates_ok]):
        print(f"\n🎉 DIAGNOSTIC RÉUSSI !")
        print(f"   Le système d'images devrait fonctionner correctement")
        if test_image:
            print(f"   Utilisez l'image de test pour créer votre carte Barbus")
    else:
        print(f"\n⚠️  PROBLÈMES DÉTECTÉS")
        print(f"   Vérifiez les erreurs ci-dessus")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
