# 🚀 GUIDE D'INSTALLATION - Éditeur de cartes Love2D

## 📋 PRÉREQUIS

### 1. Python (Obligatoire)
- **Version recommandée** : Python 3.9 ou plus récent
- **Téléchargement** : https://python.org/downloads/
- **⚠️ IMPORTANT** : Cocher "Add Python to PATH" pendant l'installation

### 2. Bibliothèques Python
Les bibliothèques suivantes sont installées automatiquement :
- `tkinter` (interface graphique)
- `sqlite3` (base de données)
- `Pillow` (traitement d'images)

## 🛠️ INSTALLATION

### Étape 1 : Télécharger le projet
1. Téléchargez le projet depuis GitHub
2. Extrayez l'archive dans un dossier de votre choix
3. Ouvrez le dossier du projet

### Étape 2 : Vérifier Python
1. Ouvrez une invite de commande (cmd)
2. Tapez : `python --version`
3. Vous devriez voir : `Python 3.x.x`

Si Python n'est pas reconnu :
- Réinstallez Python avec "Add to PATH" coché
- Redémarrez votre ordinateur

### Étape 3 : Lancer l'application
**Méthode 1 (Recommandée)** :
```
Double-cliquez sur START.bat
Choisissez l'option [1]
```

**Méthode 2 (Alternative)** :
```
Double-cliquez sur LAUNCH_PORTABLE.bat
```

**Méthode 3 (Manuel)** :
```
Ouvrez cmd dans le dossier du projet
Tapez : python app_final.py
```

## 🔧 RÉSOLUTION DES PROBLÈMES

### Erreur "Python non trouvé"
**Solution** :
1. Vérifiez que Python est installé : `python --version`
2. Si non installé, téléchargez depuis python.org
3. Cochez "Add Python to PATH" pendant l'installation
4. Redémarrez l'ordinateur

### Erreur "Chemin d'accès spécifié introuvable"
**Cause** : Scripts non compatibles avec votre système
**Solution** : Utilisez `LAUNCH_PORTABLE.bat` au lieu de START.bat

### Erreur de modules manquants
**Solution** :
```
pip install Pillow
pip install tkinter  # (généralement inclus avec Python)
```

### L'application ne se lance pas
1. Vérifiez que vous êtes dans le bon dossier
2. Vérifiez que `app_final.py` existe
3. Essayez : `python -c "import tkinter; print('OK')"`

## 📁 STRUCTURE DU PROJET

```
editeur-cartes-love2d/
├── START.bat              # Menu principal
├── LAUNCH_PORTABLE.bat    # Lancement portable
├── app_final.py           # Application principale
├── data/
│   └── cartes.db         # Base de données des cartes
├── lib/                  # Bibliothèques Python
├── images/               # Images des cartes
└── dev/                  # Scripts de développement
```

## 🎮 UTILISATION

1. **Lancer** : START.bat → Option [1]
2. **Éditer** : Sélectionnez une carte → Cliquez "Formater texte"
3. **Exporter** : Menu → Export Love2D
4. **Sauvegarder** : Les modifications sont automatiques

## 🌐 SUPPORT

- **Documentation** : README.md
- **Issues** : GitHub Issues
- **Version** : Voir l'audit complet avec `python audit_complet.py`

## ✅ VÉRIFICATION RAPIDE

Pour vérifier que tout fonctionne :
```bat
python audit_complet.py
```
Score attendu : 100/100 ✅

---
*Guide mis à jour le 22 août 2025*
