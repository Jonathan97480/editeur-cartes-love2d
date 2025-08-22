#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour standardiser tous les curseurs avec les nouvelles spécifications
"""
import re
from pathlib import Path

def standardize_sliders():
    """Standardise tous les curseurs selon les nouvelles spécifications"""
    file_path = Path("lib/interface/text_formatting_editor.py")
    
    # Lire le contenu du fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Standardisation des curseurs...")
    
    # 1. Remplacer toutes les références à slider_length par 199
    content = re.sub(r'length=slider_length', 'length=199', content)
    print("✅ Longueur des curseurs fixée à 199px")
    
    # 2. S'assurer que tous les Scale ont orient=tk.HORIZONTAL
    content = re.sub(
        r'(ttk\.Scale\([^)]+)(?<!orient=tk\.HORIZONTAL)(\))',
        r'\1, orient=tk.HORIZONTAL\2',
        content
    )
    
    # Nettoyer les doublons d'orient
    content = re.sub(r'orient=tk\.HORIZONTAL,\s*orient=tk\.HORIZONTAL', 'orient=tk.HORIZONTAL', content)
    print("✅ Orientation horizontale appliquée à tous les curseurs")
    
    # 3. Remplacer tous les anciens formats de curseurs par le nouveau format standardisé
    # Pattern pour les curseurs avec labels inline
    old_pattern = r'ttk\.Label\([^,]+,\s*text="([^"]+)"\)\.pack\(side=tk\.LEFT\)\s*\n\s*([^=]+)=\s*tk\.(\w+)Var\([^)]+\)\s*\n\s*ttk\.Scale\(([^,]+),([^)]+)\)\.pack\([^)]+\)\s*\n\s*ttk\.Label\([^,]+,\s*textvariable=\2[^)]*\)\.pack\([^)]+\)'
    
    # Nouveau format standardisé
    def replace_slider(match):
        label_text = match.group(1)
        var_name = match.group(2)
        var_type = match.group(3)
        parent = match.group(4)
        scale_params = match.group(5)
        
        return f"""# Label et valeur au-dessus
        label_frame = ttk.Frame({parent})
        label_frame.pack(fill=tk.X)
        ttk.Label(label_frame, text="{label_text}").pack(side=tk.LEFT)
        ttk.Label(label_frame, textvariable={var_name}).pack(side=tk.RIGHT, padx=(0, 45))
        
        # Curseur
        ttk.Scale({parent},{scale_params}, length=199, orient=tk.HORIZONTAL).pack(side=tk.LEFT, pady=(2, 0))"""
    
    # Sauvegarder le fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Standardisation terminée !")
    
    # Afficher les statistiques
    slider_count = content.count('ttk.Scale')
    print(f"📊 {slider_count} curseurs standardisés")
    print("📏 Spécifications appliquées :")
    print("   - Longueur : 199px")
    print("   - Marge droite : 45px")
    print("   - Texte au-dessus du curseur")
    print("   - Orientation horizontale")

if __name__ == "__main__":
    standardize_sliders()
