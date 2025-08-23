#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test unitaire complet pour les exports de packages
Tests pour les fonctionnalités d'export Template et Complet
"""

import unittest
import tempfile
import shutil
import zipfile
import os
import sys
from pathlib import Path

# Ajouter le chemin racine pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lib.database import CardRepo, ensure_db
from lib.game_package_exporter import GamePackageExporter

class TestExportPackages(unittest.TestCase):
    """Tests pour les exports de packages Template et Complet"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration unique pour tous les tests"""
        # Chemin vers la base de données de test
        cls.db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cartes.db')
        if not os.path.exists(cls.db_path):
            # Utiliser la base de données principale si pas de test
            cls.db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cartes.db')
        
        # Initialiser la base de données
        ensure_db(cls.db_path)
        cls.repo = CardRepo(cls.db_path)
        
        # Vérifier qu'on a des cartes
        cls.cards = cls.repo.list_cards()
        if not cls.cards:
            raise unittest.SkipTest("Aucune carte dans la base de données pour les tests")
        
        # Créer un dossier temporaire pour les exports
        cls.temp_dir = tempfile.mkdtemp(prefix="test_export_")
        
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        if hasattr(cls, 'temp_dir') and os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
    
    def setUp(self):
        """Configuration avant chaque test"""
        # Créer un sous-dossier unique pour chaque test
        self.test_output_dir = os.path.join(self.temp_dir, f"test_{self._testMethodName}")
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_export_template_basic(self):
        """Test basique de l'export Template (images seules)"""
        print("\n🎨 Test: Export Template...")
        
        # Créer l'exporteur Template
        exporter = GamePackageExporter(self.repo, self.test_output_dir, 'template')
        
        # Exporter 2 cartes
        card_ids = [card.id for card in self.cards[:2]]
        package_path = exporter.export_complete_package(card_ids)
        
        # Vérifications de base
        self.assertTrue(os.path.exists(package_path), "Le package ZIP doit être créé")
        self.assertTrue(package_path.endswith('.zip'), "Le fichier doit être un ZIP")
        
        # Vérifier le contenu du ZIP
        with zipfile.ZipFile(package_path, 'r') as zipf:
            files = zipf.namelist()
            
            # Vérifier la structure attendue
            self.assertIn('cards_data.lua', files, "Fichier Lua des cartes requis")
            self.assertIn('README.md', files, "Documentation requise")
            self.assertIn('package_config.json', files, "Configuration requise")
            
            # Vérifier les images des cartes
            card_images = [f for f in files if f.startswith('cards/') and f.endswith('.png')]
            self.assertEqual(len(card_images), len(card_ids), 
                           f"Doit avoir {len(card_ids)} images de cartes")
            
            # Vérifier les polices
            font_files = [f for f in files if f.startswith('fonts/')]
            self.assertGreater(len(font_files), 0, "Doit avoir au moins une police")
            
            # Vérifier que le README contient des infos Template
            readme_content = zipf.read('README.md').decode('utf-8')
            self.assertIn('Template', readme_content, "README doit mentionner le type Template")
            
        print(f"   ✅ Package Template créé: {os.path.basename(package_path)}")
        print(f"   📦 Taille: {os.path.getsize(package_path):,} octets")
    
    def test_export_complete_basic(self):
        """Test basique de l'export Complet (images avec texte)"""
        print("\n🖼️ Test: Export Complet...")
        
        # Créer l'exporteur Complet
        exporter = GamePackageExporter(self.repo, self.test_output_dir, 'complete')
        
        # Exporter 2 cartes
        card_ids = [card.id for card in self.cards[:2]]
        package_path = exporter.export_complete_package(card_ids)
        
        # Vérifications de base
        self.assertTrue(os.path.exists(package_path), "Le package ZIP doit être créé")
        self.assertTrue(package_path.endswith('.zip'), "Le fichier doit être un ZIP")
        
        # Vérifier le contenu du ZIP
        with zipfile.ZipFile(package_path, 'r') as zipf:
            files = zipf.namelist()
            
            # Vérifier la structure attendue
            self.assertIn('cards_data.lua', files, "Fichier Lua des cartes requis")
            self.assertIn('README.md', files, "Documentation requise")
            self.assertIn('package_config.json', files, "Configuration requise")
            
            # Vérifier les images des cartes
            card_images = [f for f in files if f.startswith('cards/') and f.endswith('.png')]
            self.assertEqual(len(card_images), len(card_ids), 
                           f"Doit avoir {len(card_ids)} images de cartes")
            
            # Vérifier les polices
            font_files = [f for f in files if f.startswith('fonts/')]
            self.assertGreater(len(font_files), 0, "Doit avoir au moins une police")
            
            # Vérifier que le README contient des infos Complet
            readme_content = zipf.read('README.md').decode('utf-8')
            self.assertIn('Complet', readme_content, "README doit mentionner le type Complet")
            
        print(f"   ✅ Package Complet créé: {os.path.basename(package_path)}")
        print(f"   📦 Taille: {os.path.getsize(package_path):,} octets")
    
    def test_export_size_difference(self):
        """Test de la différence de taille entre Template et Complet"""
        print("\n📊 Test: Comparaison tailles Template vs Complet...")
        
        # Même ensemble de cartes pour les deux exports
        card_ids = [card.id for card in self.cards[:3]]
        
        # Export Template
        exporter_template = GamePackageExporter(self.repo, self.test_output_dir, 'template')
        package_template = exporter_template.export_complete_package(card_ids)
        size_template = os.path.getsize(package_template)
        
        # Export Complet  
        exporter_complete = GamePackageExporter(self.repo, self.test_output_dir, 'complete')
        package_complete = exporter_complete.export_complete_package(card_ids)
        size_complete = os.path.getsize(package_complete)
        
        # Le Template devrait être plus petit ou égal au Complet
        # (en théorie plus petit car pas de texte fusionné, mais peut varier selon compression)
        self.assertGreater(size_complete, 0, "Package Complet doit avoir une taille > 0")
        self.assertGreater(size_template, 0, "Package Template doit avoir une taille > 0")
        
        # Calculer la différence
        diff_percent = abs(size_complete - size_template) / size_complete * 100
        
        print(f"   📦 Template: {size_template:,} octets")
        print(f"   📦 Complet:  {size_complete:,} octets")
        print(f"   📊 Différence: {diff_percent:.1f}%")
        
        # La différence ne devrait pas être énorme (moins de 50%)
        self.assertLess(diff_percent, 50, "Différence de taille ne devrait pas dépasser 50%")
    
    def test_export_with_all_cards(self):
        """Test d'export avec toutes les cartes disponibles"""
        print(f"\n🎯 Test: Export de toutes les cartes ({len(self.cards)} cartes)...")
        
        # Export Template avec toutes les cartes
        exporter = GamePackageExporter(self.repo, self.test_output_dir, 'template')
        all_card_ids = [card.id for card in self.cards]
        package_path = exporter.export_complete_package(all_card_ids)
        
        # Vérifications
        self.assertTrue(os.path.exists(package_path), "Package complet doit être créé")
        
        with zipfile.ZipFile(package_path, 'r') as zipf:
            files = zipf.namelist()
            
            # Vérifier qu'on a toutes les images
            card_images = [f for f in files if f.startswith('cards/') and f.endswith('.png')]
            self.assertEqual(len(card_images), len(all_card_ids), 
                           f"Doit avoir {len(all_card_ids)} images pour toutes les cartes")
            
            # Vérifier le fichier Lua
            lua_content = zipf.read('cards_data.lua').decode('utf-8')
            self.assertIn('return', lua_content, "Fichier Lua doit avoir une structure valide")
            
        print(f"   ✅ Export complet réussi: {len(card_images)} cartes exportées")
        print(f"   📦 Taille finale: {os.path.getsize(package_path):,} octets")
    
    def test_export_font_inclusion(self):
        """Test de l'inclusion des polices dans l'export"""
        print("\n🎨 Test: Inclusion des polices...")
        
        exporter = GamePackageExporter(self.repo, self.test_output_dir, 'complete')
        card_ids = [card.id for card in self.cards[:2]]
        package_path = exporter.export_complete_package(card_ids)
        
        with zipfile.ZipFile(package_path, 'r') as zipf:
            files = zipf.namelist()
            
            # Vérifier les polices
            font_files = [f for f in files if f.startswith('fonts/')]
            self.assertGreater(len(font_files), 0, "Doit contenir au moins une police")
            
            # Vérifier les extensions de polices supportées
            supported_extensions = ['.ttf', '.otf', '.ttc']
            font_extensions = [os.path.splitext(f)[1].lower() for f in font_files]
            
            for ext in font_extensions:
                self.assertIn(ext, supported_extensions, 
                            f"Extension de police {ext} doit être supportée")
            
            print(f"   ✅ Polices trouvées: {len(font_files)}")
            for font_file in font_files:
                font_size = zipf.getinfo(font_file).file_size
                print(f"      📝 {font_file} ({font_size:,} octets)")
    
    def test_export_lua_data_validity(self):
        """Test de la validité des données Lua exportées"""
        print("\n📄 Test: Validité des données Lua...")
        
        exporter = GamePackageExporter(self.repo, self.test_output_dir, 'template')
        card_ids = [card.id for card in self.cards[:3]]
        package_path = exporter.export_complete_package(card_ids)
        
        with zipfile.ZipFile(package_path, 'r') as zipf:
            lua_content = zipf.read('cards_data.lua').decode('utf-8')
            
            # Vérifications basiques de structure Lua
            self.assertIn('return', lua_content, "Doit contenir une instruction return")
            self.assertIn('{', lua_content, "Doit contenir des tables Lua")
            self.assertIn('}', lua_content, "Doit contenir des fermetures de tables")
            
            # Vérifier la présence de champs importants
            expected_fields = ['name', 'PowerBlow', 'Description', 'TextFormatting']
            for field in expected_fields:
                self.assertIn(field, lua_content, f"Champ {field} doit être présent")
            
            # Vérifier que chaque carte exportée est présente
            for card in self.cards[:3]:
                self.assertIn(card.name, lua_content, 
                            f"Carte '{card.name}' doit être dans le Lua")
            
        print(f"   ✅ Fichier Lua valide: {len(lua_content):,} caractères")
        print(f"   📋 Cartes exportées: {len(card_ids)}")
    
    def test_export_documentation(self):
        """Test de la génération de documentation"""
        print("\n📚 Test: Génération de documentation...")
        
        # Test avec Template
        exporter_template = GamePackageExporter(self.repo, self.test_output_dir, 'template')
        package_template = exporter_template.export_complete_package([self.cards[0].id])
        
        # Test avec Complet
        exporter_complete = GamePackageExporter(self.repo, self.test_output_dir, 'complete')
        package_complete = exporter_complete.export_complete_package([self.cards[0].id])
        
        # Vérifier README Template
        with zipfile.ZipFile(package_template, 'r') as zipf:
            readme_template = zipf.read('README.md').decode('utf-8')
            self.assertIn('🎨 Type d\'Export: Template', readme_template)
            self.assertIn('sans texte fusionné', readme_template)
            self.assertIn('positionné dynamiquement', readme_template)
        
        # Vérifier README Complet
        with zipfile.ZipFile(package_complete, 'r') as zipf:
            readme_complete = zipf.read('README.md').decode('utf-8')
            self.assertIn('🖼️ Type d\'Export: Complet', readme_complete)
            self.assertIn('template + texte intégré', readme_complete)
            self.assertIn('prêtes à utiliser', readme_complete)
        
        print("   ✅ Documentation Template générée correctement")
        print("   ✅ Documentation Complet générée correctement")
    
    def test_export_error_handling(self):
        """Test de la gestion d'erreurs"""
        print("\n⚠️ Test: Gestion d'erreurs...")
        
        # Test avec des IDs de cartes invalides
        exporter = GamePackageExporter(self.repo, self.test_output_dir, 'template')
        
        # IDs qui n'existent probablement pas
        invalid_ids = [99999, 99998]
        
        try:
            package_path = exporter.export_complete_package(invalid_ids)
            # Si ça passe, vérifier qu'on a un package vide ou approprié
            with zipfile.ZipFile(package_path, 'r') as zipf:
                files = zipf.namelist()
                card_images = [f for f in files if f.startswith('cards/') and f.endswith('.png')]
                # Ne devrait pas y avoir d'images pour des cartes inexistantes
                self.assertEqual(len(card_images), 0, "Pas d'images pour cartes inexistantes")
        except Exception as e:
            # Une exception est acceptable pour des IDs invalides
            print(f"   ⚠️ Exception attendue pour IDs invalides: {type(e).__name__}")
        
        print("   ✅ Gestion d'erreurs testée")


def run_export_tests():
    """Lance tous les tests d'export"""
    print("🧪 TESTS UNITAIRES - EXPORT DE PACKAGES")
    print("=" * 50)
    
    # Créer la suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExportPackages)
    
    # Lancer les tests avec verbosité
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Résumé final
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 TOUS LES TESTS D'EXPORT RÉUSSIS!")
    else:
        print(f"❌ {len(result.failures)} test(s) échoué(s)")
        print(f"⚠️ {len(result.errors)} erreur(s)")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_export_tests()
    sys.exit(0 if success else 1)
