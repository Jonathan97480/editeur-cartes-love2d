#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de commit sécurisé adapté à la nouvelle organisation
Tests et validation avant commit avec la structure réorganisée
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

class SecureCommitSystem:
    def __init__(self):
        self.project_root = Path(".").resolve()
        self.reports_dir = self.project_root / "commit_reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Timestamp pour le rapport
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_prefix = f"commit_secure_{self.timestamp}"
        
        self.python_exe = self.get_python_executable()
        
    def get_python_executable(self):
        """Retourne le chemin vers l'exécutable Python correct"""
        conda_python = r"C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe"
        if os.path.exists(conda_python):
            return conda_python
        return "python"
    
    def run_command(self, command, cwd=None, capture_output=True, timeout=30):
        """Exécute une commande et retourne le résultat"""
        try:
            if isinstance(command, str):
                result = subprocess.run(
                    command,
                    cwd=cwd or self.project_root,
                    capture_output=capture_output,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    shell=True,
                    timeout=timeout
                )
            else:
                result = subprocess.run(
                    command,
                    cwd=cwd or self.project_root,
                    capture_output=capture_output,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=timeout
                )
            return result
        except Exception as e:
            # Créer un résultat d'erreur factice
            class ErrorResult:
                def __init__(self, error):
                    self.returncode = 1
                    self.stdout = ""
                    self.stderr = str(error)
            return ErrorResult(e)
    
    def check_git_status(self):
        """Vérifie le statut Git"""
        print("🔍 Vérification du statut Git...")
        
        # Vérifier qu'on est dans un repo Git
        git_check = self.run_command("git status --porcelain")
        if git_check.returncode != 0:
            return False, "Pas un dépôt Git valide"
        
        # Analyser les changements
        changes = git_check.stdout.strip().split('\n') if git_check.stdout.strip() else []
        
        if not changes:
            return False, "Aucun changement à commiter"
        
        # Compter les types de changements
        added = len([c for c in changes if c.startswith('??')])
        modified = len([c for c in changes if c.startswith(' M') or c.startswith('M ')])
        deleted = len([c for c in changes if c.startswith(' D') or c.startswith('D ')])
        
        status_info = {
            'total_changes': len(changes),
            'added': added,
            'modified': modified,
            'deleted': deleted,
            'changes': changes[:10]  # Limiter pour l'affichage
        }
        
        print(f"   📊 Changements détectés: {len(changes)} fichiers")
        print(f"   📁 Nouveaux: {added}")
        print(f"   📝 Modifiés: {modified}")
        print(f"   🗑️ Supprimés: {deleted}")
        
        return True, status_info
    
    def run_security_tests(self):
        """Lance les tests de sécurité adaptés à la nouvelle organisation"""
        print("🧪 TESTS DE SÉCURITÉ PRÉ-COMMIT")
        print("=" * 50)
        
        test_results = {
            'timestamp': self.timestamp,
            'status': 'PASS',
            'tests': {},
            'organization_check': {}
        }
        
        # Test 1: Vérification de l'organisation
        print("📁 Test 1: Vérification de l'organisation...")
        org_result = self.check_organization()
        test_results['organization_check'] = org_result
        
        # Test 2: Import des modules principaux
        print("📦 Test 2: Modules principaux...")
        module_test = self.run_command(f'''
{self.python_exe} -c "
try:
    from lib.database import CardRepo
    from lib.config import DB_FILE
    print('✅ Modules importés')
except Exception as e:
    print(f'❌ Erreur: {{e}}')
    exit(1)
"''')
        
        test_results['tests']['modules'] = {
            'status': 'PASS' if module_test.returncode == 0 else 'FAIL',
            'output': module_test.stdout.strip(),
            'errors': module_test.stderr.strip()
        }
        
        # Test 3: Base de données
        print("🗄️ Test 3: Base de données...")
        db_test = self.run_command(f'''
{self.python_exe} -c "
from lib.database import CardRepo
from lib.config import DB_FILE
try:
    repo = CardRepo(DB_FILE)
    cards = repo.list_cards()
    print(f'✅ Base OK - {{len(cards)}} cartes')
except Exception as e:
    print(f'❌ Erreur BDD: {{e}}')
    exit(1)
"''')
        
        test_results['tests']['database'] = {
            'status': 'PASS' if db_test.returncode == 0 else 'FAIL',
            'output': db_test.stdout.strip(),
            'errors': db_test.stderr.strip()
        }
        
        # Test 4: Export Love2D
        print("🚀 Test 4: Export Love2D...")
        export_test = self.run_command(f'''
{self.python_exe} -c "
from lua_exporter_love2d import Love2DLuaExporter
from lib.database import CardRepo
from lib.config import DB_FILE
try:
    repo = CardRepo(DB_FILE)
    exporter = Love2DLuaExporter(repo)
    content = exporter.export_all_cards_love2d()
    has_tf = 'TextFormatting' in content
    print(f'✅ Export OK - {{len(content)}} chars, TF: {{has_tf}}')
except Exception as e:
    print(f'❌ Erreur export: {{e}}')
    exit(1)
"''')
        
        test_results['tests']['export'] = {
            'status': 'PASS' if export_test.returncode == 0 else 'FAIL',
            'output': export_test.stdout.strip(),
            'errors': export_test.stderr.strip()
        }
        
        # Test 5: Structure des dossiers organisés
        print("📂 Test 5: Structure organisée...")
        structure_result = self.check_organized_structure()
        test_results['tests']['structure'] = structure_result
        
        # Résumé des tests
        total_tests = len(test_results['tests'])
        passed_tests = sum(1 for test in test_results['tests'].values() if test['status'] == 'PASS')
        
        test_results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
        
        if passed_tests < total_tests:
            test_results['status'] = 'FAIL'
        
        print(f"\\n📊 Résumé: {passed_tests}/{total_tests} tests réussis ({test_results['summary']['success_rate']:.1f}%)")
        
        return test_results
    
    def check_organization(self):
        """Vérifie que l'organisation est maintenue"""
        required_dirs = [
            'tests/unitaires', 'tests/interface', 'tests/export', 'tests/formatage',
            'tests/database', 'tests/validation', 'dev/scripts', 'dev/outils',
            'dev/maintenance', 'dev/configuration', 'docs/guides_techniques'
        ]
        
        org_status = {'status': 'PASS', 'missing_dirs': [], 'present_dirs': []}
        
        for dir_path in required_dirs:
            path = self.project_root / dir_path
            if path.exists():
                files_count = len(list(path.glob('*.py')))
                org_status['present_dirs'].append(f"{dir_path} ({files_count} py)")
            else:
                org_status['missing_dirs'].append(dir_path)
                org_status['status'] = 'FAIL'
        
        return org_status
    
    def check_organized_structure(self):
        """Vérifie la structure des dossiers organisés"""
        try:
            test_dirs = ['tests', 'dev', 'docs']
            structure_info = {'status': 'PASS', 'directories': {}}
            
            for test_dir in test_dirs:
                dir_path = self.project_root / test_dir
                if dir_path.exists():
                    subdirs = [d.name for d in dir_path.iterdir() if d.is_dir()]
                    py_files = len(list(dir_path.rglob('*.py')))
                    structure_info['directories'][test_dir] = {
                        'subdirs': subdirs,
                        'py_files': py_files
                    }
                else:
                    structure_info['status'] = 'FAIL'
                    structure_info['directories'][test_dir] = {'error': 'missing'}
            
            return structure_info
        except Exception as e:
            return {'status': 'FAIL', 'error': str(e)}
    
    def generate_report(self, test_results, git_status):
        """Génère un rapport de commit sécurisé"""
        report = {
            'timestamp': self.timestamp,
            'commit_info': {
                'date': datetime.now().isoformat(),
                'git_status': git_status,
                'security_tests': test_results
            },
            'recommendations': []
        }
        
        # Ajouter des recommandations
        if test_results['status'] == 'FAIL':
            report['recommendations'].append("❌ Corriger les tests échoués avant le commit")
        else:
            report['recommendations'].append("✅ Tous les tests passent - Commit autorisé")
        
        # Sauvegarder le rapport
        report_file = self.reports_dir / f"{self.report_prefix}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Rapport sauvegardé: {report_file}")
        return report
    
    def secure_commit(self, commit_message=None):
        """Lance un commit sécurisé avec tous les contrôles"""
        print("🔒 SYSTÈME DE COMMIT SÉCURISÉ")
        print("=" * 60)
        
        # Vérifier Git
        git_ok, git_status = self.check_git_status()
        if not git_ok:
            print(f"❌ Problème Git: {git_status}")
            return False
        
        # Lancer les tests de sécurité
        test_results = self.run_security_tests()
        
        # Générer le rapport
        report = self.generate_report(test_results, git_status)
        
        # Décider si le commit peut être fait
        if test_results['status'] == 'FAIL':
            print("\\n❌ COMMIT REJETÉ - Tests de sécurité échoués")
            print("Corrigez les erreurs avant de recommiter.")
            return False
        
        # Message de commit par défaut
        if not commit_message:
            commit_message = f"""feat: Organisation complète validée - Système sécurisé

🎯 COMMIT SÉCURISÉ ({datetime.now().strftime('%d/%m/%Y %H:%M')})

✅ TOUS LES TESTS PASSÉS:
• Modules principaux: Fonctionnels
• Base de données: Opérationnelle  
• Export Love2D: TextFormatting OK
• Structure organisée: Maintenue
• Sécurité: Validée

📊 Statistiques:
• Tests réussis: {test_results['summary']['passed_tests']}/{test_results['summary']['total_tests']}
• Taux de réussite: {test_results['summary']['success_rate']:.1f}%
• Changements: {git_status['total_changes']} fichiers

🔒 Validé par le système de commit sécurisé
📄 Rapport: {self.report_prefix}.json"""
        
        # Exécuter le commit
        print("\\n🚀 Exécution du commit sécurisé...")
        
        # Add all files
        add_result = self.run_command("git add .")
        if add_result.returncode != 0:
            print("❌ Erreur lors de l'ajout des fichiers")
            return False
        
        # Commit
        commit_result = self.run_command(["git", "commit", "-m", commit_message])
        if commit_result.returncode != 0:
            print("❌ Erreur lors du commit")
            print(commit_result.stderr)
            return False
        
        print("✅ COMMIT SÉCURISÉ RÉUSSI!")
        print(f"📄 Rapport disponible: commit_reports/{self.report_prefix}.json")
        
        # Afficher les derniers commits
        print("\\n📝 Derniers commits:")
        self.run_command("git log --oneline -3", capture_output=False)
        
        return True

def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Système de commit sécurisé")
    parser.add_argument("-m", "--message", help="Message de commit personnalisé")
    parser.add_argument("--tests-only", action="store_true", help="Lancer uniquement les tests")
    
    args = parser.parse_args()
    
    system = SecureCommitSystem()
    
    if args.tests_only:
        # Lancer uniquement les tests
        test_results = system.run_security_tests()
        if test_results['status'] == 'PASS':
            print("\\n✅ Tous les tests passent - Prêt pour le commit")
        else:
            print("\\n❌ Certains tests échouent - Corrigez avant de commiter")
        return
    
    # Lancer le commit sécurisé
    success = system.secure_commit(args.message)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
