#!/usr/bin/env python3
"""
Démonstration du système de changement de rareté amélioré.
"""

import os
import sys
import sqlite3
import time
from datetime import datetime

def demonstrate_rarity_change():
    """Démontre le fonctionnement du système de changement de rareté."""
    print("🎭 DÉMONSTRATION - Changement de rareté avec gestion d'images")
    print("=" * 60)
    
    if not os.path.exists("cartes.db"):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect("cartes.db")
    cursor = conn.cursor()
    
    # Sélectionner une carte pour la démonstration
    cursor.execute("SELECT id, name, rarity, img FROM cards WHERE img IS NOT NULL LIMIT 1")
    card = cursor.fetchone()
    
    if not card:
        print("❌ Aucune carte avec image trouvée")
        return
    
    card_id, name, current_rarity, img_path = card
    
    print(f"\n📋 Carte de démonstration : {name}")
    print(f"   ID : {card_id}")
    print(f"   Rareté actuelle : {current_rarity}")
    print(f"   Image : {img_path}")
    
    if os.path.exists(img_path):
        file_size = os.path.getsize(img_path)
        file_time = datetime.fromtimestamp(os.path.getmtime(img_path))
        print(f"   📊 Taille actuelle : {file_size:,} bytes")
        print(f"   📅 Dernière modification : {file_time}")
    else:
        print(f"   ❌ Fichier image manquant")
        return
    
    print(f"\n🔧 FONCTIONNEMENT DU SYSTÈME :")
    print(f"   1. Quand vous changez la rareté d'une carte")
    print(f"   2. Le système détecte automatiquement le changement")
    print(f"   3. Il charge le template correspondant à la nouvelle rareté")
    print(f"   4. Il génère une nouvelle image fusionnée")
    print(f"   5. L'ancienne image est remplacée (même nom de fichier)")
    print(f"   6. La base de données est mise à jour")
    print(f"   7. Le système valide que l'opération a réussi")
    
    print(f"\n✅ AMÉLIORATIONS APPORTÉES :")
    
    improvements = [
        "Détection automatique des changements de rareté",
        "Validation que l'image a été mise à jour",
        "Messages informatifs dans la console",
        "Gestion d'erreur si le template est manquant",
        "Avertissement si la génération échoue",
        "Conservation de l'ancienne image en cas d'échec",
        "Traçabilité complète du processus"
    ]
    
    for i, improvement in enumerate(improvements, 1):
        print(f"   {i}. {improvement}")
    
    print(f"\n🎯 POURQUOI L'ANCIENNE IMAGE N'EST PAS 'SUPPRIMÉE' :")
    print(f"   ▶ Le système utilise le même nom de fichier")
    print(f"   ▶ L'image est REMPLACÉE, pas supprimée puis recréée")
    print(f"   ▶ Cela évite les problèmes de références brisées")
    print(f"   ▶ Seul le CONTENU change selon la rareté")
    
    print(f"\n🧪 POUR TESTER :")
    print(f"   1. Lancez : python app_final.py")
    print(f"   2. Sélectionnez la carte '{name}'")
    print(f"   3. Changez sa rareté vers 'Rare' ou 'Légendaire'")
    print(f"   4. Sauvegardez")
    print(f"   5. Observez les messages dans la console")
    
    # Montrer les templates disponibles
    print(f"\n🎨 TEMPLATES DISPONIBLES :")
    templates_dir = "images/templates"
    if os.path.exists(templates_dir):
        templates = [f for f in os.listdir(templates_dir) if f.endswith('.png')]
        for template in sorted(templates):
            template_path = os.path.join(templates_dir, template)
            size = os.path.getsize(template_path)
            print(f"   📄 {template:<25} ({size:,} bytes)")
    
    conn.close()
    
    print(f"\n" + "=" * 60)
    print(f"🎯 Le système est prêt et fonctionnel !")

if __name__ == "__main__":
    demonstrate_rarity_change()
