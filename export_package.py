#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 SCRIPT D'EXPORT DE PACKAGE SIMPLE
====================================

Script simple pour exporter un package de jeu complet.
Peut être intégré facilement dans l'interface existante.
"""

import sys
import os
sys.path.insert(0, 'lib')

from lib.database import CardRepo
from lib.config import DB_FILE
from lib.game_package_exporter import GamePackageExporter
from datetime import datetime

def export_game_package(package_name=None, output_dir="exports"):
    """
    Exporte un package de jeu complet.
    
    Args:
        package_name: Nom du package (optionnel)
        output_dir: Dossier de sortie (par défaut: exports)
        
    Returns:
        Chemin vers le package créé ou None en cas d'erreur
    """
    
    print("🎮 EXPORT DE PACKAGE DE JEU COMPLET")
    print("=" * 50)
    
    try:
        # 1. Initialiser le repository
        print("📊 Chargement des cartes...")
        repo = CardRepo(DB_FILE)
        cards = repo.list_cards()
        
        if not cards:
            print("❌ Aucune carte trouvée dans la base de données!")
            return None
        
        print(f"   ✅ {len(cards)} cartes trouvées")
        
        # 2. Nom du package par défaut
        if not package_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            package_name = f"cards_package_{timestamp}"
        
        print(f"📦 Nom du package: {package_name}")
        
        # 3. Créer l'exporteur
        print("🏭 Initialisation de l'exporteur...")
        exporter = GamePackageExporter(repo, output_dir)
        
        # 4. Analyser les ressources
        resources = exporter.analyze_cards_resources(cards)
        print(f"📊 Ressources détectées:")
        print(f"   - Cartes: {resources['card_count']}")
        print(f"   - Polices: {len(resources['fonts'])}")
        print(f"   - Images: {len(resources['images'])}")
        
        # 5. Créer le package
        print("\n🚀 Création du package en cours...")
        package_path = exporter.export_complete_package(package_name)
        
        # 6. Informations finales
        if os.path.exists(package_path):
            size = os.path.getsize(package_path)
            print(f"\n🎉 PACKAGE CRÉÉ AVEC SUCCÈS!")
            print(f"📍 Emplacement: {package_path}")
            print(f"📏 Taille: {size:,} octets ({size/1024:.1f} KB)")
            
            # Analyser le contenu
            import zipfile
            with zipfile.ZipFile(package_path, 'r') as zipf:
                files = zipf.namelist()
                image_files = [f for f in files if f.endswith('.png')]
                font_files = [f for f in files if f.endswith(('.ttf', '.otf'))]
                
                print(f"📋 Contenu:")
                print(f"   - {len(image_files)} images de cartes")
                print(f"   - {len(font_files)} polices")
                print(f"   - 1 fichier Lua de données")
                print(f"   - Documentation complète")
            
            return package_path
        else:
            print("❌ Erreur: Le package n'a pas été créé")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Fonction principale."""
    
    # Demander le nom du package
    package_name = input("🎮 Nom du package (Entrée pour auto): ").strip()
    if not package_name:
        package_name = None
    
    # Demander le dossier de sortie
    output_dir = input("📁 Dossier de sortie (Entrée pour 'exports'): ").strip()
    if not output_dir:
        output_dir = "exports"
    
    # Lancer l'export
    result = export_game_package(package_name, output_dir)
    
    if result:
        # Demander si on veut ouvrir le dossier
        response = input("\n📂 Ouvrir le dossier contenant le package ? (o/N): ").strip().lower()
        if response in ['o', 'oui', 'y', 'yes']:
            try:
                folder_path = os.path.dirname(result)
                os.startfile(folder_path)  # Windows
            except Exception as e:
                print(f"Impossible d'ouvrir le dossier: {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
