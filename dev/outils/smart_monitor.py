#!/usr/bin/env python3
"""
Surveillant intelligent d'export Lua
- Surveille les fichiers en temps réel
- Analyse automatiquement les exports
- Diagnostique les problèmes de code
"""

import os
import time
from datetime import datetime
import shutil

class IntelligentMonitor:
    def __init__(self):
        self.result_dir = "result_export_lua"
        self.monitored_files = [
            "cards_joueur.lua",
            "c:/Users/berou/Downloads/cards_joueur.lua",
            os.path.join(self.result_dir, "cards_joueur.lua")
        ]
        
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
    
    def start_monitoring(self):
        """Démarre la surveillance"""
        print("👁️  SURVEILLANCE INTELLIGENTE D'EXPORT LUA")
        print("=" * 50)
        print()
        print("📁 Fichiers surveillés:")
        for path in self.monitored_files:
            print(f"   - {path}")
        print()
        print("🎯 INSTRUCTIONS:")
        print("   1. Lancez votre application (START.bat)")
        print("   2. Choisissez l'option 1 (Export)")
        print("   3. Exportez vos cartes")
        print("   4. L'analyse se fera automatiquement")
        print()
        print("👁️  Surveillance active... (Ctrl+C pour arrêter)")
        print()
        
        last_mod_times = {}
        
        try:
            while True:
                for file_path in self.monitored_files:
                    if os.path.exists(file_path):
                        current_mod_time = os.path.getmtime(file_path)
                        
                        if file_path not in last_mod_times:
                            last_mod_times[file_path] = current_mod_time
                            continue
                        
                        if current_mod_time > last_mod_times[file_path]:
                            print(f"🔄 EXPORT DÉTECTÉ: {file_path}")
                            print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
                            
                            # Attendre que l'écriture se termine
                            time.sleep(1)
                            
                            # Analyser
                            self.analyze_and_diagnose(file_path)
                            
                            last_mod_times[file_path] = current_mod_time
                            print()
                            print("👁️  Surveillance continue...")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print()
            print("⏹️  Surveillance arrêtée")
    
    def analyze_and_diagnose(self, file_path):
        """Analyse le fichier et diagnostique si nécessaire"""
        print()
        print("🔍 ANALYSE AUTOMATIQUE")
        print("=" * 30)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Erreur lecture: {e}")
            return
        
        # Statistiques
        file_size = len(content)
        card_count = content.count('--[[ CARTE')
        
        print(f"📊 Fichier: {file_size:,} caractères, {card_count} cartes")
        
        # Vérifications
        has_textformatting = 'TextFormatting' in content
        has_dimensions = 'width = 280' in content
        has_positioning = 'title = {' in content
        
        print(f"🎨 TextFormatting: {'✅' if has_textformatting else '❌'}")
        print(f"📐 Dimensions: {'✅' if has_dimensions else '❌'}")
        print(f"📍 Positionnement: {'✅' if has_positioning else '❌'}")
        
        # Copier dans result
        backup_file = os.path.join(self.result_dir, f"export_{datetime.now().strftime('%H%M%S')}.lua")
        try:
            shutil.copy2(file_path, backup_file)
            print(f"💾 Sauvegardé: {backup_file}")
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde: {e}")
        
        # Diagnostic si problème
        if not has_textformatting or not has_dimensions:
            print()
            print("❌ PROBLÈME DÉTECTÉ - DIAGNOSTIC DU CODE...")
            self.diagnose_application_code()
            self.create_corrected_version(content, backup_file)
        else:
            print()
            print("🎉 EXPORT PARFAIT!")
    
    def diagnose_application_code(self):
        """Diagnostic du code d'application"""
        print()
        print("🔧 DIAGNOSTIC DU CODE D'APPLICATION")
        print("=" * 40)
        
        # Chercher les fichiers d'export
        export_files = self.find_export_files()
        
        if export_files:
            print("📄 Fichiers d'export trouvés:")
            for file_path in export_files:
                print(f"   - {file_path}")
                self.analyze_export_code(file_path)
        else:
            print("❌ Aucun fichier d'export trouvé")
        
        # Analyser main.py
        self.check_main_integration()
    
    def find_export_files(self):
        """Trouve les fichiers d'export dans le code"""
        export_files = []
        search_terms = ['export', 'lua', 'Lua', 'Export']
        
        # Chercher dans lib/
        if os.path.exists('lib'):
            for filename in os.listdir('lib'):
                if filename.endswith('.py'):
                    if any(term in filename for term in search_terms):
                        export_files.append(os.path.join('lib', filename))
        
        # Chercher dans le répertoire principal
        for filename in os.listdir('.'):
            if filename.endswith('.py'):
                if any(term in filename for term in search_terms):
                    export_files.append(filename)
        
        return export_files
    
    def analyze_export_code(self, file_path):
        """Analyse un fichier de code d'export"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            print(f"\n🔍 Analyse de {file_path}:")
            
            # Vérifications
            has_textformatting = 'TextFormatting' in code
            has_dimensions = 'width' in code and 'height' in code
            has_love2d = 'love2d' in code.lower()
            has_export_func = 'def export' in code
            
            print(f"   TextFormatting: {'✅' if has_textformatting else '❌'}")
            print(f"   Dimensions: {'✅' if has_dimensions else '❌'}")  
            print(f"   Love2D: {'✅' if has_love2d else '❌'}")
            print(f"   Fonction export: {'✅' if has_export_func else '❌'}")
            
            # Problème identifié
            if not has_textformatting:
                print(f"   🐛 PROBLÈME: Ce fichier ne génère pas TextFormatting")
                print(f"      Solution: Ajouter les données de formatage Love2D")
            
            # Montrer un exemple de fonction
            if 'def export' in code:
                start = code.find('def export')
                end = code.find('\n\n', start)
                if end == -1:
                    end = start + 150
                snippet = code[start:end]
                print(f"   📝 Fonction: {snippet[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    def check_main_integration(self):
        """Vérifie l'intégration dans main.py"""
        print(f"\n🔍 Vérification de main.py:")
        
        if not os.path.exists('main.py'):
            print("   ❌ main.py non trouvé")
            return
        
        try:
            with open('main.py', 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Chercher les imports
            export_imports = [line for line in code.split('\n') 
                            if 'import' in line and 'export' in line.lower()]
            
            if export_imports:
                print("   📦 Imports d'export:")
                for imp in export_imports:
                    print(f"      {imp.strip()}")
            else:
                print("   ❌ Pas d'import d'export")
            
            # Chercher l'utilisation
            if 'export' in code.lower():
                print("   ✅ Code d'export présent")
            else:
                print("   ❌ Pas de code d'export")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    def create_corrected_version(self, content, original_file):
        """Crée une version corrigée"""
        print()
        print("🔧 CRÉATION VERSION CORRIGÉE")
        print("=" * 35)
        
        # Template complet
        formatting_template = '''        TextFormatting = {
            card = {
                width = 280,
                height = 392,
                scale = 1.0
            },
            title = {
                x = 50, y = 25,
                font = "Arial", size = 16, color = "black"
            },
            description = {
                x = 20, y = 80,
                width = 240, height = 200,
                font = "Arial", size = 12, color = "black"
            },
            energy = {
                x = 240, y = 25,
                font = "Arial", size = 14, color = "blue"
            }
        },'''
        
        # Traitement
        lines = content.split('\n')
        new_lines = []
        corrections = 0
        
        for line in lines:
            new_lines.append(line)
            if line.strip() == "Cards = {}":
                new_lines.pop()  # Retirer Cards = {}
                new_lines.append(formatting_template)
                new_lines.append("        Cards = {}")
                corrections += 1
        
        # Sauvegarder
        corrected_file = original_file.replace('.lua', '_CORRECTED.lua')
        with open(corrected_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ Version corrigée: {corrected_file}")
        print(f"📊 {corrections} cartes corrigées")

def main():
    print("🎯 SURVEILLANT INTELLIGENT D'EXPORT LUA")
    print("=" * 50)
    
    monitor = IntelligentMonitor()
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
