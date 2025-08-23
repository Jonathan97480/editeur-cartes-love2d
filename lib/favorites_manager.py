#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire des favoris de formatage
Gère la logique métier pour les favoris de formatage de texte
"""

import sqlite3
from pathlib import Path
from datetime import datetime

# Pattern try/except pour imports relatifs/absolus
try:
    from .database import (
        save_formatting_favorite, get_formatting_favorite,
        list_formatting_favorites, delete_formatting_favorite,
        validate_formatting_data
    )
except ImportError:
    from database import (
        save_formatting_favorite, get_formatting_favorite,
        list_formatting_favorites, delete_formatting_favorite,
        validate_formatting_data
    )


class FavoritesManager:
    """Gestionnaire des favoris de formatage avec validation et gestion d'erreurs."""
    
    def __init__(self, db_path: str):
        """Initialise le gestionnaire avec le chemin de la base de données."""
        self.db_path = db_path
        self._validate_db_access()
    
    def _validate_db_access(self):
        """Vérifie que la base de données est accessible."""
        try:
            if not Path(self.db_path).exists():
                raise FileNotFoundError(f"Base de données introuvable: {self.db_path}")
            
            # Test de connexion
            con = sqlite3.connect(self.db_path)
            con.close()
            
        except Exception as e:
            print(f"❌ Erreur accès base de données: {e}")
            raise
    
    def save_favorite(self, slot_number: int, data: dict, name: str = "") -> tuple[bool, str]:
        """
        Sauvegarde un favori avec validation complète.
        
        Args:
            slot_number: Numéro du slot (1, 2 ou 3)
            data: Dictionnaire des données de formatage
            name: Nom optionnel du favori
            
        Returns:
            tuple[bool, str]: (succès, message)
        """
        try:
            # Validation du slot
            if slot_number not in [1, 2, 3]:
                return False, f"Slot invalide: {slot_number}. Doit être 1, 2 ou 3."
            
            # Validation des données
            is_valid, validation_msg = validate_formatting_data(data)
            if not is_valid:
                return False, f"Données invalides: {validation_msg}"
            
            # Nettoyage du nom
            name = str(name).strip() if name else f"Favori {slot_number}"
            if len(name) > 50:
                name = name[:50]
            
            # Sauvegarde
            success = save_formatting_favorite(self.db_path, slot_number, data, name)
            
            if success:
                return True, f"Favori '{name}' sauvegardé avec succès"
            else:
                return False, "Échec de la sauvegarde"
                
        except Exception as e:
            error_msg = f"Erreur sauvegarde favori: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def load_favorite(self, slot_number: int) -> tuple[dict | None, str]:
        """
        Charge un favori avec validation.
        
        Args:
            slot_number: Numéro du slot (1, 2 ou 3)
            
        Returns:
            tuple[dict | None, str]: (données ou None, message)
        """
        try:
            if slot_number not in [1, 2, 3]:
                return None, f"Slot invalide: {slot_number}"
            
            favorite = get_formatting_favorite(self.db_path, slot_number)
            
            if not favorite:
                return None, f"Aucun favori dans le slot {slot_number}"
            
            # Validation des données chargées
            is_valid, validation_msg = validate_formatting_data(favorite)
            if not is_valid:
                print(f"⚠️ Favori slot {slot_number} corrompu - {validation_msg}")
                return None, f"Favori corrompu: {validation_msg}"
            
            return favorite, f"Favori '{favorite['name']}' chargé avec succès"
            
        except Exception as e:
            error_msg = f"Erreur chargement favori: {e}"
            print(f"❌ {error_msg}")
            return None, error_msg
    
    def get_all_favorites_status(self) -> dict:
        """
        Récupère l'état de tous les slots.
        
        Returns:
            dict: {slot: {'status': 'empty'|'filled'|'corrupted', 'name': str}}
        """
        try:
            favorites_list = list_formatting_favorites(self.db_path)
            status = {}
            
            for slot in [1, 2, 3]:
                if slot in favorites_list:
                    # Vérifier si le favori est valide
                    favorite, _ = self.load_favorite(slot)
                    if favorite:
                        status[slot] = {
                            'status': 'filled',
                            'name': favorites_list[slot]
                        }
                    else:
                        status[slot] = {
                            'status': 'corrupted',
                            'name': favorites_list[slot]
                        }
                else:
                    status[slot] = {
                        'status': 'empty',
                        'name': f'Favori {slot}'
                    }
            
            return status
            
        except Exception as e:
            print(f"❌ Erreur récupération statut favoris: {e}")
            return {i: {'status': 'empty', 'name': f'Favori {i}'} for i in [1, 2, 3]}
    
    def delete_favorite(self, slot_number: int) -> tuple[bool, str]:
        """
        Supprime un favori.
        
        Args:
            slot_number: Numéro du slot (1, 2 ou 3)
            
        Returns:
            tuple[bool, str]: (succès, message)
        """
        try:
            if slot_number not in [1, 2, 3]:
                return False, f"Slot invalide: {slot_number}"
            
            success = delete_formatting_favorite(self.db_path, slot_number)
            
            if success:
                return True, f"Favori slot {slot_number} supprimé"
            else:
                return False, f"Aucun favori à supprimer dans slot {slot_number}"
                
        except Exception as e:
            error_msg = f"Erreur suppression favori: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def is_slot_occupied(self, slot_number: int) -> bool:
        """Vérifie si un slot contient des données."""
        try:
            status = self.get_all_favorites_status()
            return status.get(slot_number, {}).get('status') in ['filled', 'corrupted']
        except:
            return False
    
    def get_default_formatting_data(self) -> dict:
        """Retourne les données de formatage par défaut."""
        return {
            'title_x': 50, 'title_y': 30, 'title_font': 'Arial', 
            'title_size': 16, 'title_color': '#000000',
            'text_x': 50, 'text_y': 100, 'text_width': 200, 'text_height': 150,
            'text_font': 'Arial', 'text_size': 12, 'text_color': '#000000',
            'text_align': 'left', 'line_spacing': 1.2, 'text_wrap': 1,
            'energy_x': 25, 'energy_y': 25, 'energy_font': 'Arial', 
            'energy_size': 14, 'energy_color': '#FFFFFF'
        }
    
    def repair_corrupted_favorite(self, slot_number: int) -> tuple[bool, str]:
        """
        Tente de réparer un favori corrompu en le réinitialisant.
        
        Args:
            slot_number: Numéro du slot à réparer
            
        Returns:
            tuple[bool, str]: (succès, message)
        """
        try:
            # Supprimer le favori corrompu
            delete_success, _ = self.delete_favorite(slot_number)
            
            if delete_success:
                print(f"⚠️ Favori slot {slot_number} corrompu - réinitialisé")
                return True, f"Favori slot {slot_number} réinitialisé"
            else:
                return False, f"Impossible de réparer le favori slot {slot_number}"
                
        except Exception as e:
            error_msg = f"Erreur réparation favori: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg


def create_favorites_manager(db_path: str) -> FavoritesManager | None:
    """
    Factory function pour créer un gestionnaire de favoris avec gestion d'erreurs.
    
    Args:
        db_path: Chemin vers la base de données
        
    Returns:
        FavoritesManager ou None si erreur
    """
    try:
        return FavoritesManager(db_path)
    except Exception as e:
        print(f"❌ Impossible de créer le gestionnaire de favoris: {e}")
        return None
