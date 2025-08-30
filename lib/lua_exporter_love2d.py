#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export Lua compatible avec le format cards_joueur.lua
Inclut les données de formatage de texte
"""

from lib.database import CardRepo
from lib.config import DB_FILE
from pathlib import Path
import os

def lua_escape(text):
    """Escape special characters for Lua strings."""
    if text is None:
        return '""'
    text = str(text)
    text = text.replace('\\', '\\\\')
    text = text.replace("'", "\\'")
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('\t', '\\t')
    return f"'{text}'"

def sanitize_filename(name):
    """
    Convertit un nom de carte en nom de fichier valide.
    
    Args:
        name: Nom de la carte
        
    Returns:
        Nom de fichier sécurisé
    """
    import re
    if not name:
        return "carte_sans_nom"
    
    # Supprimer les caractères spéciaux et remplacer par des underscores
    clean_name = re.sub(r'[^\w\s-]', '', name.strip())
    # Remplacer les espaces par des underscores
    clean_name = re.sub(r'\s+', '_', clean_name)
    # Supprimer les underscores multiples
    clean_name = re.sub(r'_+', '_', clean_name)
    # Supprimer les underscores en début et fin
    clean_name = clean_name.strip('_')
    
    return clean_name if clean_name else "carte_sans_nom"

def get_card_image_name(card):
    """
    Génère le nom d'image pour une carte dans l'export.
    
    Args:
        card: Objet carte
        
    Returns:
        Nom de fichier pour l'image de la carte
    """
    safe_name = sanitize_filename(card.name)
    return f"cards/{safe_name}.png"

def get_font_path_with_extension(font_name):
    """
    Retourne le chemin de la police avec son extension pour Love2D.
    
    Args:
        font_name: Nom de la police (peut inclure 🎨 préfixe)
        
    Returns:
        Chemin de la police avec extension ou nom original si non trouvé
    """
    if not font_name or font_name.strip() == '':
        return 'fonts/Arial.ttf'  # Police par défaut
    
    # Nettoyer le nom de police
    clean_name = font_name.replace("🎨 ", "").strip()
    
    # Si c'est déjà un chemin avec extension, le retourner tel quel
    if '.' in clean_name and clean_name.lower().endswith(('.ttf', '.otf')):
        return clean_name
    
    # Chercher dans les dossiers de polices
    fonts_base = Path("fonts")
    
    # 1. Chercher dans les sous-dossiers (titre, texte, special)
    for subdir in ["titre", "texte", "special"]:
        subdir_path = fonts_base / subdir
        if subdir_path.exists():
            for ext in [".ttf", ".otf"]:
                font_file = subdir_path / f"{clean_name}{ext}"
                if font_file.exists():
                    return str(font_file).replace('\\', '/')
    
    # 2. Chercher dans le dossier fonts racine
    if fonts_base.exists():
        for ext in [".ttf", ".otf"]:
            font_file = fonts_base / f"{clean_name}{ext}"
            if font_file.exists():
                return str(font_file).replace('\\', '/')
    
    # 3. Pour les polices système communes, retourner un chemin Love2D standard
    system_fonts_mapping = {
        "Arial": "fonts/Arial.ttf",
        "Times New Roman": "fonts/Times.ttf", 
        "Courier New": "fonts/Courier.ttf",
        "Verdana": "fonts/Verdana.ttf",
        "Calibri": "fonts/Calibri.ttf",
        "Georgia": "fonts/Georgia.ttf",
        "Trebuchet MS": "fonts/Trebuchet.ttf",
        "Comic Sans MS": "fonts/Comic.ttf",
        "Impact": "fonts/Impact.ttf"
    }
    
    if clean_name in system_fonts_mapping:
        return system_fonts_mapping[clean_name]
    
    # 4. Dernier recours : ajouter .ttf par défaut
    return f"fonts/{clean_name}.ttf"
    """
    Retourne le chemin de la police avec son extension pour Love2D.
    
    Args:
        font_name: Nom de la police (peut inclure 🎨 préfixe)
        
    Returns:
        Chemin de la police avec extension ou nom original si non trouvé
    """
    if not font_name or font_name.strip() == '':
        return 'fonts/Arial.ttf'  # Police par défaut
    
    # Nettoyer le nom de police
    clean_name = font_name.replace("🎨 ", "").strip()
    
    # Si c'est déjà un chemin avec extension, le retourner tel quel
    if '.' in clean_name and clean_name.lower().endswith(('.ttf', '.otf')):
        return clean_name
    
    # Chercher dans les dossiers de polices
    fonts_base = Path("fonts")
    
    # 1. Chercher dans les sous-dossiers (titre, texte, special)
    for subdir in ["titre", "texte", "special"]:
        subdir_path = fonts_base / subdir
        if subdir_path.exists():
            for ext in [".ttf", ".otf"]:
                font_file = subdir_path / f"{clean_name}{ext}"
                if font_file.exists():
                    return str(font_file).replace('\\', '/')
    
    # 2. Chercher dans le dossier fonts racine
    if fonts_base.exists():
        for ext in [".ttf", ".otf"]:
            font_file = fonts_base / f"{clean_name}{ext}"
            if font_file.exists():
                return str(font_file).replace('\\', '/')
    
    # 3. Pour les polices système communes, retourner un chemin Love2D standard
    system_fonts_mapping = {
        "Arial": "fonts/Arial.ttf",
        "Times New Roman": "fonts/Times.ttf", 
        "Courier New": "fonts/Courier.ttf",
        "Verdana": "fonts/Verdana.ttf",
        "Calibri": "fonts/Calibri.ttf",
        "Georgia": "fonts/Georgia.ttf",
        "Trebuchet MS": "fonts/Trebuchet.ttf",
        "Comic Sans MS": "fonts/Comic.ttf",
        "Impact": "fonts/Impact.ttf"
    }
    
    if clean_name in system_fonts_mapping:
        return system_fonts_mapping[clean_name]
    
    # 4. Dernier recours : ajouter .ttf par défaut
    return f"fonts/{clean_name}.ttf"

class Love2DLuaExporter:
    def __init__(self, repo):
        self.repo = repo

    def build_types_array(self, types_list):
        """Construit le tableau des types au format Lua"""
        if not types_list:
            return "{}"
        
        lua_types = []
        for t in types_list:
            lua_types.append(f"'{t}'")
        
        return "{ " + ", ".join(lua_types) + " }"

    def build_effect_section(self, card):
        """Construit la section Effect au format Love2D"""
        actor_data = card.hero
        enemy_data = card.enemy
        
        effect = f"""Effect = {{
            Actor = {{ heal = {actor_data['heal']}, shield = {actor_data['shield']}, Epine = {actor_data['Epine']}, attack = {actor_data['attack']}, AttackReduction = {actor_data['AttackReduction']}, shield_pass = {actor_data['shield_pass']}, bleeding = {{ value = {actor_data['bleeding']['value']}, number_turns = {actor_data['bleeding']['number_turns']} }}, force_augmented = {{ value = {actor_data['force_augmented']['value']}, number_turns = {actor_data['force_augmented']['number_turns']} }}, chancePassedTour = {actor_data['chancePassedTour']}, energyCostIncrease = {actor_data['energyCostIncrease']}, energyCostDecrease = {actor_data['energyCostDecrease']} }},
            Enemy = {{ heal = {enemy_data['heal']}, attack = {enemy_data['attack']}, AttackReduction = {enemy_data['AttackReduction']}, Epine = {enemy_data['Epine']}, shield = {enemy_data['shield']}, shield_pass = {enemy_data['shield_pass']}, bleeding = {{ value = {enemy_data['bleeding']['value']}, number_turns = {enemy_data['bleeding']['number_turns']} }}, force_augmented = {{ value = {enemy_data['force_augmented']['value']}, number_turns = {enemy_data['force_augmented']['number_turns']} }}, chancePassedTour = {enemy_data['chancePassedTour']}, energyCostIncrease = {enemy_data['energyCostIncrease']}, energyCostDecrease = {enemy_data['energyCostDecrease']} }},
            action = function()"""
        
        if card.action and card.action.strip():
            # Nettoyer et indenter l'action Lua
            action_lines = card.action.strip().split('\n')
            for line in action_lines:
                effect += f"\n                {line}"
        else:
            effect += "\n                -- Aucune action spécifiée"
        
        effect += "\n            end"
        effect += "\n        }"
        
        return effect

    def build_text_formatting_section(self, card):
        """Construit la section de formatage de texte avec taille de carte"""
        return f"""TextFormatting = {{
            card = {{
                width = 280,  -- Largeur standard de carte Love2D
                height = 392, -- Hauteur standard de carte Love2D (ratio 5:7)
                scale = 1.0   -- Facteur d'échelle
            }},
            title = {{
                x = {card.title_x},
                y = {card.title_y},
                font = {lua_escape(get_font_path_with_extension(card.title_font))},
                size = {card.title_size},
                color = {lua_escape(card.title_color)}
            }},
            text = {{
                x = {card.text_x},
                y = {card.text_y},
                width = {card.text_width},
                height = {card.text_height},
                font = {lua_escape(get_font_path_with_extension(card.text_font))},
                size = {card.text_size},
                color = {lua_escape(card.text_color)},
                align = {lua_escape(card.text_align)},
                line_spacing = {card.line_spacing},
                wrap = {'true' if card.text_wrap else 'false'}
            }},
            energy = {{
                x = {card.energy_x},
                y = {card.energy_y},
                font = {lua_escape(get_font_path_with_extension(card.energy_font))},
                size = {card.energy_size},
                color = {lua_escape(card.energy_color)}
            }}
        }}"""

    def build_card_lua_love2d(self, card, card_number):
        """Construit l'export Lua d'une carte au format Love2D"""
        types = self.build_types_array(card.types)
        effect = self.build_effect_section(card)
        formatting = self.build_text_formatting_section(card)
        
        # Utiliser le nom de la carte pour générer le nom d'image
        image_name = get_card_image_name(card)
        
        return f"""    --[[ CARTE {card_number} - 🎮 Joueur ]]
    {{
        name = {lua_escape(card.name)},
        ImgIlustration = {lua_escape(image_name)},
        Description = {lua_escape(card.description)},
        PowerBlow = {card.powerblow},
        Rarete = {lua_escape(card.rarity)},
        Type = {types},
        {effect},
        {formatting},
        Cards = {{}}
    }}"""

    def export_all_cards_love2d(self):
        """Exporte toutes les cartes au format Love2D avec formatage"""
        cards = self.repo.list_cards()
        return self.export_cards_love2d(cards)
        
    def export_cards_love2d(self, cards):
        """Exporte une liste spécifique de cartes au format Love2D avec formatage"""
        lua_content = "local cards = {\n"
        
        for i, card in enumerate(cards, 1):
            lua_content += self.build_card_lua_love2d(card, i)
            if i < len(cards):
                lua_content += ",\n\n"
            else:
                lua_content += "\n"
        
        lua_content += "}\n\nreturn cards\n"
        
        return lua_content

    def export_to_file(self, filename):
        """Exporte les cartes dans un fichier Lua"""
        content = self.export_all_cards_love2d()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return len(content)

if __name__ == "__main__":
    # Test de l'exporteur
    repo = CardRepo(DB_FILE)
    exporter = Love2DLuaExporter(repo)
    
    print("🎮 Export Love2D avec formatage de texte")
    print("=" * 50)
    
    content = exporter.export_all_cards_love2d()
    print(f"📝 Contenu généré ({len(content)} caractères)")
    print("\n🎯 Aperçu du contenu:")
    print(content[:1000] + "..." if len(content) > 1000 else content)
