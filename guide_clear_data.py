#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guide d'utilisation de la fonctionnalité Clear Data
"""

def afficher_guide_clear_data():
    """Affiche le guide complet de la fonctionnalité Clear Data."""
    
    print("🗑️ GUIDE CLEAR DATA - SUPPRESSION COMPLÈTE")
    print("=" * 60)
    
    print("\n🎯 OBJECTIF :")
    print("   La fonctionnalité Clear Data permet de remettre l'application")
    print("   dans un état complètement vierge en supprimant toutes les données.")
    
    print("\n📍 LOCALISATION :")
    print("   Menu : 🔧 Réglages → 🗑️ Clear Data (Vider tout)")
    print("   Position : En bas du menu Réglages")
    
    print("\n🗑️ QUE SUPPRIME CLEAR DATA ?")
    print("\n   📄 BASE DE DONNÉES :")
    print("      • TOUTES les cartes (joueur, IA, acteurs)")
    print("      • TOUS les acteurs créés")
    print("      • TOUTES les liaisons cartes-acteurs")
    print("      • TOUTES les données de configuration")
    print("      • Réinitialisation des compteurs auto-increment")
    
    print("\n   🖼️ FICHIERS IMAGES :")
    print("      • Tous les fichiers du dossier images/")
    print("      • Tous les sous-dossiers et leurs contenus")
    print("      • Images de cartes générées automatiquement")
    print("      • Templates personnalisés")
    print("      • Recréation d'un dossier images/ vide")
    
    print("\n⚠️ SYSTÈME DE SÉCURITÉ :")
    
    print("\n   🛡️ DOUBLE CONFIRMATION :")
    print("      1️⃣ Première fenêtre : Explication des conséquences")
    print("         → Bouton Oui/Non avec avertissement détaillé")
    
    print("      2️⃣ Seconde fenêtre : Confirmation par saisie")
    print("         → Vous devez taper exactement : 'SUPPRIMER TOUT'")
    print("         → Texte masqué pour éviter les erreurs")
    
    print("\n   🚨 POINTS DE SÉCURITÉ :")
    print("      • Action IRRÉVERSIBLE - aucun retour en arrière")
    print("      • Pas de sauvegarde automatique avant suppression")
    print("      • Messages d'avertissement explicites")
    print("      • Annulation possible à chaque étape")
    
    print("\n🔄 PROCESSUS DÉTAILLÉ :")
    
    print("\n   📋 ÉTAPE 1 : Déclenchement")
    print("      • Clic sur 'Clear Data (Vider tout)' dans le menu")
    print("      • Ouverture de la première fenêtre d'avertissement")
    
    print("\n   📋 ÉTAPE 2 : Premier avertissement")
    print("      • Affichage détaillé des données qui seront supprimées")
    print("      • Choix Oui/Non pour continuer")
    print("      • Annulation possible → Retour à l'application")
    
    print("\n   📋 ÉTAPE 3 : Confirmation stricte")
    print("      • Demande de saisie du code 'SUPPRIMER TOUT'")
    print("      • Vérification exacte (sensible à la casse)")
    print("      • Annulation si code incorrect")
    
    print("\n   📋 ÉTAPE 4 : Exécution")
    print("      • Suppression de tous les fichiers images/")
    print("      • Vidage complet de la base de données")
    print("      • Actualisation de l'interface utilisateur")
    
    print("\n   📋 ÉTAPE 5 : Confirmation finale")
    print("      • Message de succès ou d'erreur")
    print("      • Application dans un état vierge")
    
    print("\n✅ RÉSULTAT ATTENDU :")
    
    print("\n   🎯 APPLICATION VIERGE :")
    print("      • Interface sans aucune carte")
    print("      • Listes d'acteurs vides")
    print("      • Dossier images/ recréé et vide")
    print("      • Compteurs remis à zéro")
    print("      • Prêt pour une nouvelle utilisation")
    
    print("\n   📊 MÉTRIQUES POST-SUPPRESSION :")
    print("      • Cartes : 0")
    print("      • Acteurs : 0")
    print("      • Liaisons : 0")
    print("      • Fichiers images : 0")
    print("      • Taille base de données : minimale")
    
    print("\n🎯 CAS D'UTILISATION :")
    
    print("\n   🔄 REMISE À ZÉRO COMPLÈTE :")
    print("      • Démarrer un nouveau projet de cartes")
    print("      • Nettoyer après des tests massifs")
    print("      • Résoudre des problèmes de corruption")
    print("      • Libérer de l'espace disque")
    
    print("\n   🧪 DÉVELOPPEMENT ET TESTS :")
    print("      • Nettoyer les données de test")
    print("      • Repartir sur une base saine")
    print("      • Valider les migrations")
    print("      • Tester l'application vierge")
    
    print("\n   🚀 PRÉPARATION DISTRIBUTION :")
    print("      • Créer une version propre à distribuer")
    print("      • Supprimer les données personnelles")
    print("      • Réinitialiser pour un nouvel utilisateur")
    
    print("\n⚠️ PRÉCAUTIONS D'USAGE :")
    
    print("\n   💾 AVANT UTILISATION :")
    print("      • Faire une sauvegarde manuelle si nécessaire")
    print("      • Exporter les cartes importantes")
    print("      • Copier les images personnalisées")
    print("      • Noter les configurations spéciales")
    
    print("\n   🎯 ALTERNATIVE MOINS RADICALE :")
    print("      • Suppression manuelle de cartes spécifiques")
    print("      • Export puis réimport sélectif")
    print("      • Nettoyage partiel du dossier images/")
    
    print("\n   🚨 EN CAS DE PROBLÈME :")
    print("      • Clear Data ne résout pas les bugs logiciels")
    print("      • Contacter le support pour les erreurs persistantes")
    print("      • Vérifier l'intégrité des fichiers système")
    
    print("\n🔧 INFORMATIONS TECHNIQUES :")
    
    print("\n   📁 FICHIERS CONCERNÉS :")
    print("      • cartes.db (base de données SQLite)")
    print("      • images/ (dossier et tout son contenu)")
    print("      • Sous-dossiers images récursivement")
    
    print("\n   🏗️ OPÉRATIONS SYSTÈME :")
    print("      • DELETE FROM pour chaque table")
    print("      • DELETE FROM sqlite_sequence")
    print("      • os.unlink() pour chaque fichier")
    print("      • os.rmdir() pour dossiers vides")
    print("      • os.mkdir() pour recréer images/")
    
    print("\n   ⚡ PERFORMANCES :")
    print("      • Temps d'exécution : < 5 secondes typiquement")
    print("      • Dépend du nombre de fichiers images")
    print("      • Opération atomique pour la base de données")
    
    print("\n🎊 APRÈS CLEAR DATA :")
    
    print("\n   🚀 REDÉMARRAGE RECOMMANDÉ :")
    print("      • Relancer l'application pour un état optimal")
    print("      • Vérifier que tous les compteurs sont à zéro")
    print("      • Tester la création d'une nouvelle carte")
    
    print("\n   📚 DOCUMENTATION À JOUR :")
    print("      • Ce guide reste valide après Clear Data")
    print("      • Fonctionnalités de l'application inchangées")
    print("      • Templates et configurations par défaut disponibles")
    
    print("\n" + "=" * 60)
    print("🎯 CLEAR DATA : SUPPRESSION COMPLÈTE ET SÉCURISÉE")
    print("🛡️ UTILISEZ AVEC PRÉCAUTION - ACTION IRRÉVERSIBLE")
    print("=" * 60)

if __name__ == "__main__":
    afficher_guide_clear_data()
