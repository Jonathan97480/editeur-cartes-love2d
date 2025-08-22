#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaires pour les tests - gestion des imports
"""
import sys
import os

def setup_test_environment():
    """Configure l'environnement pour les tests dans le sous-dossier tests/"""
    # Ajouter le répertoire parent au path pour importer lib
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    return parent_dir

# Configuration automatique lors de l'import
setup_test_environment()
