#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'organisation automatique du projet Love2D Card Editor
Applique toutes les améliorations de structure, sécurité et qualité de code
puis lance les tests de validation
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import sqlite3
import json

def get_python_executable():
    """Retourne le chemin vers l'exécutable Python correct"""
    # Chemin vers l'environnement Conda configuré
    conda_python = r"C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe"
    
    if os.path.exists(conda_python):
        return conda_python
    
    # Fallback vers l'exécutable Python actuel
    return sys.executable

def log_info(message):
    """Affiche un message d'information"""
    print(f"ℹ️  {message}")

def log_success(message):
    """Affiche un message de succès"""
    print(f"✅ {message}")

def log_warning(message):
    """Affiche un message d'avertissement"""
    print(f"⚠️  {message}")

def log_error(message):
    """Affiche un message d'erreur"""
    print(f"❌ {message}")

def creer_dossier_securise(chemin):
    """Crée un dossier de manière sécurisée"""
    try:
        Path(chemin).mkdir(exist_ok=True)
        return True
    except Exception as e:
        log_error(f"Impossible de créer le dossier {chemin}: {e}")
        return False

def deplacer_fichier_securise(source, destination):
    """Déplace un fichier de manière sécurisée"""
    try:
        if os.path.exists(source):
            shutil.move(source, destination)
            return True
        return False
    except Exception as e:
        log_error(f"Impossible de déplacer {source} vers {destination}: {e}")
        return False

def organiser_structure_dossiers():
    """Organise la structure des dossiers du projet"""
    log_info("Organisation de la structure des dossiers...")
    
    # Créer les dossiers principaux
    dossiers = [
        "data",           # Base de données sécurisée
        "logs",           # Logs de l'application
        "tests",          # Tests unitaires
        "docs",           # Documentation technique
        "guides",         # Guides utilisateur
        "rapports",       # Rapports d'analyse
        "dbBackup",       # Sauvegardes de base de données
        "luaBackup",      # Sauvegardes Lua
        "imagesBackup"    # Sauvegardes d'images
    ]
    
    for dossier in dossiers:
        if creer_dossier_securise(dossier):
            log_success(f"Dossier {dossier}/ créé")
    
    return True

def deplacer_base_donnees():
    """Déplace la base de données vers le dossier data/"""
    log_info("Déplacement de la base de données vers data/...")
    
    # Vérifier si la base est déjà dans data/
    if os.path.exists("data/cartes.db"):
        log_success("Base de données déjà dans data/cartes.db")
        return True
    
    # Sinon, chercher la base dans le dossier racine
    if os.path.exists("cartes.db"):
        if deplacer_fichier_securise("cartes.db", "data/cartes.db"):
            log_success("Base de données déplacée vers data/cartes.db")
            return True
        else:
            log_error("Échec du déplacement de la base de données")
            return False
    else:
        # Créer une base de données vide si aucune n'existe
        try:
            import sqlite3
            with sqlite3.connect("data/cartes.db") as conn:
                # Créer les tables de base
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS cards (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        cost INTEGER DEFAULT 0,
                        attack INTEGER DEFAULT 0,
                        defense INTEGER DEFAULT 0,
                        description TEXT,
                        image_path TEXT,
                        rarity TEXT DEFAULT 'Commun',
                        types_json TEXT DEFAULT '{}',
                        final_image_path TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
            log_success("Nouvelle base de données créée dans data/cartes.db")
            return True
        except Exception as e:
            log_error(f"Impossible de créer une nouvelle base de données: {e}")
            return False

def organiser_fichiers_backup():
    """Organise les fichiers de sauvegarde"""
    log_info("Organisation des fichiers de sauvegarde...")
    
    # Fichiers de sauvegarde de base de données
    fichiers_db = [f for f in os.listdir(".") if f.startswith("cartes_backup_") and f.endswith(".db")]
    for fichier in fichiers_db:
        if deplacer_fichier_securise(fichier, f"dbBackup/{fichier}"):
            log_success(f"Sauvegarde DB déplacée: {fichier}")
    
    # Fichiers de sauvegarde Lua
    fichiers_lua_backup = [f for f in os.listdir(".") if "backup" in f.lower() and f.endswith(".lua")]
    for fichier in fichiers_lua_backup:
        if deplacer_fichier_securise(fichier, f"luaBackup/{fichier}"):
            log_success(f"Sauvegarde Lua déplacée: {fichier}")
    
    # Dossiers de sauvegarde d'images
    if os.path.exists("images_backup"):
        if deplacer_fichier_securise("images_backup", "imagesBackup/images_backup"):
            log_success("Dossier images_backup déplacé")
    
    return True

def organiser_documentation():
    """Organise les fichiers de documentation"""
    log_info("Organisation de la documentation...")
    
    # Documentation technique
    docs_patterns = ["ARCHITECTURE", "CHANGELOG", "MIGRATION", "TECHNICAL", "API"]
    fichiers_docs = [f for f in os.listdir(".") if any(pattern in f.upper() for pattern in docs_patterns) and f.endswith(".md")]
    
    for fichier in fichiers_docs:
        if deplacer_fichier_securise(fichier, f"docs/{fichier}"):
            log_success(f"Documentation déplacée: {fichier}")
    
    # Guides utilisateur
    guides_patterns = ["GUIDE", "MANUEL", "HOWTO", "TUTORIAL"]
    fichiers_guides = [f for f in os.listdir(".") if any(pattern in f.upper() for pattern in guides_patterns) and f.endswith(".md")]
    
    for fichier in fichiers_guides:
        if deplacer_fichier_securise(fichier, f"guides/{fichier}"):
            log_success(f"Guide déplacé: {fichier}")
    
    # Rapports
    rapports_patterns = ["RAPPORT", "ANALYSIS", "AUDIT", "DIAGNOSTIC", "VERIFICATION"]
    fichiers_rapports = [f for f in os.listdir(".") if any(pattern in f.upper() for pattern in rapports_patterns) and (f.endswith(".md") or f.endswith(".py"))]
    
    for fichier in fichiers_rapports:
        if deplacer_fichier_securise(fichier, f"rapports/{fichier}"):
            log_success(f"Rapport déplacé: {fichier}")
    
    return True

def organiser_tests():
    """Organise les fichiers de tests"""
    log_info("Organisation des tests...")
    
    # Fichiers de tests
    fichiers_tests = [f for f in os.listdir(".") if (f.startswith("test_") or f.startswith("validation") or f.startswith("verification")) and f.endswith(".py") and f != "test.py"]
    
    for fichier in fichiers_tests:
        if deplacer_fichier_securise(fichier, f"tests/{fichier}"):
            log_success(f"Test déplacé: {fichier}")
    
    return True

def creer_systeme_logging():
    """Crée le système de logging centralisé"""
    log_info("Création du système de logging centralisé...")
    
    # Vérifier si le fichier existe déjà et semble correct
    if os.path.exists("lib/logging_utils.py"):
        try:
            with open("lib/logging_utils.py", "r", encoding="utf-8") as f:
                contenu = f.read()
            if "safe_print" in contenu and "def log_info" in contenu:
                log_success("Système de logging déjà présent et correct")
                return True
        except Exception:
            pass  # Continuer avec la recréation
    
    contenu_logging = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de logging centralisé pour l'éditeur de cartes Love2D
Remplace les instructions print() par un logging professionnel
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

def setup_logging(log_level=logging.INFO):
    """Configure le système de logging"""
    # Créer le dossier logs s'il n'existe pas
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Nom du fichier de log avec timestamp
    log_filename = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configuration du logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # Aussi afficher dans la console
        ]
    )
    
    return logging.getLogger(__name__)

def get_logger():
    """Retourne le logger configuré"""
    return logging.getLogger(__name__)

def safe_print(prefix, message):
    """Affichage sécurisé qui gère les problèmes d'encodage"""
    try:
        # Tenter d'abord avec les émojis
        if prefix == "INFO":
            print(f"ℹ️  {message}")
        elif prefix == "WARNING":
            print(f"⚠️  {message}")
        elif prefix == "ERROR":
            print(f"❌ {message}")
        elif prefix == "SUCCESS":
            print(f"✅ {message}")
        else:
            print(f"[{prefix}] {message}")
    except (UnicodeEncodeError, UnicodeError):
        # Fallback sans émojis si problème d'encodage
        print(f"[{prefix}] {message}")

def log_info(message):
    """Log un message d'information"""
    logger = get_logger()
    logger.info(message)
    safe_print("INFO", message)

def log_warning(message):
    """Log un message d'avertissement"""
    logger = get_logger()
    logger.warning(message)
    safe_print("WARNING", message)

def log_error(message):
    """Log un message d'erreur"""
    logger = get_logger()
    logger.error(message)
    safe_print("ERROR", message)

def log_success(message):
    """Log un message de succès"""
    logger = get_logger()
    logger.info(f"SUCCESS: {message}")
    safe_print("SUCCESS", message)
'''
    
    try:
        with open("lib/logging_utils.py", "w", encoding="utf-8") as f:
            f.write(contenu_logging)
        log_success("Système de logging créé: lib/logging_utils.py")
        return True
    except Exception as e:
        log_error(f"Impossible de créer le système de logging: {e}")
        return False

def mettre_a_jour_configuration():
    """Met à jour les fichiers de configuration"""
    log_info("Mise à jour de la configuration...")
    
    # Mise à jour de lib/config.py
    try:
        if os.path.exists("lib/config.py"):
            with open("lib/config.py", "r", encoding="utf-8") as f:
                contenu = f.read()
            
            # Remplacer le chemin de la base de données
            nouveau_contenu = contenu.replace('DB_FILE = "cartes.db"', 'DB_FILE = "data/cartes.db"')
            
            with open("lib/config.py", "w", encoding="utf-8") as f:
                f.write(nouveau_contenu)
            
            log_success("Configuration mise à jour: lib/config.py")
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour de lib/config.py: {e}")
    
    # Mise à jour de lib/utils.py pour le nouveau chemin
    try:
        if os.path.exists("lib/utils.py"):
            with open("lib/utils.py", "r", encoding="utf-8") as f:
                contenu = f.read()
            
            # Remplacer la fonction default_db_path
            ancien_code = '''def default_db_path():
    """Retourne le chemin par défaut de la base de données."""
    return "cartes.db"'''
            
            nouveau_code = '''def default_db_path():
    """Retourne le chemin par défaut de la base de données."""
    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)
    return "data/cartes.db"'''
            
            if ancien_code in contenu:
                nouveau_contenu = contenu.replace(ancien_code, nouveau_code)
                with open("lib/utils.py", "w", encoding="utf-8") as f:
                    f.write(nouveau_contenu)
                log_success("Configuration mise à jour: lib/utils.py")
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour de lib/utils.py: {e}")
    
    return True

def mettre_a_jour_gitignore():
    """Met à jour le fichier .gitignore"""
    log_info("Mise à jour du .gitignore...")
    
    ajouts_gitignore = """
# Dossier de données sensibles
data/
data/*.db

# Logs
logs/
*.log

# Sauvegardes automatiques
*_backup_*
backup_*

# Fichiers temporaires
temp/
tmp/
"""
    
    try:
        with open(".gitignore", "a", encoding="utf-8") as f:
            f.write(ajouts_gitignore)
        log_success("Fichier .gitignore mis à jour")
        return True
    except Exception as e:
        log_error(f"Impossible de mettre à jour .gitignore: {e}")
        return False

def optimiser_imports_app_final():
    """Optimise les imports et le formatage dans app_final.py"""
    log_info("Optimisation de app_final.py...")
    
    try:
        if not os.path.exists("app_final.py"):
            log_warning("app_final.py non trouvé, optimisation ignorée")
            return True
        
        with open("app_final.py", "r", encoding="utf-8") as f:
            contenu = f.read()
        
        # Ajouter l'import du système de logging après les autres imports
        if "from lib.logging_utils import" not in contenu:
            # Chercher la ligne des imports tkinter
            lignes = contenu.split("\n")
            for i, ligne in enumerate(lignes):
                if "from tkinter import ttk, messagebox, filedialog" in ligne:
                    lignes.insert(i + 1, "from lib.logging_utils import log_info, log_warning, log_error, log_success, setup_logging")
                    break
            
            contenu = "\n".join(lignes)
        
        # Remplacer quelques instructions print() courantes
        remplacements = [
            ('print(f"Erreur avec settings_window: {e}")', 'log_error(f"Erreur avec settings_window: {e}")'),
            ('print(f"🗑️ {len(deleted_files)} fichiers supprimés du dossier images/")', 'log_success(f"🗑️ {len(deleted_files)} fichiers supprimés du dossier images/")'),
            ('print(f"🗑️ Toutes les données supprimées de {len(tables)} tables")', 'log_success(f"🗑️ Toutes les données supprimées de {len(tables)} tables")'),
            ('print(f"[INFO] Ouverture du guide: {guide_path}")', 'log_info(f"[INFO] Ouverture du guide: {guide_path}")'),
            ('print("Exécution des tests...")', 'log_info("Execution des tests...")'),
            ('print("Scripts générés :", paths)', 'log_info(f"Scripts generes : {paths}")'),
            ('print("🚀 Démarrage de l\'éditeur de cartes Love2D...")', 'log_info("🚀 Demarrage de l\'editeur de cartes Love2D...")'),
            ('print("=" * 50)', 'log_info("=" * 50)'),
            ('print("✅ Base de données initialisée et vérifiée")', 'log_success("✅ Base de donnees initialisee et verifiee")'),
            ('print(f"❌ Erreur lors de l\'initialisation de la base de données :")', 'log_error(f"❌ Erreur lors de l\'initialisation de la base de donnees :")'),
            ('print(f"   {e}")', 'log_error(f"   {e}")'),
            ('print("❌ Arrêt de l\'application.")', 'log_error("❌ Arret de l\'application.")'),
            ('print("⚠️  Mode de compatibilité activé (legacy)")', 'log_warning("⚠️  Mode de compatibilite active (legacy)")')
        ]
        
        for ancien, nouveau in remplacements:
            contenu = contenu.replace(ancien, nouveau)
        
        # Ajouter setup_logging() au début de main si pas déjà présent
        if "setup_logging()" not in contenu:
            contenu = contenu.replace(
                'log_info("🚀 Demarrage de l\'editeur de cartes Love2D...")',
                'setup_logging()\n    log_info("🚀 Demarrage de l\'editeur de cartes Love2D...")'
            )
        
        with open("app_final.py", "w", encoding="utf-8") as f:
            f.write(contenu)
        
        log_success("app_final.py optimisé")
        return True
    except Exception as e:
        log_error(f"Erreur lors de l'optimisation de app_final.py: {e}")
        return False

def executer_tests():
    """Exécute tous les tests pour vérifier que l'organisation fonctionne"""
    log_info("Exécution des tests de validation...")
    
    try:
        # Lancer les tests intégrés avec le bon environnement Python
        python_exe = get_python_executable()
        result = subprocess.run([
            python_exe, "app_final.py", "--test"
        ], capture_output=True, text=True, cwd=".", encoding='utf-8', errors='replace')
        
        # Vérifier si les tests ont réussi en analysant la sortie
        success_indicators = ["OK", "Ran", "tests in"]
        failure_indicators = ["FAILED", "ERROR", "FAIL"]
        
        output_text = result.stdout + result.stderr
        
        # Analyser la sortie pour déterminer le succès
        has_success = any(indicator in output_text for indicator in success_indicators)
        has_failure = any(indicator in output_text for indicator in failure_indicators)
        
        if result.returncode == 0 and has_success and not has_failure:
            log_success("Tous les tests sont passés avec succès !")
            # Afficher seulement les lignes importantes
            lines = result.stdout.split('\n')
            for line in lines:
                if any(word in line for word in ["test_", "Ran", "OK", "tests in"]):
                    print(line)
            return True
        else:
            log_error("Certains tests ont échoué")
            print("Sortie complète:")
            print(result.stdout)
            if result.stderr:
                print("Erreurs:")
                print(result.stderr)
            return False
    except Exception as e:
        log_error(f"Erreur lors de l'exécution des tests: {e}")
        return False

def creer_script_maintenance():
    """Crée un script de maintenance pour les futures organisations"""
    log_info("Création du script de maintenance...")
    
    contenu_maintenance = '''#!/usr/bin/env python3
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
'''
    
    try:
        with open("maintenance.py", "w", encoding="utf-8") as f:
            f.write(contenu_maintenance)
        log_success("Script de maintenance créé: maintenance.py")
        return True
    except Exception as e:
        log_error(f"Impossible de créer le script de maintenance: {e}")
        return False

def main():
    """Fonction principale d'organisation automatique"""
    print("🚀 ORGANISATION AUTOMATIQUE DU PROJET LOVE2D CARD EDITOR")
    print("=" * 70)
    print()
    
    # Vérifier qu'on est dans le bon dossier
    if not os.path.exists("app_final.py"):
        log_error("app_final.py non trouvé. Exécutez ce script depuis le dossier racine du projet.")
        return False
    
    etapes = [
        ("Organisation des dossiers", organiser_structure_dossiers),
        ("Déplacement de la base de données", deplacer_base_donnees),
        ("Organisation des sauvegardes", organiser_fichiers_backup),
        ("Organisation de la documentation", organiser_documentation),
        ("Organisation des tests", organiser_tests),
        ("Création du système de logging", creer_systeme_logging),
        ("Mise à jour de la configuration", mettre_a_jour_configuration),
        ("Mise à jour du .gitignore", mettre_a_jour_gitignore),
        ("Optimisation du code principal", optimiser_imports_app_final),
        ("Création du script de maintenance", creer_script_maintenance)
    ]
    
    succes = 0
    for nom_etape, fonction_etape in etapes:
        print(f"\n📋 {nom_etape}...")
        if fonction_etape():
            succes += 1
        else:
            log_warning(f"Étape '{nom_etape}' partiellement échouée")
    
    print(f"\n📊 RÉSULTATS: {succes}/{len(etapes)} étapes réussies")
    
    # Tests finaux
    print("\n🧪 TESTS DE VALIDATION...")
    if executer_tests():
        print("\n🎉 ORGANISATION TERMINÉE AVEC SUCCÈS !")
        print("Le projet est maintenant organisé avec une structure professionnelle.")
        print()
        print("📁 Structure créée:")
        print("  ├── data/           # Base de données sécurisée")
        print("  ├── logs/           # Logs de l'application")
        print("  ├── tests/          # Tests unitaires")
        print("  ├── docs/           # Documentation technique")
        print("  ├── guides/         # Guides utilisateur")
        print("  ├── rapports/       # Rapports d'analyse")
        print("  ├── dbBackup/       # Sauvegardes DB")
        print("  ├── luaBackup/      # Sauvegardes Lua")
        print("  └── imagesBackup/   # Sauvegardes images")
        print()
        print("🔧 Améliorations appliquées:")
        print("  ✅ Sécurité: Base de données dans data/")
        print("  ✅ Logging: Système centralisé")
        print("  ✅ Structure: Organisation professionnelle")
        print("  ✅ Tests: Validation automatique")
        print()
        print("💡 Utilisation:")
        print("  • Exécutez 'python maintenance.py' pour la maintenance")
        print("  • Les logs sont dans le dossier logs/")
        print("  • La base de données est sécurisée dans data/")
        
        return True
    else:
        log_error("Des problèmes ont été détectés lors des tests")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
