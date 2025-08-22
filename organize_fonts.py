#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 ORGANISATION DES FICHIERS POLICES
==================================

Script pour organiser les nouveaux fichiers liés au système de polices.
"""

import os
import shutil
from pathlib import Path

def organize_font_files():
    """Organise les fichiers du système de polices."""
    print("📁 ORGANISATION DU SYSTÈME DE POLICES")
    print("=" * 40)
    
    # Créer le dossier dev/polices pour les outils de développement
    dev_fonts_dir = Path("dev/polices")
    dev_fonts_dir.mkdir(parents=True, exist_ok=True)
    
    # Déplacer les scripts de développement vers dev/polices/
    scripts_to_move = [
        ("test_font_manager.py", "Script de test du gestionnaire de polices"),
        ("install_fonts.py", "Installateur de polices interactif"),
        ("test_editor_fonts.py", "Test de l'éditeur avec polices personnalisées")
    ]
    
    moved_files = []
    
    for script_name, description in scripts_to_move:
        source = Path(script_name)
        if source.exists():
            dest = dev_fonts_dir / script_name
            try:
                shutil.move(str(source), str(dest))
                moved_files.append((script_name, description))
                print(f"✅ {script_name} → dev/polices/")
            except Exception as e:
                print(f"❌ Erreur déplacement {script_name}: {e}")
    
    # Créer un README.md dans dev/polices/
    readme_content = f"""# 🎨 Outils de Développement - Polices

Ce dossier contient les outils de développement pour le système de polices personnalisées.

## Scripts disponibles

"""
    
    for script_name, description in moved_files:
        readme_content += f"### {script_name}\n{description}\n\n**Usage :**\n```bash\npython dev/polices/{script_name}\n```\n\n"
    
    readme_content += f"""## Architecture du système de polices

### Composants principaux :
- **`lib/font_manager.py`** : Gestionnaire principal des polices
- **`lib/text_formatting_editor.py`** : Éditeur intégré avec support polices
- **`fonts/`** : Dossier de stockage des polices personnalisées

### Structure des polices :
```
fonts/
├── titre/          # Polices pour les titres
├── texte/          # Polices pour le texte principal  
├── special/        # Polices décoratives
└── README.md       # Documentation utilisateur
```

### Intégration :
Le système de polices est automatiquement intégré dans :
- L'éditeur de formatage de texte
- L'exporteur Love2D (à venir)
- L'aperçu en temps réel

## Installation de nouvelles polices

1. **Via l'installateur :**
   ```bash
   python dev/polices/install_fonts.py
   ```

2. **Manuellement :**
   - Copiez les fichiers .ttf/.otf dans fonts/
   - Redémarrez l'application
   - Utilisez "🎨 Actualiser polices" dans l'éditeur

## Tests et validation

- **`test_font_manager.py`** : Test du gestionnaire de base
- **`test_editor_fonts.py`** : Test d'intégration complète

Ces scripts valident que le système fonctionne correctement.
"""
    
    readme_path = dev_fonts_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ README.md créé → dev/polices/")
    
    # Vérifier la structure du dossier fonts/
    fonts_dir = Path("fonts")
    print(f"\n📁 Structure du dossier fonts/ :")
    
    subdirs = ["titre", "texte", "special"]
    for subdir in subdirs:
        full_path = fonts_dir / subdir
        if full_path.exists():
            font_files = list(full_path.glob("*.ttf")) + list(full_path.glob("*.otf"))
            print(f"  ✅ {subdir}/ ({len(font_files)} polices)")
        else:
            print(f"  ❌ {subdir}/ manquant")
    
    # Compter les polices au total
    total_fonts = len(list(fonts_dir.glob("**/*.ttf"))) + len(list(fonts_dir.glob("**/*.otf")))
    print(f"\n📊 Total : {total_fonts} polices personnalisées installées")
    
    if total_fonts == 0:
        print(f"💡 Ajoutez des polices avec : python dev/polices/install_fonts.py")
    
    print(f"\n🎯 SYSTÈME DE POLICES ORGANISÉ")
    print(f"=" * 30)
    print(f"✅ Scripts déplacés vers dev/polices/")
    print(f"✅ Documentation créée")
    print(f"✅ Structure fonts/ vérifiée")
    print(f"✅ Système prêt à l'utilisation")
    
    return True

if __name__ == "__main__":
    organize_font_files()
