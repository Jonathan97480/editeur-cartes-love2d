# 📁 Dossier Legacy - Fichiers archivés

## 🎯 Organisation

Ce dossier contient tous les fichiers legacy (anciens) qui ne sont plus utilisés dans le workflow principal mais conservés pour référence.

### 📂 Structure

```
legacy/
├── confirmations/     # Anciens scripts de confirmation
├── demos/            # Scripts de démonstration
├── fixes/            # Scripts de correction/réparation
├── builders/         # Scripts de création d'exécutables
├── migrations/       # Scripts de migration et vérification
├── setup/           # Scripts d'installation/configuration
└── solutions/       # Solutions temporaires
```

## 📋 Contenu par dossier

### 🔐 confirmations/
Scripts d'interface utilisateur pour confirmations diverses :
- `confirmation_clear_data.py` - Confirmation effacement données
- `confirmation_commit*.py` - Confirmations de commit
- `confirmation_merge.py` - Confirmation de merge
- `confirmation_raccourci.py` - Confirmation raccourcis
- `correction_confirmee.py` - Corrections confirmées

### 🎮 demos/
Scripts de démonstration et exemples :
- `demo_actors.py` - Démonstration système acteurs
- `demo_finale_migration.py` - Démo migration finale
- `demo_rarity_system.py` - Démo système de rareté
- `demo_selection_multiple.py` - Démo sélection multiple
- `demo_template_organization.py` - Démo organisation templates
- `demo_templates/` - Dossier templates de démo

### 🔧 fixes/
Scripts de correction et réparation :
- `fix_docstring_imports.py` - Correction imports docstring
- `fix_fused_images.py` - Correction images fusionnées
- `fix_malformed_tests.py` - Correction tests malformés
- `fix_templates.py` - Correction templates
- `fix_test_imports.py` - Correction imports tests
- `clean_test_imports.py` - Nettoyage imports tests
- `validate_all_tests.py` - Validation tous tests

### 🏗️ builders/
Scripts de création d'exécutables et build :
- `create_executable*.py` - Création exécutables
- `create_minimal_internal.py` - Création version minimale
- `create_portable_exe.py` - Création version portable
- `create_simple_solution.py` - Création solution simple
- `EditeurCartesLove2D*.spec` - Fichiers spec PyInstaller

### 🔄 migrations/
Scripts de migration et vérification :
- `migrate_images.py` - Migration images
- `check_paths.py` - Vérification chemins
- `convert_paths.py` - Conversion chemins
- `MIGRATION_TESTS_SUMMARY.py` - Résumé migration tests
- `verify_db_protection.py` - Vérification protection DB
- `verify_relative_paths.py` - Vérification chemins relatifs

### ⚙️ setup/
Scripts d'installation et configuration :
- `setup_test_automation.py` - Configuration automatisation tests

### 💡 solutions/
Solutions temporaires et finales :
- `solution_finale.py` - Solution finale temporaire

## ⚠️ Note importante

**Ces fichiers sont archivés et ne doivent plus être utilisés dans le workflow principal.**

### 🚀 Workflow actuel recommandé :
- **Lancement** : `START.bat`
- **Développement** : `dev/git.bat`
- **Tests** : `dev/run_tests.bat`
- **Organisation** : `organiser_projet.py`

### 📖 Documentation active :
- `README_GITHUB.md` - Guide utilisateur principal
- `GUIDE_ENVIRONNEMENT_PYTHON.md` - Guide environnement
- `dev/README_DEV.md` - Guide développeur

## 🗂️ Pourquoi archivé ?

Ces fichiers représentent l'évolution du projet et les différentes approches testées. Ils sont conservés pour :
- **Référence historique**
- **Débogage** en cas de problème
- **Apprentissage** des solutions essayées
- **Recovery** si besoin de restaurer une fonctionnalité

**✅ Projet maintenant propre et organisé !**
