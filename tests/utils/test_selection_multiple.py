#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la fonctionnalité de sélection multiple d'acteurs
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.database import CardRepo, ensure_db
from lib.ui_components import CardForm, get_available_actors
from lib.actors import ActorManager
from lib.config import DB_FILE


def test_selection_multiple():
    """Test de l'interface de sélection multiple d'acteurs."""
    
    print("🎯 TEST : Sélection multiple d'acteurs")
    print("=" * 50)
    
    # Initialiser la base de données
    ensure_db(DB_FILE)
    repo = CardRepo(DB_FILE)
    
    # Vérifier les acteurs disponibles
    print("📋 Acteurs disponibles :")
    actors = get_available_actors()
    for i, actor in enumerate(actors, 1):
        print(f"   {i}. {actor}")
    
    if len(actors) < 2:
        print("⚠️  Il faut au moins 2 acteurs pour tester la sélection multiple")
        return False
    
    # Créer la fenêtre de test
    root = tk.Tk()
    root.title("Test - Sélection Multiple d'Acteurs")
    root.geometry("1000x800")
    
    def on_card_saved():
        """Callback appelé quand une carte est sauvegardée."""
        print("✅ Carte sauvegardée avec succès !")
    
    # Créer le formulaire de carte
    form = CardForm(root, repo, on_card_saved)
    form.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Informations d'aide
    help_frame = ttk.LabelFrame(root, text="Instructions", padding=10)
    help_frame.pack(fill='x', padx=10, pady=(0,10))
    
    instructions = [
        "1. Utilisez Ctrl+clic pour sélectionner plusieurs acteurs",
        "2. Cliquez sans Ctrl pour sélectionner un seul acteur",
        "3. Maj+clic pour sélectionner une plage d'acteurs",
        "4. Créez une carte de test et sauvegardez",
        "5. Vérifiez que la carte est liée aux acteurs sélectionnés"
    ]
    
    for instruction in instructions:
        ttk.Label(help_frame, text=instruction).pack(anchor='w')
    
    # Test automatique de sélection multiple
    def test_auto():
        """Test automatique de la sélection multiple."""
        print("\n🤖 Test automatique de la sélection multiple...")
        
        # Sélectionner les 2 premiers acteurs
        form.actors_listbox.selection_clear(0, 'end')
        form.actors_listbox.selection_set(0, 1)  # Sélectionner les indices 0 et 1
        
        # Remplir le formulaire
        form.name_var.set("Test Multi-Acteurs")
        form.img_var.set("test_image.png")
        form.desc_txt.delete('1.0', 'end')
        form.desc_txt.insert('1.0', "Carte de test pour la sélection multiple d'acteurs")
        form.power_var.set(5)
        
        # Vérifier la sélection
        selected = form._get_selected_actors()
        print(f"   Acteurs sélectionnés : {selected}")
        
        if len(selected) >= 2:
            print("   ✅ Sélection multiple fonctionne")
            return True
        else:
            print("   ❌ Sélection multiple ne fonctionne pas")
            return False
    
    # Bouton de test automatique
    test_button = ttk.Button(help_frame, text="🧪 Test Automatique", command=test_auto)
    test_button.pack(pady=5)
    
    # Afficher les informations sur la listbox
    def show_listbox_info():
        """Affiche les informations sur la listbox actuelle."""
        selected_indices = form.actors_listbox.curselection()
        selected_actors = form._get_selected_actors()
        print(f"\n📊 État actuel de la sélection :")
        print(f"   Indices sélectionnés : {list(selected_indices)}")
        print(f"   Acteurs sélectionnés : {selected_actors}")
        print(f"   Nombre d'acteurs : {len(selected_actors)}")
    
    info_button = ttk.Button(help_frame, text="📊 Afficher Info Sélection", command=show_listbox_info)
    info_button.pack(pady=2)
    
    print("\n🚀 Interface de test lancée !")
    print("   Testez la sélection multiple dans l'interface")
    print("   Fermez la fenêtre pour terminer le test")
    
    # Lancer l'interface
    root.mainloop()
    
    print("\n✅ Test de sélection multiple terminé")
    return True


def test_database_linkage():
    """Test de la liaison en base de données avec plusieurs acteurs."""
    
    print("\n🔗 TEST : Liaison base de données avec plusieurs acteurs")
    print("=" * 50)
    
    try:
        # Initialiser la base
        ensure_db(DB_FILE)
        repo = CardRepo(DB_FILE)
        actor_manager = ActorManager(DB_FILE)
        
        # Créer une carte de test
        from lib.database import Card
        
        test_card = Card()
        test_card.name = "Carte Test Multi-Acteurs"
        test_card.img = "test.png"
        test_card.description = "Test de liaison multiple"
        test_card.powerblow = 3
        test_card.side = "joueur"
        test_card.rarity = "commun"
        
        # Sauvegarder la carte
        card_id = repo.insert(test_card)
        print(f"   Carte créée avec ID : {card_id}")
        
        # Obtenir les acteurs disponibles
        actors = actor_manager.list_actors()
        if len(actors) < 2:
            print("   ⚠️  Pas assez d'acteurs pour le test de liaison multiple")
            return False
        
        # Lier la carte à plusieurs acteurs
        linked_actors = actors[:3]  # Prendre les 3 premiers acteurs
        for actor in linked_actors:
            actor_manager.link_card_to_actor(card_id, actor['id'])
            print(f"   ✅ Carte liée à l'acteur : {actor['name']}")
        
        # Vérifier les liaisons
        card_actors = actor_manager.get_card_actors(card_id)
        print(f"\n   📋 Acteurs liés à la carte :")
        for actor in card_actors:
            print(f"      - {actor['name']}")
        
        if len(card_actors) == len(linked_actors):
            print(f"   ✅ Liaison multiple réussie : {len(card_actors)} acteurs liés")
            return True
        else:
            print(f"   ❌ Erreur de liaison : {len(card_actors)} au lieu de {len(linked_actors)}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test de liaison : {e}")
        return False


if __name__ == "__main__":
    print("🎯 TESTS DE SÉLECTION MULTIPLE D'ACTEURS")
    print("=" * 60)
    
    # Test 1 : Liaison en base de données
    test1_ok = test_database_linkage()
    
    # Test 2 : Interface utilisateur
    test2_ok = test_selection_multiple()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS DES TESTS :")
    print(f"   Test liaison BDD : {'✅ RÉUSSI' if test1_ok else '❌ ÉCHEC'}")
    print(f"   Test interface   : {'✅ RÉUSSI' if test2_ok else '❌ ÉCHEC'}")
    
    if test1_ok and test2_ok:
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("   La sélection multiple d'acteurs fonctionne correctement")
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus")
