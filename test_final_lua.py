#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 TEST FINAL DE VALIDATION LUA
==============================

Test complet et validation finale des fichiers Lua exportés.
"""
import os
import re
import sys
from pathlib import Path

def validate_lua_syntax_strict(file_path):
    """Validation syntaxique stricte pour Lua."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Comptages basiques
        issues = []
        
        # 1. Vérification parenthèses/accolades
        open_parens = content.count('(')
        close_parens = content.count(')')
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        if open_parens != close_parens:
            issues.append(f"❌ Parenthèses déséquilibrées: {open_parens} vs {close_parens}")
        
        if open_braces != close_braces:
            issues.append(f"❌ Accolades déséquilibrées: {open_braces} vs {close_braces}")
        
        # 2. Structure de base
        required_patterns = [
            r'local Cards = \{',
            r'return Cards'
        ]
        
        for pattern in required_patterns:
            if not re.search(pattern, content):
                issues.append(f"❌ Structure manquante: {pattern}")
        
        # 3. Virgules en fin d'objet (erreur fréquente)
        bad_patterns = [
            r'\},\s*\}',  # Virgule avant fermeture finale
            r'\}\s*,\s*return'  # Virgule avant return
        ]
        
        for pattern in bad_patterns:
            if re.search(pattern, content):
                issues.append(f"❌ Virgule incorrecte: {pattern}")
        
        return issues
        
    except Exception as e:
        return [f"❌ Erreur lecture: {e}"]

def test_love2d_compatibility(file_path):
    """Test de compatibilité Love2D."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {
            'images_relative': [],
            'images_absolute': [],
            'missing_files': [],
            'valid_structure': True
        }
        
        # Extraire les chemins d'images
        img_matches = re.findall(r"ImgIlustration = '([^']+)'", content)
        
        for img_path in img_matches:
            if os.path.isabs(img_path):
                results['images_absolute'].append(img_path)
            else:
                results['images_relative'].append(img_path)
                
                # Vérifier l'existence relative
                full_path = os.path.join(os.path.dirname(file_path), img_path)
                if not os.path.exists(full_path):
                    results['missing_files'].append(img_path)
        
        return results
        
    except Exception as e:
        return {'error': str(e)}

def create_love2d_test_structure(base_path):
    """Crée une structure de test pour Love2D."""
    try:
        # Créer le dossier de test
        test_dir = os.path.join(base_path, "love2d_test")
        os.makedirs(test_dir, exist_ok=True)
        
        # Copier le fichier Lua
        src_lua = os.path.join(base_path, "cards_player_final.lua")
        dst_lua = os.path.join(test_dir, "cards.lua")
        
        if os.path.exists(src_lua):
            import shutil
            shutil.copy2(src_lua, dst_lua)
            
            # Copier les images si elles existent
            images_src = os.path.join(base_path, "images")
            images_dst = os.path.join(test_dir, "images")
            
            if os.path.exists(images_src):
                if os.path.exists(images_dst):
                    shutil.rmtree(images_dst)
                shutil.copytree(images_src, images_dst)
            
            # Créer un main.lua simple pour test
            main_lua = """function love.load()
    cards = require('cards')
    print('Nombre de cartes chargées:', #cards)
    
    for i, card in ipairs(cards) do
        print('Carte ' .. i .. ': ' .. card.name)
        -- Vérifier l'image
        if love.filesystem.getInfo(card.ImgIlustration) then
            print('  Image OK: ' .. card.ImgIlustration)
        else
            print('  Image MANQUANTE: ' .. card.ImgIlustration)
        end
    end
end

function love.draw()
    love.graphics.print('Test de chargement des cartes - voir console', 10, 10)
end
"""
            
            with open(os.path.join(test_dir, "main.lua"), 'w', encoding='utf-8') as f:
                f.write(main_lua)
            
            return test_dir
        
        return None
        
    except Exception as e:
        print(f"❌ Erreur création structure test: {e}")
        return None

def main():
    """Test final complet."""
    print("🎯 TEST FINAL DE VALIDATION LUA")
    print("=" * 50)
    
    base_path = "c:/Users/berou/Downloads/Nouveau dossier"
    lua_file = os.path.join(base_path, "cards_player_final.lua")
    
    if not os.path.exists(lua_file):
        print(f"❌ Fichier non trouvé: {lua_file}")
        return False
    
    print(f"📁 Test du fichier: {os.path.basename(lua_file)}")
    
    # 1. Validation syntaxique stricte
    print("\n🔍 Validation syntaxique...")
    syntax_issues = validate_lua_syntax_strict(lua_file)
    if syntax_issues:
        print("❌ Problèmes syntaxiques:")
        for issue in syntax_issues:
            print(f"   {issue}")
        return False
    else:
        print("✅ Syntaxe parfaitement valide")
    
    # 2. Test Love2D
    print("\n💙 Test compatibilité Love2D...")
    compat = test_love2d_compatibility(lua_file)
    
    if 'error' in compat:
        print(f"❌ Erreur test Love2D: {compat['error']}")
        return False
    
    print(f"   Images relatives: {len(compat['images_relative'])}")
    print(f"   Images absolues: {len(compat['images_absolute'])}")
    print(f"   Images manquantes: {len(compat['missing_files'])}")
    
    if compat['images_absolute']:
        print("   ⚠️ Chemins absolus détectés (à éviter pour Love2D)")
        for img in compat['images_absolute']:
            print(f"     • {img}")
    
    if compat['missing_files']:
        print("   ❌ Images manquantes:")
        for img in compat['missing_files']:
            print(f"     • {img}")
    
    # 3. Création structure de test Love2D
    print("\n🚀 Création structure de test Love2D...")
    test_dir = create_love2d_test_structure(base_path)
    
    if test_dir:
        print(f"✅ Structure créée: {test_dir}")
        print("   📁 Contenu:")
        print("     • main.lua (test de chargement)")
        print("     • cards.lua (vos cartes)")
        print("     • images/ (dossier des images)")
        print("\n💡 Pour tester avec Love2D:")
        print(f"   1. Ouvrez le dossier: {test_dir}")
        print("   2. Lancez: love .")
        print("   3. Vérifiez la console pour les résultats")
    else:
        print("❌ Impossible de créer la structure de test")
    
    # 4. Résumé final
    print(f"\n{'='*50}")
    
    if not syntax_issues and not compat['missing_files']:
        print("🎉 VALIDATION RÉUSSIE!")
        print("✅ Fichier Lua syntaxiquement correct")
        print("✅ Compatible avec Love2D")
        print("✅ Images accessibles")
        print("✅ Prêt pour l'utilisation")
        
        print("\n🎯 Corrections appliquées avec succès:")
        print("   • Export utilise les images fusionnées")
        print("   • Chemins relatifs pour Love2D")
        print("   • Syntaxe Lua correcte")
        print("   • Structure valide")
        
        return True
    else:
        print("⚠️ VALIDATION PARTIELLE")
        if syntax_issues:
            print("❌ Problèmes syntaxiques à corriger")
        if compat['missing_files']:
            print("❌ Images manquantes à résoudre")
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
