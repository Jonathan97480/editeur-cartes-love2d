#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide du système de base de données après correction
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print('🔧 Test de correction du système de base de données...')
try:
    # Test avec notre nouvelle structure simplifiée
    from lib.database_simple import CardRepo
    
    repo = CardRepo('cartes.db')
    cards = repo.list_cards()
    print(f'✅ {len(cards)} cartes trouvées')
    
    # Test des fonctionnalités
    for card in cards:
        print(f'   🃏 {card.nom} ({card.type}) - Formatage: {card.title_font}')
    
    # Test de création d'une nouvelle carte
    from lib.database_simple import Card
    test_card = Card()
    test_card.nom = "Test Correction"
    test_card.type = "Sort"
    test_card.rarete = "Commun" 
    test_card.cout = 1
    test_card.description = "Test de correction"
    
    card_id = repo.save_card(test_card)
    print(f'✅ Carte de test créée avec ID: {card_id}')
    
    # Supprimer la carte de test
    repo.delete_card(card_id)
    print('✅ Carte de test supprimée')
    
    print('\n✅ Test réussi ! Le système de base de données fonctionne.')
    
except Exception as e:
    print(f'❌ Erreur : {e}')
    import traceback
    traceback.print_exc()

print('\nTest terminé automatiquement.')
