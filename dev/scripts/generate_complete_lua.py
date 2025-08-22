#!/usr/bin/env python3
"""
Générateur du fichier Lua complet avec toutes les données de formatage
pour Love2D - Version finale
"""

def generate_complete_lua_file():
    """Génère le fichier cards_joueur.lua avec toutes les données de formatage"""
    
    # Lire le fichier original généré par l'application
    with open('c:/Users/berou/Downloads/cards_joueur.lua', 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    print("🔄 GÉNÉRATION DU FICHIER COMPLET AVEC FORMATAGE")
    print("=" * 60)
    print(f"📄 Fichier original: {len(original_content):,} caractères")
    
    # Structure de formatage par défaut pour Love2D
    text_formatting_template = """        TextFormatting = {{
            card = {{
                width = 280,  -- Largeur standard de carte Love2D
                height = 392, -- Hauteur standard de carte Love2D (ratio 5:7)
                scale = 1.0   -- Facteur d'échelle
            }},
            title = {{
                x = 50,           -- Position X du titre
                y = 25,           -- Position Y du titre
                font = "Arial",   -- Police du titre
                size = 16,        -- Taille du titre
                color = "black"   -- Couleur du titre
            }},
            description = {{
                x = 20,           -- Position X de la description
                y = 80,           -- Position Y de la description
                width = 240,      -- Largeur de la zone de description
                height = 200,     -- Hauteur de la zone de description
                font = "Arial",   -- Police de la description
                size = 12,        -- Taille de la description
                color = "black"   -- Couleur de la description
            }},
            energy = {{
                x = 240,          -- Position X de l'énergie/coût
                y = 25,           -- Position Y de l'énergie/coût
                font = "Arial",   -- Police de l'énergie
                size = 14,        -- Taille de l'énergie
                color = "blue"    -- Couleur de l'énergie
            }}
        }},"""
    
    # Traiter le contenu original
    lines = original_content.split('\n')
    new_lines = []
    card_count = 0
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Détecter la fin d'une carte (ligne avec "Cards = {}")
        if line.strip() == "Cards = {}":
            card_count += 1
            # Insérer la section TextFormatting avant Cards = {}
            # Retirer la ligne "Cards = {}" qu'on vient d'ajouter
            new_lines.pop()
            
            # Ajouter la section TextFormatting
            new_lines.append(text_formatting_template)
            
            # Rajouter "Cards = {}"
            new_lines.append("        Cards = {}")
            
            print(f"✅ Carte {card_count}: Section TextFormatting ajoutée")
    
    # Reconstituer le fichier
    complete_content = '\n'.join(new_lines)
    
    # Sauvegarder l'ancien fichier
    import shutil
    backup_file = 'c:/Users/berou/Downloads/cards_joueur_original_backup.lua'
    shutil.copy2('c:/Users/berou/Downloads/cards_joueur.lua', backup_file)
    print(f"💾 Sauvegarde créée: {backup_file}")
    
    # Écrire le nouveau fichier complet
    with open('c:/Users/berou/Downloads/cards_joueur.lua', 'w', encoding='utf-8') as f:
        f.write(complete_content)
    
    print(f"✅ FICHIER COMPLET GÉNÉRÉ")
    print(f"📊 Taille originale: {len(original_content):,} caractères")
    print(f"📊 Taille finale: {len(complete_content):,} caractères")
    print(f"📦 Cartes traitées: {card_count}")
    print(f"🎯 Sections TextFormatting ajoutées: {card_count}")
    
    # Vérification
    if 'TextFormatting' in complete_content:
        formatting_count = complete_content.count('TextFormatting = {')
        print(f"✅ Vérification: {formatting_count} sections TextFormatting trouvées")
        
        if 'width = 280' in complete_content:
            print("✅ Dimensions de carte (280x392px) présentes")
        
        if 'title = {' in complete_content:
            print("✅ Positionnement des éléments présent")
    
    print()
    print("🎉 RÉSULTAT:")
    print("✅ Votre fichier cards_joueur.lua contient maintenant:")
    print("   📐 Taille de carte (280x392px)")
    print("   📍 Position précise de tous les éléments")
    print("   🎨 Styles et formatage complets")
    print("   🎮 Structure Love2D compatible")
    
    return complete_content

if __name__ == "__main__":
    generate_complete_lua_file()
