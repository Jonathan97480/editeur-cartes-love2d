# 🎭 Guide du Système d'Acteurs et Tri par Acteur

## 🆕 Nouvelles Fonctionnalités - Version 2025

L'éditeur de cartes Love2D dispose maintenant d'un **système d'acteurs complet** permettant une organisation thématique de vos cartes par personnage, faction ou type d'entité.

---

## 🎭 Système d'Acteurs

### **Qu'est-ce qu'un Acteur ?**
Un acteur est une entité personnalisable (personnage, faction, classe, etc.) à laquelle vous pouvez associer des cartes. Chaque acteur possède :
- **Nom** personnalisé
- **Icône** distinctive (🎮, 🎭, 👹, 🤖, etc.)
- **Couleur** d'identification
- **Description** optionnelle

### **Accéder à la Gestion d'Acteurs**
1. **Menu 🎭 Acteurs** → **Gérer les Acteurs**
2. Interface dédiée avec liste des acteurs et boutons de gestion

### **Créer un Acteur**
1. Cliquez **"Créer un Acteur"**
2. Saisissez le **nom** (ex: "Paladin", "Mage Noir", "Roi Démon")
3. Choisissez une **icône** dans la liste déroulante
4. Sélectionnez une **couleur** d'identification
5. Ajoutez une **description** (optionnel)
6. Cliquez **"Créer"**

### **Lier des Cartes aux Acteurs**
Dans le formulaire de création/édition de carte :
1. Section **"🎭 Acteurs"** en bas du formulaire
2. **Sélectionnez un ou plusieurs acteurs** dans la liste
3. **Sauvegardez** la carte - elle sera automatiquement liée

---

## 🃏 Visualiseur de Deck avec Tri par Acteur

### **Ouvrir le Visualiseur**
- **Menu Affichage** → **🃏 Voir le deck**
- **Raccourci** : `Ctrl+V`
- Fenêtre dédiée avec toutes vos cartes en grille

### **Section 🎭 Acteurs (Nouveau !)**
Dans la barre latérale gauche :
- **"Tous"** : Affiche toutes les cartes
- **Liste des acteurs** : Filtre les cartes d'un acteur spécifique
- **Icônes et noms** pour identification rapide

### **Utilisation du Filtre par Acteur**
1. **Sélectionnez un acteur** dans la liste
2. Seules **les cartes de cet acteur s'affichent**
3. Le **compteur** indique le nombre de cartes filtrées
4. **"Tous"** pour revenir à l'affichage complet

### **Tri par Acteur (Nouveau !)**
Dans la section **📋 Tri** :
1. Sélectionnez **"Par acteur"**
2. Les cartes se **regroupent par acteur**
3. **Ordre alphabétique** des noms d'acteurs
4. **Cartes sans acteur** apparaissent à la fin

### **Affichage Enrichi des Cartes**
Chaque carte affiche maintenant :
- **🎭 Ligne acteur** avec icône et nom
- **Maximum 2 acteurs** affichés par carte
- **"..."** si plus de 2 acteurs associés
- **"Aucun acteur"** si carte non assignée

### **Filtres Combinés**
Combinez les filtres pour des recherches précises :
- **Rareté + Acteur** : Ex: Cartes légendaires du Roi Démon
- **Type + Acteur** : Ex: Sorts du Mage Noir
- **Rareté + Type + Acteur** : Ex: Attaques rares du Paladin

---

## 📤 Export par Acteur

### **Nouveau Système d'Export**
Remplace l'ancien système Joueur/IA par des exports personnalisés :

### **🎭 Exporter Acteur**
1. **Menu 🎭 Acteurs** → **🎭 Exporter Acteur**
2. **Sélectionnez un acteur** dans la liste
3. **Choisissez l'emplacement** du fichier .lua
4. **Fichier généré** : `export_[nom_acteur].lua`

### **📤 Exporter Tout**
1. **Menu 🎭 Acteurs** → **📤 Exporter Tout**
2. **Tous les acteurs** dans un seul fichier organisé
3. **Sections séparées** par acteur avec commentaires
4. **Fichier généré** : `export_all_actors.lua`

### **Format d'Export Love2D**
```lua
local Cards = {
    --[[ ACTEUR: 🎭 Paladin - 5 cartes ]]
    --[[ CARTE 1 ]]
    {
        name = 'Lumière Divine',
        ImgIlustration = 'lumiere_divine.png',
        Description = 'Soigne tous les alliés',
        PowerBlow = 4,
        Rarete = 'legendaire',
        Type = {'soutien', 'sort'},
        Effect = {
            Actor = { heal = 25, boost = 10 },
            Enemy = { damage = 0 }
        },
        Action = function(card, target) 
            -- Code Love2D 
        end
    },
    -- ... autres cartes
}
return Cards
```

---

## 🎯 Cas d'Utilisation

### **Organisation par Personnage**
- **Héros principal** : Cartes uniques du protagoniste
- **Compagnons** : Cartes spécifiques à chaque allié
- **Boss** : Cartes exclusives des antagonistes

### **Organisation par Faction**
- **Empire** : Cartes militaires et bureaucratiques
- **Rebelles** : Cartes de guérilla et sabotage
- **Neutres** : Cartes communes à tous

### **Organisation par Classe**
- **Guerrier** : Cartes d'attaque et défense
- **Mage** : Cartes de sorts et magie
- **Voleur** : Cartes de vitesse et furtivité

---

## 🔧 Conseils d'Utilisation

### **Bonnes Pratiques**
- **Noms explicites** : "Roi Démon" plutôt que "Boss1"
- **Icônes cohérentes** : 👑 pour royauté, ⚔️ pour guerriers
- **Couleurs logiques** : Rouge pour feu, Bleu pour glace
- **Descriptions utiles** : Contexte du personnage

### **Workflow Recommandé**
1. **Créez vos acteurs** avant les cartes
2. **Organisez par thème** : personnages → factions → classes
3. **Utilisez le visualiseur** pour vérifier l'équilibre
4. **Exportez par acteur** pour des fichiers organisés
5. **Testez** dans votre jeu Love2D

### **Migration depuis l'Ancien Système**
- **Anciennes cartes Joueur/IA** : Création automatique d'acteurs "Joueur" et "IA"
- **Réorganisation** : Créez de nouveaux acteurs et réassignez les cartes
- **Export mixte** : Ancien système toujours disponible dans Menu Fichier

---

## 🎊 Avantages du Nouveau Système

### **Avant (Joueur/IA)**
- ❌ Limité à 2 catégories
- ❌ Export unique non organisé
- ❌ Pas de personnalisation visuelle
- ❌ Difficile à organiser

### **Après (Système d'Acteurs)**
- ✅ **Acteurs illimités** et personnalisables
- ✅ **Export organisé** par acteur/groupe
- ✅ **Interface visuelle** avec icônes et couleurs
- ✅ **Tri et filtrage** avancés
- ✅ **Organisation thématique** intuitive
- ✅ **Cartes multi-acteurs** supportées

---

## 🚀 Pour Commencer

1. **Lancez l'application** : `python app_final.py`
2. **Créez vos premiers acteurs** : Menu 🎭 Acteurs → Gérer les Acteurs
3. **Assignez vos cartes** : Utilisez la section 🎭 Acteurs du formulaire
4. **Explorez le visualiseur** : Ctrl+V pour voir le tri par acteur
5. **Exportez vos cartes** : Menu 🎭 Acteurs → Export par choix

**Profitez de l'organisation thématique parfaite de vos cartes Love2D ! 🎮**
