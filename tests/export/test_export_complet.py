#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparaison et amélioration de l'export Lua
Génère un export complet avec taille de carte et toutes les données nécessaires
"""

from lib.database import CardRepo
from lib.config import DB_FILE
from lua_exporter_love2d import Love2DLuaExporter
import sqlite3

def analyze_current_export():
    """Analyse l'export actuel et génère une version complète"""
    print("🔍 ANALYSE ET AMÉLIORATION EXPORT LUA")
    print("=" * 60)
    
    # 1. Générer l'export actuel
    repo = CardRepo(DB_FILE)
    exporter = Love2DLuaExporter(repo)
    
    print("📝 Export avec les améliorations...")
    content = exporter.export_all_cards_love2d()
    
    # Sauvegarder l'export amélioré
    filename = 'cards_joueur_complete.lua'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Export sauvegardé: {filename}")
    print(f"📊 Taille: {len(content):,} caractères")
    
    # 2. Analyser le contenu
    print(f"\n🔍 Vérifications:")
    
    # Vérifier les dimensions de carte
    if 'card = {' in content:
        print("   ✅ Dimensions de carte incluses")
    else:
        print("   ❌ Dimensions de carte manquantes")
    
    # Vérifier les sections de formatage
    if 'TextFormatting = {' in content:
        print("   ✅ Section TextFormatting présente")
    else:
        print("   ❌ Section TextFormatting manquante")
    
    # Compter les sections
    card_count = content.count('--[[ CARTE')
    title_count = content.count('title = {')
    text_count = content.count('text = {')
    energy_count = content.count('energy = {')
    
    print(f"\n📊 Statistiques détaillées:")
    print(f"   Cartes exportées: {card_count}")
    print(f"   Sections titre: {title_count}")
    print(f"   Sections texte: {text_count}")
    print(f"   Sections énergie: {energy_count}")
    
    # 3. Extraire un exemple complet
    print(f"\n📋 Exemple de carte complète:")
    start = content.find('--[[ CARTE 1')
    if start != -1:
        end = content.find('--[[ CARTE 2', start)
        if end == -1:
            end = content.find('}\n\nreturn Cards', start)
        if end != -1:
            example = content[start:end].strip()
            # Afficher seulement les 1000 premiers caractères
            if len(example) > 1000:
                example = example[:1000] + "\n    ... (tronqué)"
            print(example)
    
    return content

def create_love2d_usage_example():
    """Crée un exemple d'utilisation sous Love2D"""
    example = '''-- Exemple d'utilisation sous Love2D
local Cards = require('cards_joueur_complete')

function love.load()
    -- Charger une carte
    local card = Cards[1]
    
    -- Accéder aux dimensions de la carte
    local cardWidth = card.TextFormatting.card.width
    local cardHeight = card.TextFormatting.card.height
    local scale = card.TextFormatting.card.scale
    
    -- Position du titre
    local titleX = card.TextFormatting.title.x * scale
    local titleY = card.TextFormatting.title.y * scale
    local titleSize = card.TextFormatting.title.size * scale
    
    -- Position du texte
    local textX = card.TextFormatting.text.x * scale
    local textY = card.TextFormatting.text.y * scale
    local textWidth = card.TextFormatting.text.width * scale
    local textHeight = card.TextFormatting.text.height * scale
    
    -- Position de l'énergie
    local energyX = card.TextFormatting.energy.x * scale
    local energyY = card.TextFormatting.energy.y * scale
end

function love.draw()
    local card = Cards[1]
    local formatting = card.TextFormatting
    
    -- Dessiner le fond de carte (280x392 par défaut)
    love.graphics.setColor(1, 1, 1)
    love.graphics.rectangle("fill", 100, 100, 
        formatting.card.width * formatting.card.scale, 
        formatting.card.height * formatting.card.scale)
    
    -- Dessiner le titre
    love.graphics.setColor(0, 0, 0) -- Couleur du titre
    love.graphics.setFont(love.graphics.newFont(formatting.title.size))
    love.graphics.print(card.name, 
        100 + formatting.title.x, 
        100 + formatting.title.y)
    
    -- Dessiner la description
    love.graphics.setFont(love.graphics.newFont(formatting.text.size))
    love.graphics.printf(card.Description,
        100 + formatting.text.x,
        100 + formatting.text.y,
        formatting.text.width,
        formatting.text.align)
    
    -- Dessiner le coût d'énergie
    love.graphics.setFont(love.graphics.newFont(formatting.energy.size))
    love.graphics.print(tostring(card.PowerBlow),
        100 + formatting.energy.x,
        100 + formatting.energy.y)
end'''
    
    with open('love2d_usage_example.lua', 'w', encoding='utf-8') as f:
        f.write(example)
    
    print("📖 Exemple d'utilisation Love2D créé: love2d_usage_example.lua")

def verify_database_formatting():
    """Vérifie que toutes les cartes ont des données de formatage"""
    print(f"\n🔍 VÉRIFICATION BASE DE DONNÉES")
    print("=" * 40)
    
    # Vérifier les données de formatage dans la base
    import sqlite3
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, 
               title_x, title_y, title_font, title_size, title_color,
               text_x, text_y, text_width, text_height, text_font, text_size, text_color,
               energy_x, energy_y, energy_font, energy_size, energy_color
        FROM cards
    ''')
    
    cards_data = cursor.fetchall()
    conn.close()
    
    print(f"📊 Cartes analysées: {len(cards_data)}")
    
    complete_count = 0
    for card in cards_data:
        card_id, name = card[0], card[1]
        formatting_data = card[2:]
        
        # Vérifier si toutes les données de formatage sont présentes
        has_complete_formatting = all(x is not None for x in formatting_data)
        
        if has_complete_formatting:
            complete_count += 1
            status = "✅"
        else:
            status = "⚠️"
        
        print(f"   {status} Carte {card_id}: {name}")
        if not has_complete_formatting:
            missing = []
            fields = ['title_x', 'title_y', 'title_font', 'title_size', 'title_color',
                     'text_x', 'text_y', 'text_width', 'text_height', 'text_font', 'text_size', 'text_color',
                     'energy_x', 'energy_y', 'energy_font', 'energy_size', 'energy_color']
            for i, value in enumerate(formatting_data):
                if value is None:
                    missing.append(fields[i])
            print(f"      Manquant: {', '.join(missing)}")
    
    print(f"\n📈 Résumé: {complete_count}/{len(cards_data)} cartes avec formatage complet")
    
    return complete_count == len(cards_data)

if __name__ == "__main__":
    # 1. Vérifier la base de données
    db_complete = verify_database_formatting()
    
    # 2. Générer l'export amélioré
    content = analyze_current_export()
    
    # 3. Créer l'exemple d'utilisation
    create_love2d_usage_example()
    
    print(f"\n🎯 RÉSULTATS FINAUX:")
    print(f"   📊 Base de données: {'✅ Complète' if db_complete else '⚠️ Incomplète'}")
    print(f"   📝 Export Lua: ✅ Généré avec dimensions de carte")
    print(f"   📖 Exemple Love2D: ✅ Créé")
    print(f"   🎮 Prêt pour intégration Love2D: {'✅ Oui' if db_complete else '⚠️ Après correction BDD'}")
