#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour diagnostiquer et corriger le problème d'ID de carte
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from database_simple import CardRepo, Card
import sqlite3

def main():
    print("🔍 Diagnostic du problème d'ID de carte")
    print("=" * 50)
    
    # 1. Vérifier les cartes existantes
    repo = CardRepo('cartes.db')
    cards = repo.list_cards()
    
    print(f"📊 Cartes dans database_simple: {len(cards)}")
    for card in cards:
        print(f"   - ID: {card.id}, Nom: '{card.nom}'")
    
    # 2. Vérifier la table SQLite directement
    conn = sqlite3.connect('cartes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nom FROM cards ORDER BY id')
    sql_cards = cursor.fetchall()
    
    print(f"\n📊 Cartes dans SQLite: {len(sql_cards)}")
    for card in sql_cards:
        print(f"   - ID: {card[0]}, Nom: '{card[1]}'")
    
    # 3. Vérifier les IDs disponibles
    if cards:
        max_id = max(card.id for card in cards)
        print(f"\n🔢 ID maximum: {max_id}")
        
        # Vérifier s'il y a des trous dans les IDs
        existing_ids = {card.id for card in cards}
        all_ids = set(range(1, max_id + 1))
        missing_ids = all_ids - existing_ids
        
        if missing_ids:
            print(f"⚠️  IDs manquants: {sorted(missing_ids)}")
        else:
            print("✅ Aucun ID manquant")
    
    # 4. Test d'accès à différents IDs
    print(f"\n🧪 Test d'accès aux cartes:")
    test_ids = [1, 2, 10]
    
    for test_id in test_ids:
        try:
            card = repo.get_card(test_id)
            if card:
                print(f"   ✅ ID {test_id}: '{card.nom}'")
            else:
                print(f"   ❌ ID {test_id}: Carte non trouvée")
        except Exception as e:
            print(f"   ❌ ID {test_id}: Erreur - {e}")
    
    conn.close()
    
    print(f"\n💡 Solution recommandée:")
    if cards:
        valid_id = cards[0].id
        print(f"   - Utiliser un ID valide comme {valid_id}")
        print(f"   - Ou créer une nouvelle carte si nécessaire")
    else:
        print(f"   - Créer une nouvelle carte de test")

if __name__ == "__main__":
    main()
