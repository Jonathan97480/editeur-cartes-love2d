#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

🔍 TEST D'INTÉGRITÉ DES FICHIERS LUA EXPORTÉS
============================================

Ce script vérifie l'intégrité syntaxique et logique des fichiers Lua
générés par l'export, et identifie les erreurs potentielles.
"""
# Configurer l'environnement de test
from test_utils import setup_test_environment
setup_test_environment()


import os
import re
import sys
from pathlib import Path

def check_lua_syntax_issues(file_path):
    """Vérifie les problèmes de syntaxe Lua communs."""

    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Vérifications syntaxiques
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # 1. Virgules en fin de table (erreur commune)
            if line_stripped.endswith('),') and not line_stripped.endswith('})') and not line_stripped.endswith('},'):
                issues.append(f"Ligne {i}: Virgule après parenthèse fermante - '{line_stripped}'")
            
            # 2. Accolades mal fermées
            if '{' in line and '}' in line:
                open_count = line.count('{')
                close_count = line.count('}')
                if open_count != close_count and not line_stripped.endswith(','):
                    issues.append(f"Ligne {i}: Déséquilibre accolades - '{line_stripped}'")
            
            # 3. Chemins Windows non échappés (problème potentiel)
            if '\\' in line and not '\\\\' in line:
                issues.append(f"Ligne {i}: Chemin Windows non échappé - '{line_stripped}'")
            
            # 4. Caractères non-ASCII problématiques
            try:
                line.encode('ascii')
            except UnicodeEncodeError:
                # Vérifier si c'est dans une chaîne
                if "'" in line or '"' in line:
                    issues.append(f"Ligne {i}: Caractères non-ASCII dans chaîne - '{line_stripped}'")
        
        # 5. Vérification globale des parenthèses/accolades
        open_parens = content.count('(')
        close_parens = content.count(')')
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        if open_parens != close_parens:
            issues.append(f"Déséquilibre parenthèses: {open_parens} ouvertes, {close_parens} fermées")
        
        if open_braces != close_braces:
            issues.append(f"Déséquilibre accolades: {open_braces} ouvertes, {close_braces} fermées")
        
        return issues
        
    except Exception as e:
        return [f"Erreur lecture fichier: {e}"]

def check_lua_structure(file_path):
    """Vérifie la structure logique du fichier Lua."""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Vérifier la structure de base
        if 'local Cards = {' not in content:
            issues.append("Structure de base manquante: 'local Cards = {'")
        
        if 'return Cards' not in content:
            issues.append("Instruction de retour manquante: 'return Cards'")
        
        # 2. Vérifier les champs obligatoires des cartes
        card_pattern = r'{\s*name\s*='
        cards_found = re.findall(card_pattern, content)
        
        if cards_found:
            # Vérifier chaque carte
            required_fields = ['name', 'ImgIlustration', 'Description', 'PowerBlow', 'Rarete', 'Type', 'Effect']
            
            for field in required_fields:
                if content.count(field + ' =') < len(cards_found):
                    issues.append(f"Champ manquant dans certaines cartes: '{field}'")
        
        # 3. Vérifier les types de données
        if 'Type = {' in content:
            # Vérifier que les types sont des chaînes
            type_matches = re.findall(r"Type = \{([^}]+)\}", content)
            for match in type_matches:
                if not all("'" in item or '"' in item for item in match.split(',')):
                    issues.append(f"Types non-string détectés: {match}")
        
        return issues
        
    except Exception as e:
        return [f"Erreur analyse structure: {e}"]

def test_lua_with_love2d_syntax(file_path):
    """Teste la compatibilité Love2D spécifique."""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Chemins de fichiers
        img_matches = re.findall(r"ImgIlustration = '([^']+)'", content)
        for img_path in img_matches:
            # Vérifier que le chemin est relatif pour Love2D
            if os.path.isabs(img_path):
                issues.append(f"Chemin absolu détecté (devrait être relatif): {img_path}")
            
            # Vérifier l'existence du fichier
            if os.path.isabs(img_path) and not os.path.exists(img_path):
                issues.append(f"Fichier image introuvable: {img_path}")
        
        # 2. Fonctions vides
        if 'action = function() end' in content:
            issues.append("Fonctions d'action vides détectées (normal mais à noter)")
        
        return issues
        
    except Exception as e:
        return [f"Erreur test Love2D: {e}"]

def fix_common_lua_issues(file_path):
    """Corrige automatiquement les erreurs communes."""
    backup_path = file_path + '.backup'
    fixes_applied = []
    
    try:
        # Créer une sauvegarde
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        original_content = content
        
        # Fix 1: Retirer les virgules après les parenthèses fermantes
        pattern1 = r'\),(\s*\n)'
        if re.search(pattern1, content):
            content = re.sub(pattern1, r')\1', content)
            fixes_applied.append("Virgules après parenthèses fermantes supprimées")
        
        # Fix 2: Convertir chemins absolus en relatifs
        def convert_path(match):
            full_path = match.group(1)
            if 'images' in full_path:
                # Extraire la partie relative depuis 'images'
                parts = full_path.split('/')
                if 'images' in parts:
                    idx = parts.index('images')
                    relative_path = '/'.join(parts[idx:])
                    return f"ImgIlustration = '{relative_path}'"
            return match.group(0)
        
        new_content = re.sub(r"ImgIlustration = '([^']+)'", convert_path, content)
        if new_content != content:
            content = new_content
            fixes_applied.append("Chemins absolus convertis en relatifs")
        
        # Sauvegarder les corrections
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return fixes_applied
        
    except Exception as e:
        return [f"Erreur lors des corrections: {e}"]

def test_lua_file_integrity(file_path):
    """Test complet d'intégrité d'un fichier Lua."""
    print(f"\n🔍 Test d'intégrité : {os.path.basename(file_path)}")
    print("=" * 50)
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier introuvable: {file_path}")
        return False
    
    # Tests syntaxiques
    print("\n📝 Vérification syntaxique...")
    syntax_issues = check_lua_syntax_issues(file_path)
    if syntax_issues:
        print("❌ Problèmes syntaxiques détectés:")
        for issue in syntax_issues:
            print(f"   • {issue}")
    else:
        print("✅ Syntaxe OK")
    
    # Tests structurels
    print("\n🏗️ Vérification structure...")
    structure_issues = check_lua_structure(file_path)
    if structure_issues:
        print("❌ Problèmes structurels détectés:")
        for issue in structure_issues:
            print(f"   • {issue}")
    else:
        print("✅ Structure OK")
    
    # Tests Love2D
    print("\n💙 Vérification compatibilité Love2D...")
    love2d_issues = test_lua_with_love2d_syntax(file_path)
    if love2d_issues:
        print("⚠️ Problèmes Love2D détectés:")
        for issue in love2d_issues:
            print(f"   • {issue}")
    else:
        print("✅ Compatibilité Love2D OK")
    
    # Corrections automatiques
    all_issues = syntax_issues + structure_issues + [i for i in love2d_issues if not i.startswith("Fonctions")]
    
    if all_issues:
        print(f"\n🔧 Tentative de correction automatique...")
        fixes = fix_common_lua_issues(file_path)
        if fixes:
            print("✅ Corrections appliquées:")
            for fix in fixes:
                print(f"   • {fix}")
            print(f"   • Sauvegarde créée: {file_path}.backup")
            
            # Re-test après corrections
            print(f"\n🔄 Re-test après corrections...")
            post_fix_issues = check_lua_syntax_issues(file_path)
            if not post_fix_issues:
                print("✅ Fichier corrigé avec succès!")
                return True
            else:
                print("⚠️ Problèmes persistants après correction")
                return False
        else:
            print("❌ Aucune correction automatique possible")
            return False
    else:
        print("\n🎉 Fichier parfaitement valide!")
        return True

def main():
    """Point d'entrée principal."""
    print("🔍 TEST D'INTÉGRITÉ DES FICHIERS LUA EXPORTÉS")
    print("=" * 55)
    
    # Rechercher tous les fichiers .lua
    workspace = Path("c:/Users/berou/Downloads/Nouveau dossier")
    lua_files = list(workspace.glob("*.lua"))
    
    if not lua_files:
        print("❌ Aucun fichier .lua trouvé")
        return False
    
    print(f"📁 Fichiers Lua trouvés: {len(lua_files)}")
    
    all_valid = True
    for lua_file in lua_files:
        valid = test_lua_file_integrity(str(lua_file))
        all_valid = all_valid and valid
    
    print(f"\n{'='*55}")
    if all_valid:
        print("🎉 TOUS LES FICHIERS LUA SONT VALIDES!")
    else:
        print("❌ CERTAINS FICHIERS NÉCESSITENT ATTENTION")
    
    print("\n💡 Conseils pour Love2D:")
    print("   • Utilisez des chemins relatifs pour les images")
    print("   • Vérifiez que les images existent dans votre projet Love2D")
    print("   • Testez l'import dans votre jeu Love2D")
    
    return all_valid

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'='*55}")
        print("Appuyez sur Entrée pour fermer...")
        input()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrompu")
        sys.exit(1)
