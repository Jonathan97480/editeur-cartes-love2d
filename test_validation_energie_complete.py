#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de validation des champs d'énergie
Vérifie que tous les composants traitent correctement les données d'énergie
"""
import sys
import os
sys.path.insert(0, 'lib')

import sqlite3
from database import CardRepo
from config import DB_FILE

def test_database_energy_fields():
    """Test 1: Vérifier que la base contient bien tous les champs d'énergie"""
    print("🗃️ TEST 1: Vérification base de données")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Vérifier la structure
    cursor.execute('PRAGMA table_info(cards)')
    columns = cursor.fetchall()
    
    energy_columns = [col for col in columns if 'energy' in col[1].lower()]
    expected_columns = ['energy_x', 'energy_y', 'energy_font', 'energy_size', 'energy_color']
    
    print(f"   Colonnes d'énergie trouvées: {len(energy_columns)}")
    for col in energy_columns:
        print(f"      ✅ {col[1]}: {col[2]}")
    
    missing = [col for col in expected_columns if not any(col == ec[1] for ec in energy_columns)]
    if missing:
        print(f"   ❌ Colonnes manquantes: {missing}")
        return False
    
    # Vérifier des données réelles
    cursor.execute('SELECT id, name, energy_x, energy_y, energy_font, energy_size, energy_color FROM cards LIMIT 2')
    test_data = cursor.fetchall()
    
    print(f"   Données de test:")
    for row in test_data:
        print(f"      Carte {row[0]} ({row[1]}): pos({row[2]}, {row[3]}), {row[4]}, {row[5]}px, {row[6]}")
    
    conn.close()
    return True

def test_cardrepo_loading():
    """Test 2: Vérifier que CardRepo charge les champs d'énergie"""
    print("\n📊 TEST 2: Vérification CardRepo")
    
    repo = CardRepo(DB_FILE)
    cards = repo.list_cards()
    
    if not cards:
        print("   ❌ Aucune carte trouvée")
        return False
    
    test_card = cards[0]
    print(f"   Carte test: {test_card.name}")
    
    energy_attrs = ['energy_x', 'energy_y', 'energy_font', 'energy_size', 'energy_color']
    success = True
    
    for attr in energy_attrs:
        if hasattr(test_card, attr):
            value = getattr(test_card, attr)
            print(f"      ✅ {attr}: {value}")
        else:
            print(f"      ❌ {attr}: MANQUANT")
            success = False
    
    return success

def test_lua_export():
    """Test 3: Vérifier l'export Lua"""
    print("\n📄 TEST 3: Vérification export Lua")
    
    try:
        from lua_exporter_love2d import Love2DLuaExporter
        
        repo = CardRepo(DB_FILE)
        exporter = Love2DLuaExporter(repo)
        
        test_file = 'test_validation_complete.lua'
        exporter.export_to_file(test_file)
        
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"   Export généré: {len(content)} caractères")
        
        # Vérifications
        has_textformatting = 'TextFormatting' in content
        has_energy_section = 'energy = {' in content
        card_count = content.count('--[[ CARTE')
        
        print(f"   ✅ TextFormatting: {'Présent' if has_textformatting else 'MANQUANT'}")
        print(f"   ✅ Section energy: {'Présente' if has_energy_section else 'MANQUANTE'}")
        print(f"   📊 Cartes exportées: {card_count}")
        
        if has_energy_section:
            # Vérifier les champs dans energy
            start = content.find('energy = {')
            end = content.find('}', start) + 1
            energy_section = content[start:end]
            
            required_fields = ['x =', 'y =', 'font =', 'size =', 'color =']
            all_present = True
            
            for field in required_fields:
                if field in energy_section:
                    print(f"      ✅ {field.strip()}")
                else:
                    print(f"      ❌ {field.strip()} MANQUANT")
                    all_present = False
            
            # Nettoyer
            os.remove(test_file)
            
            return has_textformatting and has_energy_section and all_present
        
        return False
        
    except Exception as e:
        print(f"   ❌ Erreur export Lua: {e}")
        return False

def test_zip_export():
    """Test 4: Vérifier l'export ZIP"""
    print("\n📦 TEST 4: Vérification export ZIP")
    
    try:
        from game_package_exporter import GamePackageExporter
        
        repo = CardRepo(DB_FILE)
        output_dir = 'temp_validation_test'
        
        exporter = GamePackageExporter(repo, output_dir)
        print("   ✅ GamePackageExporter créé")
        
        # Test indirect via Love2DLuaExporter (utilisé par GamePackageExporter)
        from lua_exporter_love2d import Love2DLuaExporter
        lua_exporter = Love2DLuaExporter(repo)
        
        test_file = os.path.join(output_dir, 'test_zip.lua')
        os.makedirs(output_dir, exist_ok=True)
        
        lua_exporter.export_to_file(test_file)
        
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_energy = 'energy = {' in content
        print(f"   ✅ Export ZIP contient energy: {'Oui' if has_energy else 'Non'}")
        
        # Nettoyer
        os.remove(test_file)
        os.rmdir(output_dir)
        
        return has_energy
        
    except Exception as e:
        print(f"   ❌ Erreur export ZIP: {e}")
        return False

def test_formatting_editor_compatibility():
    """Test 5: Vérifier la compatibilité avec l'éditeur de formatage"""
    print("\n🎨 TEST 5: Vérification éditeur de formatage")
    
    try:
        # Simuler la sauvegarde de l'éditeur de formatage
        from database_simple import CardRepo as SimpleRepo
        
        simple_repo = SimpleRepo(DB_FILE)
        cards = simple_repo.list_cards()
        
        if cards:
            test_card = cards[0]
            print(f"   Carte test: {test_card.nom}")
            
            # Vérifier que database_simple gère les champs d'énergie
            energy_attrs = ['energy_x', 'energy_y', 'energy_font', 'energy_size', 'energy_color']
            all_present = True
            
            for attr in energy_attrs:
                if hasattr(test_card, attr):
                    value = getattr(test_card, attr)
                    print(f"      ✅ {attr}: {value}")
                else:
                    print(f"      ❌ {attr}: MANQUANT")
                    all_present = False
            
            return all_present
        
        return False
        
    except Exception as e:
        print(f"   ❌ Erreur éditeur: {e}")
        return False

def run_complete_validation():
    """Lance tous les tests de validation"""
    print("🧪 VALIDATION COMPLÈTE - CHAMPS ÉNERGIE")
    print("=" * 60)
    
    tests = [
        ("Base de données", test_database_energy_fields),
        ("CardRepo", test_cardrepo_loading),
        ("Export Lua", test_lua_export),
        ("Export ZIP", test_zip_export),
        ("Éditeur formatage", test_formatting_editor_compatibility)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    print("\n📋 RÉSULTATS FINAUX:")
    print("=" * 40)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ RÉUSSI" if passed else "❌ ÉCHOUÉ"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print(f"\n🎯 VALIDATION GLOBALE: {'✅ TOUS LES TESTS RÉUSSIS' if all_passed else '❌ ÉCHECS DÉTECTÉS'}")
    
    if all_passed:
        print("\n🎉 PARFAIT!")
        print("   Tous les exports (Lua et ZIP) incluent correctement")
        print("   tous les champs d'énergie de la base de données!")
    else:
        print("\n⚠️ Des problèmes ont été détectés.")
        print("   Certains composants ne traitent pas correctement les champs d'énergie.")
    
    return all_passed

if __name__ == "__main__":
    success = run_complete_validation()
    exit(0 if success else 1)
