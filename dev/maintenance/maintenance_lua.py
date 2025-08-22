#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de maintenance des fichiers Lua
Exécute automatiquement l'organisation et le nettoyage
"""

import subprocess
import sys
import os

def main():
    print("🧹 MAINTENANCE AUTOMATIQUE DES FICHIERS LUA")
    print("=" * 50)
    
    # Nettoyer et organiser
    try:
        result = subprocess.run([sys.executable, "nettoyer_projet.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Nettoyage terminé avec succès")
            print(result.stdout)
        else:
            print("❌ Erreur lors du nettoyage:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")

if __name__ == "__main__":
    main()
