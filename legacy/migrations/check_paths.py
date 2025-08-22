#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier les chemins d'images dans la base
"""
import sqlite3

conn = sqlite3.connect('cartes.db')
cursor = conn.cursor()
cursor.execute('SELECT name, img FROM cards WHERE img IS NOT NULL AND img != "" ORDER BY id LIMIT 10')
rows = cursor.fetchall()

print("Chemins d'images actuellement stockés :")
print("=" * 50)
for name, img_path in rows:
    print(f"{name}: {img_path}")

conn.close()
