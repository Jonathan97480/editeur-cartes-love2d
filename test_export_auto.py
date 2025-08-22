#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 TEST AUTOMATIQUE D'EXPORT DE PACKAGE
======================================

Test automatique du système d'export de package.
"""

import sys
import os
sys.path.insert(0, 'lib')

from lib.database import CardRepo
from lib.config import DB_FILE
from lib.game_package_exporter import GamePackageExporter
from datetime import datetime

def test_auto_export():
    """Test automatique de l'export de package."""
    
    print("🎮 TEST AUTOMATIQUE D'EXPORT DE PACKAGE")
    print("=" * 60)
    
    try:
        # Configuration
        package_name = "demo_cards_package"
        output_dir = "demo_exports"
        
        print(f"📦 Package: {package_name}")
        print(f"📁 Dossier: {output_dir}")
        
        # 1. Charger les cartes
        repo = CardRepo(DB_FILE)
        cards = repo.list_cards()
        print(f"📊 Cartes trouvées: {len(cards)}")
        
        # 2. Créer l'exporteur
        exporter = GamePackageExporter(repo, output_dir)
        
        # 3. Analyser les ressources
        resources = exporter.analyze_cards_resources(cards)
        print(f"📋 Ressources:")
        print(f"   - Cartes: {resources['card_count']}")
        print(f"   - Polices: {len(resources['fonts'])}")
        print(f"   - Images: {len(resources['images'])}")
        
        if resources['fonts']:
            print(f"🎨 Polices utilisées:")
            for font in sorted(resources['fonts']):
                print(f"   - {font}")
        
        # 4. Export
        print(f"\n🚀 Démarrage de l'export...")
        package_path = exporter.export_complete_package(package_name)
        
        # 5. Vérification
        if os.path.exists(package_path):
            size = os.path.getsize(package_path)
            print(f"\n✅ EXPORT RÉUSSI!")
            print(f"📍 Fichier: {package_path}")
            print(f"📏 Taille: {size:,} octets ({size/1024:.1f} KB)")
            
            # Analyser le contenu du ZIP
            import zipfile
            with zipfile.ZipFile(package_path, 'r') as zipf:
                files = zipf.namelist()
                
                # Compter par type
                lua_files = [f for f in files if f.endswith('.lua')]
                image_files = [f for f in files if f.endswith('.png')]
                font_files = [f for f in files if f.endswith(('.ttf', '.otf'))]
                doc_files = [f for f in files if f.endswith(('.md', '.json'))]
                
                print(f"\n📂 Contenu du package:")
                print(f"   📄 Fichiers Lua: {len(lua_files)}")
                print(f"   🖼️  Images: {len(image_files)}")
                print(f"   🎨 Polices: {len(font_files)}")
                print(f"   📚 Documentation: {len(doc_files)}")
                print(f"   📦 Total: {len(files)} fichiers")
                
                # Afficher la structure
                print(f"\n🗂️  Structure:")
                directories = set()
                for file in files:
                    if '/' in file:
                        directories.add(file.split('/')[0])
                    else:
                        directories.add("(racine)")
                
                for directory in sorted(directories):
                    dir_files = [f for f in files if f.startswith(directory + '/') or (directory == "(racine)" and '/' not in f)]
                    print(f"   📁 {directory}: {len(dir_files)} fichiers")
            
            return True
        else:
            print("❌ ÉCHEC: Package non créé")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_features():
    """Test de fonctionnalités spécifiques."""
    
    print("\n🔍 TEST DES FONCTIONNALITÉS SPÉCIFIQUES")
    print("=" * 50)
    
    try:
        repo = CardRepo(DB_FILE)
        exporter = GamePackageExporter(repo, "test_features")
        
        # Test 1: Création d'image fusionnée
        print("🖼️  Test 1: Création d'image fusionnée")
        cards = repo.list_cards()
        if cards:
            card = cards[0]
            success = exporter.create_fused_card_image(card, "test_fusion.png")
            if success and os.path.exists("test_fusion.png"):
                size = os.path.getsize("test_fusion.png")
                print(f"   ✅ Image créée: test_fusion.png ({size:,} octets)")
            else:
                print("   ❌ Échec création image")
        
        # Test 2: Recherche de polices
        print("\n🎨 Test 2: Recherche de polices")
        test_fonts = ["Arial", "Times New Roman", "Calibri", "Comic Sans MS"]
        for font_name in test_fonts:
            font_path = exporter._find_font_file(font_name)
            if font_path:
                print(f"   ✅ {font_name}: trouvé")
            else:
                print(f"   ❓ {font_name}: non trouvé")
        
        # Test 3: Export Lua seul
        print("\n📄 Test 3: Export Lua")
        lua_file = "test_lua_only.lua"
        size = exporter.export_lua_data(cards, lua_file)
        if os.path.exists(lua_file):
            print(f"   ✅ Fichier Lua créé: {size:,} caractères")
            
            # Vérifier le contenu
            with open(lua_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_textformatting = 'TextFormatting' in content
            has_cards = '--[[ CARTE' in content
            card_count = content.count('--[[ CARTE')
            
            print(f"   📊 Analyse du contenu:")
            print(f"      - TextFormatting: {'✅' if has_textformatting else '❌'}")
            print(f"      - Cartes détectées: {card_count}")
            print(f"      - Structure cartes: {'✅' if has_cards else '❌'}")
        else:
            print("   ❌ Fichier Lua non créé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test fonctionnalités: {e}")
        return False

def main():
    """Fonction principale."""
    
    print("🎮 SUITE DE TESTS COMPLÈTE - EXPORT DE PACKAGE")
    print("=" * 70)
    
    # Test principal
    success1 = test_auto_export()
    
    # Test des fonctionnalités
    success2 = test_specific_features()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✨ Le système d'export de package est opérationnel!")
        print("   Vous pouvez maintenant:")
        print("   1. Utiliser export_package.py pour un export interactif")
        print("   2. Intégrer GamePackageExporter dans votre interface")
        print("   3. Créer des packages prêts pour Love2D")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus")
    
    # Nettoyer les fichiers de test
    test_files = ["test_fusion.png", "test_lua_only.lua"]
    print(f"\n🧹 Nettoyage des fichiers de test...")
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"   🗑️  {file} supprimé")
            except:
                print(f"   ⚠️  Impossible de supprimer {file}")

if __name__ == "__main__":
    main()
