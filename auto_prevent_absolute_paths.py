#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SYSTÈME DE PRÉVENTION AUTOMATIQUE DES CHEMINS ABSOLUS
=========================================================

Ce script s'intègre au processus de démarrage pour:
1. Détecter les chemins absolus existants
2. Les corriger automatiquement
3. Prévenir les futurs problèmes
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

def run_prevention_system():
    """Lance le système de prévention complet"""
    
    print('🛡️ SYSTÈME DE PRÉVENTION DES CHEMINS ABSOLUS')
    print('=' * 55)
    
    # 1. Lancer la vérification directe (sans subprocess)
    print('🔍 Étape 1: Vérification de la base de données...')
    
    try:
        # Import direct pour éviter les problèmes d'encodage subprocess
        import check_database_paths
        import importlib
        importlib.reload(check_database_paths)
        
        issues = check_database_paths.check_database_paths()
        
        if len(issues) > 0:
            print(f'⚠️  {len(issues)} problèmes détectés - Correction en cours...')
            
            # 2. Lancer la correction directe
            import fix_database_paths
            importlib.reload(fix_database_paths)
            
            success = fix_database_paths.fix_database_paths()
            if success:
                print('✅ Chemins corrigés automatiquement')
            else:
                print('❌ Erreur lors de la correction')
        else:
            print('✅ Base de données propre')
            
    except Exception as e:
        print(f'❌ Erreur lors de la vérification: {e}')
    
    # 3. Vérifier que les corrections de code sont appliquées
    print('\n🔧 Étape 2: Vérification des corrections de code...')
    
    try:
        # Tester la fonction de validation
        from ui_components import validate_and_convert_path
        
        # Test rapide
        test_result = validate_and_convert_path('C:/test/images/cards/test.png')
        if not test_result.startswith('C:'):
            print('✅ Système de validation actif')
        else:
            print('❌ Système de validation défaillant')
            
    except ImportError:
        print('❌ Fonction de validation non trouvée - Corrections non appliquées')
        print('   → Relancez fix_absolute_path_sources.py')
    except Exception as e:
        print(f'❌ Erreur de validation: {e}')
    
    print('\n🎯 Système de prévention initialisé')
    print('   Les nouveaux chemins seront automatiquement convertis')

if __name__ == '__main__':
    run_prevention_system()
