# Dossier Fonts - Polices Personnalisées

Ce dossier contient les polices personnalisées utilisables dans l'éditeur de formatage de texte.

## Formats supportés
- **TTF** (TrueType Font) - Recommandé
- **OTF** (OpenType Font) - Supporté

## Installation d'une nouvelle police
1. Copiez le fichier de police (`.ttf` ou `.otf`) dans ce dossier
2. Redémarrez l'application
3. La police sera disponible dans l'éditeur de formatage

## Polices incluses par défaut
- Aucune police personnalisée installée pour le moment

## Structure recommandée
```
fonts/
├── titre/          # Polices pour les titres de cartes
├── texte/          # Polices pour le texte descriptif
├── special/        # Polices décoratives ou spéciales
└── README.md       # Ce fichier
```

## Notes techniques
- L'application charge automatiquement toutes les polices présentes dans ce dossier
- Les polices sont utilisables immédiatement après redémarrage
- Évitez les polices trop lourdes (> 5MB) pour maintenir les performances
- Privilégiez les polices avec support Unicode pour la compatibilité

## Polices recommandées pour les cartes de jeu
- **Titres** : Polices bold, serif ou fantasy
- **Descriptions** : Polices lisibles, sans-serif ou serif classique
- **Effets spéciaux** : Polices décoratives pour mettre en avant certains éléments
