#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export Lua avec support du formatage de texte pour Love2D
"""

def lua_escape(text):
    """Escape special characters for Lua strings."""
    if text is None:
        return '""'
    text = str(text)
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('\t', '\\t')
    return f'"{text}"'

class LuaExporter:
    def __init__(self, repo):
        self.repo = repo

    def build_text_formatting_lua(self, card) -> str:
        """Construit la table Lua pour le formatage de texte"""
        return f"""{{
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
        }}
    }}"""

    def build_card_lua_enhanced(self, card) -> str:
        """Construit l'export Lua complet d'une carte avec formatage"""
        formatting = self.build_text_formatting_lua(card)
        
        return f"""{{
    id = {card.id or 'nil'},
    nom = {lua_escape(card.nom)},
    type = {lua_escape(card.type)},
    rarete = {lua_escape(card.rarete)},
    cout = {card.cout},
    description = {lua_escape(card.description)},
    image_path = {lua_escape(card.image_path)},
    formatting = {formatting}
}}"""

    def export_all_cards(self) -> str:
        """Exporte toutes les cartes au format Lua avec formatage"""
        cards = self.repo.list_cards()
        
        lua_content = "-- Export des cartes Love2D avec formatage de texte\n"
        lua_content += f"-- Généré automatiquement - {len(cards)} cartes\n\n"
        lua_content += "local cards = {\n"
        
        for i, card in enumerate(cards):
            lua_content += f"    -- Carte {i+1}: {card.nom}\n"
            lua_content += f"    {self.build_card_lua_enhanced(card)}"
            if i < len(cards) - 1:
                lua_content += ","
            lua_content += "\n\n"
        
        lua_content += "}\n\n"
        lua_content += "return cards\n"
        
        return lua_content

    def export_single_card(self, card) -> str:
        """Exporte une seule carte au format Lua"""
        return f"-- Carte: {card.nom}\nlocal card = {self.build_card_lua_enhanced(card)}\n\nreturn card\n"
