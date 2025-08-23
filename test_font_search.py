#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test spécifique de recherche de police Cambria
"""

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'lib'))

from game_package_exporter import GamePackageExporter
from database import CardRepo

def test_font_search():
    """Test de recherche de police"""
    print("🔍 Test de recherche de police Cambria")
    print("=" * 50)
    
    repo = CardRepo("cartes.db")
    exporter = GamePackageExporter(repo)
    
    # Tester la recherche de Cambria
    fonts_to_test = ["Cambria", "Arial", "Times New Roman", "Calibri"]
    
    for font_name in fonts_to_test:
        font_file = exporter._find_font_file(font_name)
        if font_file:
            print(f"✅ {font_name} -> {font_file}")
        else:
            print(f"❌ {font_name} -> NON TROUVÉE")
    
    # Vérifier le dossier Windows Fonts
    windows_fonts = "C:/Windows/Fonts"
    if os.path.exists(windows_fonts):
        print(f"\n📁 Contenu de {windows_fonts} (fichiers Cambria):")
        cambria_files = [f for f in os.listdir(windows_fonts) if 'cambria' in f.lower()]
        for f in cambria_files:
            print(f"  - {f}")
    else:
        print("❌ Dossier Windows Fonts introuvable")

if __name__ == "__main__":
    test_font_search()
