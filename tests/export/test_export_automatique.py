#!/usr/bin/env python3
"""
Système automatique de test et diagnostic d'export Lua
- Lance l'application automatiquement
- Surveille l'export
- Analyse le fichier
- Diagnostique les problèmes dans le code
"""

import subprocess
import time
import os
import psutil
import shutil
from datetime import datetime

class ExportAnalyzer:
    def __init__(self):
        self.result_dir = "result_export_lua"
        self.app_process = None
        
    def start_application(self):
        """Lance l'application automatiquement"""
        print("🚀 LANCEMENT AUTOMATIQUE DE L'APPLICATION")
        print("=" * 50)
        
        try:
            # Utiliser START.bat qui gère l'environnement
            self.app_process = subprocess.Popen(
                ["START.bat"],
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd="."
            )
            
            print("✅ Application lancée via START.bat")
            print("👤 L'application va s'ouvrir...")
            print("🎯 Choisissez l'option 1 (Export) dans l'application")
            print("📁 Mettez le fichier dans result_export_lua/ quand demandé")
            print()
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lancement: {e}")
            print("🔧 Essayez de lancer START.bat manuellement")
            return False
    
    def wait_for_export(self):
        """Surveille l'apparition du fichier d'export"""
        print("👁️  SURVEILLANCE DE L'EXPORT")
        print("=" * 30)
        
        export_paths = [
            os.path.join(self.result_dir, "cards_joueur.lua"),
            "cards_joueur.lua",
            "c:/Users/berou/Downloads/cards_joueur.lua"
        ]
        
        print("📁 Surveillance des emplacements:")
        for path in export_paths:
            print(f"   - {path}")
        print()
        
        last_sizes = {}
        
        while True:
            # Vérifier si l'application est toujours en cours
            if self.app_process and self.app_process.poll() is not None:
                print("⚠️  Application fermée")
                break
            
            # Vérifier les fichiers
            for path in export_paths:
                if os.path.exists(path):
                    current_size = os.path.getsize(path)
                    
                    if path not in last_sizes:
                        last_sizes[path] = current_size
                        print(f"📄 Fichier détecté: {path} ({current_size} octets)")
                        continue
                    
                    # Si le fichier a changé
                    if current_size != last_sizes[path]:
                        print(f"🔄 Export mis à jour: {path}")
                        last_sizes[path] = current_size
                        
                        # Attendre que l'écriture se termine
                        time.sleep(1)
                        
                        # Analyser immédiatement
                        if self.analyze_export_file(path):
                            return True
            
            time.sleep(1)
        
        # Si on arrive ici, chercher le dernier fichier créé
        print("🔍 Recherche du fichier d'export...")
        return self.find_and_analyze_export()
    
    def find_and_analyze_export(self):
        """Trouve et analyse le fichier d'export le plus récent"""
        possible_files = [
            "cards_joueur.lua",
            "c:/Users/berou/Downloads/cards_joueur.lua",
            os.path.join(self.result_dir, "cards_joueur.lua")
        ]
        
        latest_file = None
        latest_time = 0
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                mod_time = os.path.getmtime(file_path)
                if mod_time > latest_time:
                    latest_time = mod_time
                    latest_file = file_path
        
        if latest_file:
            print(f"📄 Fichier trouvé: {latest_file}")
            return self.analyze_export_file(latest_file)
        else:
            print("❌ Aucun fichier d'export trouvé")
            return False
    
    def analyze_export_file(self, file_path):
        """Analyse le fichier d'export"""
        print()
        print("🔍 ANALYSE DU FICHIER D'EXPORT")
        print("=" * 40)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Erreur lecture: {e}")
            return False
        
        # Statistiques de base
        file_size = len(content)
        card_count = content.count('--[[ CARTE')
        mod_time = os.path.getmtime(file_path)
        
        print(f"📊 Informations du fichier:")
        print(f"   📄 Taille: {file_size:,} caractères")
        print(f"   📦 Cartes: {card_count}")
        print(f"   📅 Modifié: {datetime.fromtimestamp(mod_time).strftime('%H:%M:%S')}")
        
        # Vérifications critiques
        has_textformatting = 'TextFormatting' in content
        has_dimensions = 'width = 280' in content
        has_positioning = 'title = {' in content
        formatting_count = content.count('TextFormatting = {')
        
        print()
        print("🔍 Vérifications:")
        print(f"   🎨 Section TextFormatting: {'✅' if has_textformatting else '❌'}")
        print(f"   📐 Dimensions carte: {'✅' if has_dimensions else '❌'}")
        print(f"   📍 Positionnement: {'✅' if has_positioning else '❌'}")
        print(f"   📊 Sections formatage: {formatting_count}")
        
        # Copier dans result_export_lua
        result_file = os.path.join(self.result_dir, "cards_joueur_exported.lua")
        try:
            if not os.path.exists(self.result_dir):
                os.makedirs(self.result_dir)
            shutil.copy2(file_path, result_file)
            print(f"📋 Copié vers: {result_file}")
        except Exception as e:
            print(f"⚠️  Erreur copie: {e}")
        
        # Diagnostic
        if has_textformatting and has_dimensions:
            print()
            print("🎉 EXPORT CORRECT!")
            print("   Toutes les données de formatage sont présentes")
            return True
        else:
            print()
            print("❌ EXPORT INCOMPLET!")
            print("   Les données de formatage manquent")
            
            # Analyser le code de l'application
            self.diagnose_application_code()
            
            # Créer version corrigée
            self.create_corrected_version(content)
            return False
    
    def diagnose_application_code(self):
        """Analyse le code de l'application pour comprendre le problème"""
        print()
        print("🔧 DIAGNOSTIC DU CODE D'APPLICATION")
        print("=" * 45)
        
        # Chercher les fichiers d'export dans l'application
        export_files = []
        
        # Patterns à chercher
        search_patterns = [
            "lua_export",
            "LuaExporter", 
            "export_lua",
            "export.*lua",
            "cards_joueur"
        ]
        
        print("🔍 Recherche des fichiers d'export...")
        
        # Chercher dans lib/
        lib_dir = "lib"
        if os.path.exists(lib_dir):
            for filename in os.listdir(lib_dir):
                if filename.endswith('.py'):
                    file_path = os.path.join(lib_dir, filename)
                    if any(pattern.lower() in filename.lower() for pattern in search_patterns):
                        export_files.append(file_path)
                        print(f"   📄 Trouvé: {file_path}")
        
        # Chercher dans le répertoire principal
        for filename in os.listdir('.'):
            if filename.endswith('.py'):
                if any(pattern.lower() in filename.lower() for pattern in search_patterns):
                    export_files.append(filename)
                    print(f"   📄 Trouvé: {filename}")
        
        # Analyser les fichiers trouvés
        if export_files:
            print()
            print("🔍 Analyse des fichiers d'export:")
            for file_path in export_files:
                self.analyze_export_code(file_path)
        else:
            print("❌ Aucun fichier d'export trouvé dans le code")
            
        # Chercher dans main.py
        self.analyze_main_code()
    
    def analyze_export_code(self, file_path):
        """Analyse un fichier de code d'export"""
        print(f"\n📄 Analyse de {file_path}:")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Chercher les patterns importants
            has_textformatting = 'TextFormatting' in code or 'text_formatting' in code
            has_dimensions = 'width' in code and 'height' in code
            has_love2d = 'love2d' in code.lower() or 'Love2D' in code
            has_export_function = 'def export' in code or 'class' in code and 'Export' in code
            
            print(f"   🎨 TextFormatting: {'✅' if has_textformatting else '❌'}")
            print(f"   📐 Dimensions: {'✅' if has_dimensions else '❌'}")
            print(f"   🎮 Love2D: {'✅' if has_love2d else '❌'}")
            print(f"   📤 Fonction export: {'✅' if has_export_function else '❌'}")
            
            # Extraire des exemples de code
            if 'def export' in code:
                start = code.find('def export')
                end = code.find('\n\n', start)
                if end == -1:
                    end = start + 200
                export_snippet = code[start:end]
                print(f"   📝 Fonction trouvée: {export_snippet[:100]}...")
            
            if not has_textformatting:
                print(f"   ⚠️  PROBLÈME: {file_path} ne génère pas TextFormatting")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")
    
    def analyze_main_code(self):
        """Analyse le fichier main.py"""
        print(f"\n📄 Analyse de main.py:")
        
        if not os.path.exists('main.py'):
            print("   ❌ main.py non trouvé")
            return
        
        try:
            with open('main.py', 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Chercher les imports d'export
            import_lines = [line for line in code.split('\n') if 'import' in line and any(term in line.lower() for term in ['export', 'lua'])]
            
            if import_lines:
                print("   📦 Imports d'export trouvés:")
                for line in import_lines:
                    print(f"      {line.strip()}")
            else:
                print("   ❌ Aucun import d'export trouvé")
            
            # Chercher les appels d'export
            if 'export' in code.lower():
                print("   📤 Code d'export détecté dans main.py")
            else:
                print("   ❌ Pas de code d'export dans main.py")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")
    
    def create_corrected_version(self, original_content):
        """Crée une version corrigée avec formatage Love2D"""
        print()
        print("🔧 CRÉATION DE LA VERSION CORRIGÉE")
        print("=" * 40)
        
        # Template de formatage Love2D
        text_formatting_template = '''        TextFormatting = {
            card = {
                width = 280,  -- Largeur standard de carte Love2D
                height = 392, -- Hauteur standard de carte Love2D (ratio 5:7)
                scale = 1.0   -- Facteur d'échelle
            },
            title = {
                x = 50,           -- Position X du titre
                y = 25,           -- Position Y du titre
                font = "Arial",   -- Police du titre
                size = 16,        -- Taille du titre
                color = "black"   -- Couleur du titre
            },
            description = {
                x = 20,           -- Position X de la description
                y = 80,           -- Position Y de la description
                width = 240,      -- Largeur de la zone de description
                height = 200,     -- Hauteur de la zone de description
                font = "Arial",   -- Police de la description
                size = 12,        -- Taille de la description
                color = "black"   -- Couleur de la description
            },
            energy = {
                x = 240,          -- Position X de l'énergie/coût
                y = 25,           -- Position Y de l'énergie/coût
                font = "Arial",   -- Police de l'énergie
                size = 14,        -- Taille de l'énergie
                color = "blue"    -- Couleur de l'énergie
            }
        },'''
        
        # Traiter le contenu
        lines = original_content.split('\n')
        new_lines = []
        card_count = 0
        
        for line in lines:
            new_lines.append(line)
            
            # Détecter la fin d'une carte
            if line.strip() == "Cards = {}":
                card_count += 1
                # Retirer la ligne qu'on vient d'ajouter
                new_lines.pop()
                
                # Ajouter TextFormatting
                new_lines.append(text_formatting_template)
                
                # Rajouter Cards = {}
                new_lines.append("        Cards = {}")
        
        # Créer le contenu corrigé
        corrected_content = '\n'.join(new_lines)
        
        # Sauvegarder
        corrected_file = os.path.join(self.result_dir, "cards_joueur_CORRECTED.lua")
        with open(corrected_file, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        
        print(f"✅ Version corrigée créée: {corrected_file}")
        print(f"📊 Cartes traitées: {card_count}")
        print(f"📈 Taille: {len(original_content):,} → {len(corrected_content):,} caractères")

def main():
    """Fonction principale"""
    print("🎯 SYSTÈME AUTOMATIQUE DE TEST ET DIAGNOSTIC")
    print("=" * 60)
    
    analyzer = ExportAnalyzer()
    
    # Créer le dossier de résultats
    if not os.path.exists(analyzer.result_dir):
        os.makedirs(analyzer.result_dir)
        print(f"📁 Dossier créé: {analyzer.result_dir}")
    
    print()
    print("🚀 Étapes:")
    print("   1. Lance l'application automatiquement")
    print("   2. Vous faites l'export")
    print("   3. Analyse automatique du fichier")
    print("   4. Si problème: diagnostic du code de l'application")
    print()
    
    # Lancer l'application
    if analyzer.start_application():
        # Surveiller l'export
        analyzer.wait_for_export()
    
    print()
    print("🎉 ANALYSE TERMINÉE!")
    print(f"📁 Vérifiez les résultats dans: {analyzer.result_dir}/")

if __name__ == "__main__":
    main()
