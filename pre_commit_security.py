#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de sécurité pré-commit avec tests globaux et audit complet
Génère des rapports détaillés dans commit_reports/
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

# Configuration pour éviter les problèmes d'encodage Unicode
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class PreCommitSecurity:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "commit_reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Timestamp pour le rapport
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_prefix = f"commit_report_{self.timestamp}"
        
        self.python_exe = self.get_python_executable()
        
    def get_python_executable(self):
        """Retourne le chemin vers l'exécutable Python correct"""
        conda_python = r"C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe"
        if os.path.exists(conda_python):
            return conda_python
        return sys.executable
    
    def run_command(self, command, cwd=None, capture_output=True, timeout=30):
        """Exécute une commande et retourne le résultat"""
        try:
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
            return result
        except subprocess.TimeoutExpired:
            return type('Result', (), {
                'returncode': 124,  # Code pour timeout
                'stdout': '',
                'stderr': f'Timeout après {timeout}s'
            })()
        except Exception as e:
            return type('Result', (), {
                'returncode': 1,
                'stdout': '',
                'stderr': str(e)
            })()
    
    def test_application_integrity(self):
        """Lance les tests complets de l'application"""
        print("🧪 TESTS D'INTÉGRITÉ DE L'APPLICATION")
        print("=" * 50)
        
        test_results = {
            'timestamp': self.timestamp,
            'status': 'PASS',
            'tests': {},
            'summary': {}
        }
        
        # Test 1: Syntaxe Python
        print("📝 Test syntaxe Python...")
        python_files = list(self.project_root.glob("*.py"))
        syntax_errors = []
        
        for py_file in python_files:
            if py_file.name.startswith('.'):
                continue
            result = self.run_command([self.python_exe, "-m", "py_compile", str(py_file)])
            if result.returncode != 0:
                syntax_errors.append({
                    'file': str(py_file),
                    'error': result.stderr
                })
        
        test_results['tests']['syntax'] = {
            'status': 'PASS' if not syntax_errors else 'FAIL',
            'files_tested': len(python_files),
            'errors': syntax_errors
        }
        
        # Test 2: Application principale
        print("🎮 Test application principale...")
        app_result = self.run_command([self.python_exe, "app_final.py", "--test"])
        test_results['tests']['main_app'] = {
            'status': 'PASS' if app_result.returncode == 0 else 'FAIL',
            'output': app_result.stdout,
            'errors': app_result.stderr
        }
        
        # Test 3: Base de données
        print("🗄️ Test base de données...")
        db_result = self.run_command([self.python_exe, "db_tools.py", "--validate"])
        test_results['tests']['database'] = {
            'status': 'PASS' if db_result.returncode == 0 else 'FAIL',
            'output': db_result.stdout,
            'errors': db_result.stderr
        }
        
        # Test 4: Scripts de configuration
        print("⚙️ Test scripts configuration...")
        config_result = self.run_command([self.python_exe, "configure_python_env.py", "--check"])
        test_results['tests']['configuration'] = {
            'status': 'PASS' if config_result.returncode == 0 else 'FAIL',
            'output': config_result.stdout,
            'errors': config_result.stderr
        }
        
        # Test 5: Validation automatique
        print("✅ Test validation automatique...")
        validation_result = self.run_command([self.python_exe, "validate_tests_auto.py"])
        test_results['tests']['validation'] = {
            'status': 'PASS' if validation_result.returncode == 0 else 'FAIL',
            'output': validation_result.stdout,
            'errors': validation_result.stderr
        }
        
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
        
        print(f"📊 Résumé: {passed_tests}/{total_tests} tests réussis ({test_results['summary']['success_rate']:.1f}%)")
        
        return test_results
    
    def run_security_audit(self):
        """Exécute un audit de sécurité complet"""
        print("\nAUDIT DE SECURITE")
        print("=" * 50)
        
        audit_results = {
            'timestamp': self.timestamp,
            'status': 'PASS',
            'checks': {},
            'summary': {}
        }
        
        # Audit 1: Fichiers sensibles
        print("🔍 Vérification fichiers sensibles...")
        sensitive_patterns = ['.env', '.key', '.secret', 'password', '.config']
        sensitive_files = []
        
        for pattern in sensitive_patterns:
            files = list(self.project_root.rglob(f"*{pattern}*"))
            for f in files:
                if f.is_file() and not f.name.startswith('.git'):
                    sensitive_files.append(str(f))
        
        audit_results['checks']['sensitive_files'] = {
            'status': 'PASS' if not sensitive_files else 'WARNING',
            'files_found': sensitive_files,
            'count': len(sensitive_files)
        }
        
        # Audit 2: Permissions et accès
        print("🛡️ Vérification permissions...")
        critical_files = ['app_final.py', 'data/cartes.db', 'START.bat', 'UPDATE.bat']
        permission_issues = []
        
        for file_path in critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                try:
                    # Test d'accès en lecture
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        f.read(100)
                except Exception as e:
                    permission_issues.append({
                        'file': file_path,
                        'issue': str(e)
                    })
        
        audit_results['checks']['permissions'] = {
            'status': 'PASS' if not permission_issues else 'FAIL',
            'issues': permission_issues,
            'files_checked': len(critical_files)
        }
        
        # Audit 3: Structure projet
        print("📁 Vérification structure projet...")
        required_dirs = ['dev', 'data', 'legacy', 'commit_reports']
        required_files = ['START.bat', 'UPDATE.bat', 'app_final.py', 'README_GITHUB.md']
        
        missing_dirs = [d for d in required_dirs if not (self.project_root / d).exists()]
        missing_files = [f for f in required_files if not (self.project_root / f).exists()]
        
        audit_results['checks']['structure'] = {
            'status': 'PASS' if not missing_dirs and not missing_files else 'FAIL',
            'missing_directories': missing_dirs,
            'missing_files': missing_files,
            'structure_score': ((len(required_dirs) - len(missing_dirs) + len(required_files) - len(missing_files)) / 
                               (len(required_dirs) + len(required_files)) * 100)
        }
        
        # Audit 4: Git état
        print("📋 Vérification état Git...")
        git_status = self.run_command(["git", "status", "--porcelain"])
        git_log = self.run_command(["git", "log", "--oneline", "-5"])
        
        audit_results['checks']['git_status'] = {
            'status': 'PASS',
            'staged_files': len([line for line in git_status.stdout.splitlines() if line.startswith('A')]),
            'modified_files': len([line for line in git_status.stdout.splitlines() if line.startswith('M')]),
            'recent_commits': git_log.stdout.splitlines()[:5]
        }
        
        # Audit 5: Dépendances et environnement
        print("🔧 Vérification environnement...")
        python_version = self.run_command([self.python_exe, "--version"])
        
        audit_results['checks']['environment'] = {
            'status': 'PASS',
            'python_version': python_version.stdout.strip() if python_version.returncode == 0 else 'Unknown',
            'python_path': self.python_exe,
            'working_directory': str(self.project_root)
        }
        
        # Résumé audit
        total_checks = len(audit_results['checks'])
        passed_checks = sum(1 for check in audit_results['checks'].values() if check['status'] == 'PASS')
        warning_checks = sum(1 for check in audit_results['checks'].values() if check['status'] == 'WARNING')
        failed_checks = total_checks - passed_checks - warning_checks
        
        audit_results['summary'] = {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'warning_checks': warning_checks,
            'failed_checks': failed_checks,
            'security_score': (passed_checks / total_checks * 100) if total_checks > 0 else 0
        }
        
        if failed_checks > 0:
            audit_results['status'] = 'FAIL'
        elif warning_checks > 0:
            audit_results['status'] = 'WARNING'
        
        print(f"Resume audit: {passed_checks} PASS, {warning_checks} WARNING, {failed_checks} FAIL")
        
        return audit_results
    
    def generate_reports(self, test_results, audit_results):
        """Génère les rapports finaux"""
        print(f"\n📄 GÉNÉRATION DES RAPPORTS")
        print("=" * 50)
        
        # Rapport JSON détaillé
        json_report = {
            'metadata': {
                'timestamp': self.timestamp,
                'date': datetime.now().isoformat(),
                'project': 'editeur-cartes-love2d',
                'python_executable': self.python_exe
            },
            'tests': test_results,
            'audit': audit_results,
            'overall_status': 'PASS' if test_results['status'] == 'PASS' and audit_results['status'] in ['PASS', 'WARNING'] else 'FAIL'
        }
        
        json_file = self.reports_dir / f"{self.report_prefix}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
        
        # Rapport Markdown lisible
        md_report = self.generate_markdown_report(test_results, audit_results)
        md_file = self.reports_dir / f"{self.report_prefix}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_report)
        
        # Rapport résumé court
        summary_report = self.generate_summary_report(test_results, audit_results)
        summary_file = self.reports_dir / f"{self.report_prefix}_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_report)
        
        print(f"✅ Rapports générés:")
        print(f"   📋 Détaillé: {json_file}")
        print(f"   📄 Markdown: {md_file}")
        print(f"   📝 Résumé: {summary_file}")
        
        return {
            'json_report': str(json_file),
            'markdown_report': str(md_file),
            'summary_report': str(summary_file),
            'overall_status': json_report['overall_status']
        }
    
    def generate_markdown_report(self, test_results, audit_results):
        """Génère un rapport Markdown lisible"""
        md = f"""# 🔒 Rapport de Sécurité Pré-Commit

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Projet**: Éditeur de cartes Love2D  
**Statut global**: {'✅ VALIDÉ' if test_results['status'] == 'PASS' and audit_results['status'] in ['PASS', 'WARNING'] else '❌ ÉCHEC'}

## 🧪 Tests d'Intégrité

**Résumé**: {test_results['summary']['passed_tests']}/{test_results['summary']['total_tests']} tests réussis ({test_results['summary']['success_rate']:.1f}%)

"""
        
        for test_name, test_data in test_results['tests'].items():
            status_emoji = "✅" if test_data['status'] == 'PASS' else "❌"
            md += f"### {status_emoji} {test_name.replace('_', ' ').title()}\n"
            md += f"**Statut**: {test_data['status']}\n"
            if test_data.get('errors'):
                md += f"**Erreurs**: {len(test_data['errors'])}\n"
            md += "\n"
        
        md += f"""## 🔒 Audit de Sécurité

**Score sécurité**: {audit_results['summary']['security_score']:.1f}%  
**Vérifications**: {audit_results['summary']['passed_checks']} PASS, {audit_results['summary']['warning_checks']} WARNING, {audit_results['summary']['failed_checks']} FAIL

"""
        
        for check_name, check_data in audit_results['checks'].items():
            status_emoji = "✅" if check_data['status'] == 'PASS' else "⚠️" if check_data['status'] == 'WARNING' else "❌"
            md += f"### {status_emoji} {check_name.replace('_', ' ').title()}\n"
            md += f"**Statut**: {check_data['status']}\n"
            md += "\n"
        
        md += f"""## 📊 Conclusion

{'🚀 **COMMIT AUTORISÉ** - Tous les tests sont valides' if test_results['status'] == 'PASS' and audit_results['status'] in ['PASS', 'WARNING'] else '🛑 **COMMIT BLOQUÉ** - Des erreurs doivent être corrigées'}

---
*Rapport généré automatiquement par le système de sécurité pré-commit*
"""
        
        return md
    
    def generate_summary_report(self, test_results, audit_results):
        """Génère un résumé court"""
        status = "PASS" if test_results['status'] == 'PASS' and audit_results['status'] in ['PASS', 'WARNING'] else "FAIL"
        
        summary = f"""RAPPORT SÉCURITÉ PRE-COMMIT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

STATUT GLOBAL: {status}

TESTS: {test_results['summary']['passed_tests']}/{test_results['summary']['total_tests']} réussis ({test_results['summary']['success_rate']:.1f}%)
AUDIT: {audit_results['summary']['security_score']:.1f}% sécurité

{'✅ COMMIT AUTORISÉ' if status == 'PASS' else '❌ COMMIT BLOQUÉ'}
"""
        return summary
    
    def run_full_security_check(self):
        """Lance la vérification complète de sécurité"""
        print("SYSTEME DE SECURITE PRE-COMMIT")
        print("=" * 60)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        try:
            # Tests d'intégrité
            test_results = self.test_application_integrity()
            
            # Audit de sécurité
            audit_results = self.run_security_audit()
            
            # Génération des rapports
            reports = self.generate_reports(test_results, audit_results)
            
            # Décision finale
            overall_status = reports['overall_status']
            
            print(f"\n🎯 DÉCISION FINALE")
            print("=" * 50)
            
            if overall_status == 'PASS':
                print("✅ COMMIT AUTORISÉ - Tous les tests passent")
                print("🚀 Le projet est prêt pour GitHub")
                return True
            else:
                print("❌ COMMIT BLOQUÉ - Des erreurs doivent être corrigées")
                print("⚠️ Consultez les rapports pour plus de détails")
                return False
                
        except Exception as e:
            print(f"💥 ERREUR CRITIQUE: {e}")
            return False

def main():
    """Fonction principale"""
    security = PreCommitSecurity()
    success = security.run_full_security_check()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
