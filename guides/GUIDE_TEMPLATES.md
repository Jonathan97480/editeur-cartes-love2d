# Guide : Templates d'Image par Rareté

## Nouvelle Fonctionnalité 🎨

L'éditeur de cartes Love2D supporte maintenant des **templates d'image spécifiques** pour chaque rareté de carte !

## Comment ça marche ?

### 1. Configuration des Templates

Dans le menu **"Configuration des images"** :

- **📁 Template Commun** : Image superposée pour les cartes communes
- **🔹 Template Rare** : Image superposée pour les cartes rares  
- **🌟 Template Légendaire** : Image superposée pour les cartes légendaires
- **💎 Template Mythique** : Image superposée pour les cartes mythiques

### 2. Création d'une Carte

Quand vous créez ou modifiez une carte :

1. **Sélectionnez l'image** de base (illustration)
2. **Choisissez la rareté** (commun, rare, légendaire, mythique)
3. **Sauvegardez** la carte

### 3. Génération Automatique

L'application va automatiquement :

✅ **Détecter la rareté** de la carte  
✅ **Sélectionner le bon template** selon la rareté  
✅ **Fusionner l'image** de base avec le template correspondant  
✅ **Sauvegarder** le résultat final dans `/images/`

## Types de Templates Recommandés

### 🎨 Design par Rareté

- **Commun** : Bordure simple, couleurs neutres
- **Rare** : Bordure bleue, effets subtils
- **Légendaire** : Bordure dorée, effets lumineux
- **Mythique** : Bordure violette/rouge, effets spectaculaires

### 📏 Spécifications Techniques

- **Format** : PNG avec transparence (recommandé)
- **Taille** : Identique à l'image de base
- **Zones transparentes** : Pour laisser voir l'illustration
- **Zones opaques** : Bordures, textes, icônes de rareté

## Exemples d'Utilisation

### Configuration Type
```
📁 Templates/
├── commun.png        → Bordure grise simple
├── rare.png          → Bordure bleue avec gemme
├── legendaire.png    → Bordure dorée avec ornements
└── mythique.png      → Bordure violette avec étoiles
```

### Résultat Attendu
```
🃏 Carte "Gobelin Archer" (Commun)
   → gobelin_archer.png avec bordure grise

🃏 Carte "Dragon de Feu" (Légendaire)  
   → dragon_de_feu.png avec bordure dorée
```

## Fallback et Compatibilité

### ⚡ Système de Fallback

Si aucun template n'est défini pour une rareté :
1. ✅ Utilise le template par défaut (legacy)
2. ✅ Si aucun template, utilise l'image originale
3. ✅ Aucune erreur, toujours fonctionnel

### 🔄 Migration depuis l'ancien système

- Les anciens templates restent fonctionnels
- Configuration graduelle possible
- Pas de perte de données

## Interface Utilisateur

### 🖥️ Fenêtre de Configuration

- **Interface Scrollable** : Toutes les raretés visibles
- **Boutons individuels** : Parcourir/Effacer par rareté
- **Preview instantané** : Voir le chemin sélectionné
- **Validation** : Vérification des fichiers

### 🎛️ Modes d'Interface

- **Mode Complet** : Émojis et interface moderne
- **Mode Compatibilité** : Texte uniquement, plus simple

## Avantages

### 🚀 Améliore le Gameplay
- Identification visuelle immédiate des raretés
- Consistance graphique dans le jeu
- Valeur perçue des cartes légendaires/mythiques

### 🛠️ Facilite le Développement
- Génération automatique des visuels
- Workflow unifié pour toutes les cartes
- Pas de post-traitement manuel requis

### 🎨 Flexibilité Créative
- Templates modulaires et réutilisables
- Design évolutif par rareté
- Support de tous formats d'image

## Conseils de Design

### 🎯 Bonnes Pratiques

1. **Hiérarchie visuelle** : Plus c'est rare, plus c'est spectaculaire
2. **Cohérence** : Même style pour toute une rareté  
3. **Lisibilité** : Ne pas masquer l'illustration principale
4. **Performance** : Optimiser la taille des templates

### ⚠️ À Éviter

- Templates trop lourds (>2MB)
- Masquage de zones importantes de l'illustration
- Couleurs qui se confondent entre raretés
- Effets trop complexes pour les cartes communes

---

**Profitez de cette nouvelle fonctionnalité pour créer des cartes visuellement impactantes ! ✨**
