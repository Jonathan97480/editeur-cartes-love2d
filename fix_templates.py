#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réparation rapide des templates
"""

import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.config import APP_SETTINGS, load_settings, save_settings
from lib.utils import ensure_images_subfolders

def check_and_fix_templates():
    """Vérifie et répare la configuration des templates."""
    
    print("🔧 RÉPARATION DES TEMPLATES")
    print("=" * 40)
    
    # Charger la configuration
    load_settings()
    
    print("📋 Configuration actuelle :")
    for rarity, path in APP_SETTINGS['rarity_templates'].items():
        status = "✅ OK" if path and os.path.exists(path) else "❌ MANQUANT"
        print(f"   {rarity:12} : {path or '(vide)'} {status}")
    
    # Obtenir le dossier templates
    subfolders = ensure_images_subfolders()
    templates_dir = subfolders['templates']
    
    print(f"\n📁 Dossier templates : {templates_dir}")
    
    # Lister les fichiers disponibles
    if os.path.exists(templates_dir):
        template_files = [f for f in os.listdir(templates_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f"📋 Fichiers disponibles ({len(template_files)}) :")
        for file in template_files:
            print(f"   - {file}")
    else:
        template_files = []
        print("❌ Dossier templates inexistant")
    
    # Créer des templates par défaut
    if not template_files:
        print(f"\n🎨 Création de templates par défaut...")
        created_templates = create_default_templates(templates_dir)
        template_files.extend(created_templates)
    
    # Assigner automatiquement les templates
    if template_files:
        print(f"\n🔄 Attribution automatique des templates...")
        
        # Logique d'attribution intelligente
        for rarity in ['commun', 'rare', 'legendaire', 'mythique']:
            if not APP_SETTINGS['rarity_templates'][rarity] or not os.path.exists(APP_SETTINGS['rarity_templates'][rarity]):
                
                # Chercher un template spécifique à la rareté
                specific_template = None
                for file in template_files:
                    if rarity in file.lower():
                        specific_template = os.path.join(templates_dir, file)
                        break
                
                # Sinon, utiliser le premier template disponible
                if not specific_template and template_files:
                    specific_template = os.path.join(templates_dir, template_files[0])
                
                if specific_template:
                    APP_SETTINGS['rarity_templates'][rarity] = specific_template
                    print(f"   ✅ {rarity:12} → {os.path.basename(specific_template)}")
        
        # Sauvegarder la configuration
        save_settings()
        print(f"\n💾 Configuration sauvegardée")
    
    print(f"\n📋 Configuration finale :")
    for rarity, path in APP_SETTINGS['rarity_templates'].items():
        status = "✅ OK" if path and os.path.exists(path) else "❌ ERREUR"
        print(f"   {rarity:12} : {os.path.basename(path) if path else '(vide)'} {status}")

def create_default_templates(templates_dir):
    """Crée des templates par défaut si aucun n'existe."""
    
    try:
        from PIL import Image, ImageDraw
        
        created = []
        colors = {
            'commun': (128, 128, 128),     # Gris
            'rare': (0, 100, 255),         # Bleu
            'legendaire': (255, 165, 0),   # Orange
            'mythique': (255, 0, 255)      # Magenta
        }
        
        for rarity, color in colors.items():
            template_path = os.path.join(templates_dir, f"template_{rarity}.png")
            
            # Créer une image de template simple
            img = Image.new('RGBA', (400, 300), (255, 255, 255, 0))  # Transparent
            draw = ImageDraw.Draw(img)
            
            # Bordure colorée
            draw.rectangle([5, 5, 395, 295], outline=color, width=8)
            
            # Coin décoratif
            draw.rectangle([10, 10, 60, 60], fill=color)
            draw.rectangle([340, 10, 390, 60], fill=color)
            draw.rectangle([10, 240, 60, 290], fill=color)
            draw.rectangle([340, 240, 390, 290], fill=color)
            
            # Sauvegarder
            img.save(template_path, 'PNG')
            created.append(f"template_{rarity}.png")
            print(f"   ✅ Créé : template_{rarity}.png")
        
        return created
        
    except Exception as e:
        print(f"❌ Erreur création templates : {e}")
        return []

if __name__ == "__main__":
    check_and_fix_templates()
    print(f"\n🎉 Réparation terminée !")
    print(f"   Vous pouvez maintenant créer votre carte avec l'acteur Barbus")
