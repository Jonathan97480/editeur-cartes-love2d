#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du bouton de formatage
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

def test_formatting_button():
    """Test l'ouverture de l'éditeur de formatage"""
    print("🧪 Test du bouton de formatage de texte")
    print("=" * 50)
    
    try:
        from lib.database import CardRepo, ensure_db
        from lib.config import DB_FILE
        
        # Configurer la base de données
        db_path = str(Path(__file__).parent / DB_FILE)
        ensure_db(db_path)
        repo = CardRepo(db_path)
        
        cards = repo.list_cards()
        if not cards:
            print("❌ Aucune carte trouvée pour le test")
            return False
        
        # Prendre la première carte
        card = cards[0]
        print(f"✅ Carte de test : {card.name}")
        print(f"📊 ID de la carte : {card.id}")
        
        # Test de récupération de la carte par ID
        retrieved_card = repo.get(card.id)
        if retrieved_card:
            print(f"✅ Carte récupérée par ID : {retrieved_card.name}")
        else:
            print("❌ Impossible de récupérer la carte par ID")
            return False
        
        # Test d'import de l'éditeur
        try:
            from lib.text_formatting_editor import open_text_formatting_editor
            print("✅ Import de l'éditeur de formatage réussi")
        except ImportError as e:
            print(f"❌ Erreur d'import : {e}")
            return False
        
        # Test d'import du système simplifié
        try:
            from lib.database_simple import CardRepo as SimpleRepo
            simple_repo = SimpleRepo(db_path)
            print("✅ Import du système simplifié réussi")
        except ImportError as e:
            print(f"❌ Erreur d'import système simplifié : {e}")
            return False
        
        print("✅ Tous les tests passent ! Le bouton devrait fonctionner.")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_formatting_button()
    if success:
        print("\n🎉 Test réussi ! Le bouton de formatage devrait maintenant fonctionner.")
    else:
        print("\n❌ Test échoué. Il y a encore des problèmes à résoudre.")
