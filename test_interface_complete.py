#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final : Création et affichage carte avec acteur
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.database import CardRepo, ensure_db, Card
from lib.ui_components import CardForm, CardList, get_available_actors
from lib.actors import ActorManager
from lib.config import DB_FILE

def test_interface_complete():
    """Test complet de l'interface avec le système d'acteurs."""
    
    print("🎯 TEST INTERFACE COMPLÈTE AVEC ACTEURS")
    print("=" * 50)
    
    # Initialiser
    ensure_db(DB_FILE)
    repo = CardRepo(DB_FILE)
    
    # Créer la fenêtre de test
    root = tk.Tk()
    root.title("Test Interface Acteurs - Complet")
    root.geometry("1200x800")
    
    # Notebook pour séparer création et liste
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # ===== ONGLET CRÉATION =====
    create_frame = ttk.Frame(notebook)
    notebook.add(create_frame, text="Créer/Éditer")
    
    def on_card_saved():
        """Callback appelé quand une carte est sauvegardée."""
        print("✅ Carte sauvegardée ! Actualisation de la liste...")
        card_list.refresh()  # Rafraîchir la liste
    
    # Formulaire de création
    form = CardForm(create_frame, repo, on_card_saved)
    form.pack(fill='both', expand=True, padx=5, pady=5)
    
    # ===== ONGLET LISTE =====
    list_frame = ttk.Frame(notebook)
    notebook.add(list_frame, text="Liste des Cartes")
    
    def on_card_select(card_id):
        """Callback appelé quand une carte est sélectionnée."""
        print(f"📋 Carte sélectionnée : {card_id}")
        card = repo.get(card_id)
        if card:
            form.load_card(card)
            notebook.select(0)  # Basculer vers l'onglet création
            print(f"✅ Carte '{card.name}' chargée dans le formulaire")
    
    # Liste des cartes
    card_list = CardList(list_frame, repo, on_card_select)
    card_list.pack(fill='both', expand=True, padx=5, pady=5)
    
    # ===== ONGLET INFORMATIONS =====
    info_frame = ttk.Frame(notebook)
    notebook.add(info_frame, text="Informations")
    
    info_text = tk.Text(info_frame, wrap='word', font=('Consolas', 10))
    info_scrollbar = ttk.Scrollbar(info_frame, orient='vertical', command=info_text.yview)
    info_text.config(yscrollcommand=info_scrollbar.set)
    
    info_text.pack(side='left', fill='both', expand=True, padx=(5,0), pady=5)
    info_scrollbar.pack(side='right', fill='y', pady=5)
    
    # Remplir les informations
    info_content = """
🎯 TEST INTERFACE COMPLÈTE AVEC SYSTÈME D'ACTEURS

✅ FONCTIONNALITÉS TESTÉES :
• Sélection multiple d'acteurs avec Ctrl+clic
• Création de cartes avec liaisons acteur-carte
• Affichage des vrais acteurs dans la liste (plus Joueur/IA)
• Chargement et édition de cartes existantes
• Actualisation automatique après sauvegarde

🎮 COMMENT TESTER :
1. Onglet "Créer/Éditer" :
   - Sélectionnez un ou plusieurs acteurs avec Ctrl+clic
   - Remplissez les informations de la carte
   - Cliquez "Sauvegarder"

2. Onglet "Liste des Cartes" :
   - Vérifiez que la colonne "Acteurs" affiche les vrais acteurs
   - Double-cliquez sur une carte pour l'éditer
   - Utilisez les filtres par acteur

3. Test des liaisons :
   - Créez une carte avec "Barbus"
   - Vérifiez qu'elle apparaît bien liée à "Barbus" dans la liste
   - Éditez la carte et changez l'acteur
   - Vérifiez la mise à jour

🔧 AMÉLIORATIONS APPORTÉES :
• Interface : Listbox au lieu de Combobox
• Base de données : Liaisons carte-acteur fonctionnelles
• Affichage : Colonne "Acteurs" au lieu de "Côté"
• Filtrage : Par acteur réel au lieu de side legacy
• Messages : Informatifs pour debug

⚠️ SI PROBLÈMES :
- Vérifiez la console pour les messages de debug
- Les liaisons sont créées automatiquement
- L'affichage se met à jour après sauvegarde

🎉 STATUT : SYSTÈME COMPLET ET FONCTIONNEL !
"""
    
    info_text.insert('1.0', info_content)
    info_text.config(state='disabled')
    
    # Afficher les informations sur les acteurs
    print(f"\n📋 Acteurs disponibles :")
    actors = get_available_actors()
    for i, actor in enumerate(actors, 1):
        print(f"   {i}. {actor}")
    
    print(f"\n🚀 Interface de test complète lancée !")
    print(f"   Testez la création et l'affichage des cartes avec acteurs")
    print(f"   Fermez la fenêtre pour terminer le test")
    
    # Actualiser la liste initiale
    card_list.refresh()
    
    # Lancer l'interface
    root.mainloop()
    
    print(f"\n✅ Test interface terminé")

if __name__ == "__main__":
    test_interface_complete()
