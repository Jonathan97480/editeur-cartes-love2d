#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'organisation des templates
"""
# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()


import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.utils import organize_all_images, ensure_images_subfolders
from lib.config import APP_SETTINGS, save_settings

def test_template_organization():
    """Test de l'organisation des templates."""

    print("🧪 Test de l'organisation des templates")
    print("=" * 50)
    
    # Créer la structure de dossiers
    subfolders = ensure_images_subfolders()
    print(f"📁 Structure de dossiers :")
    for name, path in subfolders.items():
        print(f"   - {name}: {path}")
    
    # Vérifier les paramètres actuels
    rarity_templates = APP_SETTINGS.get("rarity_templates", {})
    print(f"\n📋 Templates configurés actuellement :")
    
    if not rarity_templates:
        print("   ⚠️  Aucun template configuré dans les paramètres")
        print("   💡 Configurez des templates dans Réglages > Configuration des images")
        return True
    
    for rarity, template_path in rarity_templates.items():
        print(f"   - {rarity}: {template_path}")
        if template_path and os.path.exists(template_path):
            print(f"     ✅ Fichier existe")
        elif template_path:
            print(f"     ❌ Fichier introuvable")
        else:
            print(f"     ⚠️  Pas de template défini")
    
    # Test de l'organisation
    print(f"\n🗂️ Test de l'organisation...")
    try:
        results = organize_all_images()
        
        print(f"\n📊 Résultats :")
        print(f"   Templates copiés : {results['templates_copied']}")
        print(f"   Erreurs : {results['templates_errors']}")
        
        if results['templates_details']:
            print(f"\n📋 Détails des templates :")
            for rarity, path in results['templates_details'].items():
                print(f"   - {rarity}: {os.path.basename(path)}")
                print(f"     📁 {path}")
        
        print(f"\n{results['summary']}")
        
        # Vérifier le contenu du dossier templates
        templates_folder = subfolders['templates']
        if os.path.exists(templates_folder):
            files = os.listdir(templates_folder)
            print(f"\n📂 Contenu du dossier templates/ :")
            if files:
                for file in files:
                    print(f"   - {file}")
            else:
                print("   (vide)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_template_organization()
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
