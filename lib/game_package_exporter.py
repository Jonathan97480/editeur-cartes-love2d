#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 EXPORTEUR DE PACKAGE DE JEU COMPLET
=====================================

Crée un package ZIP structuré contenant :
- Fichier Lua des cartes avec formatage
- Images fusionnées des cartes
- Polices utilisées
- Configuration et documentation

Prêt pour intégration dans un projet Love2D
"""

import os
import zipfile
import shutil
from pathlib import Path
from typing import List, Dict, Set, Optional
import json
from PIL import Image, ImageDraw, ImageFont
import logging

try:
    # Import avec préfixe de module pour intégration UI
    from .database import CardRepo
    from .font_manager import FontManager
    from .config import DB_FILE
except ImportError:
    # Import direct pour utilisation standalone
    from database import CardRepo
    from font_manager import FontManager
    from config import DB_FILE

class GamePackageExporter:
    """Exporteur de package de jeu complet."""
    
    def __init__(self, repo: CardRepo, output_dir: str = "game_packages"):
        """
        Initialise l'exporteur de package.
        
        Args:
            repo: Repository des cartes
            output_dir: Dossier de sortie pour les packages
        """
        self.repo = repo
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Gestionnaire de polices
        self.font_manager = FontManager()
        
        # Collections pour suivre les ressources utilisées
        self.used_fonts: Set[str] = set()
        self.used_images: Set[str] = set()
        
        # Configuration du package
        self.package_config = {
            "name": "Cards Package",
            "version": "1.0.0",
            "created_by": "Editeur de Cartes",
            "love2d_version": "11.4",
            "description": "Package complet de cartes pour Love2D"
        }
    
    def analyze_cards_resources(self, cards: List) -> Dict:
        """
        Analyse les ressources utilisées par les cartes.
        
        Returns:
            Dictionnaire des ressources utilisées
        """
        resources = {
            "fonts": set(),
            "images": set(),
            "card_count": len(cards),
            "total_size": 0
        }
        
        for card in cards:
            # Analyser les polices utilisées
            if hasattr(card, 'title_font') and card.title_font:
                resources["fonts"].add(card.title_font)
            if hasattr(card, 'text_font') and card.text_font:
                resources["fonts"].add(card.text_font)
            if hasattr(card, 'energy_font') and card.energy_font:
                resources["fonts"].add(card.energy_font)
            
            # Analyser les images utilisées
            if hasattr(card, 'img') and card.img:
                resources["images"].add(card.img)
            if hasattr(card, 'original_img') and card.original_img:
                resources["images"].add(card.original_img)
        
        return resources
    
    def create_fused_card_image(self, card, output_path: str) -> bool:
        """
        Crée une image fusionnée de la carte avec texte et éléments.
        
        Args:
            card: Carte à traiter
            output_path: Chemin de sortie pour l'image
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Dimensions standard d'une carte Love2D
            card_width = 280
            card_height = 392
            
            # Créer une image de base
            if hasattr(card, 'img') and card.img and os.path.exists(card.img):
                # Charger l'image de base de la carte
                base_image = Image.open(card.img)
                base_image = base_image.resize((card_width, card_height), Image.Resampling.LANCZOS)
            else:
                # Créer une image par défaut
                base_image = Image.new('RGB', (card_width, card_height), color='#f0f0f0')
            
            # Créer un objet de dessin
            draw = ImageDraw.Draw(base_image)
            
            # Ajouter le titre
            if hasattr(card, 'name') and card.name:
                try:
                    # Charger la police du titre
                    title_font_size = getattr(card, 'title_size', 16)
                    title_font_name = getattr(card, 'title_font', 'Arial')
                    
                    # Essayer de charger la police
                    title_font = self._load_font_for_image(title_font_name, title_font_size)
                    
                    # Position du titre
                    title_x = getattr(card, 'title_x', 20)
                    title_y = getattr(card, 'title_y', 20)
                    title_color = getattr(card, 'title_color', '#000000')
                    
                    # Dessiner le titre
                    draw.text((title_x, title_y), card.name, 
                             font=title_font, fill=title_color)
                    
                except Exception as e:
                    logging.warning(f"Erreur lors de l'ajout du titre: {e}")
            
            # Ajouter le coût d'énergie
            if hasattr(card, 'powerblow') and card.powerblow is not None:
                try:
                    energy_font_size = getattr(card, 'energy_size', 14)
                    energy_font_name = getattr(card, 'energy_font', 'Arial')
                    energy_font = self._load_font_for_image(energy_font_name, energy_font_size)
                    
                    energy_x = getattr(card, 'energy_x', card_width - 40)
                    energy_y = getattr(card, 'energy_y', 20)
                    energy_color = getattr(card, 'energy_color', '#0066cc')
                    
                    # Dessiner le coût d'énergie dans un cercle
                    circle_radius = 15
                    draw.ellipse([energy_x - circle_radius, energy_y - circle_radius,
                                 energy_x + circle_radius, energy_y + circle_radius],
                                fill='#ffffff', outline=energy_color, width=2)
                    
                    # Centrer le texte dans le cercle
                    energy_text = str(card.powerblow)
                    bbox = draw.textbbox((0, 0), energy_text, font=energy_font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    draw.text((energy_x - text_width // 2, energy_y - text_height // 2),
                             energy_text, font=energy_font, fill=energy_color)
                    
                except Exception as e:
                    logging.warning(f"Erreur lors de l'ajout de l'énergie: {e}")
            
            # Ajouter la description (si elle rentre)
            if hasattr(card, 'description') and card.description:
                try:
                    text_font_size = getattr(card, 'text_size', 12)
                    text_font_name = getattr(card, 'text_font', 'Arial')
                    text_font = self._load_font_for_image(text_font_name, text_font_size)
                    
                    text_x = getattr(card, 'text_x', 20)
                    text_y = getattr(card, 'text_y', 200)
                    text_width = getattr(card, 'text_width', card_width - 40)
                    text_color = getattr(card, 'text_color', '#333333')
                    
                    # Diviser le texte en lignes
                    lines = self._wrap_text(card.description, text_font, text_width, draw)
                    
                    # Dessiner chaque ligne
                    line_height = text_font_size + 2
                    for i, line in enumerate(lines[:6]):  # Limiter à 6 lignes
                        draw.text((text_x, text_y + i * line_height),
                                 line, font=text_font, fill=text_color)
                    
                except Exception as e:
                    logging.warning(f"Erreur lors de l'ajout de la description: {e}")
            
            # Sauvegarder l'image fusionnée
            base_image.save(output_path, "PNG", quality=90)
            return True
            
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'image fusionnée: {e}")
            return False
    
    def _load_font_for_image(self, font_name: str, size: int) -> ImageFont.FreeTypeFont:
        """
        Charge une police pour PIL/ImageDraw.
        
        Args:
            font_name: Nom de la police
            size: Taille de la police
            
        Returns:
            Police chargée ou police par défaut
        """
        try:
            # Essayer de charger une police personnalisée
            font_path = self._find_font_file(font_name)
            if font_path and os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
            
            # Police par défaut
            return ImageFont.load_default()
            
        except Exception:
            return ImageFont.load_default()
    
    def _find_font_file(self, font_name: str) -> Optional[str]:
        """
        Trouve le fichier de police correspondant au nom.
        
        Args:
            font_name: Nom de la police
            
        Returns:
            Chemin vers le fichier de police ou None
        """
        # Nettoyer le nom de police pour supprimer le préfixe 🎨
        clean_font_name = font_name.replace("🎨 ", "")
        
        # 1. Chercher dans le dossier fonts personnalisées
        fonts_dir = Path("fonts")
        
        for subdir in ["titre", "texte", "special"]:
            subdir_path = fonts_dir / subdir
            if subdir_path.exists():
                for ext in [".ttf", ".otf", ".TTF", ".OTF"]:
                    font_file = subdir_path / f"{clean_font_name}{ext}"
                    if font_file.exists():
                        return str(font_file)
        
        # 2. Chercher dans le dossier fonts racine
        if fonts_dir.exists():
            for ext in [".ttf", ".otf", ".TTF", ".OTF"]:
                font_file = fonts_dir / f"{clean_font_name}{ext}"
                if font_file.exists():
                    return str(font_file)
        
        # 3. Pour les polices système courantes, essayer de les trouver dans Windows
        if os.name == 'nt':  # Windows
            windows_fonts_dir = Path("C:/Windows/Fonts")
            if windows_fonts_dir.exists():
                # Mapping des noms de polices vers leurs fichiers
                system_font_mapping = {
                    "Arial": ["arial.ttf", "Arial.ttf"],
                    "Times New Roman": ["times.ttf", "timesbd.ttf", "Times New Roman.ttf"],
                    "Courier New": ["cour.ttf", "Courier New.ttf"],
                    "Verdana": ["verdana.ttf", "Verdana.ttf"],
                    "Calibri": ["calibri.ttf", "Calibri.ttf"],
                    "Cambria": ["cambria.ttc", "cambria.ttf", "Cambria.ttf"],
                    "Tahoma": ["tahoma.ttf", "Tahoma.ttf"],
                    "Georgia": ["georgia.ttf", "Georgia.ttf"],
                    "Comic Sans MS": ["comic.ttf", "Comic Sans MS.ttf"],
                    "Impact": ["impact.ttf", "Impact.ttf"],
                    "Trebuchet MS": ["trebuc.ttf", "Trebuchet MS.ttf"],
                    "Segoe UI": ["segoeui.ttf", "Segoe UI.ttf"],
                    "Microsoft Sans Serif": ["micross.ttf", "Microsoft Sans Serif.ttf"]
                }
                
                if clean_font_name in system_font_mapping:
                    for font_filename in system_font_mapping[clean_font_name]:
                        font_path = windows_fonts_dir / font_filename
                        if font_path.exists():
                            return str(font_path)
                
                # 4. Recherche générale dans le dossier Windows Fonts
                for ext in [".ttf", ".ttc", ".otf", ".TTF", ".TTC", ".OTF"]:
                    # Essayer le nom exact
                    font_path = windows_fonts_dir / f"{clean_font_name}{ext}"
                    if font_path.exists():
                        return str(font_path)
                    
                    # Essayer avec des variations courantes
                    variations = [
                        clean_font_name.lower(),
                        clean_font_name.replace(" ", ""),
                        clean_font_name.replace(" ", "").lower()
                    ]
                    
                    for variation in variations:
                        font_path = windows_fonts_dir / f"{variation}{ext}"
                        if font_path.exists():
                            return str(font_path)
        
        return None
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, 
                   max_width: int, draw: ImageDraw.Draw) -> List[str]:
        """
        Divise le texte en lignes pour qu'il rentre dans la largeur donnée.
        
        Args:
            text: Texte à diviser
            font: Police utilisée
            max_width: Largeur maximale
            draw: Objet de dessin
            
        Returns:
            Liste des lignes
        """
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def copy_used_fonts(self, fonts: Set[str], fonts_dir: Path) -> Dict[str, str]:
        """
        Copie les polices utilisées dans le package.
        
        Args:
            fonts: Set des noms de polices utilisées
            fonts_dir: Dossier de destination
            
        Returns:
            Dictionnaire {nom_police: chemin_copié}
        """
        copied_fonts = {}
        fonts_dir.mkdir(exist_ok=True)
        
        for font_name in fonts:
            # Nettoyer le nom de police pour supprimer le préfixe 🎨
            clean_font_name = font_name.replace("🎨 ", "")
            
            # Chercher le fichier de police
            font_file = self._find_font_file(clean_font_name)
            
            if font_file and os.path.exists(font_file):
                # Copier le fichier
                dest_file = fonts_dir / os.path.basename(font_file)
                shutil.copy2(font_file, dest_file)
                copied_fonts[font_name] = str(dest_file)
                print(f"📝 Police copiée: {font_name} -> {dest_file.name}")
            else:
                print(f"⚠️  Police non trouvée: {font_name}")
        
        return copied_fonts
    
    def export_lua_data(self, cards: List, lua_file: Path) -> int:
        """
        Exporte les données Lua des cartes.
        
        Args:
            cards: Liste des cartes
            lua_file: Fichier de destination
            
        Returns:
            Taille du fichier généré
        """
        # Import de l'exporteur Love2D
        try:
            from lua_exporter_love2d import Love2DLuaExporter
        except ImportError:
            # Import depuis le répertoire parent si import relatif échoue
            import sys
            import os
            parent_dir = os.path.dirname(os.path.dirname(__file__))
            sys.path.insert(0, parent_dir)
            from lua_exporter_love2d import Love2DLuaExporter
        
        exporter = Love2DLuaExporter(self.repo)
        content = exporter.export_all_cards_love2d()
        
        with open(lua_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return len(content)
    
    def create_package_documentation(self, package_dir: Path, resources: Dict) -> None:
        """
        Crée la documentation du package.
        
        Args:
            package_dir: Dossier du package
            resources: Informations sur les ressources
        """
        readme_content = f"""# 🎮 Package de Cartes Love2D

## Description
{self.package_config['description']}

**Version:** {self.package_config['version']}
**Créé par:** {self.package_config['created_by']}
**Compatible Love2D:** {self.package_config['love2d_version']}+

## Structure du Package

```
📁 {package_dir.name}/
├── 📁 cards/               # Images fusionnées des cartes
├── 📁 fonts/               # Polices utilisées
├── 📄 cards_data.lua       # Données des cartes
├── 📄 package_config.json  # Configuration du package
└── 📄 README.md           # Cette documentation
```

## Statistiques

- **Cartes:** {resources['card_count']}
- **Polices:** {len(resources['fonts'])}
- **Images:** {len(resources['images'])}

## Utilisation dans Love2D

### 1. Charger les données des cartes
```lua
local cards = require("cards_data")

-- Accéder aux cartes
for i, card in ipairs(cards) do
    print("Carte:", card.name)
    print("Coût:", card.PowerBlow)
    print("Description:", card.Description)
end
```

### 2. Utiliser les polices
```lua
-- Les polices sont dans le dossier fonts/
local titleFont = love.graphics.newFont("fonts/ma_police.ttf", 16)
```

### 3. Charger les images
```lua
-- Les images fusionnées sont dans le dossier cards/
local cardImage = love.graphics.newImage("cards/carte_001.png")
```

### 4. Formatage de texte
Chaque carte contient une section `TextFormatting` avec:
- Position et style du titre
- Position et zone de texte de description
- Position et style du coût d'énergie
- Dimensions de la carte

## Exemple d'utilisation complète

```lua
local cards = require("cards_data")

function love.load()
    -- Charger une carte
    local card = cards[1]
    
    -- Charger l'image fusionnée
    card.image = love.graphics.newImage("cards/carte_001.png")
    
    -- Charger les polices si nécessaire
    if card.TextFormatting.title.font ~= "Arial" then
        card.titleFont = love.graphics.newFont("fonts/" .. card.TextFormatting.title.font .. ".ttf", 
                                             card.TextFormatting.title.size)
    end
end

function love.draw()
    local card = cards[1]
    
    -- Dessiner l'image de la carte
    love.graphics.draw(card.image, 100, 100)
    
    -- Ou utiliser les données de formatage pour dessiner séparément
    local fmt = card.TextFormatting
    love.graphics.setColor(1, 1, 1) -- Blanc
    love.graphics.printf(card.name, 
                        100 + fmt.title.x, 100 + fmt.title.y, 
                        fmt.card.width, "center")
end
```

## Notes

- Les images fusionnées incluent déjà le texte rendu
- Utilisez les données TextFormatting pour un contrôle précis
- Toutes les polices utilisées sont incluses dans le package
- Compatible avec Love2D 11.4 et versions ultérieures

---
*Généré automatiquement par l'Éditeur de Cartes*
"""
        
        readme_file = package_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def create_package_config(self, package_dir: Path, resources: Dict) -> None:
        """
        Crée le fichier de configuration du package.
        
        Args:
            package_dir: Dossier du package
            resources: Informations sur les ressources
        """
        config = {
            **self.package_config,
            "resources": {
                "card_count": resources['card_count'],
                "font_count": len(resources['fonts']),
                "image_count": len(resources['images']),
                "fonts_used": list(resources['fonts']),
                "images_used": list(resources['images'])
            },
            "structure": {
                "cards_dir": "cards/",
                "fonts_dir": "fonts/",
                "lua_file": "cards_data.lua"
            }
        }
        
        config_file = package_dir / "package_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def export_complete_package(self, package_name: str = "cards_package") -> str:
        """
        Exporte un package complet de jeu.
        
        Args:
            package_name: Nom du package
            
        Returns:
            Chemin vers le fichier ZIP créé
        """
        print(f"🎮 Création du package complet: {package_name}")
        print("=" * 60)
        
        # Récupérer les cartes
        cards = self.repo.list_cards()
        if not cards:
            raise ValueError("Aucune carte trouvée dans la base de données")
        
        print(f"📝 Cartes trouvées: {len(cards)}")
        
        # Analyser les ressources
        resources = self.analyze_cards_resources(cards)
        print(f"🎨 Polices utilisées: {len(resources['fonts'])}")
        print(f"🖼️  Images utilisées: {len(resources['images'])}")
        
        # Créer le dossier temporaire
        temp_dir = self.output_dir / f"{package_name}_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True)
        
        try:
            # 1. Créer les dossiers de structure
            cards_dir = temp_dir / "cards"
            fonts_dir = temp_dir / "fonts"
            cards_dir.mkdir()
            fonts_dir.mkdir()
            
            # 2. Exporter le fichier Lua
            print("📄 Export des données Lua...")
            lua_file = temp_dir / "cards_data.lua"
            lua_size = self.export_lua_data(cards, lua_file)
            print(f"   ✅ Fichier Lua créé: {lua_size:,} caractères")
            
            # 3. Créer les images fusionnées
            print("🖼️  Création des images fusionnées...")
            for i, card in enumerate(cards, 1):
                image_name = f"carte_{i:03d}.png"
                image_path = cards_dir / image_name
                
                if self.create_fused_card_image(card, str(image_path)):
                    print(f"   ✅ Image créée: {image_name} ({card.name})")
                else:
                    print(f"   ⚠️  Erreur image: {image_name}")
            
            # 4. Copier les polices utilisées
            print("🎨 Copie des polices...")
            copied_fonts = self.copy_used_fonts(resources['fonts'], fonts_dir)
            print(f"   ✅ Polices copiées: {len(copied_fonts)}")
            
            # 5. Créer la documentation
            print("📚 Création de la documentation...")
            self.create_package_documentation(temp_dir, resources)
            self.create_package_config(temp_dir, resources)
            print("   ✅ Documentation créée")
            
            # 6. Créer le fichier ZIP
            print("📦 Création du package ZIP...")
            zip_path = self.output_dir / f"{package_name}.zip"
            if zip_path.exists():
                zip_path.unlink()
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arc_path = file_path.relative_to(temp_dir)
                        zipf.write(file_path, arc_path)
            
            # Calculer la taille du ZIP
            zip_size = zip_path.stat().st_size
            print(f"   ✅ Package créé: {zip_path.name} ({zip_size:,} octets)")
            
            # 7. Nettoyer le dossier temporaire
            shutil.rmtree(temp_dir)
            
            print(f"\n🎉 Package complet créé avec succès!")
            print(f"📍 Emplacement: {zip_path}")
            print(f"📊 Contenu: {len(cards)} cartes, {len(copied_fonts)} polices, documentation")
            
            return str(zip_path)
            
        except Exception as e:
            # Nettoyer en cas d'erreur
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            raise e


def main():
    """Test de l'exporteur de package."""
    try:
        repo = CardRepo(DB_FILE)
        exporter = GamePackageExporter(repo)
        
        package_path = exporter.export_complete_package("mon_jeu_cartes")
        print(f"Package créé: {package_path}")
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
