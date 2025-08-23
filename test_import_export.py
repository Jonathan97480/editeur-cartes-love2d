#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'import game_package_exporter dans le contexte app
"""

import sys
import os

# Ajouter le chemin lib (comme dans app_final.py)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))

print("🧪 Test d'import game_package_exporter")
print("=" * 50)

# Test 1: Import direct
try:
    from game_package_exporter import GamePackageExporter
    print("✅ Test 1: Import direct depuis lib/ - SUCCÈS")
except ImportError as e:
    print(f"❌ Test 1: Erreur import direct - {e}")

# Test 2: Import avec chemin complet
try:
    import lib.game_package_exporter
    print("✅ Test 2: Import lib.game_package_exporter - SUCCÈS")
except ImportError as e:
    print(f"❌ Test 2: Erreur import lib. - {e}")

# Test 3: Vérifier si la classe existe
try:
    from game_package_exporter import GamePackageExporter
    print(f"✅ Test 3: Classe GamePackageExporter trouvée - {GamePackageExporter}")
    
    # Créer une instance de test
    print("🔍 Test de création d'instance...")
    # On ne peut pas tester sans repo, mais on peut vérifier la classe
    print(f"   - Méthodes disponibles: {[m for m in dir(GamePackageExporter) if not m.startswith('_')]}")
    
except Exception as e:
    print(f"❌ Test 3: Erreur avec la classe - {e}")

print("=" * 50)
print("🏁 Test terminé")
