#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour l'éditeur de cartes Love2D
"""
import os
import tempfile
import unittest

# Pattern try/except pour imports relatifs/absolus
try:
    from .database import Card, CardRepo, ensure_db
    from .lua_export import build_hero_lua, build_enemy_lua, build_types_lua, build_card_lua, export_lua
    from .utils import lua_escape
except ImportError:
    from database import Card, CardRepo, ensure_db
    from lua_export import build_hero_lua, build_enemy_lua, build_types_lua, build_card_lua, export_lua
    from utils import lua_escape

class TestLuaHelpers(unittest.TestCase):
    def test_lua_escape_quotes_and_newlines(self):
        s = "A 'quote'\\path\nline2"
        esc = lua_escape(s)
        self.assertIn("\\'", esc)
        self.assertIn("\\\\", esc)
        self.assertIn("\\n", esc)

    def test_build_hero_lua_full_structure(self):
        h = {"heal": 5, "shield": 3, "attack": 2, "energyCostDecrease": 1}
        out = build_hero_lua(h)
        for key in ["heal = 5", "shield = 3", "attack = 2", "energyCostDecrease = 1"]:
            self.assertIn(key, out)

    def test_build_enemy_lua_full_structure(self):
        e = {"attack":8, "AttackReduction":25, "Epine":0, "heal":2, "shield":6, "shield_pass":1,
             "bleeding": {"value":2, "number_turns":3}, "force_augmented": {"value":4, "number_turns":5},
             "chancePassedTour": 10, "energyCostIncrease": 3}
        out = build_enemy_lua(e)
        for key in ["attack = 8", "AttackReduction = 25", "heal = 2", "shield = 6", "shield_pass = 1", 
                   "chancePassedTour = 10", "energyCostIncrease = 3"]:
            self.assertIn(key, out)
        self.assertIn("bleeding = { value = 2, number_turns = 3 }", out)
        self.assertIn("force_augmented = { value = 4, number_turns = 5 }", out)

    def test_build_types_lua(self):
        self.assertEqual(build_types_lua([]), "{}")
        self.assertEqual(build_types_lua(['attaque']), "{ 'attaque' }")
        self.assertEqual(build_types_lua(['attaque','soin']), "{ 'attaque', 'soin' }")

class TestRarityAndTypes(unittest.TestCase):
    def test_defaults(self):
        c = Card()
        self.assertEqual(c.rarity, 'commun')
        self.assertEqual(c.types, [])

    def test_build_card_lua_includes_rarete_and_type(self):
        c = Card()
        c.name = "TestR"; c.img = "img/x.png"; c.description = "Desc"; c.powerblow = 2
        c.rarity = 'legendaire'; c.types = ['attaque','soin']
        out = build_card_lua(c)
        self.assertIn("Rarete = 'legendaire'", out)
        self.assertIn("Type = { 'attaque', 'soin' }", out)

class TestExport(unittest.TestCase):
    def test_export_lua_creates_file_with_header_footer(self):
        with tempfile.TemporaryDirectory() as td:
            dbp = os.path.join(td, 'test.db')
            ensure_db(dbp)
            r = CardRepo(dbp)
            c = Card(); c.side = 'joueur'; c.name = 'Griffure'; c.img = 'img/card/ilustration/Claw.png'
            c.description = 'Inflige 8 degats.'; c.powerblow = 1; c.rarity = 'commun'; c.types = ['attaque']
            r.insert(c)
            outp = os.path.join(td, 'cards_player.lua')
            export_lua(r, 'joueur', outp)
            with open(outp, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertTrue(content.startswith('local cards ='))  # Format corrigé (minuscule)
            self.assertTrue(content.strip().endswith('return cards'))  # Format corrigé (minuscule)
            # Nouvelle assertion adaptée au format actuel avec icône
            self.assertIn("--[[ CARTE 1", content)  # Format: "--[[ CARTE 1 - 🎮 Joueur ]]"
            self.assertIn("Rarete = 'commun'", content)
            self.assertIn("Type = { 'attaque' }", content)

def run_tests():
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestLuaHelpers))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestRarityAndTypes))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestExport))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()
