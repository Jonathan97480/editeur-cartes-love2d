#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 TEST DE L'EXPORTEUR DE PACKAGE COMPLET
=========================================

Test du nouveau système d'export qui crée un package ZIP structuré
avec fichier Lua, images fusionnées et polices.
"""

import sys
import os
sys.path.insert(0, 'lib')

from lib.database import CardRepo
from lib.config import DB_FILE
from lib.game_package_exporter import GamePackageExporter

def test_package_exporter():
    """Test complet de l'exporteur de package."""
    
    print("🎮 TEST DE L'EXPORTEUR DE PACKAGE COMPLET")
    print("=" * 60)
    
    # 1. Initialiser le repository
    print("📊 Initialisation...")
    try:
        repo = CardRepo(DB_FILE)
        cards = repo.list_cards()
        print(f"   ✅ Repository initialisé: {len(cards)} cartes")
        
        if not cards:
            print("   ❌ Aucune carte trouvée!")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur repository: {e}")
        return False
    
    # 2. Créer l'exporteur
    print("\n🏭 Création de l'exporteur...")
    try:
        exporter = GamePackageExporter(repo, "test_packages")
        print("   ✅ Exporteur créé")
    except Exception as e:
        print(f"   ❌ Erreur exporteur: {e}")
        return False
    
    # 3. Analyser les ressources
    print("\n🔍 Analyse des ressources...")
    try:
        resources = exporter.analyze_cards_resources(cards)
        print(f"   📝 Cartes: {resources['card_count']}")
        print(f"   🎨 Polices: {len(resources['fonts'])}")
        print(f"   🖼️  Images: {len(resources['images'])}")
        
        if resources['fonts']:
            print("   📋 Polices utilisées:")
            for font in sorted(resources['fonts']):
                print(f"      - {font}")
                
    except Exception as e:
        print(f"   ❌ Erreur analyse: {e}")
        return False
    
    # 4. Test de création d'image fusionnée
    print("\n🖼️  Test de création d'image fusionnée...")
    try:
        if cards:
            test_card = cards[0]
            success = exporter.create_fused_card_image(test_card, "test_fused_card.png")
            if success:
                print(f"   ✅ Image fusionnée créée: test_fused_card.png")
                # Vérifier si le fichier existe
                if os.path.exists("test_fused_card.png"):
                    size = os.path.getsize("test_fused_card.png")
                    print(f"      Taille: {size:,} octets")
            else:
                print("   ⚠️  Échec de création de l'image fusionnée")
    except Exception as e:
        print(f"   ❌ Erreur image fusionnée: {e}")
    
    # 5. Test du package complet
    print("\n📦 Test de création du package complet...")
    try:
        package_name = "test_cards_package"
        package_path = exporter.export_complete_package(package_name)
        
        print(f"\n🎉 PACKAGE CRÉÉ AVEC SUCCÈS!")
        print(f"📍 Chemin: {package_path}")
        
        # Vérifier la taille du package
        if os.path.exists(package_path):
            size = os.path.getsize(package_path)
            print(f"📏 Taille du package: {size:,} octets ({size/1024:.1f} KB)")
            
            # Analyser le contenu du ZIP
            import zipfile
            with zipfile.ZipFile(package_path, 'r') as zipf:
                files = zipf.namelist()
                print(f"📋 Fichiers dans le package: {len(files)}")
                
                # Organiser par type
                lua_files = [f for f in files if f.endswith('.lua')]
                image_files = [f for f in files if f.endswith('.png')]
                font_files = [f for f in files if f.endswith(('.ttf', '.otf'))]
                doc_files = [f for f in files if f.endswith(('.md', '.json'))]
                
                print(f"   📄 Fichiers Lua: {len(lua_files)}")
                print(f"   🖼️  Images: {len(image_files)}")
                print(f"   🎨 Polices: {len(font_files)}")
                print(f"   📚 Documentation: {len(doc_files)}")
                
                print(f"\n📂 Structure du package:")
                for file in sorted(files)[:20]:  # Montrer les 20 premiers
                    print(f"   {file}")
                if len(files) > 20:
                    print(f"   ... et {len(files) - 20} autres fichiers")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur package: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_components():
    """Test des composants individuels."""
    
    print("\n🧪 TEST DES COMPOSANTS INDIVIDUELS")
    print("=" * 50)
    
    try:
        repo = CardRepo(DB_FILE)
        exporter = GamePackageExporter(repo)
        
        # Test du gestionnaire de polices
        print("🎨 Test du gestionnaire de polices...")
        font_manager = exporter.font_manager
        available_fonts = font_manager.get_all_fonts()
        print(f"   Polices disponibles: {len(available_fonts)}")
        
        system_fonts = len([f for f in available_fonts if not f.startswith("🎨")])
        custom_fonts = len([f for f in available_fonts if f.startswith("🎨")])
        print(f"   - Système: {system_fonts}")
        print(f"   - Personnalisées: {custom_fonts}")
        
        # Test de recherche de fichier de police
        print("\n🔍 Test de recherche de polices...")
        test_fonts = ["Arial", "Times New Roman", "Courier New"]
        for font_name in test_fonts:
            font_file = exporter._find_font_file(font_name)
            if font_file:
                print(f"   ✅ {font_name}: {font_file}")
            else:
                print(f"   ❓ {font_name}: Non trouvé (normal pour police système)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test composants: {e}")
        return False

def main():
    """Fonction principale de test."""
    
    print("🎮 SUITE DE TESTS - EXPORTEUR DE PACKAGE")
    print("=" * 70)
    
    # Test des composants individuels
    success1 = test_individual_components()
    
    # Test principal
    success2 = test_package_exporter()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("   Le système d'export de package fonctionne correctement.")
        print("   Vous pouvez maintenant utiliser le nouvel exporteur.")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus.")
    
    print("\n📝 Fichiers générés:")
    test_files = ["test_fused_card.png", "test_packages/test_cards_package.zip"]
    for file in test_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size:,} octets)")
        else:
            print(f"   ❌ {file} (non créé)")

if __name__ == "__main__":
    main()
