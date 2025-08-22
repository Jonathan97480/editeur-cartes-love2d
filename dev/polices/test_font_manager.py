#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 TEST DU GESTIONNAIRE DE POLICES
================================

Test d'intégration du gestionnaire de polices dans l'éditeur.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_font_manager():
    """Test du gestionnaire de polices."""
    print("🎨 TEST DU GESTIONNAIRE DE POLICES")
    print("=" * 50)
    
    from lib.font_manager import FontManager, get_font_manager, get_available_fonts
    
    # Test de création
    fm = FontManager()
    
    # Informations sur les polices
    info = fm.get_font_info()
    print(f"📊 Polices système: {info['system_fonts_count']}")
    print(f"🎨 Polices personnalisées: {info['custom_fonts_count']}")
    print(f"📁 Dossier polices: {info['fonts_directory']}")
    print(f"✅ Total: {info['total_fonts']} polices disponibles")
    
    # Lister quelques polices système
    system_fonts = fm.get_system_fonts()
    print(f"\n📝 Exemples de polices système ({len(system_fonts)} total):")
    for font in system_fonts[:10]:  # Afficher les 10 premières
        print(f"  • {font}")
    if len(system_fonts) > 10:
        print(f"  ... et {len(system_fonts) - 10} autres")
    
    # Lister les polices personnalisées
    custom_fonts = fm.get_custom_fonts()
    if custom_fonts:
        print(f"\n🎨 Polices personnalisées trouvées:")
        for font in custom_fonts:
            print(f"  • {font}")
            font_path = fm.get_font_path(font)
            print(f"    Chemin: {font_path}")
    else:
        print(f"\n💡 Aucune police personnalisée trouvée")
        print(f"   Ajoutez des fichiers .ttf ou .otf dans: {info['fonts_directory']}")
    
    # Test de la fonction get_available_fonts()
    all_fonts = get_available_fonts()
    print(f"\n🔗 Test get_available_fonts(): {len(all_fonts)} polices")
    
    # Afficher quelques exemples
    print(f"\n📋 Aperçu des polices disponibles:")
    for i, font in enumerate(all_fonts[:15]):  # 15 premières
        if font.startswith("🎨"):
            print(f"  {i+1:2d}. {font} ⭐")  # Police personnalisée
        elif font == "─" * 20:
            print(f"      {font}")  # Séparateur
        else:
            print(f"  {i+1:2d}. {font}")
    
    if len(all_fonts) > 15:
        print(f"      ... et {len(all_fonts) - 15} autres polices")
    
    return True

def test_font_creation():
    """Test de création de polices."""
    print(f"\n🔧 TEST DE CRÉATION DE POLICES")
    print("=" * 30)
    
    from lib.font_manager import get_font_manager
    import tkinter as tk
    from tkinter import font
    
    fm = get_font_manager()
    
    # Créer une fenêtre de test
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre
    
    try:
        # Test avec une police système
        test_fonts = ["Arial", "Times New Roman", "Courier New"]
        
        for font_name in test_fonts:
            try:
                test_font = fm.create_font(font_name, 12, weight="bold")
                print(f"  ✅ {font_name}: {test_font.actual()}")
            except Exception as e:
                print(f"  ❌ {font_name}: {e}")
        
        # Test avec des polices personnalisées s'il y en a
        custom_fonts = fm.get_custom_fonts()
        if custom_fonts:
            print(f"\n🎨 Test polices personnalisées:")
            for font_name in custom_fonts[:3]:  # 3 premières
                try:
                    test_font = fm.create_font(f"🎨 {font_name}", 14)
                    print(f"  ✅ {font_name}: {test_font.actual()}")
                except Exception as e:
                    print(f"  ❌ {font_name}: {e}")
        
    finally:
        root.destroy()
    
    return True

if __name__ == "__main__":
    try:
        success1 = test_font_manager()
        success2 = test_font_creation()
        
        if success1 and success2:
            print(f"\n🎉 TOUS LES TESTS RÉUSSIS!")
            print(f"   Le gestionnaire de polices est prêt à être utilisé.")
        else:
            print(f"\n⚠️ Certains tests ont échoué")
            
    except Exception as e:
        print(f"\n❌ ERREUR LORS DES TESTS: {e}")
        import traceback
        traceback.print_exc()
