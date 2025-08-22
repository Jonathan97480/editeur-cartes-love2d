#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction automatique des chemins d'images fusionnées
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

def fix_fused_image_paths():
    """Corrige automatiquement les chemins des images fusionnées en base."""
    print("🔧 Correction automatique des chemins d'images fusionnées")
    print("=" * 60)
    
    try:
        from lib.database import CardRepo
        from lib.utils import ensure_images_subfolders, get_fused_card_image_path
        
        repo = CardRepo("cartes.db")
        cards = repo.list_cards()
        
        if not cards:
            print("   ⚠️ Aucune carte en base")
            return False
        
        subfolders = ensure_images_subfolders()
        cards_folder = subfolders['cards']
        
        print(f"📂 Vérification du dossier : {cards_folder}")
        
        fixed_count = 0
        already_correct = 0
        no_fusion = 0
        
        for card in cards:
            if not card.img:
                continue
            
            # Vérifier si la carte pointe déjà vers une image fusionnée
            if "cards/" in card.img or cards_folder in card.img:
                already_correct += 1
                print(f"   ✅ {card.name}: déjà correct ({os.path.basename(card.img)})")
                continue
            
            # Chercher une image fusionnée pour cette carte
            fused_path = get_fused_card_image_path(card.name)
            
            if fused_path and os.path.exists(fused_path):
                # Mettre à jour le chemin en base
                old_path = card.img
                card.img = fused_path.replace('\\', '/')
                repo.update(card)
                fixed_count += 1
                print(f"   🔧 {card.name}: {os.path.basename(old_path)} → {os.path.basename(fused_path)}")
            else:
                no_fusion += 1
                print(f"   ℹ️ {card.name}: pas d'image fusionnée trouvée")
        
        print(f"\n📊 Résultats de la correction :")
        print(f"   Cartes corrigées : {fixed_count}")
        print(f"   Déjà correctes : {already_correct}")
        print(f"   Sans fusion : {no_fusion}")
        print(f"   Total traité : {len(cards)}")
        
        if fixed_count > 0:
            print(f"\n🎉 {fixed_count} cartes ont été corrigées !")
            print("   Au prochain redémarrage, elles utiliseront les bonnes images.")
        elif already_correct > 0:
            print(f"\n✅ Toutes les cartes utilisent déjà les bonnes images")
        else:
            print(f"\n⚠️ Aucune image fusionnée trouvée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Point d'entrée principal."""
    try:
        print("🚀 CORRECTION AUTOMATIQUE DES IMAGES FUSIONNÉES")
        print("=" * 70)
        print("Ce script va corriger les chemins des images fusionnées en base de données.")
        print("Cela résout le problème : 'pas d'image' au redémarrage de l'application.")
        print("")
        
        success = fix_fused_image_paths()
        
        print(f"\n{'='*70}")
        if success:
            print("✅ Correction terminée avec succès !")
            print("\n📝 Que fait cette correction :")
            print("   • Détecte les cartes qui ont des images fusionnées sur disque")
            print("   • Met à jour leurs chemins en base pour pointer vers ces images")
            print("   • Résout le problème de 'pas d'image' au redémarrage")
            
            print("\n🔮 À l'avenir :")
            print("   • Les nouvelles cartes sauvegardées utiliseront automatiquement")
            print("     les bonnes images grâce à la correction dans le code")
        else:
            print("❌ Erreur lors de la correction")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'='*70}")
        print("Appuyez sur Entrée pour fermer...")
        input()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Correction interrompue")
        sys.exit(1)
