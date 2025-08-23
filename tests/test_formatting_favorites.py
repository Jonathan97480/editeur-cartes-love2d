#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour la fonctionnalité des favoris de formatage
"""

import unittest
import sqlite3
import tempfile
import os
from pathlib import Path
import sys

# Ajouter le chemin lib pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from database import (
    ensure_formatting_favorites_table,
    save_formatting_favorite,
    get_formatting_favorite,
    list_formatting_favorites,
    delete_formatting_favorite,
    validate_formatting_data
)
from favorites_manager import FavoritesManager, create_favorites_manager


class TestFormattingFavoritesDatabase(unittest.TestCase):
    """Tests pour les fonctions de base de données des favoris."""
    
    def setUp(self):
        """Prépare une base de données temporaire pour chaque test."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # Créer la base et la table
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        ensure_formatting_favorites_table(cursor)
        con.commit()
        con.close()
        
        # Données de test
        self.test_data = {
            'title_x': 100.5, 'title_y': 50.5, 'title_font': 'Arial',
            'title_size': 18, 'title_color': '#FF0000',
            'text_x': 75.0, 'text_y': 120.0, 'text_width': 250.0, 
            'text_height': 180.0, 'text_font': 'Helvetica', 'text_size': 14,
            'text_color': '#00FF00', 'text_align': 'center', 
            'line_spacing': 1.5, 'text_wrap': 1,
            'energy_x': 30.0, 'energy_y': 35.0, 'energy_font': 'Verdana',
            'energy_size': 16, 'energy_color': '#0000FF'
        }
    
    def tearDown(self):
        """Nettoie la base de données temporaire."""
        try:
            os.unlink(self.db_path)
        except:
            pass
    
    def test_table_creation(self):
        """Test de création de la table formatting_favorites."""
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        
        # Vérifier que la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formatting_favorites'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        
        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(formatting_favorites)")
        columns = [row[1] for row in cursor.fetchall()]
        
        expected_columns = [
            'id', 'slot_number', 'name', 'title_x', 'title_y', 'title_font',
            'title_size', 'title_color', 'text_x', 'text_y', 'text_width',
            'text_height', 'text_font', 'text_size', 'text_color', 'text_align',
            'line_spacing', 'text_wrap', 'energy_x', 'energy_y', 'energy_font',
            'energy_size', 'energy_color', 'created_at', 'updated_at'
        ]
        
        for col in expected_columns:
            self.assertIn(col, columns)
        
        con.close()
    
    def test_save_and_get_favorite(self):
        """Test de sauvegarde et récupération d'un favori."""
        # Sauvegarder
        success = save_formatting_favorite(self.db_path, 1, self.test_data, "Test Favori")
        self.assertTrue(success)
        
        # Récupérer
        favorite = get_formatting_favorite(self.db_path, 1)
        self.assertIsNotNone(favorite)
        self.assertEqual(favorite['name'], "Test Favori")
        self.assertEqual(favorite['slot_number'], 1)
        self.assertEqual(favorite['title_x'], 100.5)
        self.assertEqual(favorite['title_font'], 'Arial')
    
    def test_invalid_slot_numbers(self):
        """Test avec des numéros de slot invalides."""
        with self.assertRaises(ValueError):
            save_formatting_favorite(self.db_path, 0, self.test_data)
        
        with self.assertRaises(ValueError):
            save_formatting_favorite(self.db_path, 4, self.test_data)
        
        with self.assertRaises(ValueError):
            get_formatting_favorite(self.db_path, -1)
    
    def test_overwrite_favorite(self):
        """Test d'écrasement d'un favori existant."""
        # Première sauvegarde
        save_formatting_favorite(self.db_path, 2, self.test_data, "Premier")
        
        # Données modifiées
        modified_data = self.test_data.copy()
        modified_data['title_x'] = 200.0
        
        # Seconde sauvegarde (écrasement)
        save_formatting_favorite(self.db_path, 2, modified_data, "Deuxième")
        
        # Vérifier l'écrasement
        favorite = get_formatting_favorite(self.db_path, 2)
        self.assertEqual(favorite['name'], "Deuxième")
        self.assertEqual(favorite['title_x'], 200.0)
    
    def test_list_favorites(self):
        """Test de listage des favoris."""
        # Aucun favori au début
        favorites = list_formatting_favorites(self.db_path)
        self.assertEqual(len(favorites), 0)
        
        # Ajouter des favoris
        save_formatting_favorite(self.db_path, 1, self.test_data, "Favori 1")
        save_formatting_favorite(self.db_path, 3, self.test_data, "Favori 3")
        
        favorites = list_formatting_favorites(self.db_path)
        self.assertEqual(len(favorites), 2)
        self.assertIn(1, favorites)
        self.assertIn(3, favorites)
        self.assertEqual(favorites[1], "Favori 1")
        self.assertEqual(favorites[3], "Favori 3")
    
    def test_delete_favorite(self):
        """Test de suppression d'un favori."""
        # Ajouter un favori
        save_formatting_favorite(self.db_path, 2, self.test_data, "À supprimer")
        
        # Vérifier qu'il existe
        favorite = get_formatting_favorite(self.db_path, 2)
        self.assertIsNotNone(favorite)
        
        # Supprimer
        success = delete_formatting_favorite(self.db_path, 2)
        self.assertTrue(success)
        
        # Vérifier la suppression
        favorite = get_formatting_favorite(self.db_path, 2)
        self.assertIsNone(favorite)
        
        # Tentative de suppression d'un favori inexistant
        success = delete_formatting_favorite(self.db_path, 2)
        self.assertFalse(success)
    
    def test_validate_formatting_data(self):
        """Test de validation des données de formatage."""
        # Données valides
        valid, message = validate_formatting_data(self.test_data)
        self.assertTrue(valid)
        
        # Données manquantes
        incomplete_data = {'title_x': 50}
        valid, message = validate_formatting_data(incomplete_data)
        self.assertFalse(valid)
        self.assertIn("manquant", message)
        
        # Valeurs invalides
        invalid_data = self.test_data.copy()
        invalid_data['title_size'] = -5
        valid, message = validate_formatting_data(invalid_data)
        self.assertFalse(valid)
        self.assertIn("invalide", message)


class TestFavoritesManager(unittest.TestCase):
    """Tests pour la classe FavoritesManager."""
    
    def setUp(self):
        """Prépare un gestionnaire de favoris pour les tests."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # Créer la base
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        ensure_formatting_favorites_table(cursor)
        con.commit()
        con.close()
        
        self.manager = FavoritesManager(self.db_path)
        
        self.test_data = {
            'title_x': 100.0, 'title_y': 50.0, 'title_font': 'Arial',
            'title_size': 16, 'title_color': '#000000',
            'text_x': 75.0, 'text_y': 120.0, 'text_width': 200.0,
            'text_height': 150.0, 'text_font': 'Helvetica', 'text_size': 12,
            'text_color': '#000000', 'text_align': 'left', 'line_spacing': 1.2,
            'text_wrap': 1, 'energy_x': 25.0, 'energy_y': 25.0,
            'energy_font': 'Arial', 'energy_size': 14, 'energy_color': '#FFFFFF'
        }
    
    def tearDown(self):
        """Nettoie les ressources."""
        try:
            os.unlink(self.db_path)
        except:
            pass
    
    def test_manager_creation(self):
        """Test de création du gestionnaire."""
        self.assertIsNotNone(self.manager)
        self.assertEqual(self.manager.db_path, self.db_path)
    
    def test_manager_with_invalid_db(self):
        """Test avec une base de données invalide."""
        manager = create_favorites_manager("/chemin/inexistant.db")
        self.assertIsNone(manager)
    
    def test_save_and_load_favorite(self):
        """Test de sauvegarde et chargement via le gestionnaire."""
        # Sauvegarder
        success, message = self.manager.save_favorite(1, self.test_data, "Test Manager")
        self.assertTrue(success)
        self.assertIn("succès", message)
        
        # Charger
        data, message = self.manager.load_favorite(1)
        self.assertIsNotNone(data)
        self.assertEqual(data['name'], "Test Manager")
        self.assertIn("succès", message)
    
    def test_get_all_favorites_status(self):
        """Test de récupération du statut de tous les slots."""
        # État initial (tous vides)
        status = self.manager.get_all_favorites_status()
        self.assertEqual(len(status), 3)
        for slot in [1, 2, 3]:
            self.assertEqual(status[slot]['status'], 'empty')
        
        # Ajouter un favori
        self.manager.save_favorite(2, self.test_data, "Favori Test")
        
        status = self.manager.get_all_favorites_status()
        self.assertEqual(status[1]['status'], 'empty')
        self.assertEqual(status[2]['status'], 'filled')
        self.assertEqual(status[2]['name'], 'Favori Test')
        self.assertEqual(status[3]['status'], 'empty')
    
    def test_is_slot_occupied(self):
        """Test de vérification d'occupation des slots."""
        # Slot vide
        self.assertFalse(self.manager.is_slot_occupied(1))
        
        # Ajouter un favori
        self.manager.save_favorite(1, self.test_data)
        
        # Slot occupé
        self.assertTrue(self.manager.is_slot_occupied(1))
        self.assertFalse(self.manager.is_slot_occupied(2))
    
    def test_delete_favorite(self):
        """Test de suppression via le gestionnaire."""
        # Ajouter puis supprimer
        self.manager.save_favorite(3, self.test_data, "À supprimer")
        self.assertTrue(self.manager.is_slot_occupied(3))
        
        success, message = self.manager.delete_favorite(3)
        self.assertTrue(success)
        self.assertFalse(self.manager.is_slot_occupied(3))
    
    def test_repair_corrupted_favorite(self):
        """Test de réparation d'un favori corrompu."""
        # Simuler un favori corrompu en insérant des données invalides
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO formatting_favorites (slot_number, name, title_x, created_at, updated_at)
            VALUES (1, 'Corrompu', 'invalid_value', '2023-01-01', '2023-01-01')
        """)
        con.commit()
        con.close()
        
        # Vérifier que le favori est détecté comme corrompu
        data, message = self.manager.load_favorite(1)
        self.assertIsNone(data)
        self.assertIn("corrompu", message.lower())
        
        # Réparer
        success, repair_message = self.manager.repair_corrupted_favorite(1)
        self.assertTrue(success)
        
        # Vérifier que le slot est maintenant vide
        self.assertFalse(self.manager.is_slot_occupied(1))
    
    def test_default_formatting_data(self):
        """Test des données de formatage par défaut."""
        defaults = self.manager.get_default_formatting_data()
        
        required_fields = [
            'title_x', 'title_y', 'title_font', 'title_size', 'title_color',
            'text_x', 'text_y', 'text_width', 'text_height', 'text_font',
            'text_size', 'text_color', 'text_align', 'line_spacing', 'text_wrap',
            'energy_x', 'energy_y', 'energy_font', 'energy_size', 'energy_color'
        ]
        
        for field in required_fields:
            self.assertIn(field, defaults)
        
        # Vérifier que les valeurs par défaut sont valides
        valid, message = validate_formatting_data(defaults)
        self.assertTrue(valid)


class TestIntegrationFormattingFavorites(unittest.TestCase):
    """Tests d'intégration pour la fonctionnalité complète."""
    
    def setUp(self):
        """Prépare l'environnement d'intégration."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # Créer une base complète avec tables cards et formatting_favorites
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        
        # Table cards (basique pour les tests)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        
        # Table favoris
        ensure_formatting_favorites_table(cursor)
        con.commit()
        con.close()
        
        self.manager = FavoritesManager(self.db_path)
    
    def tearDown(self):
        """Nettoie l'environnement."""
        try:
            os.unlink(self.db_path)
        except:
            pass
    
    def test_full_workflow(self):
        """Test du workflow complet : sauvegarder -> lister -> charger -> supprimer."""
        # Données de test
        config1 = self.manager.get_default_formatting_data()
        config1['title_x'] = 100
        
        config2 = self.manager.get_default_formatting_data()
        config2['title_x'] = 200
        
        # 1. Sauvegarder dans 2 slots
        success1, _ = self.manager.save_favorite(1, config1, "Configuration 1")
        success2, _ = self.manager.save_favorite(3, config2, "Configuration 3")
        self.assertTrue(success1)
        self.assertTrue(success2)
        
        # 2. Lister les favoris
        status = self.manager.get_all_favorites_status()
        self.assertEqual(status[1]['status'], 'filled')
        self.assertEqual(status[2]['status'], 'empty')
        self.assertEqual(status[3]['status'], 'filled')
        
        # 3. Charger et vérifier
        data1, _ = self.manager.load_favorite(1)
        data3, _ = self.manager.load_favorite(3)
        self.assertEqual(data1['title_x'], 100)
        self.assertEqual(data3['title_x'], 200)
        
        # 4. Supprimer un favori
        success, _ = self.manager.delete_favorite(1)
        self.assertTrue(success)
        
        # 5. Vérifier la suppression
        status = self.manager.get_all_favorites_status()
        self.assertEqual(status[1]['status'], 'empty')
        self.assertEqual(status[3]['status'], 'filled')


def run_all_tests():
    """Exécute tous les tests des favoris de formatage."""
    print("🧪 EXÉCUTION DES TESTS FAVORIS DE FORMATAGE")
    print("=" * 60)
    
    # Créer la suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    test_classes = [
        TestFormattingFavoritesDatabase,
        TestFavoritesManager,
        TestIntegrationFormattingFavorites
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Résumé
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
    else:
        print(f"❌ {len(result.failures)} échec(s), {len(result.errors)} erreur(s)")
    
    print(f"📊 {result.testsRun} tests exécutés")
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
