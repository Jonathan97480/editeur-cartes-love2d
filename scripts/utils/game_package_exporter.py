"""
Exporteur de package complet Love2D
Crée un ZIP contenant toutes les ressources nécessaires pour le jeu
"""
import os
import zipfile
import shutil
from pathlib import Path
import json
from datetime import datetime

# Import de l'exporteur Love2D (ajuster le chemin selon la structure)
try:
    from lua_exporter_love2d import Love2DLuaExporter
except ImportError:
    # Fallback si le module n'est pas trouvé
    Love2DLuaExporter = None

class GamePackageExporter:
    """Exporteur pour créer des packages complets Love2D"""
    
    def __init__(self, repo, output_dir):
        """
        Initialise l'exporteur
        
        Args:
            repo: Repository des cartes
            output_dir: Dossier de sortie pour les packages
        """
        self.repo = repo
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Dossiers sources
        self.base_dir = Path(__file__).parent
        self.images_dir = self.base_dir / "images"
        self.fonts_dir = self.base_dir / "fonts"
        
    def export_complete_package(self, package_name="love2d_cards_package"):
        """
        Exporte un package complet Love2D
        
        Args:
            package_name: Nom du package à créer
            
        Returns:
            str: Chemin vers le fichier ZIP créé
        """
        # Nom du fichier ZIP avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"{package_name}_{timestamp}.zip"
        zip_path = self.output_dir / zip_filename
        
        # Créer le dossier temporaire
        temp_dir = self.output_dir / f"temp_{timestamp}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # 1. Exporter les cartes au format Lua
            self._export_cards_lua(temp_dir)
            
            # 2. Copier les images
            self._copy_images(temp_dir)
            
            # 3. Copier les polices
            self._copy_fonts(temp_dir)
            
            # 4. Créer la documentation
            self._create_documentation(temp_dir)
            
            # 5. Créer le fichier ZIP
            self._create_zip_package(temp_dir, zip_path)
            
            return str(zip_path)
            
        finally:
            # Nettoyer le dossier temporaire
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def _export_cards_lua(self, temp_dir):
        """Exporte les cartes au format Lua"""
        temp_dir = Path(temp_dir)  # Convertir en Path si nécessaire
        cards_dir = temp_dir / "cards"
        cards_dir.mkdir(exist_ok=True)
        
        # Vérifier que l'exporteur est disponible
        if Love2DLuaExporter is None:
            raise ImportError("L'exporteur Love2D n'est pas disponible. Vérifiez que lua_exporter_love2d.py existe.")
        
        # Utiliser l'exporteur Love2D avec formatage
        exporter = Love2DLuaExporter(self.repo)
        
        # Export des cartes joueur (utiliser la bonne méthode)
        lua_content = exporter.export_all_cards_love2d()
        lua_file = cards_dir / "cards_joueur.lua"
        
        with open(lua_file, 'w', encoding='utf-8') as f:
            f.write(lua_content)
        
        print(f"✅ Cartes exportées: {lua_file}")
    
    def _copy_images(self, temp_dir):
        """Copie les images de cartes"""
        temp_dir = Path(temp_dir)  # Convertir en Path si nécessaire
        images_dest = temp_dir / "images"
        
        if self.images_dir.exists():
            shutil.copytree(self.images_dir, images_dest, dirs_exist_ok=True)
            print(f"✅ Images copiées: {images_dest}")
        else:
            images_dest.mkdir(exist_ok=True)
            print("⚠️ Dossier images non trouvé, dossier vide créé")
    
    def _copy_fonts(self, temp_dir):
        """Copie les polices"""
        temp_dir = Path(temp_dir)  # Convertir en Path si nécessaire
        fonts_dest = temp_dir / "fonts"
        
        if self.fonts_dir.exists():
            shutil.copytree(self.fonts_dir, fonts_dest, dirs_exist_ok=True)
            print(f"✅ Polices copiées: {fonts_dest}")
        else:
            fonts_dest.mkdir(exist_ok=True)
            print("⚠️ Dossier fonts non trouvé, dossier vide créé")
    
    def _create_documentation(self, temp_dir):
        """Crée la documentation du package"""
        temp_dir = Path(temp_dir)  # Convertir en Path si nécessaire
        docs_dir = temp_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # README principal
        readme_content = self._generate_readme()
        with open(docs_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Configuration Love2D
        love_config = self._generate_love_config()
        with open(temp_dir / "conf.lua", 'w', encoding='utf-8') as f:
            f.write(love_config)
        
        # Exemple d'intégration
        example_code = self._generate_example_code()
        with open(docs_dir / "example_integration.lua", 'w', encoding='utf-8') as f:
            f.write(example_code)
        
        print(f"✅ Documentation créée: {docs_dir}")
    
    def _generate_readme(self):
        """Génère le contenu du README"""
        cards = self.repo.list_cards()
        card_count = len(cards)
        
        return f"""# Package Love2D - Éditeur de Cartes

## 📦 Contenu du Package

Ce package contient toutes les ressources nécessaires pour intégrer vos cartes dans un jeu Love2D.

### 🎮 Cartes
- **{card_count} cartes** exportées avec formatage complet
- Données Love2D natives (positions, polices, couleurs)
- Système d'effets et d'actions inclus

### 🖼️ Images
- Images de cartes optimisées
- Format PNG haute qualité
- Dimensions standardisées Love2D (280x392px)

### 🔤 Polices
- Polices système et personnalisées
- Compatibilité Love2D garantie

## 🚀 Installation

1. Extractez ce package dans votre projet Love2D
2. Incluez le fichier `cards/cards_joueur.lua` dans votre code
3. Utilisez les exemples fournis dans `docs/`

## 📖 Documentation

- `docs/example_integration.lua` - Exemple d'intégration
- `conf.lua` - Configuration Love2D recommandée

## ✨ Fonctionnalités

- ✅ Formatage de texte précis
- ✅ Positionnement Love2D natif
- ✅ Système d'effets complet
- ✅ Documentation complète
- ✅ Prêt à utiliser

## 🛠️ Support

Généré par l'Éditeur de Cartes Love2D
Date: {datetime.now().strftime("%d/%m/%Y à %H:%M")}

Bon développement ! 🎮
"""
    
    def _generate_love_config(self):
        """Génère la configuration Love2D"""
        return """function love.conf(t)
    t.title = "Mon Jeu de Cartes"
    t.author = "Créé avec l'Éditeur de Cartes Love2D"
    t.version = "11.4"
    t.console = false
    
    -- Fenêtre
    t.window.width = 1024
    t.window.height = 768
    t.window.resizable = true
    t.window.minwidth = 800
    t.window.minheight = 600
    
    -- Modules nécessaires pour les cartes
    t.modules.joystick = true
    t.modules.audio = true
    t.modules.keyboard = true
    t.modules.mouse = true
    t.modules.timer = true
    t.modules.image = true
    t.modules.graphics = true
    t.modules.font = true
end
"""
    
    def _generate_example_code(self):
        """Génère un exemple d'intégration"""
        return """-- Exemple d'intégration des cartes dans Love2D

-- Charger les cartes
local cards = require("cards.cards_joueur")

function love.load()
    -- Initialiser le système de cartes
    print("Cartes chargées:", #cards)
    
    -- Exemple: afficher une carte
    current_card = cards[1]
    
    -- Charger les polices nécessaires
    font_title = love.graphics.newFont(current_card.TextFormatting.title.size)
    font_text = love.graphics.newFont(current_card.TextFormatting.text.size)
    
    -- Charger l'image de la carte
    if current_card.ImgIlustration then
        card_image = love.graphics.newImage(current_card.ImgIlustration)
    end
end

function love.draw()
    if not current_card then return end
    
    local formatting = current_card.TextFormatting
    
    -- Dessiner l'image de la carte
    if card_image then
        love.graphics.draw(card_image, 100, 100)
    end
    
    -- Dessiner le titre
    love.graphics.setColor(1, 1, 1, 1) -- Blanc
    love.graphics.setFont(font_title)
    love.graphics.print(current_card.name, 
                       100 + formatting.title.x, 
                       100 + formatting.title.y)
    
    -- Dessiner la description
    love.graphics.setFont(font_text)
    love.graphics.printf(current_card.Description,
                        100 + formatting.text.x,
                        100 + formatting.text.y,
                        formatting.text.width,
                        formatting.text.align)
    
    -- Dessiner le coût en énergie
    love.graphics.print(tostring(current_card.PowerBlow),
                       100 + formatting.energy.x,
                       100 + formatting.energy.y)
end

function love.keypressed(key)
    -- Changer de carte avec les flèches
    if key == "right" then
        local current_index = 1
        for i, card in ipairs(cards) do
            if card == current_card then
                current_index = i
                break
            end
        end
        
        current_index = current_index + 1
        if current_index > #cards then
            current_index = 1
        end
        
        current_card = cards[current_index]
        
        -- Recharger l'image
        if current_card.ImgIlustration then
            card_image = love.graphics.newImage(current_card.ImgIlustration)
        end
    end
end
"""
    
    def _create_zip_package(self, temp_dir, zip_path):
        """Crée le fichier ZIP final"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Package créé: {zip_path}")
