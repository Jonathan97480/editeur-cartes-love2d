#!/usr/bin/env python3
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
