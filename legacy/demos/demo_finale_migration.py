#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration finale : Migration automatique des templates au démarrage
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.config import APP_SETTINGS, save_settings, load_settings
from lib.database_migration import set_db_version

def demo_migration_complete():
    """Démonstration complète du système de migration des templates."""
    print("🎯 DÉMONSTRATION FINALE : Migration automatique des templates")
    print("=" * 70)
    
    try:
        # 1. Simuler une situation réelle où un utilisateur a configuré des templates
        print("📋 SCÉNARIO : Un utilisateur a déjà configuré des templates dans les réglages")
        print("mais ils ne sont pas encore organisés dans le dossier images/templates/")
        
        # Créer des templates factices comme si l'utilisateur les avait configurés
        demo_folder = "user_templates"
        os.makedirs(demo_folder, exist_ok=True)
        
        png_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x1eIDATx\x9cc\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
        
        user_templates = {}
        for rarity in ['commun', 'rare', 'legendaire', 'mythique']:
            filename = f"mon_template_{rarity}.png"
            file_path = os.path.join(demo_folder, filename)
            
            with open(file_path, 'wb') as f:
                f.write(png_header)
            
            user_templates[rarity] = os.path.abspath(file_path)
            print(f"   📁 {rarity}: {filename} (configuré par l'utilisateur)")
        
        # 2. Configurer ces templates comme si l'utilisateur l'avait fait
        load_settings()
        original_templates = APP_SETTINGS.get("rarity_templates", {}).copy()
        
        APP_SETTINGS["rarity_templates"] = user_templates
        save_settings()
        
        print(f"\n💾 Templates configurés dans les paramètres (comme dans les réglages)")
        
        # 3. Simuler une base de données v3 (avant la migration)
        db_path = "cartes.db"
        if os.path.exists(db_path):
            set_db_version(db_path, 3)
            print(f"\n🔄 Base de données réinitialisée en version 3 (simule situation avant migration)")
        
        # 4. Vérifier l'état avant
        templates_folder = "images/templates"
        files_before = os.listdir(templates_folder) if os.path.exists(templates_folder) else []
        
        print(f"\n📂 ÉTAT AVANT le démarrage de l'application :")
        print(f"   Dossier templates : {len(files_before)} fichiers")
        if files_before:
            for file in files_before:
                print(f"   - {file}")
        else:
            print(f"   (vide - les templates sont configurés mais pas encore importés)")
        
        print(f"\n   Templates configurés par l'utilisateur :")
        for rarity, path in user_templates.items():
            print(f"   - {rarity}: {os.path.basename(path)}")
        
        # 5. Simuler le démarrage de l'application (qui déclenche la migration)
        print(f"\n🚀 DÉMARRAGE DE L'APPLICATION...")
        print(f"   (La migration v3→v4 va se déclencher automatiquement)")
        
        from lib.database import ensure_db
        ensure_db("cartes.db")  # Ceci déclenche la migration automatique
        
        # 6. Vérifier l'état après
        files_after = os.listdir(templates_folder) if os.path.exists(templates_folder) else []
        
        print(f"\n📂 ÉTAT APRÈS le démarrage :")
        print(f"   Dossier templates : {len(files_after)} fichiers")
        for file in files_after:
            print(f"   - {file}")
        
        # Recharger les paramètres pour voir les mises à jour
        load_settings()
        updated_templates = APP_SETTINGS.get("rarity_templates", {})
        
        print(f"\n   Paramètres mis à jour automatiquement :")
        for rarity, path in updated_templates.items():
            if path:
                print(f"   - {rarity}: {os.path.basename(path)} (maintenant dans images/templates/)")
        
        # 7. Validation
        success = len(files_after) == 4 and all(f"template_{r}.png" in files_after for r in ['commun', 'rare', 'legendaire', 'mythique'])
        
        print(f"\n🏆 RÉSULTAT :")
        if success:
            print(f"   ✅ SUCCÈS ! Migration automatique réussie")
            print(f"   ✅ {len(files_after)} templates automatiquement importés")
            print(f"   ✅ Paramètres mis à jour avec les nouveaux chemins")
            print(f"   ✅ L'utilisateur n'a rien eu à faire !")
        else:
            print(f"   ❌ Échec de la migration automatique")
        
        # 8. Nettoyer
        print(f"\n🧹 Nettoyage...")
        for file_path in user_templates.values():
            try:
                os.remove(file_path)
            except:
                pass
        
        try:
            os.rmdir(demo_folder)
        except:
            pass
        
        # Restaurer les paramètres
        APP_SETTINGS["rarity_templates"] = original_templates
        save_settings()
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Point d'entrée principal."""
    try:
        success = demo_migration_complete()
        
        print(f"\n{'='*70}")
        print(f"🎉 DÉMONSTRATION TERMINÉE")
        
        if success:
            print(f"\n✨ FONCTIONNALITÉ IMPLÉMENTÉE :")
            print(f"   📦 Migration automatique des templates (v3→v4)")
            print(f"   🔄 Déclenchée automatiquement au démarrage de l'application")
            print(f"   📁 Importe les templates configurés vers images/templates/")
            print(f"   📝 Met à jour automatiquement les paramètres")
            print(f"   🎯 Résout le problème 'dossier template reste vide'")
            
            print(f"\n🎮 UTILISATION POUR L'UTILISATEUR :")
            print(f"   1. Configurer les templates dans Réglages > Configuration des images")
            print(f"   2. Redémarrer l'application (ou attendre le prochain démarrage)")
            print(f"   3. Les templates sont automatiquement importés !")
            print(f"   4. Plus besoin de cliquer sur 'Organiser templates'")
        else:
            print(f"\n❌ La démonstration a échoué")
        
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
        print("\n❌ Démonstration interrompue par l'utilisateur")
        sys.exit(1)
