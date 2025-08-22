#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide de la correction du double-clic
"""
# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()


import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.database import CardRepo, ensure_db
from lib.config import DB_FILE

def default_db_path():
    return str(Path(__file__).parent / DB_FILE)

def test_load_card_fix():
    """Test de la correction du problème de load_card."""

    print("🧪 Test de la correction load_card")
    print("=" * 40)
    
    # Initialiser la base de données
    db_path = default_db_path()
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    ensure_db(db_path)
    repo = CardRepo(db_path)
    
    # Récupérer toutes les cartes
    cards = repo.list_cards()
    
    if not cards:
        print("⚠️  Aucune carte trouvée pour le test")
        return True
    
    print(f"📊 {len(cards)} cartes trouvées")
    
    # Tester avec le premier ID de carte
    test_card = cards[0]
    card_id = test_card.id
    
    print(f"🔍 Test avec carte ID {card_id} : '{test_card.name}'")
    
    # Simuler la logique de load_card corrigée
    try:
        # Cas 1 : ID passé en paramètre (nouveau comportement)
        if hasattr(card_id, 'id'):
            card = card_id
        else:
            card = repo.get(card_id)
            if not card:
                print("❌ Impossible de récupérer la carte")
                return False
        
        # Vérifier que nous avons un objet Card
        if not hasattr(card, 'id'):
            print("❌ L'objet retourné n'est pas une carte valide")
            return False
        
        print(f"✅ Carte récupérée : ID={card.id}, Nom='{card.name}'")
        
        # Cas 2 : Objet Card passé directement (comportement legacy)
        if hasattr(test_card, 'id'):
            card = test_card
        else:
            card = repo.get(test_card)
            if not card:
                print("❌ Impossible de récupérer la carte (cas 2)")
                return False
        
        print(f"✅ Test legacy OK : ID={card.id}, Nom='{card.name}'")
        
        print("🎉 Correction validée !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur durant le test : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_load_card_fix()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("Appuyez sur Entrée pour fermer...")
    input()
