#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de diagnostic pour l'export des polices
"""

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'lib'))

from database import CardRepo
from game_package_exporter import GamePackageExporter

def test_fonts_export():
    """Test des polices dans l'export"""
    print("🔍 Test diagnostic export polices")
    print("=" * 50)
    
    # Créer le repo
    from database import ensure_db_legacy
    ensure_db_legacy("cartes.db")
    repo = CardRepo("cartes.db")
    
    # Obtenir toutes les cartes
    cards = repo.list_cards()
    print(f"📊 Cartes trouvées: {len(cards)}")
    
    if not cards:
        print("❌ Aucune carte trouvée")
        return
    
    # Analyser les polices
    exporter = GamePackageExporter(repo)
    resources = exporter.analyze_cards_resources(cards)
    
    print(f"🎨 Polices détectées: {len(resources['fonts'])}")
    for font in resources['fonts']:
        print(f"  - {font}")
    
    print(f"🖼️  Images détectées: {len(resources['images'])}")
    
    # Tester la recherche de polices
    print("\n🔍 Test de recherche de polices:")
    for font_name in resources['fonts']:
        font_file = exporter._find_font_file(font_name)
        if font_file:
            print(f"  ✅ {font_name} -> {font_file}")
        else:
            print(f"  ❌ {font_name} -> NON TROUVÉE")
    
    # Tester une carte spécifique
    if cards:
        card = cards[0]
        print(f"\n📝 Détails carte '{card.name}':")
        print(f"  - title_font: {getattr(card, 'title_font', 'NON DÉFINI')}")
        print(f"  - text_font: {getattr(card, 'text_font', 'NON DÉFINI')}")
        print(f"  - energy_font: {getattr(card, 'energy_font', 'NON DÉFINI')}")

if __name__ == "__main__":
    test_fonts_export()
