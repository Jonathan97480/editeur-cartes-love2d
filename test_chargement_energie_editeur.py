#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de vérification du chargement des valeurs d'énergie 
dans l'éditeur de formatage de texte
"""
import sys
import os
sys.path.insert(0, 'lib')

import sqlite3
from database import CardRepo
from config import DB_FILE

def test_energy_loading_in_editor():
    """Test que l'éditeur charge bien les valeurs d'énergie depuis la base"""
    print("🎨 TEST CHARGEMENT ÉNERGIE - ÉDITEUR FORMATAGE")
    print("=" * 60)
    
    # Étape 1: Préparer des données de test
    print("📝 ÉTAPE 1: Préparation des données de test")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Prendre une carte existante
    cursor.execute('SELECT id, name FROM cards LIMIT 1')
    test_card = cursor.fetchone()
    
    if not test_card:
        print("   ❌ Aucune carte trouvée pour le test")
        return False
    
    card_id, card_name = test_card
    print(f"   Carte de test: {card_name} (ID: {card_id})")
    
    # Définir des valeurs d'énergie spécifiques pour le test
    test_energy_x = 123
    test_energy_y = 456
    test_energy_font = 'Comic Sans MS'
    test_energy_size = 22
    test_energy_color = '#FF9900'
    
    # Mettre à jour la carte avec ces valeurs
    cursor.execute('''
        UPDATE cards SET 
            energy_x=?, energy_y=?, energy_font=?, energy_size=?, energy_color=?
        WHERE id=?
    ''', (test_energy_x, test_energy_y, test_energy_font, test_energy_size, test_energy_color, card_id))
    
    conn.commit()
    print(f"   ✅ Valeurs d'énergie de test définies:")
    print(f"      Position: ({test_energy_x}, {test_energy_y})")
    print(f"      Police: {test_energy_font}, Taille: {test_energy_size}")
    print(f"      Couleur: {test_energy_color}")
    
    # Étape 2: Simuler l'ouverture de l'éditeur comme dans ui_components.py
    print(f"\n🔧 ÉTAPE 2: Simulation du chargement par l'éditeur")
    
    # Reproduire la logique de ui_components.py pour récupérer les données
    cursor.execute("""
        SELECT title_x, title_y, title_font, title_size, title_color,
               text_x, text_y, text_width, text_height, text_font,
               text_size, text_color, text_align, line_spacing, text_wrap,
               energy_x, energy_y, energy_font, energy_size, energy_color
        FROM cards WHERE id = ?
    """, (card_id,))
    
    formatting_data = cursor.fetchone()
    conn.close()
    
    if not formatting_data:
        print("   ❌ Aucune donnée de formatage récupérée")
        return False
    
    print(f"   ✅ Données récupérées par la requête SQL:")
    print(f"      Données complètes: {len(formatting_data)} champs")
    
    # Vérifier que les champs d'énergie sont aux bonnes positions
    energy_data = formatting_data[15:20]  # Les 5 derniers champs
    print(f"      Données d'énergie: {energy_data}")
    
    # Étape 3: Reproduire la création du card_data
    print(f"\n📋 ÉTAPE 3: Construction des données pour l'éditeur")
    
    # Reproduire exactement la logique de ui_components.py
    repo = CardRepo(DB_FILE)
    card = repo.get(card_id)
    
    card_data = {
        'id': card_id,
        'nom': card.name,
        'description': card.description,
        'img': card.img,
        'powerblow': card.powerblow,
        'title_x': formatting_data[0] or 50,
        'title_y': formatting_data[1] or 30,
        'title_font': formatting_data[2] or 'Arial',
        'title_size': formatting_data[3] or 16,
        'title_color': formatting_data[4] or '#000000',
        'text_x': formatting_data[5] or 50,
        'text_y': formatting_data[6] or 100,
        'text_width': formatting_data[7] or 200,
        'text_height': formatting_data[8] or 150,
        'text_font': formatting_data[9] or 'Arial',
        'text_size': formatting_data[10] or 12,
        'text_color': formatting_data[11] or '#000000',
        'text_align': formatting_data[12] or 'left',
        'line_spacing': formatting_data[13] or 1.2,
        'text_wrap': bool(formatting_data[14]) if formatting_data[14] is not None else True,
        'energy_x': formatting_data[15] or 25,
        'energy_y': formatting_data[16] or 25,
        'energy_font': formatting_data[17] or 'Arial',
        'energy_size': formatting_data[18] or 14,
        'energy_color': formatting_data[19] or '#FFFFFF'
    }
    
    print(f"   ✅ card_data créé avec les champs d'énergie:")
    print(f"      energy_x: {card_data['energy_x']}")
    print(f"      energy_y: {card_data['energy_y']}")
    print(f"      energy_font: {card_data['energy_font']}")
    print(f"      energy_size: {card_data['energy_size']}")
    print(f"      energy_color: {card_data['energy_color']}")
    
    # Étape 4: Vérifier que les valeurs correspondent
    print(f"\n🎯 ÉTAPE 4: Validation des valeurs")
    
    success = True
    checks = [
        ('energy_x', card_data['energy_x'], test_energy_x),
        ('energy_y', card_data['energy_y'], test_energy_y),
        ('energy_font', card_data['energy_font'], test_energy_font),
        ('energy_size', card_data['energy_size'], test_energy_size),
        ('energy_color', card_data['energy_color'], test_energy_color)
    ]
    
    for field_name, loaded_value, expected_value in checks:
        if loaded_value == expected_value:
            print(f"      ✅ {field_name}: {loaded_value} (correct)")
        else:
            print(f"      ❌ {field_name}: {loaded_value} (attendu: {expected_value})")
            success = False
    
    # Étape 5: Test avec TextFormattingEditor
    print(f"\n🎨 ÉTAPE 5: Test de création de l'éditeur")
    
    try:
        from text_formatting_editor import TextFormattingEditor
        import tkinter as tk
        
        # Créer une fenêtre de test (invisible)
        root = tk.Tk()
        root.withdraw()
        
        # Créer l'éditeur avec les données
        editor = TextFormattingEditor(root, card_id, card_data)
        
        # Vérifier que l'éditeur a bien chargé les valeurs
        editor_checks = [
            ('energy_x', editor.energy_x, test_energy_x),
            ('energy_y', editor.energy_y, test_energy_y),
            ('energy_font', editor.energy_font, test_energy_font),
            ('energy_size', editor.energy_size, test_energy_size),
            ('energy_color', editor.energy_color, test_energy_color)
        ]
        
        print(f"   ✅ TextFormattingEditor créé avec succès")
        editor_success = True
        
        for field_name, editor_value, expected_value in editor_checks:
            if editor_value == expected_value:
                print(f"      ✅ Editor.{field_name}: {editor_value} (correct)")
            else:
                print(f"      ❌ Editor.{field_name}: {editor_value} (attendu: {expected_value})")
                editor_success = False
        
        # Nettoyer
        root.destroy()
        
        success = success and editor_success
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la création de l'éditeur: {e}")
        success = False
    
    # Résultat final
    print(f"\n📋 RÉSULTAT FINAL:")
    if success:
        print("   🎉 SUCCÈS: L'éditeur charge correctement toutes les valeurs d'énergie!")
        print("   ✅ Requête SQL: Récupère les champs d'énergie")
        print("   ✅ card_data: Contient les valeurs d'énergie")
        print("   ✅ TextFormattingEditor: Initialise correctement les valeurs")
    else:
        print("   ❌ ÉCHEC: Des problèmes de chargement ont été détectés")
        print("   ⚠️ L'éditeur ne charge pas correctement les valeurs d'énergie")
    
    return success

if __name__ == "__main__":
    success = test_energy_loading_in_editor()
    exit(0 if success else 1)
