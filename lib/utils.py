#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaires pour l'éditeur de cartes Love2D
"""
import os
import re
import sys
from tkinter import messagebox
from .config import APP_SETTINGS, IMAGES_FOLDER, APP_TITLE

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

# ======================= Utilitaires généraux =======================

def default_db_path() -> str:
    """Chemin par défaut de la BDD.
    - Exécutable (PyInstaller, sys.frozen) : %APPDATA%/EditeurCartesLove2D/cartes.db
    - Script : ./cartes.db
    """
    if getattr(sys, 'frozen', False):
        base = os.environ.get('APPDATA') or os.path.expanduser('~')
        folder = os.path.join(base, 'EditeurCartesLove2D')
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception:
            folder = os.path.expanduser('~')
        return os.path.join(folder, 'cartes.db')
    return "cartes.db"

def to_int(x) -> int:
    """Convertit une valeur en entier, retourne 0 si impossible."""
    try:
        return int(x)
    except Exception:
        return 0

def lua_escape(s: str) -> str:
    """Échapper une chaîne pour Lua (quotes simples + newlines)."""
    if s is None:
        return ''
    return (
        s.replace("\\", "\\\\")
         .replace("'", "\\'")
         .replace("\r\n", "\n")
         .replace("\r", "\n")
         .replace("\n", "\\n")
    )

# ======================= Gestion des images =======================

def sanitize_filename(name: str) -> str:
    """Nettoie un nom de fichier en remplaçant les caractères interdits par des underscores."""
    # Remplace les espaces et caractères spéciaux par des underscores
    cleaned = re.sub(r'[^\w\-_.]', '_', name)
    # Évite les underscores multiples
    cleaned = re.sub(r'_{2,}', '_', cleaned)
    return cleaned.strip('_')

def ensure_images_folder() -> str:
    """Crée le dossier images s'il n'existe pas et retourne son chemin."""
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', IMAGES_FOLDER)
    folder_path = os.path.normpath(folder_path)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def ensure_images_subfolders() -> dict:
    """Crée la structure de sous-dossiers pour les images et retourne les chemins."""
    base_folder = ensure_images_folder()
    
    subfolders = {
        'originals': os.path.join(base_folder, 'originals'),
        'cards': os.path.join(base_folder, 'cards'), 
        'templates': os.path.join(base_folder, 'templates')
    }
    
    # Créer tous les sous-dossiers
    for folder_path in subfolders.values():
        os.makedirs(folder_path, exist_ok=True)
    
    return subfolders

def copy_image_to_originals(source_path: str, card_name: str) -> str | None:
    """
    Copie une image source vers le dossier originals avec un nom basé sur la carte.
    Retourne le chemin de l'image copiée ou None en cas d'erreur.
    """
    if not os.path.exists(source_path):
        return None
        
    try:
        subfolders = ensure_images_subfolders()
        
        # Obtenir l'extension du fichier source
        _, ext = os.path.splitext(source_path)
        if not ext:
            ext = '.png'  # Extension par défaut
            
        # Générer le nom de fichier cible
        safe_name = sanitize_filename(card_name)
        target_filename = f"{safe_name}{ext}"
        target_path = os.path.join(subfolders['originals'], target_filename)
        
        # Copier le fichier
        import shutil
        shutil.copy2(source_path, target_path)
        
        return target_path
        
    except Exception as e:
        print(f"Erreur lors de la copie d'image : {e}")
        return None

def get_fused_card_image_path(card_name: str) -> str | None:
    """
    Retourne le chemin de l'image fusionnée d'une carte si elle existe.
    Sinon retourne None.
    """
    try:
        subfolders = ensure_images_subfolders()
        safe_name = sanitize_filename(card_name)
        fused_image_path = os.path.join(subfolders['cards'], f"{safe_name}.png")
        
        if os.path.exists(fused_image_path):
            return fused_image_path
        
        return None
        
    except Exception:
        return None

def get_card_image_for_export(card) -> str:
    """
    Retourne le chemin de l'image à utiliser pour l'export Lua.
    Priorité : image fusionnée > image originale
    Retourne un chemin relatif adapté pour Love2D.
    """
    # Essayer d'abord l'image fusionnée
    fused_path = get_fused_card_image_path(card.name)
    if fused_path:
        # Convertir en chemin relatif depuis le dossier 'images'
        if 'images' in fused_path:
            parts = fused_path.replace('\\', '/').split('/')
            try:
                idx = parts.index('images')
                relative_path = '/'.join(parts[idx:])
                return relative_path
            except ValueError:
                pass
        return fused_path.replace('\\', '/')
    
    # Sinon utiliser l'image originale
    if card.img:
        # Convertir en chemin relatif
        if 'images' in card.img:
            parts = card.img.replace('\\', '/').split('/')
            try:
                idx = parts.index('images')
                relative_path = '/'.join(parts[idx:])
                return relative_path
            except ValueError:
                pass
        return card.img.replace('\\', '/')
    
    return ''

def copy_templates_to_folder() -> dict:
    """
    Copie les templates configurés vers le dossier templates/ et retourne les nouveaux chemins.
    Retourne un dictionnaire {rareté: nouveau_chemin} pour les templates copiés.
    """
    from .config import APP_SETTINGS, save_settings
    
    try:
        subfolders = ensure_images_subfolders()
        templates_folder = subfolders['templates']
        rarity_templates = APP_SETTINGS.get("rarity_templates", {})
        
        copied_templates = {}
        updated_settings = False
        
        for rarity, template_path in rarity_templates.items():
            if not template_path or not os.path.exists(template_path):
                continue
                
            # Vérifier si le template est déjà dans le bon dossier
            if templates_folder in template_path:
                copied_templates[rarity] = template_path
                continue
            
            # Générer le nom de fichier cible
            _, ext = os.path.splitext(template_path)
            if not ext:
                ext = '.png'
            
            target_filename = f"template_{rarity}{ext}"
            target_path = os.path.join(templates_folder, target_filename)
            
            # Copier le fichier
            import shutil
            shutil.copy2(template_path, target_path)
            
            # Mettre à jour les paramètres
            APP_SETTINGS["rarity_templates"][rarity] = target_path.replace('\\', '/')
            copied_templates[rarity] = target_path
            updated_settings = True
            
            print(f"✅ Template {rarity} copié : {target_path}")
        
        # Sauvegarder les nouveaux chemins
        if updated_settings:
            save_settings()
            print("📝 Paramètres mis à jour avec les nouveaux chemins")
        
        return copied_templates
        
    except Exception as e:
        print(f"Erreur lors de la copie des templates : {e}")
        return {}

def organize_all_images() -> dict:
    """
    Organise toutes les images : templates vers templates/, originaux vers originals/.
    Retourne un dictionnaire avec les résultats de l'organisation.
    """
    results = {
        'templates_copied': 0,
        'templates_errors': 0,
        'originals_migrated': 0,
        'originals_errors': 0,
        'templates_details': {},
        'summary': ''
    }
    
    print("🗂️ Organisation complète des images...")
    print("=" * 50)
    
    # 1. Organiser les templates
    print("📁 Organisation des templates...")
    copied_templates = copy_templates_to_folder()
    results['templates_copied'] = len(copied_templates)
    results['templates_details'] = copied_templates
    
    if copied_templates:
        print(f"✅ {len(copied_templates)} templates organisés")
        for rarity, path in copied_templates.items():
            print(f"   - {rarity}: {os.path.basename(path)}")
    else:
        print("ℹ️  Aucun template à organiser")
    
    # 2. Organiser les originaux (si nécessaire)
    print("\n📁 Vérification des images originales...")
    # Cette partie peut être étendue si nécessaire
    
    # Résumé
    print(f"\n📊 Résumé de l'organisation :")
    print(f"   Templates copiés : {results['templates_copied']}")
    
    summary = f"Organisation terminée !\n"
    summary += f"✅ Templates organisés : {results['templates_copied']}\n"
    summary += f"📁 Dossier templates : images/templates/"
    
    results['summary'] = summary
    return results

def create_card_image(card_image_path: str, template_image_path: str, card_name: str) -> str | None:
    """
    Fusionne l'image de la carte avec le template et sauvegarde le résultat.
    Retourne le chemin de l'image créée ou None en cas d'erreur.
    """
    if not PILLOW_AVAILABLE:
        messagebox.showwarning(APP_TITLE, 
            "Pillow n'est pas installé. Installez-le avec :\npip install Pillow")
        return None
    
    if not os.path.exists(card_image_path) or not os.path.exists(template_image_path):
        print(f"❌ Fichier manquant : carte={os.path.exists(card_image_path)}, template={os.path.exists(template_image_path)}")
        return None
    
    try:
        print(f"🖼️ Chargement des images...")
        print(f"   Carte : {card_image_path}")
        print(f"   Template : {template_image_path}")
        
        # Charge les images avec gestion des erreurs améliorée
        try:
            from PIL import ImageFile
            ImageFile.LOAD_TRUNCATED_IMAGES = True  # Permet de charger les images tronquées
            
            card_img = Image.open(card_image_path)
            card_img.load()  # Force le chargement complet de l'image
            print(f"   ✅ Image carte chargée : {card_img.size} ({card_img.mode})")
            
        except Exception as e:
            print(f"   ❌ Erreur image carte : {e}")
            messagebox.showerror(APP_TITLE, f"Erreur lors du chargement de l'image de la carte :\n{e}\n\nVeuillez choisir une autre image.")
            return None
        
        try:
            template_img = Image.open(template_image_path)
            template_img.load()  # Force le chargement complet du template
            print(f"   ✅ Template chargé : {template_img.size} ({template_img.mode})")
            
        except Exception as e:
            print(f"   ❌ Erreur template : {e}")
            messagebox.showerror(APP_TITLE, f"Erreur lors du chargement du template :\n{e}\n\nVérifiez le template configuré.")
            return None
        
        # Redimensionne l'image de la carte pour qu'elle s'adapte au template
        template_size = template_img.size
        print(f"🔄 Redimensionnement vers {template_size}...")
        card_img = card_img.resize(template_size, Image.Resampling.LANCZOS)
        
        # Crée l'image finale
        print(f"🎨 Fusion des images...")
        if template_img.mode == 'RGBA':
            # Le template a de la transparence, on le superpose à la carte
            final_img = Image.new('RGBA', template_size)
            final_img.paste(card_img, (0, 0))
            final_img.paste(template_img, (0, 0), template_img)
        else:
            # Le template est opaque, on le convertit en RGBA pour simuler la transparence
            final_img = card_img.copy()
            if template_img.mode != 'RGBA':
                template_img = template_img.convert('RGBA')
            final_img.paste(template_img, (0, 0), template_img)
        
        # Sauvegarde l'image dans le dossier cards
        subfolders = ensure_images_subfolders()
        filename = f"{sanitize_filename(card_name)}.png"
        output_path = os.path.join(subfolders['cards'], filename)
        
        print(f"💾 Sauvegarde vers {output_path}...")
        
        # Convertit en RGB si nécessaire pour PNG
        if final_img.mode == 'RGBA':
            # Crée un fond blanc pour remplacer la transparence
            rgb_img = Image.new('RGB', final_img.size, (255, 255, 255))
            rgb_img.paste(final_img, mask=final_img.split()[-1])  # Utilise le canal alpha comme masque
            final_img = rgb_img
        
        final_img.save(output_path, 'PNG')
        print(f"✅ Image fusionnée créée avec succès : {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la fusion : {e}")
        messagebox.showerror(APP_TITLE, f"Erreur lors de la création de l'image :\n{e}\n\nVeuillez vérifier :\n- La qualité de l'image source\n- Les permissions d'écriture\n- L'espace disque disponible")
        return None

# ======================= Scripts Windows =======================

def write_bat_scripts():
    """Crée `run.bat` et `build.bat` dans le dossier du script."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run_bat_path = os.path.join(base, 'run.bat')
    build_bat_path = os.path.join(base, 'build.bat')

    run_bat = r"""@echo off
setlocal
SET SCRIPT=%~dp0test.py
SET VENV_DIR=%~dp0venv
SET REQUIREMENTS=%~dp0requirements.txt

echo ========================================
echo   Editeur de Cartes Love2D - Launcher
echo ========================================

REM Verification de Python
where python >nul 2>nul || where py >nul 2>nul || (
  echo [ERREUR] Python introuvable. Installez-le depuis https://www.python.org/
  echo Assurez-vous d'ajouter Python au PATH lors de l'installation.
  pause
  exit /b 1
)

REM Creation de l'environnement virtuel s'il n'existe pas
if not exist "%VENV_DIR%" (
  echo Creation de l'environnement virtuel...
  python -m venv "%VENV_DIR%" 2>nul || (
    echo Tentative avec py...
    py -m venv "%VENV_DIR%" || (
      echo [ERREUR] Impossible de creer l'environnement virtuel.
      pause
      exit /b 1
    )
  )
  echo Environnement virtuel cree avec succes.
)

REM Activation de l'environnement virtuel
echo Activation de l'environnement virtuel...
call "%VENV_DIR%\Scripts\activate.bat" || (
  echo [ERREUR] Impossible d'activer l'environnement virtuel.
  pause
  exit /b 1
)

REM Mise a jour de pip
echo Mise a jour de pip...
python -m pip install --upgrade pip >nul 2>nul

REM Installation des dependances si requirements.txt existe
if exist "%REQUIREMENTS%" (
  echo Installation des dependances...
  pip install -r "%REQUIREMENTS%" || (
    echo [ERREUR] Echec de l'installation des dependances.
    pause
    exit /b 1
  )
  echo Dependances installees avec succes.
) else (
  echo Installation manuelle de Pillow...
  pip install Pillow || (
    echo [ERREUR] Echec de l'installation de Pillow.
    pause
    exit /b 1
  )
)

REM Lancement de l'application
echo Lancement de l'application...
echo.
python "%SCRIPT%" %*

REM En cas d'erreur, afficher un message et attendre
if errorlevel 1 (
  echo.
  echo [ERREUR] L'application s'est fermee de maniere inattendue.
  echo Tentative de lancement en mode compatibilite...
  echo.
  python "%~dp0test_compat.py" --compat
  if errorlevel 1 (
    echo.
    echo [ERREUR] Echec du mode compatibilite.
    echo Verifiez que tous les modules sont presents dans le dossier lib/
    pause
  )
)

REM Desactivation de l'environnement virtuel
deactivate 2>nul
"""

    build_bat = r"""@echo off
setlocal
set NAME=EditeurCartesLove2D
set SCRIPT=test.py
set ICON=icon.ico
set VENV_DIR=%~dp0venv
set REQUIREMENTS=%~dp0requirements.txt

echo ========================================
echo   Build Editeur de Cartes Love2D
echo ========================================

REM Verification de Python
where python >nul 2>nul || where py >nul 2>nul || (
  echo [ERREUR] Python introuvable. Installez-le depuis https://www.python.org/
  pause
  exit /b 1
)

REM Creation de l'environnement virtuel s'il n'existe pas
if not exist "%VENV_DIR%" (
  echo Creation de l'environnement virtuel pour le build...
  python -m venv "%VENV_DIR%" 2>nul || py -m venv "%VENV_DIR%" || (
    echo [ERREUR] Impossible de creer l'environnement virtuel.
    pause
    exit /b 1
  )
)

REM Activation de l'environnement virtuel
call "%VENV_DIR%\Scripts\activate.bat" || (
  echo [ERREUR] Impossible d'activer l'environnement virtuel.
  pause
  exit /b 1
)

REM Mise a jour de pip
python -m pip install --upgrade pip >nul 2>nul

REM Installation des dependances
if exist "%REQUIREMENTS%" (
  echo Installation des dependances...
  pip install -r "%REQUIREMENTS%"
) else (
  echo Installation manuelle de Pillow...
  pip install Pillow
)

REM Installation de PyInstaller
echo Installation de PyInstaller...
pip install --upgrade pyinstaller || (
  echo [ERREUR] Echec de l'installation de PyInstaller.
  pause
  exit /b 1
)

REM Nettoyage des builds precedents
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Configuration de l'icone
if exist "%ICON%" (
  set ICON_ARG=--icon "%ICON%"
) else (
  set ICON_ARG=
)

REM Build interface graphique
echo Build de l'executable avec interface graphique...
pyinstaller --noconfirm --windowed --name "%NAME%" %ICON_ARG% --add-data "lib;lib" "%SCRIPT%" || (
  echo [ERREUR] Echec du build GUI.
  pause
  exit /b 1
)

REM Build console
echo Build de l'executable console...
pyinstaller --noconfirm --onefile --name "%NAME%_console" --add-data "lib;lib" "%SCRIPT%" || (
  echo [ERREUR] Echec du build console.
  pause
  exit /b 1
)

echo.
echo ========================================
echo   Build termine avec succes !
echo ========================================
echo Executables disponibles dans le dossier 'dist':
echo - %NAME%.exe (interface graphique)
echo - %NAME%_console.exe (console)
echo.

REM Desactivation de l'environnement virtuel
deactivate 2>nul

pause
"""

    with open(run_bat_path, 'w', encoding='utf-8') as f:
        f.write(run_bat)
    with open(build_bat_path, 'w', encoding='utf-8') as f:
        f.write(build_bat)

    return run_bat_path, build_bat_path
