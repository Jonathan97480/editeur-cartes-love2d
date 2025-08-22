#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction automatique des imports relatifs
"""

import re
import os

def fix_relative_imports(file_path):
    """Corrige les imports relatifs dans un fichier Python"""
    print(f"🔧 Correction des imports dans {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour détecter les imports relatifs
    import_pattern = r'from \.([a-zA-Z_][a-zA-Z0-9_]*) import ([a-zA-Z_][a-zA-Z0-9_, \(\)]*)'
    
    def replace_import(match):
        module_name = match.group(1)
        import_items = match.group(2)
        
        # Créer le pattern try/except
        return f"""try:
    from .{module_name} import {import_items}
except ImportError:
    from {module_name} import {import_items}"""
    
    # Remplacer les imports relatifs par des try/except
    imports_found = re.findall(import_pattern, content)
    
    if imports_found:
        print(f"  📍 Trouvé {len(imports_found)} imports relatifs à corriger")
        
        # Remplacer chaque import individuellement
        for module_name, import_items in imports_found:
            old_import = f"from .{module_name} import {import_items}"
            new_import = f"""try:
    from .{module_name} import {import_items}
except ImportError:
    from {module_name} import {import_items}"""
            
            # Remplacer seulement si ce n'est pas déjà un try/except
            if "try:" not in content[max(0, content.find(old_import) - 50):content.find(old_import) + len(old_import) + 50]:
                content = content.replace(old_import, new_import)
                print(f"    ✅ Corrigé: {module_name}")
    
    # Sauvegarder le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return len(imports_found)

def main():
    """Fonction principale"""
    print("🚀 CORRECTION AUTOMATIQUE DES IMPORTS RELATIFS")
    print("=" * 60)
    
    # Fichiers à corriger
    files_to_fix = [
        'lib/ui_components.py',
        'lib/database.py', 
        'lib/text_formatting_editor.py',
        'lib/game_package_exporter.py'
    ]
    
    total_corrections = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            corrections = fix_relative_imports(file_path)
            total_corrections += corrections
        else:
            print(f"⚠️ Fichier non trouvé: {file_path}")
    
    print(f"\n🎯 CORRECTION TERMINÉE: {total_corrections} imports corrigés")

if __name__ == "__main__":
    main()
