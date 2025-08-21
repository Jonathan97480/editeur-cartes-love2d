# 🎮 Guide d'Utilisation - Éditeur de Cartes Love2D

## 🚀 Comment lancer l'application

### ✨ **Méthode la plus simple**
1. **Double-cliquez** sur le fichier `run.bat`
2. L'application se configure automatiquement
3. Si une erreur survient, elle bascule automatiquement vers le mode compatibilité

### ⚡ **Lancement rapide**
- **Double-cliquez** sur `launch.bat` pour un démarrage immédiat

## 🎨 Interface de l'Application

### **Panneau Gauche** : Création/Édition
- Formulaire complet pour créer et modifier les cartes
- Champs pour tous les attributs (nom, description, effets, etc.)
- Aperçu de l'image de la carte
- Boutons de sauvegarde et suppression

### **Panneau Droit** : Navigation
- **Onglet "Toutes"** : Voir toutes les cartes
- **Onglet "Commun"** : Cartes de rareté commune
- **Onglet "Rare"** : Cartes de rareté rare  
- **Onglet "Légendaire"** : Cartes légendaires
- **Onglet "Mythique"** : Cartes mythiques

## 🎯 Fonctionnalités Principales

### ✏️ **Créer une Carte**
1. Cliquez dans le formulaire à gauche
2. Remplissez le nom et la description
3. Choisissez le côté (Joueur/IA)
4. Définissez la rareté et les types
5. Configurez les effets héros et ennemis
6. Cliquez **Sauvegarder**

### 🔄 **Modifier une Carte**
1. Cliquez sur une carte dans la liste de droite
2. Modifiez les champs dans le formulaire
3. Cliquez **Sauvegarder** pour confirmer

### 📤 **Exporter pour Love2D**
- **Menu Fichier** → **Exporter Joueur** (cartes du joueur)
- **Menu Fichier** → **Exporter IA** (cartes de l'intelligence artificielle)
- Les fichiers `.lua` sont créés automatiquement

### 🎨 **Personnaliser l'Apparence**
- **Menu Affichage** → **Thèmes et Apparence**
- Choisissez entre : Automatique, Clair, Sombre
- L'application s'adapte instantanément

## 🖼️ Gestion des Images

### **Configuration des Templates**
1. **Menu Réglages** → **Configuration des images**
2. Sélectionnez un template de carte
3. Les nouvelles cartes utiliseront ce template automatiquement

### **Fusion d'Images**
- Lors de la sauvegarde, l'application fusionne automatiquement :
  - L'image de base de la carte
  - Le template sélectionné
- Le résultat est sauvé dans le dossier `images/`

## ⌨️ Raccourcis Clavier

| Touche | Action |
|--------|--------|
| `Ctrl+S` | Sauvegarder la carte |
| `Ctrl+N` | Nouvelle carte |
| `Ctrl+D` | Dupliquer la carte |
| `Del` | Supprimer la carte |
| `F5` | Actualiser les listes |

## 🔧 En cas de Problème

### **L'application ne se lance pas**
- Vérifiez que Python est installé
- Utilisez `run.bat` qui installe automatiquement tout
- Si ça persiste, utilisez `launch.bat`

### **L'interface semble bizarre**
- L'application bascule automatiquement vers le mode compatibilité
- Toutes les fonctionnalités restent disponibles

### **Les exports ne fonctionnent pas**
- Vérifiez que vous avez créé au moins une carte
- Les fichiers sont créés dans le même dossier que l'application

### **Les images ne se génèrent pas**
- Configurez un template dans **Réglages** → **Configuration des images**
- Vérifiez que l'image source existe

## 📁 Organisation des Fichiers

```
📁 Éditeur de Cartes/
├── 🚀 run.bat              # Lancement complet avec installation
├── ⚡ launch.bat           # Lancement rapide
├── 📄 test.py              # Application principale
├── 🗃️ cartes.db           # Base de données des cartes
├── 📤 cards_player.lua     # Export cartes joueur (généré)
├── 📤 cards_ai.lua         # Export cartes IA (généré)
├── 📁 images/              # Images générées des cartes
└── 📁 lib/                # Modules de l'application
```

## 💡 Conseils d'Utilisation

- **Organisez vos cartes** par rareté pour un meilleur workflow
- **Utilisez les types** pour catégoriser vos cartes (Attaque, Défense, etc.)
- **Testez régulièrement** vos exports dans votre jeu Love2D
- **Sauvegardez** votre fichier `cartes.db` pour ne pas perdre vos créations

---

🎮 **Bon développement de jeu avec Love2D !**
