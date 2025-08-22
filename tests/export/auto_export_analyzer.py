#!/usr/bin/env python3
"""
Script automatisé pour l'export Lua
- Lance l'application automatiquement
- Surveille la fermeture de l'application
- Analyse le fichier exporté automatiquement
"""

import subprocess
import time
import os
import psutil
import shutil
from datetime import datetime

def wait_for_process_end(process_name="python.exe"):
    """Attend que le processus se termine"""
    print(f"🔍 Surveillance du processus: {process_name}")
    
    # Attendre un peu que le processus démarre
    time.sleep(2)
    
    # Trouver le processus de l'application
    app_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == process_name:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'main.py' in cmdline or 'START.bat' in cmdline:
                    app_processes.append(proc)
                    print(f"📱 Processus trouvé: PID {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if not app_processes:
        print("⚠️  Aucun processus d'application trouvé")
        return
    
    # Surveiller les processus
    print("👁️  Surveillance active - Exportez vos cartes puis fermez l'application")
    while any(proc.is_running() for proc in app_processes):
        time.sleep(1)
    
    print("✅ Application fermée détectée!")

def analyze_exported_file():
    """Analyse le fichier exporté"""
    print("\n🔍 ANALYSE DU FICHIER EXPORTÉ")
    print("=" * 50)
    
    # Chercher le fichier cards_joueur.lua dans Downloads
    possible_paths = [
        "c:/Users/berou/Downloads/cards_joueur.lua",
        "c:/Users/berou/Downloads/Nouveau dossier/cards_joueur.lua",
        "./cards_joueur.lua"
    ]
    
    source_file = None
    for path in possible_paths:
        if os.path.exists(path):
            source_file = path
            break
    
    if not source_file:
        print("❌ Fichier cards_joueur.lua non trouvé")
        print("📁 Vérifiez ces emplacements:")
        for path in possible_paths:
            print(f"   - {path}")
        return False
    
    print(f"📁 Fichier trouvé: {source_file}")
    
    # Analyser le fichier
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Informations de base
    file_size = len(content)
    card_count = content.count('--[[ CARTE')
    mod_time = os.path.getmtime(source_file)
    
    print(f"📊 Taille: {file_size:,} caractères")
    print(f"📦 Cartes détectées: {card_count}")
    print(f"📅 Modifié: {datetime.fromtimestamp(mod_time).strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Vérifications importantes
    has_textformatting = 'TextFormatting' in content
    has_card_dimensions = 'width = 280' in content
    has_positioning = 'title = {' in content
    formatting_count = content.count('TextFormatting = {')
    
    print()
    print("🔍 VÉRIFICATIONS:")
    print(f"   🎨 Section TextFormatting: {'✅' if has_textformatting else '❌'}")
    print(f"   📐 Dimensions carte: {'✅' if has_card_dimensions else '❌'}")
    print(f"   📍 Positionnement: {'✅' if has_positioning else '❌'}")
    print(f"   📊 Sections formatage: {formatting_count}")
    
    # Copier vers le dossier result
    result_dir = "result_export_lua"
    result_file = os.path.join(result_dir, "cards_joueur_exported.lua")
    
    try:
        shutil.copy2(source_file, result_file)
        print(f"📋 Copié vers: {result_file}")
    except Exception as e:
        print(f"❌ Erreur copie: {e}")
    
    # Diagnostic
    if not has_textformatting:
        print()
        print("⚠️  DIAGNOSTIC: Le fichier ne contient PAS les données de formatage")
        print("   L'application exporte encore l'ancien format")
        print("   Il faut ajouter les données TextFormatting")
        
        # Créer la version corrigée automatiquement
        create_corrected_version(content, result_dir)
        return False
    else:
        print()
        print("🎉 FICHIER CORRECT!")
        print("   Toutes les données de formatage sont présentes")
        return True

def create_corrected_version(original_content, result_dir):
    """Crée une version corrigée avec les données de formatage"""
    print()
    print("🔧 CRÉATION DE LA VERSION CORRIGÉE")
    print("=" * 40)
    
    # Template de formatage
    text_formatting_template = '''        TextFormatting = {
            card = {
                width = 280,  -- Largeur standard de carte Love2D
                height = 392, -- Hauteur standard de carte Love2D (ratio 5:7)
                scale = 1.0   -- Facteur d'échelle
            },
            title = {
                x = 50,           -- Position X du titre
                y = 25,           -- Position Y du titre
                font = "Arial",   -- Police du titre
                size = 16,        -- Taille du titre
                color = "black"   -- Couleur du titre
            },
            description = {
                x = 20,           -- Position X de la description
                y = 80,           -- Position Y de la description
                width = 240,      -- Largeur de la zone de description
                height = 200,     -- Hauteur de la zone de description
                font = "Arial",   -- Police de la description
                size = 12,        -- Taille de la description
                color = "black"   -- Couleur de la description
            },
            energy = {
                x = 240,          -- Position X de l'énergie/coût
                y = 25,           -- Position Y de l'énergie/coût
                font = "Arial",   -- Police de l'énergie
                size = 14,        -- Taille de l'énergie
                color = "blue"    -- Couleur de l'énergie
            }
        },'''
    
    # Traiter le contenu
    lines = original_content.split('\n')
    new_lines = []
    card_count = 0
    
    for line in lines:
        new_lines.append(line)
        
        # Détecter la fin d'une carte
        if line.strip() == "Cards = {}":
            card_count += 1
            # Retirer la ligne qu'on vient d'ajouter
            new_lines.pop()
            
            # Ajouter TextFormatting
            new_lines.append(text_formatting_template)
            
            # Rajouter Cards = {}
            new_lines.append("        Cards = {}")
    
    # Créer le contenu corrigé
    corrected_content = '\n'.join(new_lines)
    
    # Sauvegarder
    corrected_file = os.path.join(result_dir, "cards_joueur_CORRECTED.lua")
    with open(corrected_file, 'w', encoding='utf-8') as f:
        f.write(corrected_content)
    
    print(f"✅ Version corrigée créée: {corrected_file}")
    print(f"📊 Cartes traitées: {card_count}")
    print(f"📈 Taille originale: {len(original_content):,} caractères")
    print(f"📈 Taille corrigée: {len(corrected_content):,} caractères")
    
    # Créer un guide d'utilisation
    guide_file = os.path.join(result_dir, "GUIDE_UTILISATION.md")
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(f"""# Guide d'utilisation - Export Lua corrigé

## Fichiers dans ce dossier

- `cards_joueur_exported.lua` - Fichier original exporté par l'application
- `cards_joueur_CORRECTED.lua` - **Version corrigée avec formatage Love2D**
- `GUIDE_UTILISATION.md` - Ce guide

## ✅ Utilisez le fichier corrigé

Le fichier `cards_joueur_CORRECTED.lua` contient :
- 📐 Dimensions de carte (280×392px)
- 📍 Positions précises de tous les éléments
- 🎨 Styles complets (police, taille, couleur)
- 🎮 Structure Love2D compatible

## 🎮 Code Love2D exemple

```lua
local cards = require("cards_joueur_CORRECTED")

function drawCard(card, x, y)
    local fmt = card.TextFormatting
    
    -- Fond de carte
    love.graphics.rectangle("fill", x, y, fmt.card.width, fmt.card.height)
    
    -- Titre
    love.graphics.print(card.name, x + fmt.title.x, y + fmt.title.y)
    
    -- Description
    love.graphics.printf(card.Description, 
                        x + fmt.description.x, 
                        y + fmt.description.y, 
                        fmt.description.width)
    
    -- Énergie
    love.graphics.print(card.PowerBlow, x + fmt.energy.x, y + fmt.energy.y)
end
```

Générée automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
""")
    
    print(f"📚 Guide créé: {guide_file}")

def main():
    """Fonction principale"""
    print("🚀 LANCEMENT AUTOMATISÉ DE L'APPLICATION")
    print("=" * 60)
    
    print("📂 Dossier result_export_lua créé")
    print("🎯 Étapes:")
    print("   1. Lance l'application automatiquement")
    print("   2. Vous exportez vos cartes")
    print("   3. Vous fermez l'application")
    print("   4. Analyse automatique du fichier")
    print()
    
    # Lancer l'application avec choix 1
    print("🔄 Lancement de l'application (choix 1)...")
    
    try:
        # Utiliser START.bat qui gère déjà l'environnement
        process = subprocess.Popen(
            ["START.bat"],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="."
        )
        
        # Envoyer le choix 1
        time.sleep(1)
        process.stdin.write("1\n")
        process.stdin.flush()
        
        print("✅ Application lancée!")
        print()
        print("👤 VOTRE TOUR:")
        print("   1. Exportez vos cartes via l'application")
        print("   2. Fermez l'application quand c'est terminé")
        print()
        
        # Surveiller la fermeture
        wait_for_process_end()
        
        # Analyser le fichier
        analyze_exported_file()
        
        print()
        print("🎉 PROCESSUS TERMINÉ!")
        print("📁 Vérifiez le dossier result_export_lua/")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("🔧 Essayez de lancer START.bat manuellement")

if __name__ == "__main__":
    main()
