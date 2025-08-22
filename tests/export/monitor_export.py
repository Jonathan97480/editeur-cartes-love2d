#!/usr/bin/env python3
"""
Surveillance en temps réel du fichier cards_joueur.lua
Détecte automatiquement les modifications et analyse le fichier
"""

import os
import time
from datetime import datetime
import shutil

def monitor_file():
    """Surveille le fichier cards_joueur.lua en temps réel"""
    
    file_paths = [
        "c:/Users/berou/Downloads/cards_joueur.lua",
        "./cards_joueur.lua"
    ]
    
    print("🔍 SURVEILLANCE EN TEMPS RÉEL")
    print("=" * 50)
    print("📁 Surveillance des fichiers:")
    for path in file_paths:
        print(f"   - {path}")
    print()
    print("👁️  En attente de modifications...")
    print("   (Ctrl+C pour arrêter)")
    
    last_mod_times = {}
    
    try:
        while True:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    current_mod_time = os.path.getmtime(file_path)
                    
                    if file_path not in last_mod_times:
                        last_mod_times[file_path] = current_mod_time
                        print(f"📄 Fichier détecté: {file_path}")
                        continue
                    
                    if current_mod_time > last_mod_times[file_path]:
                        print()
                        print(f"🔄 MODIFICATION DÉTECTÉE: {file_path}")
                        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
                        
                        # Attendre un peu que l'écriture se termine
                        time.sleep(0.5)
                        
                        analyze_file_quickly(file_path)
                        last_mod_times[file_path] = current_mod_time
                        
                        print()
                        print("👁️  Surveillance continue...")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print()
        print("⏹️  Surveillance arrêtée")

def analyze_file_quickly(file_path):
    """Analyse rapide du fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Statistiques rapides
        file_size = len(content)
        card_count = content.count('--[[ CARTE')
        has_textformatting = 'TextFormatting' in content
        has_dimensions = 'width = 280' in content
        
        print(f"   📊 Taille: {file_size:,} caractères")
        print(f"   📦 Cartes: {card_count}")
        print(f"   🎨 TextFormatting: {'✅' if has_textformatting else '❌'}")
        print(f"   📐 Dimensions: {'✅' if has_dimensions else '❌'}")
        
        # Copier dans result si pas de formatage
        if not has_textformatting and card_count > 0:
            result_dir = "result_export_lua"
            if not os.path.exists(result_dir):
                os.makedirs(result_dir)
            
            timestamp = datetime.now().strftime('%H%M%S')
            backup_file = os.path.join(result_dir, f"export_{timestamp}.lua")
            shutil.copy2(file_path, backup_file)
            
            print(f"   💾 Sauvegardé: {backup_file}")
            print(f"   ⚠️  BESOIN DE CORRECTION - Pas de formatage détecté")
        
    except Exception as e:
        print(f"   ❌ Erreur lecture: {e}")

if __name__ == "__main__":
    monitor_file()
