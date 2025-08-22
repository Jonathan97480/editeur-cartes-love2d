#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 GESTIONNAIRE DE POLICES PERSONNALISÉES
=========================================

Module pour gérer les polices personnalisées dans l'éditeur de cartes.
Permet de charger et utiliser des polices TTF/OTF dans l'interface Tkinter.
"""

import os
import tkinter as tk
from tkinter import font
from pathlib import Path
from typing import List, Dict, Optional
import logging

class FontManager:
    """Gestionnaire des polices personnalisées pour l'application."""
    
    def __init__(self, fonts_dir: str = "fonts"):
        """
        Initialise le gestionnaire de polices.
        
        Args:
            fonts_dir: Chemin vers le dossier des polices
        """
        self.fonts_dir = Path(fonts_dir)
        self.loaded_fonts: Dict[str, str] = {}
        self.system_fonts: List[str] = []
        self.custom_fonts: List[str] = []
        
        # Créer le dossier fonts s'il n'existe pas
        self.fonts_dir.mkdir(exist_ok=True)
        
        # Charger les polices système
        self._load_system_fonts()
        
        # Charger les polices personnalisées
        self._load_custom_fonts()
    
    def _load_system_fonts(self):
        """Charge la liste des polices système disponibles."""
        try:
            # Créer temporairement une fenêtre racine pour accéder aux polices
            import tkinter as tk
            temp_root = tk.Tk()
            temp_root.withdraw()  # Cacher la fenêtre
            
            self.system_fonts = sorted(font.families())
            logging.info(f"🎨 Polices système chargées: {len(self.system_fonts)}")
            
            temp_root.destroy()
            
        except Exception as e:
            logging.error(f"❌ Erreur chargement polices système: {e}")
            self.system_fonts = ["Arial", "Times New Roman", "Courier New", "Helvetica", "Georgia"]
    
    def _load_custom_fonts(self):
        """Charge les polices personnalisées depuis le dossier fonts/."""
        try:
            font_files = []
            
            # Scanner tous les fichiers TTF et OTF
            for pattern in ["**/*.ttf", "**/*.otf", "**/*.TTF", "**/*.OTF"]:
                font_files.extend(self.fonts_dir.glob(pattern))
            
            # Charger chaque police
            for font_file in font_files:
                try:
                    # Extraire le nom de la police (sans extension)
                    font_name = font_file.stem
                    
                    # Ajouter à la liste des polices personnalisées
                    self.custom_fonts.append(font_name)
                    self.loaded_fonts[font_name] = str(font_file.absolute())
                    
                    logging.info(f"✅ Police chargée: {font_name}")
                    
                except Exception as e:
                    logging.warning(f"⚠️ Impossible de charger {font_file.name}: {e}")
            
            logging.info(f"🎨 Polices personnalisées: {len(self.custom_fonts)}")
            
        except Exception as e:
            logging.error(f"❌ Erreur chargement polices personnalisées: {e}")
    
    def get_all_fonts(self) -> List[str]:
        """
        Retourne la liste complète des polices disponibles.
        
        Returns:
            Liste combinée des polices système et personnalisées
        """
        # Combiner polices système et personnalisées
        all_fonts = []
        
        # Ajouter les polices personnalisées en premier (priorité)
        if self.custom_fonts:
            all_fonts.extend([f"🎨 {name}" for name in sorted(self.custom_fonts)])
            all_fonts.append("─" * 20)  # Séparateur
        
        # Ajouter les polices système
        all_fonts.extend(self.system_fonts)
        
        return all_fonts
    
    def get_custom_fonts(self) -> List[str]:
        """Retourne uniquement les polices personnalisées."""
        return sorted(self.custom_fonts)
    
    def get_system_fonts(self) -> List[str]:
        """Retourne uniquement les polices système."""
        return self.system_fonts
    
    def get_font_path(self, font_name: str) -> Optional[str]:
        """
        Retourne le chemin vers un fichier de police personnalisée.
        
        Args:
            font_name: Nom de la police
            
        Returns:
            Chemin vers le fichier ou None si non trouvé
        """
        # Nettoyer le nom (enlever le préfixe 🎨 si présent)
        clean_name = font_name.replace("🎨 ", "").strip()
        return self.loaded_fonts.get(clean_name)
    
    def is_custom_font(self, font_name: str) -> bool:
        """
        Vérifie si une police est personnalisée.
        
        Args:
            font_name: Nom de la police
            
        Returns:
            True si c'est une police personnalisée
        """
        clean_name = font_name.replace("🎨 ", "").strip()
        return clean_name in self.custom_fonts
    
    def create_font(self, font_name: str, size: int = 12, **kwargs) -> font.Font:
        """
        Crée un objet Font Tkinter.
        
        Args:
            font_name: Nom de la police
            size: Taille de la police
            **kwargs: Autres paramètres (weight, slant, etc.)
            
        Returns:
            Objet tkinter.font.Font
        """
        try:
            # Nettoyer le nom
            clean_name = font_name.replace("🎨 ", "").strip()
            
            # Si c'est une police personnalisée, utiliser le chemin complet
            if self.is_custom_font(font_name):
                font_path = self.get_font_path(clean_name)
                if font_path and os.path.exists(font_path):
                    # Pour les polices personnalisées, utiliser le nom du fichier
                    return font.Font(family=clean_name, size=size, **kwargs)
            
            # Utiliser le nom tel quel pour les polices système
            return font.Font(family=clean_name, size=size, **kwargs)
            
        except Exception as e:
            logging.warning(f"⚠️ Erreur création police {font_name}: {e}")
            # Fallback vers Arial
            return font.Font(family="Arial", size=size, **kwargs)
    
    def refresh_fonts(self):
        """Recharge toutes les polices (après ajout de nouvelles polices)."""
        logging.info("🔄 Rechargement des polices...")
        self.loaded_fonts.clear()
        self.custom_fonts.clear()
        self._load_custom_fonts()
    
    def install_font(self, font_file_path: str, category: str = "texte") -> bool:
        """
        Installe une nouvelle police dans le dossier approprié.
        
        Args:
            font_file_path: Chemin vers le fichier de police
            category: Catégorie (titre, texte, special)
            
        Returns:
            True si l'installation a réussi
        """
        try:
            source_path = Path(font_file_path)
            
            # Vérifier que le fichier existe et a la bonne extension
            if not source_path.exists():
                logging.error(f"❌ Fichier inexistant: {font_file_path}")
                return False
            
            if source_path.suffix.lower() not in ['.ttf', '.otf']:
                logging.error(f"❌ Format non supporté: {source_path.suffix}")
                return False
            
            # Créer le dossier de destination
            dest_dir = self.fonts_dir / category
            dest_dir.mkdir(exist_ok=True)
            
            # Copier le fichier
            dest_path = dest_dir / source_path.name
            
            import shutil
            shutil.copy2(source_path, dest_path)
            
            logging.info(f"✅ Police installée: {source_path.name} → {category}/")
            
            # Recharger les polices
            self.refresh_fonts()
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur installation police: {e}")
            return False
    
    def get_font_info(self) -> Dict:
        """
        Retourne des informations sur les polices chargées.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        return {
            "system_fonts_count": len(self.system_fonts),
            "custom_fonts_count": len(self.custom_fonts),
            "total_fonts": len(self.system_fonts) + len(self.custom_fonts),
            "custom_fonts": self.custom_fonts,
            "fonts_directory": str(self.fonts_dir.absolute())
        }

# Instance globale du gestionnaire de polices
_font_manager = None

def get_font_manager() -> FontManager:
    """Retourne l'instance globale du gestionnaire de polices."""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager

def get_available_fonts() -> List[str]:
    """Raccourci pour obtenir toutes les polices disponibles."""
    return get_font_manager().get_all_fonts()

def create_custom_font(font_name: str, size: int = 12, **kwargs) -> font.Font:
    """Raccourci pour créer une police."""
    return get_font_manager().create_font(font_name, size, **kwargs)

if __name__ == "__main__":
    # Test du gestionnaire de polices
    print("🎨 TEST DU GESTIONNAIRE DE POLICES")
    print("=" * 40)
    
    fm = FontManager()
    info = fm.get_font_info()
    
    print(f"📊 Polices système: {info['system_fonts_count']}")
    print(f"🎨 Polices personnalisées: {info['custom_fonts_count']}")
    print(f"📁 Dossier polices: {info['fonts_directory']}")
    
    if info['custom_fonts']:
        print("\n🎨 Polices personnalisées trouvées:")
        for font_name in info['custom_fonts']:
            print(f"  • {font_name}")
    else:
        print("\n💡 Ajoutez des fichiers .ttf ou .otf dans le dossier fonts/")
    
    print(f"\n✅ Total: {info['total_fonts']} polices disponibles")
