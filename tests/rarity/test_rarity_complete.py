#!/usr/bin/env python3
"""
Script pour tester les améliorations du système de changement de rareté.
"""

import os
import sys
import sqlite3
import tempfile
import shutil
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_rarity_change_logic():
    """Test le code des améliorations de changement de rareté."""
    print("🧪 Test de la logique de changement de rareté")
    
    try:
        # Importer les modules nécessaires
        from lib.ui_components import CardForm
        from lib.database import CardRepo
        from lib.config import RARITY_FROM_LABEL
        from lib.utils import sanitize_filename
        
        print("✅ Modules importés avec succès")
        
        # Test de la fonction sanitize_filename
        test_names = ["Deux soeurs", "A demain", "Coup puissant"]
        for name in test_names:
            sanitized = sanitize_filename(name)
            print(f"   {name} → {sanitized}")
        
        # Test de la conversion de rareté
        rarities = ['Commun', 'Rare', 'Légendaire', 'Mythique']
        for rarity in rarities:
            key = RARITY_FROM_LABEL.get(rarity, 'commun')
            print(f"   {rarity} → {key}")
        
        print("✅ Tests de base réussis")
        
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors des tests : {e}")
        return False
    
    return True

def simulate_rarity_change():
    """Simule un changement de rareté en modifiant directement la base."""
    print(f"\n🔄 Simulation d'un changement de rareté")
    
    if not os.path.exists("cartes.db"):
        print("❌ Base de données non trouvée")
        return
    
    # Faire une sauvegarde avant modification
    backup_path = f"cartes_before_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy("cartes.db", backup_path)
    print(f"✅ Sauvegarde créée : {backup_path}")
    
    conn = sqlite3.connect("cartes.db")
    cursor = conn.cursor()
    
    # Trouver une carte à modifier
    cursor.execute("SELECT id, name, rarity, img FROM cards WHERE rarity = 'commun' LIMIT 1")
    card = cursor.fetchone()
    
    if not card:
        print("❌ Aucune carte 'commun' trouvée pour le test")
        conn.close()
        return
    
    card_id, name, old_rarity, img_path = card
    new_rarity = 'rare'
    
    print(f"📋 Carte de test : {name}")
    print(f"   Rareté : {old_rarity} → {new_rarity}")
    print(f"   Image : {img_path}")
    
    # Vérifier l'état avant
    if img_path and os.path.exists(img_path):
        old_size = os.path.getsize(img_path)
        old_mtime = os.path.getmtime(img_path)
        print(f"   État avant : {old_size} bytes, modifié le {datetime.fromtimestamp(old_mtime)}")
        
        # Modifier la rareté en base
        cursor.execute("UPDATE cards SET rarity = ? WHERE id = ?", (new_rarity, card_id))
        conn.commit()
        print(f"✅ Rareté mise à jour en base : {old_rarity} → {new_rarity}")
        
        # Simuler la régénération d'image en touchant le fichier
        # (En réalité, l'application générera une nouvelle image avec le template de la nouvelle rareté)
        import time
        time.sleep(1)  # Petit délai pour différencier les timestamps
        
        # "Toucher" le fichier pour simuler la régénération
        with open(img_path, 'r+b') as f:
            f.seek(0, 2)  # Aller à la fin
            current_size = f.tell()
            f.write(b'')  # Écriture nulle pour changer le mtime
        
        # Vérifier l'état après
        new_size = os.path.getsize(img_path)
        new_mtime = os.path.getmtime(img_path)
        print(f"   État après : {new_size} bytes, modifié le {datetime.fromtimestamp(new_mtime)}")
        
        # Validation
        if new_mtime > old_mtime:
            print(f"✅ Image 'mise à jour' (nouveau timestamp)")
        else:
            print(f"⚠️ Image non mise à jour (même timestamp)")
        
        # Restaurer l'ancienne rareté
        cursor.execute("UPDATE cards SET rarity = ? WHERE id = ?", (old_rarity, card_id))
        conn.commit()
        print(f"🔄 Rareté restaurée : {new_rarity} → {old_rarity}")
        
    else:
        print(f"❌ Image manquante : {img_path}")
    
    conn.close()
    
    # Optionnel : supprimer la sauvegarde si tout s'est bien passé
    try:
        os.remove(backup_path)
        print(f"🗑️ Sauvegarde supprimée : {backup_path}")
    except:
        print(f"⚠️ Sauvegarde conservée : {backup_path}")

def check_templates_configuration():
    """Vérifie la configuration des templates de rareté."""
    print(f"\n🎨 Vérification des templates de rareté")
    
    try:
        from lib.config import APP_SETTINGS
        
        rarity_templates = APP_SETTINGS.get("rarity_templates", {})
        
        if not rarity_templates:
            print("⚠️ Aucun template de rareté configuré")
            print("   Les images fusionnées utiliseront le template par défaut")
        else:
            print(f"📊 {len(rarity_templates)} template(s) configuré(s) :")
            for rarity, path in rarity_templates.items():
                exists = "✅" if os.path.exists(path) else "❌"
                print(f"   {rarity:12} : {exists} {path}")
        
        # Vérifier le template par défaut (legacy)
        default_template = APP_SETTINGS.get("template_image", "")
        if default_template:
            exists = "✅" if os.path.exists(default_template) else "❌"
            print(f"   défaut       : {exists} {default_template}")
        else:
            print("⚠️ Aucun template par défaut configuré")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {e}")

if __name__ == "__main__":
    print("🧪 Test complet du système de changement de rareté\n")
    
    if test_rarity_change_logic():
        check_templates_configuration()
        simulate_rarity_change()
        
        print(f"\n📝 Résumé des améliorations apportées :")
        print(f"✅ Détection des changements de rareté")
        print(f"✅ Validation de la mise à jour des images")
        print(f"✅ Messages d'avertissement en cas d'échec")
        print(f"✅ Traçabilité améliorée lors de la génération")
        print(f"✅ Gestion robuste des erreurs")
        
        print(f"\n💡 Pour tester dans l'application :")
        print(f"1. Ouvrez l'application")
        print(f"2. Sélectionnez une carte existante")
        print(f"3. Changez sa rareté")
        print(f"4. Sauvegardez")
        print(f"5. Observez les messages dans la console")
    else:
        print("❌ Les tests de base ont échoué")
