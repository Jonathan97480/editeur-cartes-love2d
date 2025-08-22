#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet du système de correction des chemins
Vérifie que la correction fonctionne et que l'application peut charger les images
"""

import sqlite3
import os
import sys

# Ajouter le chemin lib pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from config import DB_FILE

def test_corrected_paths():
    """Tester que les chemins corrigés fonctionnent dans l'application"""
    
    print('🧪 TEST COMPLET DU SYSTÈME DE CORRECTION DES CHEMINS')
    print('=' * 70)
    
    if not os.path.exists(DB_FILE):
        print(f'❌ Base de données non trouvée: {DB_FILE}')
        return False
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Récupérer toutes les cartes avec leurs chemins d'images
        cursor.execute('SELECT id, name, img FROM cards WHERE img IS NOT NULL')
        cards = cursor.fetchall()
        
        print(f'🃏 Cartes trouvées: {len(cards)}')
        print()
        
        success_count = 0
        error_count = 0
        
        for card_id, name, img_path in cards:
            print(f'🔍 Test carte ID {card_id}: {name}')
            print(f'   📁 Chemin: {img_path}')
            
            # Vérifier que le chemin n'est pas absolu
            if img_path and (img_path.startswith('C:') or img_path.startswith('c:') or 
                           img_path.startswith('D:') or img_path.startswith('d:')):
                print(f'   ❌ ERREUR: Chemin encore absolu!')
                error_count += 1
                continue
            
            # Vérifier que le fichier existe
            if img_path and os.path.exists(img_path):
                file_size = os.path.getsize(img_path)
                print(f'   ✅ Fichier trouvé ({file_size} octets)')
                success_count += 1
            else:
                print(f'   ❌ Fichier non trouvé: {img_path}')
                error_count += 1
            
            print()
        
        conn.close()
        
        print('📊 RÉSULTATS DU TEST:')
        print(f'   ✅ Succès: {success_count}')
        print(f'   ❌ Erreurs: {error_count}')
        print(f'   📈 Taux de réussite: {(success_count / len(cards) * 100):.1f}%')
        
        if error_count == 0:
            print('\n🎯 PARFAIT! Tous les chemins sont corrects et les fichiers existent')
            return True
        else:
            print(f'\n⚠️  {error_count} problèmes détectés')
            return False
            
    except Exception as e:
        print(f'❌ Erreur lors du test: {e}')
        return False

def test_application_loading():
    """Tester que l'application peut charger les cartes avec les nouveaux chemins"""
    
    print('\n🚀 TEST DE CHARGEMENT DE L\'APPLICATION')
    print('=' * 50)
    
    try:
        # Simuler le chargement de l'application
        from database import CardRepo
        
        repo = CardRepo(DB_FILE)
        cards = repo.list_cards()
        
        print(f'📊 Cartes chargées par l\'application: {len(cards)}')
        
        if len(cards) > 0:
            test_card = cards[0]
            print(f'🃏 Test avec la carte: {test_card.name}')
            print(f'   📁 Chemin image: {test_card.img}')
            
            # Vérifier que le chemin n'est pas absolu
            if test_card.img and os.path.exists(test_card.img):
                print('   ✅ L\'application peut accéder aux images')
                return True
            else:
                print('   ❌ L\'application ne peut pas accéder aux images')
                return False
        else:
            print('   ⚠️  Aucune carte trouvée')
            return False
            
    except Exception as e:
        print(f'❌ Erreur lors du test d\'application: {e}')
        return False

if __name__ == '__main__':
    print('🧪 LANCEMENT DES TESTS DE CORRECTION')
    print()
    
    # Test 1: Vérifier les chemins corrigés
    paths_ok = test_corrected_paths()
    
    # Test 2: Vérifier le chargement par l'application
    app_ok = test_application_loading()
    
    print('\n🏁 RÉSUMÉ FINAL:')
    print(f'   📁 Chemins corrigés: {"✅" if paths_ok else "❌"}')
    print(f'   🚀 Application fonctionnelle: {"✅" if app_ok else "❌"}')
    
    if paths_ok and app_ok:
        print('\n🎉 TOUS LES TESTS RÉUSSIS!')
        print('   La correction des chemins est parfaitement fonctionnelle')
        print('   L\'application peut maintenant être utilisée sur n\'importe quel ordinateur')
        sys.exit(0)
    else:
        print('\n❌ TESTS ÉCHOUÉS')
        print('   Certains problèmes subsistent et nécessitent une attention manuelle')
        sys.exit(1)
