#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export Lua compatible avec le format cards_joueur.lua
Inclut les données de formatage de texte
"""

from lib.database import CardRepo
from lib.config import DB_FILE

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
                font = {lua_escape(card.title_font)},
                size = {card.title_size},
                color = {lua_escape(card.title_color)}
            }},
            text = {{
                x = {card.text_x},
                y = {card.text_y},
                width = {card.text_width},
                height = {card.text_height},
                font = {lua_escape(card.text_font)},
                size = {card.text_size},
                color = {lua_escape(card.text_color)},
                align = {lua_escape(card.text_align)},
                line_spacing = {card.line_spacing},
                wrap = {'true' if card.text_wrap else 'false'}
            }},
            energy = {{
                x = {card.energy_x},
                y = {card.energy_y},
                font = {lua_escape(card.energy_font)},
                size = {card.energy_size},
                color = {lua_escape(card.energy_color)}
            }}
        }}"""

    def build_card_lua_love2d(self, card, card_number):
        """Construit l'export Lua d'une carte au format Love2D"""
        types = self.build_types_array(card.types)
        effect = self.build_effect_section(card)
        formatting = self.build_text_formatting_section(card)
        
        return f"""    --[[ CARTE {card_number} - 🎮 Joueur ]]
    {{
        name = {lua_escape(card.name)},
        ImgIlustration = {lua_escape(card.img)},
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
