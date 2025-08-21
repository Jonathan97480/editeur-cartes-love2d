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
            print(f"   📁 {rarity}: {filename} (configuré par l'utilisateur)")\n        \n        # 2. Configurer ces templates comme si l'utilisateur l'avait fait\n        load_settings()\n        original_templates = APP_SETTINGS.get(\"rarity_templates\", {}).copy()\n        \n        APP_SETTINGS[\"rarity_templates\"] = user_templates\n        save_settings()\n        \n        print(f\"\\n💾 Templates configurés dans les paramètres (comme dans les réglages)\")\n        \n        # 3. Simuler une base de données v3 (avant la migration)\n        db_path = \"cartes.db\"\n        if os.path.exists(db_path):\n            set_db_version(db_path, 3)\n            print(f\"\\n🔄 Base de données réinitialisée en version 3 (simule situation avant migration)\")\n        \n        # 4. Vérifier l'état avant\n        templates_folder = \"images/templates\"\n        files_before = os.listdir(templates_folder) if os.path.exists(templates_folder) else []\n        \n        print(f\"\\n📂 ÉTAT AVANT le démarrage de l'application :\")\n        print(f\"   Dossier templates : {len(files_before)} fichiers\")\n        if files_before:\n            for file in files_before:\n                print(f\"   - {file}\")\n        else:\n            print(f\"   (vide - les templates sont configurés mais pas encore importés)\")\n        \n        print(f\"\\n   Templates configurés par l'utilisateur :\")\n        for rarity, path in user_templates.items():\n            print(f\"   - {rarity}: {os.path.basename(path)}\")\n        \n        # 5. Simuler le démarrage de l'application (qui déclenche la migration)\n        print(f\"\\n🚀 DÉMARRAGE DE L'APPLICATION...\")\n        print(f\"   (La migration v3→v4 va se déclencher automatiquement)\")\n        \n        from lib.database import ensure_db\n        ensure_db()  # Ceci déclenche la migration automatique\n        \n        # 6. Vérifier l'état après\n        files_after = os.listdir(templates_folder) if os.path.exists(templates_folder) else []\n        \n        print(f\"\\n📂 ÉTAT APRÈS le démarrage :\")\n        print(f\"   Dossier templates : {len(files_after)} fichiers\")\n        for file in files_after:\n            print(f\"   - {file}\")\n        \n        # Recharger les paramètres pour voir les mises à jour\n        load_settings()\n        updated_templates = APP_SETTINGS.get(\"rarity_templates\", {})\n        \n        print(f\"\\n   Paramètres mis à jour automatiquement :\")\n        for rarity, path in updated_templates.items():\n            if path:\n                print(f\"   - {rarity}: {os.path.basename(path)} (maintenant dans images/templates/)\")\n        \n        # 7. Validation\n        success = len(files_after) == 4 and all(f\"template_{r}.png\" in files_after for r in ['commun', 'rare', 'legendaire', 'mythique'])\n        \n        print(f\"\\n🏆 RÉSULTAT :\")\n        if success:\n            print(f\"   ✅ SUCCÈS ! Migration automatique réussie\")\n            print(f\"   ✅ {len(files_after)} templates automatiquement importés\")\n            print(f\"   ✅ Paramètres mis à jour avec les nouveaux chemins\")\n            print(f\"   ✅ L'utilisateur n'a rien eu à faire !\")\n        else:\n            print(f\"   ❌ Échec de la migration automatique\")\n        \n        # 8. Nettoyer\n        print(f\"\\n🧹 Nettoyage...\")\n        for file_path in user_templates.values():\n            try:\n                os.remove(file_path)\n            except:\n                pass\n        \n        try:\n            os.rmdir(demo_folder)\n        except:\n            pass\n        \n        # Restaurer les paramètres\n        APP_SETTINGS[\"rarity_templates\"] = original_templates\n        save_settings()\n        \n        return success\n        \n    except Exception as e:\n        print(f\"❌ Erreur lors de la démonstration : {e}\")\n        import traceback\n        traceback.print_exc()\n        return False\n\ndef main():\n    \"\"\"Point d'entrée principal.\"\"\"\n    try:\n        success = demo_migration_complete()\n        \n        print(f\"\\n{'='*70}\")\n        print(f\"🎉 DÉMONSTRATION TERMINÉE\")\n        \n        if success:\n            print(f\"\\n✨ FONCTIONNALITÉ IMPLÉMENTÉE :\")\n            print(f\"   📦 Migration automatique des templates (v3→v4)\")\n            print(f\"   🔄 Déclenchée automatiquement au démarrage de l'application\")\n            print(f\"   📁 Importe les templates configurés vers images/templates/\")\n            print(f\"   📝 Met à jour automatiquement les paramètres\")\n            print(f\"   🎯 Résout le problème 'dossier template reste vide'\")\n            \n            print(f\"\\n🎮 UTILISATION POUR L'UTILISATEUR :\")\n            print(f\"   1. Configurer les templates dans Réglages > Configuration des images\")\n            print(f\"   2. Redémarrer l'application (ou attendre le prochain démarrage)\")\n            print(f\"   3. Les templates sont automatiquement importés !\")\n            print(f\"   4. Plus besoin de cliquer sur 'Organiser templates'\")\n        else:\n            print(f\"\\n❌ La démonstration a échoué\")\n        \n        return success\n        \n    except Exception as e:\n        print(f\"❌ Erreur inattendue : {e}\")\n        import traceback\n        traceback.print_exc()\n        return False\n\nif __name__ == \"__main__\":\n    try:\n        success = main()\n        print(f\"\\n{'='*70}\")\n        print(\"Appuyez sur Entrée pour fermer...\")\n        input()\n        sys.exit(0 if success else 1)\n    except KeyboardInterrupt:\n        print(\"\\n❌ Démonstration interrompue par l'utilisateur\")\n        sys.exit(1)
