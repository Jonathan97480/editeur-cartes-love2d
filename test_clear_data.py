#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la fonctionnalité Clear Data
"""
import sqlite3
from pathlib import Path
import os
import shutil
from lib.database import CardRepo, ensure_db, Card
from lib.config import DB_FILE

def create_test_data():
    """Crée des données de test pour valider la suppression."""
    print("🔧 Création de données de test...")
    
    # Créer quelques cartes de test
    repo = CardRepo(DB_FILE)
    
    test_cards_data = [
        {
            'name': 'Carte Test 1',
            'powerblow': 3,
            'rarity': 'commun',
            'side': 'joueur',
            'img': 'test_image1.png'
        },
        {
            'name': 'Carte Test 2',
            'powerblow': 5,
            'rarity': 'rare',
            'side': 'ia',
            'img': 'test_image2.png'
        }
    ]
    
    card_ids = []
    for card_data in test_cards_data:
        # Créer un objet Card
        card = Card()
        card.name = card_data['name']
        card.powerblow = card_data['powerblow']
        card.rarity = card_data['rarity']
        card.side = card_data['side']
        card.img = card_data['img']
        card.description = f"Description de {card_data['name']}"
        
        # Insérer la carte
        card_id = repo.insert(card)
        card_ids.append(card_id)
        print(f"   ✅ Carte créée : ID {card_id} - {card_data['name']}")
    
    # Créer quelques fichiers de test dans images/
    images_folder = Path("images")
    images_folder.mkdir(exist_ok=True)
    
    test_files = ['test1.png', 'test2.jpg', 'subfolder/test3.gif']
    for file_path in test_files:
        full_path = images_folder / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text("Test image content")
        print(f"   ✅ Fichier test créé : {full_path}")
    
    return card_ids, test_files

def count_data():
    """Compte les données présentes."""
    print("\n📊 État actuel des données :")
    
    # Compter les cartes
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM cards")
            card_count = cursor.fetchone()[0]
            print(f"   📄 Cartes : {card_count}")
            
            # Compter les acteurs
            cursor = conn.execute("SELECT COUNT(*) FROM actors")
            actor_count = cursor.fetchone()[0]
            print(f"   🎭 Acteurs : {actor_count}")
            
            # Compter les liaisons
            cursor = conn.execute("SELECT COUNT(*) FROM card_actors")
            link_count = cursor.fetchone()[0]
            print(f"   🔗 Liaisons : {link_count}")
    except Exception as e:
        print(f"   ❌ Erreur base de données : {e}")
    
    # Compter les fichiers images
    images_folder = Path("images")
    if images_folder.exists():
        image_files = list(images_folder.rglob("*"))
        file_count = len([f for f in image_files if f.is_file()])
        print(f"   🖼️ Fichiers images : {file_count}")
    else:
        print(f"   🖼️ Fichiers images : 0 (dossier inexistant)")

def simulate_clear_data():
    """Simule la fonction clear_all_data sans les confirmations utilisateur."""
    print("\n🗑️ Simulation de Clear Data...")
    
    try:
        # Supprimer toutes les images
        images_folder = Path("images")
        if images_folder.exists():
            deleted_files = []
            for item in images_folder.rglob("*"):
                if item.is_file():
                    deleted_files.append(item)
                    item.unlink()
                elif item.is_dir() and not any(item.iterdir()):
                    item.rmdir()
            
            # Recréer le dossier vide
            if not images_folder.exists():
                images_folder.mkdir(exist_ok=True)
            
            print(f"   ✅ {len(deleted_files)} fichiers supprimés du dossier images/")
        
        # Vider complètement la base de données
        with sqlite3.connect(DB_FILE) as conn:
            # Obtenir toutes les tables
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Supprimer toutes les données de toutes les tables
            for table in tables:
                if table != 'sqlite_sequence':  # Table système SQLite
                    conn.execute(f"DELETE FROM {table}")
            
            # Réinitialiser les séquences d'auto-increment
            conn.execute("DELETE FROM sqlite_sequence")
            conn.commit()
            
            print(f"   ✅ Toutes les données supprimées de {len(tables)} tables")
        
        print("   🎉 Clear Data terminé avec succès !")
        
    except Exception as e:
        print(f"   ❌ Erreur lors du Clear Data : {e}")

def test_clear_data_complete():
    """Test complet de la fonctionnalité Clear Data."""
    print("🧪 TEST COMPLET - FONCTIONNALITÉ CLEAR DATA")
    print("=" * 50)
    
    # État initial
    print("\n📋 ÉTAPE 1 : État initial")
    count_data()
    
    # Créer des données de test
    print("\n📋 ÉTAPE 2 : Création de données de test")
    card_ids, test_files = create_test_data()
    
    # État après création
    print("\n📋 ÉTAPE 3 : État après création de test")
    count_data()
    
    # Simulation du Clear Data
    print("\n📋 ÉTAPE 4 : Exécution Clear Data")
    simulate_clear_data()
    
    # Vérification finale
    print("\n📋 ÉTAPE 5 : Vérification finale")
    count_data()
    
    # Validation
    print("\n✅ VALIDATION :")
    
    # Vérifier que la base est vide
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM cards")
            remaining_cards = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) FROM actors")
            remaining_actors = cursor.fetchone()[0]
            
            if remaining_cards == 0 and remaining_actors == 0:
                print("   ✅ Base de données correctement vidée")
            else:
                print(f"   ❌ Données restantes : {remaining_cards} cartes, {remaining_actors} acteurs")
    except Exception as e:
        print(f"   ❌ Erreur validation DB : {e}")
    
    # Vérifier que le dossier images est vide
    images_folder = Path("images")
    if images_folder.exists():
        remaining_files = list(images_folder.rglob("*"))
        file_count = len([f for f in remaining_files if f.is_file()])
        
        if file_count == 0:
            print("   ✅ Dossier images correctement vidé")
        else:
            print(f"   ❌ Fichiers restants : {file_count}")
    else:
        print("   ✅ Dossier images supprimé")
    
    print("\n" + "=" * 50)
    print("🎉 TEST CLEAR DATA TERMINÉ")

if __name__ == "__main__":
    test_clear_data_complete()
