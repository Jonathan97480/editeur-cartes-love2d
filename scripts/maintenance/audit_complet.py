#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT COMPLET DU PROJET EDITEUR-CARTES-LOVE2D
==============================================

Audit post-nettoyage pour évaluer :
- Structure du projet
- Qualité du code
- Fonctionnalités principales
- Tests et documentation
- Sécurité et bonnes pratiques
"""

import os
import ast
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime

class ProjectAuditor:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'project_structure': {},
            'code_quality': {},
            'functionality': {},
            'tests': {},
            'documentation': {},
            'security': {},
            'recommendations': []
        }
    
    def audit_project_structure(self):
        """Audit de la structure du projet"""
        print("📁 Audit de la structure du projet...")
        
        structure = {
            'total_files': 0,
            'python_files': 0,
            'directories': [],
            'essential_files': {},
            'organization_score': 0
        }
        
        # Analyser la structure
        for root, dirs, files in os.walk(self.project_root):
            relative_root = Path(root).relative_to(self.project_root)
            structure['directories'].append(str(relative_root))
            
            for file in files:
                structure['total_files'] += 1
                if file.endswith('.py'):
                    structure['python_files'] += 1
        
        # Vérifier les fichiers essentiels
        essential_files = {
            'README.md': self.project_root / 'README.md',
            'requirements.txt': self.project_root / 'requirements.txt',
            'LICENSE': self.project_root / 'LICENSE',
            'START.bat': self.project_root / 'START.bat',
            'app_final.py': self.project_root / 'app_final.py'
        }
        
        for name, path in essential_files.items():
            structure['essential_files'][name] = path.exists()
        
        # Score d'organisation (0-100)
        organization_checks = [
            ('lib/', (self.project_root / 'lib').is_dir()),
            ('tests/', (self.project_root / 'tests').is_dir()),
            ('docs/', (self.project_root / 'docs').is_dir()),
            ('data/', (self.project_root / 'data').is_dir()),
            ('images/', (self.project_root / 'images').is_dir()),
            ('No temp files', len(list(self.project_root.glob('*temp*'))) == 0),
            ('No test files at root', len(list(self.project_root.glob('test_*.py'))) == 0),
            ('Essential files', all(structure['essential_files'].values()))
        ]
        
        structure['organization_score'] = (sum(1 for _, check in organization_checks if check) / len(organization_checks)) * 100
        
        self.results['project_structure'] = structure
        print(f"   ✅ Structure analysée: {structure['total_files']} fichiers, {len(structure['directories'])} dossiers")
        print(f"   📊 Score d'organisation: {structure['organization_score']:.1f}%")
    
    def audit_code_quality(self):
        """Audit de la qualité du code"""
        print("🔍 Audit de la qualité du code...")
        
        quality = {
            'total_lines': 0,
            'python_modules': [],
            'complexity_issues': [],
            'import_issues': [],
            'docstring_coverage': 0,
            'quality_score': 0
        }
        
        lib_path = self.project_root / 'lib'
        if lib_path.exists():
            for py_file in lib_path.glob('*.py'):
                if py_file.name == '__init__.py':
                    continue
                
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    lines = len(content.splitlines())
                    quality['total_lines'] += lines
                    
                    # Analyser le AST
                    try:
                        tree = ast.parse(content)
                        module_info = {
                            'name': py_file.name,
                            'lines': lines,
                            'functions': 0,
                            'classes': 0,
                            'has_docstring': False
                        }
                        
                        # Vérifier la docstring du module
                        if (ast.get_docstring(tree)):
                            module_info['has_docstring'] = True
                        
                        # Compter fonctions et classes
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                module_info['functions'] += 1
                            elif isinstance(node, ast.ClassDef):
                                module_info['classes'] += 1
                        
                        # Détecter les fonctions complexes (>50 lignes)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                if hasattr(node, 'end_lineno') and node.end_lineno:
                                    func_lines = node.end_lineno - node.lineno
                                    if func_lines > 50:
                                        quality['complexity_issues'].append(f"{py_file.name}:{node.name} ({func_lines} lignes)")
                        
                        quality['python_modules'].append(module_info)
                        
                    except SyntaxError as e:
                        quality['import_issues'].append(f"{py_file.name}: Erreur de syntaxe - {e}")
                
                except Exception as e:
                    quality['import_issues'].append(f"{py_file.name}: {e}")
        
        # Calculer le score de qualité
        total_modules = len(quality['python_modules'])
        if total_modules > 0:
            documented_modules = sum(1 for m in quality['python_modules'] if m['has_docstring'])
            quality['docstring_coverage'] = (documented_modules / total_modules) * 100
            
            quality_factors = [
                (len(quality['complexity_issues']) == 0, 30),  # Pas de complexité excessive
                (len(quality['import_issues']) == 0, 25),      # Pas d'erreurs d'import
                (quality['docstring_coverage'] > 50, 25),      # Documentation > 50%
                (total_modules >= 5, 20)                       # Modularité suffisante
            ]
            
            quality['quality_score'] = sum(weight for check, weight in quality_factors if check)
        
        self.results['code_quality'] = quality
        print(f"   ✅ Code analysé: {quality['total_lines']} lignes, {total_modules} modules")
        print(f"   📊 Score de qualité: {quality['quality_score']:.1f}%")
    
    def audit_functionality(self):
        """Audit des fonctionnalités principales"""
        print("⚙️ Audit des fonctionnalités...")
        
        functionality = {
            'database_status': 'unknown',
            'main_modules': {},
            'export_capabilities': [],
            'ui_components': [],
            'functionality_score': 0
        }
        
        # Vérifier la base de données
        db_path = self.project_root / 'data' / 'cartes.db'
        if db_path.exists():
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cards")
                card_count = cursor.fetchone()[0]
                conn.close()
                functionality['database_status'] = f'operational ({card_count} cartes)'
            except Exception as e:
                functionality['database_status'] = f'error: {e}'
        else:
            functionality['database_status'] = 'missing'
        
        # Analyser les modules principaux
        key_modules = {
            'main_app.py': 'Application principale',
            'ui_components.py': 'Interface utilisateur',
            'database.py': 'Gestion base de données',
            'text_formatting_editor.py': 'Éditeur de formatage',
            'lua_export.py': 'Export Lua'
        }
        
        lib_path = self.project_root / 'lib'
        for module, description in key_modules.items():
            module_path = lib_path / module
            functionality['main_modules'][module] = {
                'exists': module_path.exists(),
                'description': description,
                'size': module_path.stat().st_size if module_path.exists() else 0
            }
        
        # Vérifier les capacités d'export
        export_files = ['lua_exporter_love2d.py', 'game_package_exporter.py']
        for export_file in export_files:
            if (self.project_root / export_file).exists():
                functionality['export_capabilities'].append(export_file)
        
        # Calculer le score de fonctionnalité
        functionality_checks = [
            ('Database operational', 'operational' in functionality['database_status']),
            ('Main app exists', functionality['main_modules'].get('main_app.py', {}).get('exists', False)),
            ('UI components exist', functionality['main_modules'].get('ui_components.py', {}).get('exists', False)),
            ('Text editor exists', functionality['main_modules'].get('text_formatting_editor.py', {}).get('exists', False)),
            ('Export capabilities', len(functionality['export_capabilities']) > 0)
        ]
        
        functionality['functionality_score'] = (sum(1 for _, check in functionality_checks if check) / len(functionality_checks)) * 100
        
        self.results['functionality'] = functionality
        print(f"   ✅ Fonctionnalités analysées")
        print(f"   📊 Score de fonctionnalité: {functionality['functionality_score']:.1f}%")
    
    def audit_tests(self):
        """Audit des tests"""
        print("🧪 Audit des tests...")
        
        tests = {
            'test_directory_exists': False,
            'test_files': [],
            'test_categories': [],
            'test_coverage_estimate': 0,
            'test_score': 0
        }
        
        tests_path = self.project_root / 'tests'
        if tests_path.exists():
            tests['test_directory_exists'] = True
            
            # Analyser les fichiers de test
            for test_file in tests_path.rglob('test_*.py'):
                relative_path = test_file.relative_to(tests_path)
                tests['test_files'].append(str(relative_path))
                
                # Identifier les catégories
                category = relative_path.parts[0] if len(relative_path.parts) > 1 else 'root'
                if category not in tests['test_categories']:
                    tests['test_categories'].append(category)
            
            # Estimer la couverture de test (basée sur le nombre de fichiers de test vs modules principaux)
            main_modules_count = len([m for m in self.results['functionality']['main_modules'] 
                                    if self.results['functionality']['main_modules'][m]['exists']])
            if main_modules_count > 0:
                tests['test_coverage_estimate'] = min(100, (len(tests['test_files']) / main_modules_count) * 20)
        
        # Calculer le score de test
        test_checks = [
            ('Test directory exists', tests['test_directory_exists']),
            ('Has test files', len(tests['test_files']) > 0),
            ('Organized tests', len(tests['test_categories']) > 1),
            ('Good coverage estimate', tests['test_coverage_estimate'] > 30)
        ]
        
        tests['test_score'] = (sum(1 for _, check in test_checks if check) / len(test_checks)) * 100
        
        self.results['tests'] = tests
        print(f"   ✅ Tests analysés: {len(tests['test_files'])} fichiers de test")
        print(f"   📊 Score de tests: {tests['test_score']:.1f}%")
    
    def audit_documentation(self):
        """Audit de la documentation"""
        print("📚 Audit de la documentation...")
        
        documentation = {
            'readme_exists': False,
            'readme_quality': 0,
            'docs_directory': False,
            'guides_directory': False,
            'inline_documentation': 0,
            'documentation_score': 0
        }
        
        # Vérifier README
        readme_path = self.project_root / 'README.md'
        if readme_path.exists():
            documentation['readme_exists'] = True
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                # Évaluer la qualité du README
                quality_indicators = [
                    '# ' in readme_content,  # Titre principal
                    'installation' in readme_content.lower(),
                    'usage' in readme_content.lower() or 'utilisation' in readme_content.lower(),
                    len(readme_content) > 500  # Contenu substantiel
                ]
                documentation['readme_quality'] = (sum(quality_indicators) / len(quality_indicators)) * 100
            except:
                pass
        
        # Vérifier les dossiers de documentation
        documentation['docs_directory'] = (self.project_root / 'docs').is_dir()
        documentation['guides_directory'] = (self.project_root / 'guides').is_dir()
        
        # Documentation inline (déjà calculée dans code_quality)
        if 'code_quality' in self.results:
            documentation['inline_documentation'] = self.results['code_quality']['docstring_coverage']
        
        # Calculer le score de documentation
        doc_checks = [
            ('README exists', documentation['readme_exists']),
            ('README quality', documentation['readme_quality'] > 50),
            ('Docs directory', documentation['docs_directory']),
            ('Inline documentation', documentation['inline_documentation'] > 30)
        ]
        
        documentation['documentation_score'] = (sum(1 for _, check in doc_checks if check) / len(doc_checks)) * 100
        
        self.results['documentation'] = documentation
        print(f"   ✅ Documentation analysée")
        print(f"   📊 Score de documentation: {documentation['documentation_score']:.1f}%")
    
    def audit_security(self):
        """Audit de sécurité basique"""
        print("🔒 Audit de sécurité...")
        
        security = {
            'hardcoded_paths': [],
            'sql_injection_risks': [],
            'file_access_issues': [],
            'secrets_exposed': [],
            'security_score': 0
        }
        
        # Rechercher des problèmes de sécurité potentiels
        for py_file in self.project_root.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    line_lower = line.lower()
                    
                    # Chemins absolus codés en dur
                    if 'c:\\' in line_lower or '/home/' in line_lower:
                        security['hardcoded_paths'].append(f"{py_file.name}:{i}")
                    
                    # Risques d'injection SQL
                    if 'execute(' in line and '%' in line and 'format' in line:
                        security['sql_injection_risks'].append(f"{py_file.name}:{i}")
                    
                    # Mots de passe ou clés potentiels
                    if any(keyword in line_lower for keyword in ['password', 'secret', 'key', 'token']) and '=' in line:
                        security['secrets_exposed'].append(f"{py_file.name}:{i}")
            
            except Exception:
                continue
        
        # Calculer le score de sécurité
        security_issues = (len(security['hardcoded_paths']) + 
                          len(security['sql_injection_risks']) + 
                          len(security['secrets_exposed']))
        
        security['security_score'] = max(0, 100 - (security_issues * 10))
        
        self.results['security'] = security
        print(f"   ✅ Sécurité analysée: {security_issues} problèmes détectés")
        print(f"   📊 Score de sécurité: {security['security_score']:.1f}%")
    
    def generate_recommendations(self):
        """Générer des recommandations d'amélioration"""
        print("💡 Génération des recommandations...")
        
        recommendations = []
        
        # Recommandations basées sur la structure
        if self.results['project_structure']['organization_score'] < 80:
            recommendations.append({
                'category': 'Structure',
                'priority': 'Moyenne',
                'issue': 'Organisation du projet perfectible',
                'solution': 'Vérifier que tous les dossiers essentiels (docs/, guides/) sont présents et organisés'
            })
        
        # Recommandations basées sur la qualité du code
        if self.results['code_quality']['quality_score'] < 70:
            recommendations.append({
                'category': 'Code Quality',
                'priority': 'Haute',
                'issue': 'Qualité du code à améliorer',
                'solution': 'Ajouter des docstrings, réduire la complexité des fonctions, corriger les erreurs'
            })
        
        # Recommandations basées sur les tests
        if self.results['tests']['test_score'] < 60:
            recommendations.append({
                'category': 'Tests',
                'priority': 'Haute',
                'issue': 'Couverture de tests insuffisante',
                'solution': 'Ajouter des tests unitaires pour les modules principaux'
            })
        
        # Recommandations basées sur la documentation
        if self.results['documentation']['documentation_score'] < 70:
            recommendations.append({
                'category': 'Documentation',
                'priority': 'Moyenne',
                'issue': 'Documentation incomplète',
                'solution': 'Améliorer le README, ajouter des guides utilisateur et documentation technique'
            })
        
        # Recommandations basées sur la sécurité
        if self.results['security']['security_score'] < 80:
            recommendations.append({
                'category': 'Sécurité',
                'priority': 'Haute',
                'issue': 'Problèmes de sécurité détectés',
                'solution': 'Corriger les chemins absolus, sécuriser les requêtes SQL, protéger les secrets'
            })
        
        # Calculer le score global
        scores = [
            self.results['project_structure']['organization_score'],
            self.results['code_quality']['quality_score'],
            self.results['functionality']['functionality_score'],
            self.results['tests']['test_score'],
            self.results['documentation']['documentation_score'],
            self.results['security']['security_score']
        ]
        
        global_score = sum(scores) / len(scores)
        
        # Recommandation globale
        if global_score >= 80:
            overall_status = "Excellent"
            recommendations.insert(0, {
                'category': 'Global',
                'priority': 'Info',
                'issue': 'Projet en excellent état',
                'solution': 'Maintenir la qualité actuelle et continuer les bonnes pratiques'
            })
        elif global_score >= 60:
            overall_status = "Bon"
            recommendations.insert(0, {
                'category': 'Global',
                'priority': 'Basse',
                'issue': 'Projet en bon état avec quelques améliorations possibles',
                'solution': 'Adresser les points faibles identifiés pour atteindre l\'excellence'
            })
        else:
            overall_status = "À améliorer"
            recommendations.insert(0, {
                'category': 'Global',
                'priority': 'Critique',
                'issue': 'Projet nécessite des améliorations importantes',
                'solution': 'Prioriser les corrections de sécurité et qualité du code'
            })
        
        self.results['global_score'] = global_score
        self.results['overall_status'] = overall_status
        self.results['recommendations'] = recommendations
        
        print(f"   ✅ {len(recommendations)} recommandations générées")
        print(f"   📊 Score global: {global_score:.1f}% ({overall_status})")
    
    def save_results(self):
        """Sauvegarder les résultats de l'audit"""
        # JSON détaillé
        json_path = self.project_root / 'AUDIT_RESULTS.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Rapport Markdown
        md_path = self.project_root / 'AUDIT_REPORT.md'
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown_report())
        
        return json_path, md_path
    
    def generate_markdown_report(self):
        """Générer un rapport Markdown"""
        report = f"""# 🔍 AUDIT COMPLET DU PROJET

**Date de l'audit**: {self.results['timestamp']}
**Score global**: {self.results['global_score']:.1f}% ({self.results['overall_status']})

---

## 📊 Scores par Catégorie

| Catégorie | Score | Status |
|-----------|-------|--------|
| 📁 Structure du projet | {self.results['project_structure']['organization_score']:.1f}% | {'✅' if self.results['project_structure']['organization_score'] >= 80 else '⚠️' if self.results['project_structure']['organization_score'] >= 60 else '❌'} |
| 🔍 Qualité du code | {self.results['code_quality']['quality_score']:.1f}% | {'✅' if self.results['code_quality']['quality_score'] >= 80 else '⚠️' if self.results['code_quality']['quality_score'] >= 60 else '❌'} |
| ⚙️ Fonctionnalités | {self.results['functionality']['functionality_score']:.1f}% | {'✅' if self.results['functionality']['functionality_score'] >= 80 else '⚠️' if self.results['functionality']['functionality_score'] >= 60 else '❌'} |
| 🧪 Tests | {self.results['tests']['test_score']:.1f}% | {'✅' if self.results['tests']['test_score'] >= 80 else '⚠️' if self.results['tests']['test_score'] >= 60 else '❌'} |
| 📚 Documentation | {self.results['documentation']['documentation_score']:.1f}% | {'✅' if self.results['documentation']['documentation_score'] >= 80 else '⚠️' if self.results['documentation']['documentation_score'] >= 60 else '❌'} |
| 🔒 Sécurité | {self.results['security']['security_score']:.1f}% | {'✅' if self.results['security']['security_score'] >= 80 else '⚠️' if self.results['security']['security_score'] >= 60 else '❌'} |

---

## 📁 Structure du Projet

- **Fichiers totaux**: {self.results['project_structure']['total_files']}
- **Fichiers Python**: {self.results['project_structure']['python_files']}
- **Base de données**: {self.results['functionality']['database_status']}

### Fichiers Essentiels
"""

        for file, exists in self.results['project_structure']['essential_files'].items():
            status = '✅' if exists else '❌'
            report += f"- {status} `{file}`\n"

        report += f"""
---

## 🔍 Qualité du Code

- **Lignes de code**: {self.results['code_quality']['total_lines']:,}
- **Modules Python**: {len(self.results['code_quality']['python_modules'])}
- **Documentation**: {self.results['code_quality']['docstring_coverage']:.1f}%
"""

        if self.results['code_quality']['complexity_issues']:
            report += "\n### ⚠️ Problèmes de Complexité\n"
            for issue in self.results['code_quality']['complexity_issues']:
                report += f"- {issue}\n"

        if self.results['code_quality']['import_issues']:
            report += "\n### ❌ Problèmes d'Import\n"
            for issue in self.results['code_quality']['import_issues']:
                report += f"- {issue}\n"

        report += f"""
---

## ⚙️ Fonctionnalités

### Modules Principaux
"""
        for module, info in self.results['functionality']['main_modules'].items():
            status = '✅' if info['exists'] else '❌'
            size_kb = info['size'] / 1024 if info['size'] > 0 else 0
            report += f"- {status} `{module}` - {info['description']} ({size_kb:.1f} KB)\n"

        report += f"""
### Capacités d'Export
"""
        for export_cap in self.results['functionality']['export_capabilities']:
            report += f"- ✅ `{export_cap}`\n"

        report += f"""
---

## 🧪 Tests

- **Dossier tests**: {'✅' if self.results['tests']['test_directory_exists'] else '❌'}
- **Fichiers de test**: {len(self.results['tests']['test_files'])}
- **Catégories**: {', '.join(self.results['tests']['test_categories'])}
- **Couverture estimée**: {self.results['tests']['test_coverage_estimate']:.1f}%

---

## 📚 Documentation

- **README**: {'✅' if self.results['documentation']['readme_exists'] else '❌'} (qualité: {self.results['documentation']['readme_quality']:.1f}%)
- **Dossier docs**: {'✅' if self.results['documentation']['docs_directory'] else '❌'}
- **Dossier guides**: {'✅' if self.results['documentation']['guides_directory'] else '❌'}
- **Documentation inline**: {self.results['documentation']['inline_documentation']:.1f}%

---

## 🔒 Sécurité

"""
        
        security_sections = [
            ('Chemins absolus codés en dur', self.results['security']['hardcoded_paths']),
            ('Risques d\'injection SQL', self.results['security']['sql_injection_risks']),
            ('Secrets exposés', self.results['security']['secrets_exposed'])
        ]
        
        for title, issues in security_sections:
            if issues:
                report += f"### ⚠️ {title}\n"
                for issue in issues[:5]:  # Limiter à 5 exemples
                    report += f"- {issue}\n"
                if len(issues) > 5:
                    report += f"- ... et {len(issues) - 5} autres\n"
                report += "\n"

        report += """---

## 💡 Recommandations

"""
        for rec in self.results['recommendations']:
            priority_emoji = {'Critique': '🚨', 'Haute': '⚠️', 'Moyenne': '📋', 'Basse': '💡', 'Info': 'ℹ️'}
            emoji = priority_emoji.get(rec['priority'], '📋')
            
            report += f"""### {emoji} {rec['category']} - {rec['priority']}

**Problème**: {rec['issue']}
**Solution**: {rec['solution']}

"""

        report += f"""---

## 📈 Conclusion

Le projet obtient un score global de **{self.results['global_score']:.1f}%** et est classé comme **{self.results['overall_status']}**.

### Points forts:
"""
        
        # Identifier les points forts (scores > 80)
        strong_points = []
        categories = [
            ('Structure du projet', self.results['project_structure']['organization_score']),
            ('Qualité du code', self.results['code_quality']['quality_score']),
            ('Fonctionnalités', self.results['functionality']['functionality_score']),
            ('Tests', self.results['tests']['test_score']),
            ('Documentation', self.results['documentation']['documentation_score']),
            ('Sécurité', self.results['security']['security_score'])
        ]
        
        for name, score in categories:
            if score >= 80:
                strong_points.append(f"- ✅ {name} ({score:.1f}%)")
        
        if strong_points:
            report += "\n".join(strong_points)
        else:
            report += "- Aucun point fort identifié (scores < 80%)"
        
        report += "\n\n### Points à améliorer:\n"
        
        weak_points = []
        for name, score in categories:
            if score < 70:
                weak_points.append(f"- ⚠️ {name} ({score:.1f}%)")
        
        if weak_points:
            report += "\n".join(weak_points)
        else:
            report += "- Tous les domaines sont dans une fourchette acceptable"

        report += f"""

---

*Audit généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}*
"""
        
        return report
    
    def run_full_audit(self):
        """Exécuter l'audit complet"""
        print("🔍 DÉBUT DE L'AUDIT COMPLET DU PROJET")
        print("=" * 50)
        
        self.audit_project_structure()
        self.audit_code_quality()
        self.audit_functionality()
        self.audit_tests()
        self.audit_documentation()
        self.audit_security()
        self.generate_recommendations()
        
        json_path, md_path = self.save_results()
        
        print("\n" + "=" * 50)
        print("✅ AUDIT TERMINÉ")
        print(f"📊 Score global: {self.results['global_score']:.1f}% ({self.results['overall_status']})")
        print(f"📋 Rapport détaillé: {md_path}")
        print(f"📄 Données JSON: {json_path}")
        print(f"💡 Recommandations: {len(self.results['recommendations'])}")
        
        return self.results

def main():
    """Point d'entrée principal"""
    project_root = Path(__file__).parent
    
    print("🔍 AUDIT COMPLET DU PROJET EDITEUR-CARTES-LOVE2D")
    print("=" * 60)
    print(f"📂 Dossier du projet: {project_root}")
    print()
    
    auditor = ProjectAuditor(project_root)
    results = auditor.run_full_audit()
    
    return results

if __name__ == "__main__":
    main()
