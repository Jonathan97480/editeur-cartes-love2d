# 🛠️ Dossier DEV - Outils de développement

## 📁 Contenu du dossier

### 🔧 Scripts batch principaux
- **`git.bat`** - Gestionnaire Git interactif avec validation
- **`run_app.bat`** - Lance l'application avec l'environnement Python
- **`run_tests.bat`** - Exécute tous les tests automatisés
- **`run_organize.bat`** - Organise automatiquement le projet
- **`validate_all.bat`** - Validation complète du projet

### 🔒 Scripts de sécurité et validation
- **`test_security.bat`** - Tests de sécurité complets avec pré-commit
- **`test_quick_security.bat`** - Tests de sécurité rapides
- **`test_application_complet.bat`** - Test complet simulation utilisateur
- **`validation_complete.bat`** - Validation complète (sécurité + application)

### 🧪 Tests spécialisés
- **`test_application_complete.py`** - Test Python complet de l'application
- **`test_debug_carte_non_trouvee.py`** - Test debug pour problèmes de cartes

### 🔄 Scripts Git spécialisés
- **`git_commit.bat`** - Commit avec validation automatique
- **`git_status.bat`** - Statut Git enrichi
- **`git_push.bat`** - Push avec validation préalable

### ⚙️ Configuration
- **`configure_git_hooks.bat`** - Active/désactive les hooks Git
- **`configure_python_env.py`** - Configuration environnement Python

### 📜 Scripts Legacy (anciens)
- Tous les autres fichiers `.bat` sont des versions antérieures
- Conservés pour compatibilité mais non recommandés

## 🚀 Utilisation rapide

### Git workflow complet
```bash
dev/git.bat                    # Menu interactif
dev/git.bat commit "message"   # Commit avec validation
dev/git.bat push              # Push avec tests
```

### Tests et validation
```bash
dev/run_tests.bat             # Tests automatisés
dev/validate_all.bat          # Validation complète
dev/test_security.bat         # Tests de sécurité complets
dev/test_quick_security.bat   # Tests de sécurité rapides
dev/test_application_complet.bat  # Test complet simulation utilisateur
dev/validation_complete.bat   # Validation sécurité + application
```

### Lancement de l'application
```bash
dev/run_app.bat               # Avec environnement Python
```

## 🎯 Scripts recommandés

### Pour le développement quotidien
1. **`git.bat`** - Gestion Git complète
2. **`run_tests.bat`** - Tests avant commit
3. **`validate_all.bat`** - Validation périodique
4. **`test_application_complet.bat`** - Test complet fonctionnel

### Pour la validation avant commit
1. **`test_quick_security.bat`** - Validation rapide (inclut test complet)
2. **`test_security.bat`** - Validation complète avec rapports
3. **`validation_complete.bat`** - Validation totale du projet

### Pour le debug et diagnostic
1. **`test_application_complete.py`** - Test détaillé avec logs
2. **`test_debug_carte_non_trouvee.py`** - Debug spécifique cartes

### Pour la configuration
1. **`configure_python_env.py`** - Configuration environnement
2. **`configure_git_hooks.bat`** - Gestion hooks Git

## ⚠️ Note importante

**Les utilisateurs finaux n'ont pas besoin de ce dossier.**  
Utilisez `START.bat` et `UPDATE.bat` à la racine du projet.

Ce dossier est destiné aux développeurs et contributeurs du projet.
