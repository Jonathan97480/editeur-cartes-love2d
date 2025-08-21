#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test réel du système d'export avec les cartes existantes
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

def test_real_export():
    """Test avec les vraies cartes de la base de données."""
    print("🧪 Test d'export Lua avec les vraies cartes")
    print("=" * 50)
    
    try:
        from lib.utils import get_card_image_for_export
        from lib.database import CardRepo
        
        # Récupérer une carte réelle de la base
        repo = CardRepo("cartes.db")
        cards = repo.list_cards()
        
        if not cards:
            print("   ⚠️ Aucune carte dans la base de données")
            return False
        
        # Prendre la première carte
        card = cards[0]
        print(f"   Carte test : {card.name}")
        print(f"   Image originale : {card.img}")
        
        # Test d'export
        export_path = get_card_image_for_export(card)
        print(f"   Image pour export : {export_path}")
        
        # Vérifier si c'est une image fusionnée ou originale
        if "cards/" in export_path:
            print("   ✅ Export utilise une image du dossier cards/ (priorité correcte)")
            return True
        elif export_path == card.img:
            print("   ✅ Export utilise l'image originale (normal, pas d'alternative)")
            return True
        else:
            print(f"   ❌ Chemin d'export inattendu")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fusion_detection():
    """Test la détection des images fusionnées."""
    print("\n🧪 Test de détection d'images fusionnées")
    print("=" * 50)
    
    try:
        cards_folder = "images/cards"
        if not os.path.exists(cards_folder):
            print("   ⚠️ Dossier cards non trouvé")
            return False
        
        files = os.listdir(cards_folder)
        fused_files = [f for f in files if "_fused" in f]
        
        print(f"   Fichiers dans cards/ : {len(files)}")
        print(f"   Images fusionnées : {len(fused_files)}")
        
        for fused in fused_files:
            print(f"   - {fused}")
        
        if fused_files:
            print("   ✅ Images fusionnées détectées")
            
            # Test avec une vraie image fusionnée
            from lib.utils import get_card_image_for_export
            
            class MockCard:
                def __init__(self, name, img):
                    self.name = name
                    self.img = img
            
            # Utiliser le nom de la première image fusionnée
            fused_name = fused_files[0].replace("_fused.png", "")
            test_card = MockCard(fused_name, f"images/originals/{fused_name}.png")
            
            export_path = get_card_image_for_export(test_card)
            
            if "_fused" in export_path:
                print(f"   ✅ Export priorité correcte : {os.path.basename(export_path)}")
                return True
            else:
                print(f"   ❌ Export ne privilégie pas l'image fusionnée")
                return False
        else:
            print("   ℹ️  Aucune image fusionnée (normal si pas de fusion effectuée)")
            return True
        
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Test complet."""
    print("🔍 TEST RÉEL DU SYSTÈME D'EXPORT")
    print("=" * 60)
    
    test1 = test_real_export()
    test2 = test_fusion_detection()
    
    print(f"\n{'='*60}")
    print("📊 RÉSULTATS")
    print(f"{'='*60}")
    
    if test1 and test2:
        print("✅ Système d'export Lua fonctionnel")
        print("   → Utilise intelligemment les images fusionnées quand disponibles")
        print("   → Fallback sur les images originales sinon")
    else:
        print("⚠️ Problèmes détectés dans le système d'export")
    
    return test1 and test2

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'='*60}")
        print("Appuyez sur Entrée pour fermer...")
        input()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrompu")
        sys.exit(1)
