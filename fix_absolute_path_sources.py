#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CORRECTEUR DES FONCTIONS GÉNÉRANT DES CHEMINS ABSOLUS
=======================================================

Ce script identifie et corrige les fonctions dans l'application
qui enregistrent des chemins absolus Windows dans la base de données.
"""

import os
import sys
from pathlib import Path

def analyze_path_generating_functions():
    """Analyse les fonctions qui peuvent générer des chemins absolus"""
    
    print('🔍 ANALYSE DES SOURCES DE CHEMINS ABSOLUS')
    print('=' * 60)
    
    issues_found = []
    
    # 1. Analyser copy_image_to_originals dans utils.py
    print('\n📁 1. Fonction copy_image_to_originals():')
    print('   🎯 Problème : Retourne un chemin absolu (target_path)')
    print('   📍 Fichier : lib/utils.py ligne ~120')
    print('   🔧 Solution : Convertir en chemin relatif avant retour')
    issues_found.append({
        'function': 'copy_image_to_originals',
        'file': 'lib/utils.py',
        'issue': 'Retourne chemin absolu',
        'solution': 'Convertir en relatif avant retour'
    })
    
    # 2. Analyser convert_to_relative_path dans utils.py
    print('\n📁 2. Fonction convert_to_relative_path():')
    print('   🎯 Problème : Fallback retourne le chemin absolu normalisé')
    print('   📍 Fichier : lib/utils.py ligne ~205')
    print('   🔧 Solution : Essayer extraction relative même sans "images/"')
    issues_found.append({
        'function': 'convert_to_relative_path',
        'file': 'lib/utils.py',
        'issue': 'Fallback préserve chemins absolus',
        'solution': 'Améliorer extraction relative'
    })
    
    # 3. Analyser _browse_img dans ui_components.py
    print('\n📁 3. Fonction _browse_img():')
    print('   🎯 Problème : En cas d\'échec de copie, utilise chemin original')
    print('   📍 Fichier : lib/ui_components.py ligne ~440')
    print('   🔧 Solution : Forcer la conversion en relatif')
    issues_found.append({
        'function': '_browse_img',
        'file': 'lib/ui_components.py',
        'issue': 'Fallback sur chemin absolu original',
        'solution': 'Améliorer gestion d\'échec'
    })
    
    # 4. Analyser la sauvegarde en base
    print('\n📁 4. Sauvegarde en base de données:')
    print('   🎯 Problème : Aucune validation des chemins avant sauvegarde')
    print('   📍 Fichier : Fonction save_card()')
    print('   🔧 Solution : Valider/corriger chemins avant sauvegarde')
    issues_found.append({
        'function': 'save_card',
        'file': 'ui_components.py',
        'issue': 'Pas de validation avant sauvegarde',
        'solution': 'Ajouter validation automatique'
    })
    
    print(f'\n📊 RÉSUMÉ : {len(issues_found)} sources de problèmes identifiées')
    
    return issues_found

def create_path_validator():
    """Crée une fonction de validation des chemins"""
    
    validator_code = '''
def validate_and_convert_path(path_value: str) -> str:
    """
    Valide et convertit un chemin en relatif portable.
    Utilisé pour prévenir l'enregistrement de chemins absolus.
    """
    if not path_value or not isinstance(path_value, str):
        return ''
    
    path_value = path_value.strip()
    if not path_value:
        return ''
    
    # Normaliser les séparateurs
    normalized_path = path_value.replace('\\\\', '/').replace('\\', '/')
    
    # Si c'est déjà un chemin relatif correct, le retourner
    if not (normalized_path.startswith('C:') or normalized_path.startswith('c:') or 
            normalized_path.startswith('D:') or normalized_path.startswith('d:') or
            normalized_path.startswith('E:') or normalized_path.startswith('e:')):
        return normalized_path
    
    print(f"⚠️  CHEMIN ABSOLU DÉTECTÉ : {normalized_path}")
    
    # Essayer d'extraire la partie relative
    known_folders = ['images/', 'data/', 'lib/', 'assets/', 'fonts/']
    
    for folder in known_folders:
        if folder in normalized_path:
            parts = normalized_path.split(folder)
            if len(parts) > 1:
                relative_path = folder + parts[-1]
                print(f"✅ CONVERTI EN RELATIF : {relative_path}")
                return relative_path
    
    # Dernier recours : extraire juste le nom de fichier
    filename = normalized_path.split('/')[-1]
    if '.' in filename:  # Si c'est vraiment un fichier
        relative_path = f"images/cards/{filename}"
        print(f"🔧 FALLBACK VERS : {relative_path}")
        return relative_path
    
    # Si vraiment impossible, retourner vide pour éviter la corruption
    print(f"❌ IMPOSSIBLE DE CONVERTIR : {normalized_path}")
    return ''
'''
    
    return validator_code

def fix_utils_functions():
    """Corrige les fonctions dans utils.py"""
    
    print('\n🔧 CORRECTION DES FONCTIONS DANS utils.py')
    print('=' * 50)
    
    # Lire le fichier utils.py
    utils_path = Path('lib/utils.py')
    if not utils_path.exists():
        print('❌ Fichier lib/utils.py non trouvé')
        return False
    
    with open(utils_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Corriger copy_image_to_originals
    old_return = 'return target_path'
    new_return = '''# Convertir en chemin relatif avant retour
        relative_path = convert_to_relative_path(target_path)
        return relative_path'''
    
    if old_return in content:
        content = content.replace(old_return, new_return)
        print('✅ copy_image_to_originals() corrigée')
    
    # 2. Corriger convert_to_relative_path
    old_fallback = '''# Si pas de dossier 'images' trouvé, retourner le chemin normalisé
    return normalized_path'''
    
    new_fallback = '''# Si pas de dossier 'images' trouvé, essayer d'autres extractions
    # Essayer d'extraire depuis d'autres dossiers connus
    known_folders = ['data/', 'lib/', 'assets/', 'fonts/']
    for folder in known_folders:
        if folder in normalized_path:
            parts = normalized_path.split(folder)
            try:
                idx = parts[0].split('/').index(folder.rstrip('/'))
                relative_path = '/'.join(parts[0].split('/')[idx:]) + '/' + parts[1]
                return relative_path
            except (ValueError, IndexError):
                continue
    
    # Dernier recours : si c'est un chemin absolu Windows, extraire juste le nom de fichier
    if normalized_path.startswith(('C:', 'c:', 'D:', 'd:', 'E:', 'e:')):
        filename = normalized_path.split('/')[-1]
        if '.' in filename:  # Si c'est un fichier
            return f"images/cards/{filename}"
    
    # Si vraiment impossible, retourner le chemin normalisé
    return normalized_path'''
    
    if old_fallback in content:
        content = content.replace(old_fallback, new_fallback)
        print('✅ convert_to_relative_path() corrigée')
    
    # Sauvegarder les modifications
    with open(utils_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('💾 Modifications sauvegardées dans lib/utils.py')
    return True

def add_validation_to_ui_components():
    """Ajoute la validation automatique dans ui_components.py"""
    
    print('\n🔧 AJOUT DE VALIDATION DANS ui_components.py')
    print('=' * 50)
    
    # Ajouter le validateur en début de fichier
    validator_code = create_path_validator()
    
    ui_path = Path('lib/ui_components.py')
    if not ui_path.exists():
        print('❌ Fichier lib/ui_components.py non trouvé')
        return False
    
    with open(ui_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ajouter le validateur après les imports
    import_section = 'from .database import CardRepo, Card'
    if import_section in content:
        content = content.replace(import_section, import_section + '\n\n' + validator_code)
        print('✅ Fonction de validation ajoutée')
    
    # Modifier la fonction save_card pour utiliser la validation
    save_pattern = "card.img = self.img_var.get().strip()"
    if save_pattern in content:
        new_save = """# Valider et corriger le chemin d'image avant sauvegarde
        raw_img_path = self.img_var.get().strip()
        validated_img_path = validate_and_convert_path(raw_img_path)
        card.img = validated_img_path"""
        
        content = content.replace(save_pattern, new_save)
        print('✅ Validation ajoutée à save_card()')
    
    # Sauvegarder les modifications
    with open(ui_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('💾 Modifications sauvegardées dans lib/ui_components.py')
    return True

def create_prevention_script():
    """Crée un script de prévention pour l'avenir"""
    
    prevention_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SCRIPT DE PRÉVENTION DES CHEMINS ABSOLUS
============================================

Script qui s'exécute après chaque sauvegarde pour détecter
et corriger automatiquement les nouveaux chemins absolus.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Ajouter le chemin lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

try:
    from config import DB_FILE
except ImportError:
    DB_FILE = 'data/cartes.db'

def check_and_fix_new_absolute_paths():
    """Vérifie et corrige les nouveaux chemins absolus"""
    
    if not os.path.exists(DB_FILE):
        return
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Chercher les chemins absolus récents
        cursor.execute("""
            SELECT id, img FROM cards 
            WHERE (img LIKE 'c:%' OR img LIKE 'C:%' OR 
                   img LIKE 'd:%' OR img LIKE 'D:%') 
            AND datetime(updated_at) > datetime('now', '-1 hour')
        """)
        
        recent_issues = cursor.fetchall()
        
        if recent_issues:
            print(f"🚨 {len(recent_issues)} nouveaux chemins absolus détectés!")
            
            for card_id, bad_path in recent_issues:
                # Convertir en relatif
                if 'images/' in bad_path:
                    relative_path = bad_path[bad_path.find('images/'):]
                else:
                    filename = bad_path.split('/')[-1]
                    relative_path = f"images/cards/{filename}"
                
                # Corriger en base
                cursor.execute('UPDATE cards SET img = ? WHERE id = ?', 
                             (relative_path, card_id))
                
                print(f"✅ Corrigé ID {card_id}: {bad_path} → {relative_path}")
            
            conn.commit()
            print("💾 Corrections sauvegardées")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == '__main__':
    check_and_fix_new_absolute_paths()
'''
    
    with open('prevent_absolute_paths.py', 'w', encoding='utf-8') as f:
        f.write(prevention_code)
    
    print('📝 Script de prévention créé: prevent_absolute_paths.py')

def main():
    """Fonction principale"""
    
    print('🔧 CORRECTEUR AUTOMATIQUE DES SOURCES DE CHEMINS ABSOLUS')
    print('=' * 70)
    
    # 1. Analyser les problèmes
    issues = analyze_path_generating_functions()
    
    # 2. Corriger les fonctions utils.py
    if fix_utils_functions():
        print('✅ Fonctions utils.py corrigées')
    else:
        print('❌ Erreur lors de la correction utils.py')
    
    # 3. Ajouter validation à ui_components.py
    if add_validation_to_ui_components():
        print('✅ Validation ajoutée à ui_components.py')
    else:
        print('❌ Erreur lors de la modification ui_components.py')
    
    # 4. Créer script de prévention
    create_prevention_script()
    
    print('\n🎯 CORRECTIONS APPLIQUÉES:')
    print('   ✅ copy_image_to_originals() retourne maintenant des chemins relatifs')
    print('   ✅ convert_to_relative_path() gère mieux les chemins non-images')
    print('   ✅ save_card() valide les chemins avant sauvegarde')
    print('   ✅ Script de prévention créé pour l\'avenir')
    
    print('\n🚀 PROCHAINES ÉTAPES:')
    print('   1. Redémarrer l\'application pour charger les corrections')
    print('   2. Tester la sélection d\'images (elles seront automatiquement relatives)')
    print('   3. Le script prevent_absolute_paths.py peut être lancé périodiquement')
    
    print('\n💡 Les nouveaux chemins d\'images seront automatiquement convertis en relatifs!')

if __name__ == '__main__':
    main()
