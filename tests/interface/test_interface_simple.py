#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de l'interface améliorée
"""
import sqlite3
from lib.database import CardRepo
from lib.config import DB_FILE

def test_simple_interface():
    """Test simple de l'interface"""
    print("🎨 TEST SIMPLE - INTERFACE AMÉLIORÉE")
    print("=" * 60)
    
    try:
        # Récupérer une carte
        repo = CardRepo(DB_FILE)
        cards = repo.list_cards()
        
        if not cards:
            print("❌ Aucune carte disponible")
            return
        
        test_card = cards[0]
        print(f"🎯 Carte de test: {test_card.name}")
        
        # Lancer l'application principale directement
        print("💡 Lancement de l'éditeur via l'application principale...")
        print("   Cliquez sur 'Format Texte' pour voir les améliorations:")
        print("   ✅ Zone contrôles plus large (30%)")
        print("   ✅ Curseurs pleine largeur") 
        print("   ✅ Préréglages énergie en 3 lignes")
        print("   ✅ Scrollbar plus visible")
        print("   ✅ Support roulette souris")
        
        # Importer et lancer l'app principale
        import subprocess
        subprocess.run(["python", "main.py"])
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_simple_interface()
