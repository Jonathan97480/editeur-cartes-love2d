#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de réinitialisation pour tester l'organisation automatique
Remet le projet dans un état "désordonné" pour tester organiser_projet.py
"""

import os
import shutil
from pathlib import Path

def log_info(message):
    print(f"ℹ️  {message}")

def log_success(message):
    print(f"✅ {message}")

def remettre_fichiers_racine():
    """Remet quelques fichiers dans la racine pour simuler le désordre"""
    log_info("Simulation d'un projet désordonné...")
    
    # Déplacer la base de données vers la racine si elle est dans data/
    if os.path.exists("data/cartes.db") and not os.path.exists("cartes.db"):
        shutil.move("data/cartes.db", "cartes.db")
        log_success("Base de données remise à la racine")
    
    # Remettre quelques fichiers depuis les dossiers organisés
    fichiers_a_remettre = [
        ("docs/CHANGELOG.md", "CHANGELOG.md"),
        ("rapports/audit_projet.py", "audit_projet.py"),
        ("rapports/diagnostic.py", "diagnostic.py")
    ]
    
    for source, destination in fichiers_a_remettre:
        if os.path.exists(source) and not os.path.exists(destination):
            shutil.move(source, destination)
            log_success(f"Fichier remis: {destination}")
    
    # Supprimer les dossiers vides (optionnel)
    dossiers_a_nettoyer = ["docs", "rapports", "data"]
    for dossier in dossiers_a_nettoyer:
        if os.path.exists(dossier) and not os.listdir(dossier):
            os.rmdir(dossier)
            log_success(f"Dossier vide supprimé: {dossier}")

def main():
    print("🔄 RÉINITIALISATION POUR TEST D'ORGANISATION")
    print("=" * 50)
    
    if not os.path.exists("app_final.py"):
        print("❌ app_final.py non trouvé. Exécutez depuis le dossier racine du projet.")
        return
    
    remettre_fichiers_racine()
    
    print("\n✅ Projet remis dans un état 'désordonné'")
    print("Vous pouvez maintenant tester: python organiser_projet.py")

if __name__ == "__main__":
    main()
