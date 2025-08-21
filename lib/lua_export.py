#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export des cartes au format Lua
"""
from .utils import to_int, lua_escape, get_card_image_for_export
from .database import CardRepo

# ======================= Export Lua =======================

LUA_HEADER = "local Cards = {\n"
LUA_FOOTER = "}\n\nreturn Cards\n"

def build_hero_lua(hero: dict) -> str:
    attack = to_int(hero.get("attack", 0))
    ared = to_int(hero.get("AttackReduction", 0))
    epine = to_int(hero.get("Epine", 0))
    heal = to_int(hero.get("heal", 0))
    shield = to_int(hero.get("shield", 0))
    shield_pass = to_int(hero.get("shield_pass", 0))
    chpass = to_int(hero.get("chancePassedTour", 0))
    energy_cost = to_int(hero.get("energyCostIncrease", 0))
    energy_decrease = to_int(hero.get("energyCostDecrease", 0))

    bleeding = hero.get("bleeding", {}) or {}
    b_val = to_int(bleeding.get("value", 0))
    b_turns = to_int(bleeding.get("number_turns", 0))

    force_aug = hero.get("force_augmented", {}) or {}
    f_val = to_int(force_aug.get("value", 0))
    f_turns = to_int(force_aug.get("number_turns", 0))

    return (
        "{ "
        f"heal = {heal}, "
        f"shield = {shield}, "
        f"Epine = {epine}, "
        f"attack = {attack}, "
        f"AttackReduction = {ared}, "
        f"shield_pass = {shield_pass}, "
        f"bleeding = {{ value = {b_val}, number_turns = {b_turns} }}, "
        f"force_augmented = {{ value = {f_val}, number_turns = {f_turns} }}, "
        f"chancePassedTour = {chpass}, "
        f"energyCostIncrease = {energy_cost}, "
        f"energyCostDecrease = {energy_decrease}"
        " }"
    )

def build_enemy_lua(enemy: dict) -> str:
    attack = to_int(enemy.get("attack", 0))
    ared = to_int(enemy.get("AttackReduction", 0))
    epine = to_int(enemy.get("Epine", 0))
    heal = to_int(enemy.get("heal", 0))
    shield = to_int(enemy.get("shield", 0))
    shield_pass = to_int(enemy.get("shield_pass", 0))
    chpass = to_int(enemy.get("chancePassedTour", 0))
    energy_cost = to_int(enemy.get("energyCostIncrease", 0))
    energy_decrease = to_int(enemy.get("energyCostDecrease", 0))

    bleeding = enemy.get("bleeding", {}) or {}
    b_val = to_int(bleeding.get("value", 0))
    b_turns = to_int(bleeding.get("number_turns", 0))

    force_aug = enemy.get("force_augmented", {}) or {}
    f_val = to_int(force_aug.get("value", 0))
    f_turns = to_int(force_aug.get("number_turns", 0))

    return (
        "{ "
        f"heal = {heal}, "
        f"attack = {attack}, "
        f"AttackReduction = {ared}, "
        f"Epine = {epine}, "
        f"shield = {shield}, "
        f"shield_pass = {shield_pass}, "
        f"bleeding = {{ value = {b_val}, number_turns = {b_turns} }}, "
        f"force_augmented = {{ value = {f_val}, number_turns = {f_turns} }}, "
        f"chancePassedTour = {chpass}, "
        f"energyCostIncrease = {energy_cost}, "
        f"energyCostDecrease = {energy_decrease}"
        " }"
    )

def build_types_lua(types: list[str]) -> str:
    if not types:
        return "{}"
    inner = ", ".join([f"'{t}'" for t in types])
    return f"{{ {inner} }}"

def build_action_lua(action_text: str, param: str) -> str:
    body = (action_text or '').rstrip()
    if not body:
        return "function() end"
    indented = "\n".join(["                " + line for line in body.splitlines()])
    p = param if param else ""
    return f"function({p})\n{indented}\n            end"

def build_card_lua(card) -> str:
    name = lua_escape(card.name)
    img = lua_escape(get_card_image_for_export(card))  # Utilise l'image fusionnée si disponible
    desc = lua_escape(card.description)
    hero = build_hero_lua(card.hero)
    enemy = build_enemy_lua(card.enemy)
    action_fn = build_action_lua(card.action, card.action_param)
    return (
        "    {\n"
        f"        name = '{name}',\n"
        f"        ImgIlustration = '{img}',\n"
        f"        Description = '{desc}',\n"
        f"        PowerBlow = {int(card.powerblow)},\n"
        f"        Rarete = '{card.rarity}',\n"
        f"        Type = {build_types_lua(card.types)},\n"
        f"        Effect = {{\n"
        f"            hero = {hero},\n"
        f"            enemy = {enemy},\n"
        f"            action = {action_fn}\n"
        f"        }},\n"
        f"        Cards = {{}}\n"
        "    )"
    )

def export_lua(repo: CardRepo, side: str, filepath: str) -> None:
    cards = repo.list_cards(side=side)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(LUA_HEADER)
        for i, c in enumerate(cards, start=1):
            f.write(f"    --[[ CARTE {i} ]]\n")
            f.write(build_card_lua(c))
            f.write(",\n\n" if i < len(cards) else "\n")
        f.write(LUA_FOOTER)
