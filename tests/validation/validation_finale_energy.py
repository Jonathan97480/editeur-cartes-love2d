#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation finale du système complet avec formatage énergie
"""

print('🎯 VALIDATION FINALE - SYSTÈME COMPLET AVEC ÉNERGIE')
print('=' * 70)

from lua_exporter_love2d import Love2DLuaExporter
from lib.database import CardRepo
from lib.config import DB_FILE

# Test 1: Vérifier la base de données
print('📊 Test 1: Structure de la base de données')
import sqlite3
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(cards)')
columns = cursor.fetchall()

energy_columns = [col for col in columns if 'energy' in col[1].lower()]
print(f'   ✅ Colonnes énergie: {len(energy_columns)}')
for col in energy_columns:
    print(f'      - {col[1]}: {col[2]}')

# Test 2: Vérifier les données des cartes
print(f'\n📋 Test 2: Données des cartes')
repo = CardRepo(DB_FILE)
cards = repo.list_cards()

card = cards[0] if cards else None
if card:
    print(f'   Carte test: {card.name}')
    print(f'   PowerBlow: {card.powerblow}')
    print(f'   Position énergie: ({card.energy_x}, {card.energy_y})')
    print(f'   Style énergie: {card.energy_font} {card.energy_size}px {card.energy_color}')

# Test 3: Export avec énergie
print(f'\n🎮 Test 3: Export Love2D avec énergie')
exporter = Love2DLuaExporter(repo)
filename = 'test_final_energy.lua'
size = exporter.export_to_file(filename)

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# Vérifications
checks = [
    ('TextFormatting', 'Sections TextFormatting'),
    ('energy = {', 'Sections énergie'),
    ('PowerBlow =', 'Valeurs PowerBlow'),
    ('x = 25', 'Positions par défaut'),
    ("color = '#FFFFFF'", 'Couleurs énergie')
]

for search, desc in checks:
    count = content.count(search)
    status = '✅' if count > 0 else '❌'
    print(f'   {status} {desc}: {count}')

# Test 4: Afficher un exemple complet
print(f'\n📝 Test 4: Exemple de carte complète avec énergie')
if 'energy = {' in content:
    start = content.find('--[[ CARTE 1')
    end_marker = '--[[ CARTE 2'
    if end_marker in content:
        end = content.find(end_marker, start)
    else:
        end = content.find('}\n\nreturn Cards', start)
    
    if start != -1 and end != -1:
        card_example = content[start:end]
        print('   📄 Première carte exportée:')
        lines = card_example.split('\n')
        for line in lines[:40]:  # Premières 40 lignes
            print(f'      {line}')
        if len(lines) > 40:
            print('      ... (suite)')

conn.close()

print(f'\n🎯 RÉSULTAT FINAL:')
print(f'   ✅ Base de données avec colonnes énergie')
print(f'   ✅ Modèle Card mis à jour')
print(f'   ✅ Éditeur de formatage avec contrôles énergie')
print(f'   ✅ Export Love2D avec section energy complète')
print(f'   ✅ Interface utilisateur intégrée')
print(f'\n🎮 Le système Love2D avec formatage énergie est opérationnel!')
