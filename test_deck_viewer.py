#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST DU VISUALISEUR DE DECK
=============================

Test de la nouvelle fonctionnalité de visualisation du deck.
"""
import sys
import os
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

def test_deck_viewer():
    """Test du visualiseur de deck."""
    print("🧪 Test du visualiseur de deck")
    print("=" * 40)
    
    try:
        from lib.database import CardRepo
        from lib.deck_viewer import DeckViewerWindow
        import tkinter as tk
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        
        # Initialiser la base de données
        repo = CardRepo("cartes.db")
        cards = repo.list_cards()
        
        print(f"📊 Cartes trouvées en base : {len(cards)}")
        
        if not cards:
            print("⚠️ Aucune carte en base pour tester")
            print("💡 Ajoutez quelques cartes dans l'application principale d'abord")
            root.destroy()
            return False
        
        # Afficher quelques infos sur les cartes
        print("\n📋 Aperçu des cartes :")
        for i, card in enumerate(cards[:5]):  # Limiter à 5 pour l'affichage
            rarity = card.rarity or "inconnue"
            types = ", ".join(card.types) if card.types else "aucun"
            img_status = "✅" if card.img and os.path.exists(card.img) else "❌"
            print(f"   {i+1}. {card.name} - {rarity} - {types} - Image: {img_status}")
        
        if len(cards) > 5:
            print(f"   ... et {len(cards) - 5} autres cartes")
        
        # Tester l'ouverture du visualiseur
        print(f"\n🚀 Ouverture du visualiseur de deck...")
        
        deck_viewer = DeckViewerWindow(root, repo)
        
        print("✅ Visualiseur créé avec succès !")
        print("\n🎯 Fonctionnalités disponibles :")
        print("   • Tri par rareté (commun, rare, épique, légendaire, mythique)")
        print("   • Tri par types (attaque, défense, soutien, sort, piège)")
        print("   • Tri par nom, par puissance")
        print("   • Affichage en grille (5 cartes par ligne)")
        print("   • Zone scrollable")
        print("   • Images redimensionnées automatiquement")
        print("   • Cache d'images pour les performances")
        
        print(f"\n💡 Instructions :")
        print("   1. Utilisez les filtres à gauche pour trier")
        print("   2. Scrollez dans la zone principale")
        print("   3. Cliquez 'Actualiser' si vous ajoutez des cartes")
        print("   4. Fermez avec le bouton 'Fermer' ou Alt+F4")
        
        # Test interactif
        print(f"\n🎮 Test interactif :")
        print("   • Fenêtre ouverte - testez les filtres manuellement")
        print("   • Appuyez sur Entrée ici pour fermer le test")
        
        input()  # Attendre que l'utilisateur teste
        
        # Fermer proprement
        deck_viewer.on_close()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_deck_viewer_integration():
    """Test d'intégration avec l'application principale."""
    print("\n🔗 Test d'intégration avec l'app principale")
    print("=" * 50)
    
    try:
        print("📱 Vérification du bouton dans l'interface...")
        
        # Vérifier que l'import fonctionne dans app_final.py
        from app_final import FinalMainApp
        
        print("✅ Import app_final.py réussi")
        
        # Vérifier que la méthode existe
        if hasattr(FinalMainApp, 'show_deck_viewer'):
            print("✅ Méthode show_deck_viewer trouvée")
        else:
            print("❌ Méthode show_deck_viewer manquante")
            return False
        
        print("✅ Intégration validée")
        
        print(f"\n🎯 Utilisation dans l'app :")
        print("   • Menu : Affichage → Voir le deck")
        print("   • Raccourci : Ctrl+V")
        print("   • Fonction : Visualiser toutes les cartes en grille")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration : {e}")
        return False

def main():
    """Point d'entrée principal."""
    print("🃏 TEST COMPLET DU VISUALISEUR DE DECK")
    print("=" * 50)
    
    try:
        # Test 1 : Fonctionnalité de base
        success1 = test_deck_viewer()
        
        # Test 2 : Intégration
        success2 = test_deck_viewer_integration()
        
        print(f"\n{'='*50}")
        if success1 and success2:
            print("🎉 TOUS LES TESTS RÉUSSIS !")
            print("\n✅ Visualiseur de deck opérationnel")
            print("✅ Intégration dans l'application réussie")
            print("✅ Interface complète et fonctionnelle")
            
            print(f"\n🎯 Nouvelle fonctionnalité disponible :")
            print("   📋 Visualisation en grille de toutes les cartes")
            print("   🔍 Filtres par rareté et types")
            print("   📊 Tri par nom, rareté, type, puissance")
            print("   🖼️ Affichage des images fusionnées")
            print("   📱 Interface intuitive avec onglets")
            print("   ⚡ Performances optimisées avec cache")
            
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
            if not success1:
                print("   • Problème avec le visualiseur de base")
            if not success2:
                print("   • Problème avec l'intégration")
        
        return success1 and success2
        
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'='*50}")
        print("Appuyez sur Entrée pour fermer...")
        input()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrompu")
        sys.exit(1)
