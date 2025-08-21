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
- **Menu 🎭 Acteurs** → **🎭 Exporter Acteur** (cartes d'un acteur spécifique)
- **Menu 🎭 Acteurs** → **📤 Exporter Tout** (toutes les cartes organisées par acteur)
- **Menu Fichier** → **Exporter Joueur** (cartes du joueur - ancien système)
- **Menu Fichier** → **Exporter IA** (cartes de l'intelligence artificielle - ancien système)
- Les fichiers `.lua` sont créés automatiquement avec le format Love2D complet

### 🎭 **Gérer les Acteurs**
- **Menu 🎭 Acteurs** → **Gérer les Acteurs**
- Créez des acteurs personnalisés avec nom, icône et couleur
- Liez des cartes à des acteurs pour une organisation thématique
- Exportez les cartes par acteur ou par groupe d'acteurs

### 🃏 **Visualiser le Deck**
- **Menu Affichage** → **🃏 Voir le deck** (ou Ctrl+V)
- Visualisez toutes vos cartes en grille avec images
- **Filtres disponibles** :
  - Par rareté (Commun, Rare, Épique, Légendaire, Mythique)
  - Par type (Attaque, Défense, Soutien, Sort, Piège)
  - **Par acteur** (nouveau !) - Filtrez les cartes d'un acteur spécifique
- **Options de tri** :
  - Par rareté, nom, type, puissance
  - **Par acteur** (nouveau !) - Regroupez les cartes par acteur
- Combinez les filtres pour des recherches précises

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
| `Ctrl+V` | **Visualiser le deck** (nouveau !) |
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
- **Créez des acteurs personnalisés** pour organiser vos cartes par thème/faction
- **Utilisez le visualiseur de deck** (Ctrl+V) pour avoir une vue d'ensemble
- **Filtrez par acteur** dans le visualiseur pour voir les cartes d'un personnage
- **Combinez les filtres** (rareté + type + acteur) pour des recherches précises
- **Utilisez les types** pour catégoriser vos cartes (Attaque, Défense, etc.)
- **Exportez par acteur** pour des fichiers .lua organisés par personnage
- **Testez régulièrement** vos exports dans votre jeu Love2D
- **Sauvegardez** votre fichier `cartes.db` pour ne pas perdre vos créations

## 🗑️ Clear Data - Remise à Zéro Complète

### **⚠️ Fonctionnalité de Suppression Totale**
**Localisation** : `Menu 🔧 Réglages → 🗑️ Clear Data (Vider tout)`

Cette fonctionnalité permet de **remettre l'application dans un état complètement vierge**.

### **🗑️ Que supprime Clear Data :**
- **TOUTES les cartes** (joueur, IA, acteurs)
- **TOUS les acteurs** créés
- **TOUTES les liaisons** cartes-acteurs
- **TOUS les fichiers images** (dossier images/ complet)
- **Réinitialisation** des compteurs de la base de données

### **🛡️ Système de Sécurité :**
1. **Premier avertissement** : Fenêtre avec explication détaillée
2. **Confirmation stricte** : Saisie obligatoire de "SUPPRIMER TOUT"
3. **Action irréversible** : Aucun retour en arrière possible

### **🎯 Utilisation Recommandée :**
- **Nouveau projet** : Repartir sur une base vierge
- **Nettoyage après tests** : Supprimer les données de développement
- **Résolution de problèmes** : Éliminer les corruptions potentielles
- **Distribution** : Créer une version propre à partager

### **💾 Précautions Importantes :**
- **Sauvegardez** vos cartes importantes avant utilisation
- **Exportez** vos fichiers .lua si nécessaire
- **Copiez** vos images personnalisées
- Cette action **ne peut pas être annulée**

---

🎮 **Bon développement de jeu avec Love2D !**
