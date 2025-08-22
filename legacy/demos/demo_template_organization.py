#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration de l'organisation des templates avec des fichiers de test
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.utils import organize_all_images, ensure_images_subfolders
from lib.config import APP_SETTINGS, save_settings

def create_demo_templates():
    """Crée des fichiers de template de démonstration."""
    print("🎨 Création de templates de démonstration...")
    
    # Créer des fichiers de template factices dans un dossier temporaire
    demo_folder = "demo_templates"
    os.makedirs(demo_folder, exist_ok=True)
    
    templates = {
        'commun': 'template_commun_demo.png',
        'rare': 'template_rare_demo.png', 
        'legendaire': 'template_legendaire_demo.png',
        'mythique': 'template_mythique_demo.png'
    }
    
    created_files = {}
    
    for rarity, filename in templates.items():
        file_path = os.path.join(demo_folder, filename)
        
        # Créer un fichier PNG minimal (header PNG valide)
        png_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x1eIDATx\x9cc\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
        
        with open(file_path, 'wb') as f:
            f.write(png_header)
        
        created_files[rarity] = os.path.abspath(file_path)
        print(f"   ✅ {rarity}: {file_path}")
    
    return created_files

def demo_template_organization():
    """Démonstration complète de l'organisation des templates."""
    print("🧪 Démonstration de l'organisation des templates")
    print("=" * 60)
    
    try:
        # 1. Créer des templates de démonstration
        demo_templates = create_demo_templates()
        
        # 2. Configurer les templates dans les paramètres
        print(f"\n⚙️ Configuration des templates...")
        APP_SETTINGS["rarity_templates"] = demo_templates
        save_settings()
        print(f"✅ Templates configurés dans les paramètres")
        
        # 3. Afficher l'état avant organisation
        subfolders = ensure_images_subfolders()
        templates_folder = subfolders['templates']
        
        print(f"\n📂 État AVANT organisation :")
        print(f"   Dossier templates : {templates_folder}")
        files_before = os.listdir(templates_folder) if os.path.exists(templates_folder) else []
        if files_before:
            for file in files_before:
                print(f"   - {file}")
        else:
            print(f"   (vide)")
        
        # 4. Organiser les templates
        print(f"\n🗂️ Organisation des templates...")
        results = organize_all_images()
        
        # 5. Afficher l'état après organisation
        print(f"\n📂 État APRÈS organisation :")
        files_after = os.listdir(templates_folder) if os.path.exists(templates_folder) else []
        if files_after:
            for file in files_after:
                print(f"   - {file}")
        else:
            print(f"   (vide)")
        
        # 6. Afficher les résultats
        print(f"\n📊 Résultats de l'organisation :")
        print(f"   Templates copiés : {results['templates_copied']}")
        print(f"   Détails :")
        for rarity, path in results['templates_details'].items():
            print(f"   - {rarity}: {os.path.basename(path)}")
        
        print(f"\n{results['summary']}")
        
        # 7. Nettoyer les fichiers de démonstration
        print(f"\n🧹 Nettoyage des fichiers de démonstration...")
        for file_path in demo_templates.values():
            try:
                os.remove(file_path)
                print(f"   🗑️ Supprimé : {os.path.basename(file_path)}")
            except:
                pass
        
        # Supprimer le dossier de démonstration
        try:
            os.rmdir("demo_templates")
            print(f"   🗑️ Dossier demo_templates supprimé")
        except:
            pass
        
        print(f"\n🎉 Démonstration terminée avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = demo_template_organization()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Appuyez sur Entrée pour fermer...")
    input()
