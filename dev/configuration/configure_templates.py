#!/usr/bin/env python3
"""
Script pour configurer et tester les templates de rareté.
"""

import os
import sys
import json

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_settings_file():
    """Vérifie le fichier settings.json."""
    print("🔍 Vérification du fichier settings.json")
    
    settings_file = "settings.json"
    
    if not os.path.exists(settings_file):
        print("❌ Fichier settings.json non trouvé")
        return None
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        print(f"✅ Fichier settings.json chargé")
        
        # Vérifier la section rarity_templates
        rarity_templates = settings.get("rarity_templates", {})
        print(f"📊 Templates de rareté : {len(rarity_templates)} configuré(s)")
        
        for rarity, path in rarity_templates.items():
            exists = "✅" if path and os.path.exists(path) else "❌"
            print(f"   {rarity:12} : {exists} {path}")
        
        # Vérifier le template par défaut
        default_template = settings.get("template_image", "")
        if default_template:
            exists = "✅" if os.path.exists(default_template) else "❌"
            print(f"   défaut       : {exists} {default_template}")
        
        return settings
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
        return None

def create_test_templates():
    """Crée des templates de test simples."""
    print(f"\n🎨 Création de templates de test")
    
    # Créer le dossier templates s'il n'existe pas
    templates_dir = "images/templates"
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"📁 Dossier créé : {templates_dir}")
    
    # Créer des fichiers de test simples (images 1x1 pixel PNG)
    rarities = ['commun', 'rare', 'legendaire', 'mythique']
    
    # Données d'un PNG 1x1 transparent minimal
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'
    
    created_templates = {}
    
    for rarity in rarities:
        template_path = os.path.join(templates_dir, f"template_{rarity}.png")
        
        if not os.path.exists(template_path):
            with open(template_path, 'wb') as f:
                f.write(png_data)
            print(f"✅ Template créé : {template_path}")
        else:
            print(f"📄 Template existe : {template_path}")
        
        created_templates[rarity] = template_path.replace('\\', '/')
    
    return created_templates

def update_settings_with_templates(templates):
    """Met à jour le fichier settings.json avec les templates."""
    print(f"\n⚙️ Mise à jour de settings.json")
    
    settings_file = "settings.json"
    
    # Charger les paramètres existants ou créer un nouveau fichier
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            print(f"✅ Paramètres existants chargés")
        except:
            settings = {}
            print(f"⚠️ Erreur lors du chargement, création de nouveaux paramètres")
    else:
        settings = {}
        print(f"📄 Création d'un nouveau fichier settings.json")
    
    # Mettre à jour la section rarity_templates
    settings["rarity_templates"] = templates
    
    # Sauvegarder
    try:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        print(f"✅ Fichier settings.json mis à jour")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        return False

def test_template_usage():
    """Teste l'utilisation des templates configurés."""
    print(f"\n🧪 Test de l'utilisation des templates")
    
    try:
        from lib.config import APP_SETTINGS
        from lib.utils import create_card_image
        
        # Recharger les paramètres
        import importlib
        from lib import config
        importlib.reload(config)
        
        rarity_templates = config.APP_SETTINGS.get("rarity_templates", {})
        
        if not rarity_templates:
            print("❌ Aucun template trouvé après mise à jour")
            return False
        
        print(f"✅ {len(rarity_templates)} template(s) disponible(s)")
        
        # Trouver une image de carte existante pour tester
        cards_dir = "images/cards"
        if os.path.exists(cards_dir):
            card_files = [f for f in os.listdir(cards_dir) if f.endswith('.png')]
            if card_files:
                test_card = os.path.join(cards_dir, card_files[0])
                print(f"🃏 Image de test : {test_card}")
                
                # Tester chaque template
                for rarity, template_path in rarity_templates.items():
                    if os.path.exists(template_path):
                        print(f"   Testing {rarity} template...")
                        # Test rapide sans créer de fichier
                        try:
                            result = create_card_image(test_card, template_path, f"test_{rarity}")
                            if result:
                                print(f"   ✅ Template {rarity} fonctionne")
                                # Nettoyer le fichier de test
                                if os.path.exists(result):
                                    os.remove(result)
                            else:
                                print(f"   ❌ Template {rarity} échoue")
                        except Exception as e:
                            print(f"   ❌ Erreur avec template {rarity} : {e}")
                    else:
                        print(f"   ❌ Template {rarity} manquant : {template_path}")
            else:
                print("⚠️ Aucune image de carte trouvée pour tester")
        else:
            print("⚠️ Dossier images/cards non trouvé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False

if __name__ == "__main__":
    print("🎨 Configuration des templates de rareté\n")
    
    # Vérifier l'état actuel
    current_settings = check_settings_file()
    
    # Créer des templates de test
    templates = create_test_templates()
    
    # Mettre à jour la configuration
    if update_settings_with_templates(templates):
        # Tester les templates
        if test_template_usage():
            print(f"\n✅ Configuration des templates terminée avec succès !")
            print(f"\n💡 Maintenant vous pouvez :")
            print(f"1. Remplacer les templates de test par vos vraies images")
            print(f"2. Tester le changement de rareté dans l'application")
            print(f"3. Observer la génération d'images fusionnées différentes selon la rareté")
        else:
            print(f"\n⚠️ Configuration terminée mais tests échoués")
    else:
        print(f"\n❌ Échec de la configuration")
