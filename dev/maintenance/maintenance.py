#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de maintenance automatique du projet Love2D Card Editor
À exécuter périodiquement pour maintenir l'organisation
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

def nettoyer_fichiers_temporaires():
    """Nettoie les fichiers temporaires"""
    patterns = ["*.tmp", "*.temp", "*~", "*.bak"]
    for pattern in patterns:
        for fichier in Path(".").glob(pattern):
            try:
                fichier.unlink()
                print(f"✅ Fichier temporaire supprimé: {fichier}")
            except Exception as e:
                print(f"❌ Erreur lors de la suppression de {fichier}: {e}")

def sauvegarder_base_donnees():
    """Crée une sauvegarde de la base de données"""
    if os.path.exists("data/cartes.db"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sauvegarde = f"dbBackup/cartes_backup_{timestamp}.db"
        try:
            shutil.copy2("data/cartes.db", sauvegarde)
            print(f"✅ Sauvegarde créée: {sauvegarde}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")

def nettoyer_logs_anciens():
    """Supprime les logs de plus de 30 jours"""
    if os.path.exists("logs"):
        seuil = datetime.now().timestamp() - (30 * 24 * 3600)  # 30 jours
        for fichier_log in Path("logs").glob("*.log"):
            if fichier_log.stat().st_mtime < seuil:
                try:
                    fichier_log.unlink()
                    print(f"✅ Log ancien supprimé: {fichier_log}")
                except Exception as e:
                    print(f"❌ Erreur lors de la suppression de {fichier_log}: {e}")

if __name__ == "__main__":
    print("🧹 MAINTENANCE AUTOMATIQUE DU PROJET")
    print("=" * 50)
    
    nettoyer_fichiers_temporaires()
    sauvegarder_base_donnees()
    nettoyer_logs_anciens()
    
    print("✅ Maintenance terminée")
