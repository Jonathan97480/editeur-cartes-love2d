# Guide des modes de lancement - Éditeur de cartes Love2D

## 🚀 Modes disponibles

### 1. Mode Automatique (recommandé)
- **Fichier**: `test.py`
- **Description**: Détecte automatiquement le meilleur mode selon votre environnement
- **Avantages**: 
  - Fallback automatique en cas de problème
  - Essaie d'abord le mode avancé, puis bascule en compatibilité
  - Recommandé pour la plupart des utilisateurs

### 2. Mode Final Stable  
- **Fichier**: `app_final.py`
- **Description**: Interface complète avec tous les menus et fonctionnalités
- **Avantages**:
  - Interface moderne et intuitive
  - Tous les menus accessibles
  - Gestion d'erreur robuste
  - Garantie de fonctionnement

### 3. Mode Compatibilité
- **Fichier**: `test_compat.py`  
- **Description**: Interface basique mais très robuste
- **Avantages**:
  - Fonctionne dans tous les environnements
  - Pas de dépendances avancées
  - Idéal pour les systèmes restreints

### 4. Mode Avancé (forcé)
- **Fichier**: `test.py --force-advanced`
- **Description**: Force l'utilisation des thèmes Windows 11
- **Avantages**:
  - Interface la plus moderne
  - Thèmes automatiques clair/sombre
  - Style Windows 11
- **Inconvénients**:
  - Peut échouer selon l'environnement système

## 📁 Fichiers de lancement

- **`launch.bat`**: Menu complet avec tous les modes
- **`launch_simple.bat`**: Menu simplifié avec options principales  
- **`run_final.bat`**: Lancement direct du mode stable
- **`run.bat`**: Lancement automatique avec environnement virtuel

## 🔧 Fonctionnalités communes

Tous les modes incluent :
- ✅ Édition complète des cartes
- ✅ Gestion des raretés (Commun, Rare, Légendaire, Mythique)
- ✅ Export Lua pour Love2D
- ✅ Base de données SQLite locale
- ✅ Gestion des images et templates
- ✅ Raccourcis clavier

## 💡 Recommandations

- **Débutants**: Utilisez le Mode Automatique (option 1)
- **Utilisateurs avancés**: Mode Final Stable (option 2)  
- **Problèmes système**: Mode Compatibilité (option 3)
- **Meilleure apparence**: Mode Avancé forcé (option 4)

## 🚨 Dépannage

Si un mode ne fonctionne pas :
1. Essayez le Mode Automatique
2. Si ça ne marche pas, utilisez le Mode Compatibilité
3. Vérifiez que Python 3.7+ est installé
4. Assurez-vous que le dossier `lib/` est présent
