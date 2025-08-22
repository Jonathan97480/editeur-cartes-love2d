#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de logging centralisé pour l'éditeur de cartes Love2D
Remplace les instructions print() par un logging professionnel
"""

import logging
import os
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

def log_info(message):
    """Log un message d'information"""
    logger = get_logger()
    logger.info(message)
    print(f"ℹ️  {message}")

def log_warning(message):
    """Log un message d'avertissement"""
    logger = get_logger()
    logger.warning(message)
    print(f"⚠️  {message}")

def log_error(message):
    """Log un message d'erreur"""
    logger = get_logger()
    logger.error(message)
    print(f"❌ {message}")

def log_success(message):
    """Log un message de succès"""
    logger = get_logger()
    logger.info(f"SUCCESS: {message}")
    print(f"✅ {message}")
