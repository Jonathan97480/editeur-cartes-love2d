# 🎮 Éditeur de cartes Love2D - Guide utilisateur GitHub

## 🚀 Installation rapide

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/jonathan97480/editeur-cartes-love2d.git
cd editeur-cartes-love2d
```

### 2️⃣ Mise à jour automatique
```bash
# Windows - Double-cliquez sur :
UPDATE.bat

# Ou en ligne de commande :
.\UPDATE.bat
```

### 3️⃣ Lancer le jeu
```bash
# Double-cliquez sur :
START.bat

# Ou avec Love2D directement :
love .
```

## 📦 Mise à jour du projet

### Automatique (Recommandé)
- **Double-cliquez sur `UPDATE.bat`**
- Le script fait tout automatiquement :
  - ✅ Sauvegarde vos données
  - ✅ Télécharge les mises à jour
  - ✅ Restaure vos données
  - ✅ Configure l'environnement

### Manuelle
```bash
git pull origin main
```

## 🛠️ Pour les développeurs

### Structure du projet
```
├── START.bat              # 🎮 Lancer le jeu
├── UPDATE.bat             # 🔄 Mise à jour automatique
├── dev/                   # 🛠️ Outils de développement
│   ├── git.bat           # Git avec validation
│   ├── run_app.bat       # Lancer avec env Python
│   ├── run_tests.bat     # Tests automatisés
│   └── validate_all.bat  # Validation complète
├── app_final.py          # 🐍 Application Python
├── main.lua              # 🎮 Point d'entrée Love2D
└── data/                 # 📦 Données du projet
```

### Scripts de développement (dossier `dev/`)

#### Gestion Git
```bash
dev/git.bat status        # Statut du dépôt
dev/git.bat commit "msg"  # Commit avec validation
dev/git.bat push          # Push avec tests
dev/git.bat               # Menu interactif
```

#### Tests et validation
```bash
dev/run_tests.bat         # Tests automatisés
dev/validate_all.bat      # Validation complète
dev/run_app.bat           # Lancer avec Python
```

#### Configuration
```bash
dev/configure_git_hooks.bat    # Gérer les hooks Git
dev/configure_python_env.py    # Config environnement Python
```

### Environnement Python
- **Configuration automatique** via `UPDATE.bat`
- **Documentation** : `GUIDE_ENVIRONNEMENT_PYTHON.md`
- **Résumé complet** : `RÉSUMÉ_CONFIGURATION.md`

## 🎯 Utilisation pour les utilisateurs finaux

### Première utilisation
1. **Télécharger** : `git clone` ou ZIP depuis GitHub
2. **Installer Love2D** : https://love2d.org/
3. **Mettre à jour** : Double-clic sur `UPDATE.bat`
4. **Jouer** : Double-clic sur `START.bat`

### Mises à jour régulières
- **Simple** : Double-clic sur `UPDATE.bat`
- **Automatique** : Sauvegarde et restauration des données
- **Sécurisé** : Vos cartes et images sont préservées

### Sauvegarde automatique
Le script `UPDATE.bat` sauvegarde automatiquement :
- 💾 Base de données des cartes (`cartes.db`)
- 🖼️ Images personnalisées (`images/`)
- ⚙️ Configurations (`config.lua`)
- 📁 Sauvegarde dans `backups/backup_YYYYMMDD_HHMM/`

## 🆘 Résolution de problèmes

### Love2D non trouvé
```bash
# Télécharger et installer Love2D :
https://love2d.org/

# Vérifier l'installation :
love --version
```

### Erreurs de mise à jour
```bash
# Réinitialiser les modifications locales :
git stash
git pull origin main

# Ou utiliser UPDATE.bat qui gère automatiquement
```

### Problèmes Python (développeurs)
```bash
# Reconfigurer l'environnement :
dev/configure_python_env.py

# Voir la documentation :
GUIDE_ENVIRONNEMENT_PYTHON.md
```

## 📄 Documentation complète

- **Guide utilisateur** : Ce fichier (README_GITHUB.md)
- **Guide environnement** : `GUIDE_ENVIRONNEMENT_PYTHON.md`
- **Résumé configuration** : `RÉSUMÉ_CONFIGURATION.md`
- **Documentation Love2D** : Dans le dossier `docs/`

## 🤝 Contribution

### Pour contribuer
1. Fork le projet
2. Créer une branche : `git checkout -b feature/nouvelle-fonctionnalite`
3. Utiliser les outils de dev : `dev/git.bat`
4. Tests : `dev/run_tests.bat`
5. Commit : `dev/git.bat commit "description"`
6. Push : `dev/git.bat push`
7. Créer une Pull Request

### Outils de développement
- **Validation automatique** : Tests avant chaque commit
- **Environment Python** : Configuration automatique
- **Git intégré** : Scripts avec validation
- **Organisation** : Projet structuré professionnellement

---

## 🎉 Profitez du jeu !

**Pour jouer** : `START.bat`  
**Pour développer** : Dossier `dev/`  
**Pour mettre à jour** : `UPDATE.bat`
