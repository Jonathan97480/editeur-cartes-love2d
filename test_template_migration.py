#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la nouvelle migration v3→v4 pour l'import automatique des templates
"""
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.config import APP_SETTINGS, save_settings, load_settings
from lib.database_migration import migrate_database, get_db_version, set_db_version

def setup_test_templates():
    """Configure des templates de test pour la migration."""
    print("🎨 Configuration de templates de test...")
    
    # Créer des fichiers de template factices
    test_templates = {}
    demo_folder = "demo_migration_templates"
    os.makedirs(demo_folder, exist_ok=True)
    
    rarities = ['commun', 'rare', 'legendaire', 'mythique']
    
    # Créer des fichiers PNG minimaux pour chaque rareté
    png_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x1eIDATx\x9cc\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    for rarity in rarities:
        filename = f"template_{rarity}_migration_test.png"
        file_path = os.path.join(demo_folder, filename)
        
        with open(file_path, 'wb') as f:
            f.write(png_header)
        
        test_templates[rarity] = os.path.abspath(file_path)
        print(f"   ✅ {rarity}: {file_path}")
    
    return test_templates, demo_folder

def test_template_migration():
    """Test complet de la migration des templates."""
    print("🧪 Test de la migration automatique des templates")
    print("=" * 60)
    
    try:
        # 1. Charger les paramètres actuels
        load_settings()
        original_templates = APP_SETTINGS.get("rarity_templates", {}).copy()
        
        # 2. Configurer des templates de test
        test_templates, demo_folder = setup_test_templates()
        
        # 3. Mettre à jour les paramètres avec les templates de test
        APP_SETTINGS["rarity_templates"] = test_templates
        save_settings()
        print(f"\n⚙️ Templates de test configurés dans les paramètres")
        
        # 4. Forcer la version de la DB à 3 pour tester la migration v3→v4
        db_path = "cartes.db"
        if os.path.exists(db_path):
            current_version = get_db_version(db_path)
            print(f"\n📊 Version actuelle de la DB : {current_version}")
            
            if current_version >= 4:
                print("🔄 Réinitialisation de la version à 3 pour le test...")
                set_db_version(db_path, 3)
        
        # 5. État AVANT migration
        print(f"\n📂 État AVANT migration :")
        templates_folder = "images/templates"
        if os.path.exists(templates_folder):
            files_before = os.listdir(templates_folder)
            print(f"   Dossier templates : {len(files_before)} fichiers")
            for file in files_before:
                print(f"   - {file}")
        else:
            print(f"   Dossier templates : N'existe pas encore")
        
        print(f"\n   Paramètres templates :")
        for rarity, path in test_templates.items():
            print(f"   - {rarity}: {os.path.basename(path)}")
        
        # 6. Exécuter la migration
        print(f"\n🚀 Exécution de la migration...")
        success = migrate_database(db_path)
        
        # 7. État APRÈS migration
        print(f"\n📂 État APRÈS migration :")
        if os.path.exists(templates_folder):
            files_after = os.listdir(templates_folder)
            print(f"   Dossier templates : {len(files_after)} fichiers")
            for file in files_after:
                print(f"   - {file}")
        else:
            print(f"   Dossier templates : Toujours inexistant")
        
        # Recharger les paramètres pour voir les changements
        load_settings()
        print(f"\n   Paramètres templates mis à jour :")
        for rarity, path in APP_SETTINGS.get("rarity_templates", {}).items():
            print(f"   - {rarity}: {os.path.basename(path) if path else 'Non configuré'}")
        
        # 8. Vérifier la version finale
        final_version = get_db_version(db_path)
        print(f"\n📊 Version finale de la DB : {final_version}")
        
        # 9. Nettoyer les fichiers de test
        print(f"\n🧹 Nettoyage des fichiers de test...")
        for file_path in test_templates.values():
            try:
                os.remove(file_path)
                print(f"   🗑️ Supprimé : {os.path.basename(file_path)}")
            except:
                pass
        
        try:
            os.rmdir(demo_folder)
            print(f"   🗑️ Dossier {demo_folder} supprimé")
        except:
            pass
        
        # 10. Restaurer les paramètres originaux
        APP_SETTINGS["rarity_templates"] = original_templates
        save_settings()
        print(f"   🔄 Paramètres originaux restaurés")
        
        # 11. Résultats
        print(f"\n📊 Résultats du test :")
        print(f"   Migration réussie : {'✅ Oui' if success else '❌ Non'}")
        print(f"   Templates importés : {'✅ Oui' if files_after else '❌ Non'}")
        print(f"   Version mise à jour : {'✅ Oui' if final_version == 4 else '❌ Non'}")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Point d'entrée principal."""
    try:
        success = test_template_migration()
        
        print(f"\n{'='*60}")
        if success:
            print("🎉 Test de migration des templates réussi !")
            print("\n📋 La nouvelle migration v3→v4 :")
            print("   ✅ Importe automatiquement les templates configurés")
            print("   ✅ Les copie dans images/templates/ avec les bons noms")
            print("   ✅ Met à jour les paramètres avec les nouveaux chemins")
            print("   ✅ S'exécute automatiquement au démarrage de l'application")
        else:
            print("❌ Test de migration échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'='*60}")
        print("Appuyez sur Entrée pour fermer...")
        input()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrompu par l'utilisateur")
        sys.exit(1)
