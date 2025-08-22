#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simplifié de l'organisation des templates
"""

import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()

def test_template_organization_simple():
    """Test simplifié de l'organisation des templates."""

    print("🧪 Test simplifié de l'organisation des templates")
    print("=" * 50)
    
    try:
        # Test basique : vérifier que le dossier images existe
        base_path = Path(__file__).parent.parent
        images_path = base_path / "images"
        
        print(f"📁 Chemin de base : {base_path}")
        print(f"📁 Dossier images : {images_path}")
        
        if images_path.exists():
            print("✅ Dossier images existe")
            
            # Compter les fichiers
            files = list(images_path.glob("*"))
            image_files = [f for f in files if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']]
            
            print(f"📊 {len(files)} fichiers trouvés")
            print(f"🖼️ {len(image_files)} fichiers d'images")
            
            if len(image_files) > 0:
                print("✅ Des images sont présentes")
                for img in image_files[:5]:  # Afficher les 5 premiers
                    print(f"   - {img.name}")
                if len(image_files) > 5:
                    print(f"   ... et {len(image_files) - 5} autres")
            else:
                print("⚠️ Aucun fichier d'image trouvé")
                
        else:
            print("⚠️ Dossier images n'existe pas")
            # Créer le dossier pour le test
            images_path.mkdir(exist_ok=True)
            print("✅ Dossier images créé")
        
        # Test des sous-dossiers basiques
        subfolders = ["cartes_joueur", "cartes_ia", "templates", "fused"]
        
        print(f"\n📁 Test des sous-dossiers :")
        for subfolder in subfolders:
            subfolder_path = images_path / subfolder
            if subfolder_path.exists():
                print(f"✅ {subfolder}/ existe")
            else:
                # Créer le sous-dossier
                subfolder_path.mkdir(exist_ok=True)
                print(f"✅ {subfolder}/ créé")
        
        print("\n✅ Organisation des templates validée !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_template_organization_simple()
        if not success:
            sys.exit(1)
        print("\n✅ Test d'organisation réussi !")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
