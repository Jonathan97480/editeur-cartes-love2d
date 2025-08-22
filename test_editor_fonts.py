#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 TEST DE L'ÉDITEUR AVEC POLICES PERSONNALISÉES
==============================================

Test d'intégration de l'éditeur de formatage avec le gestionnaire de polices.
"""

import sys
import tkinter as tk
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

def test_editor_with_fonts():
    """Test de l'éditeur avec le gestionnaire de polices."""
    print("🎨 TEST DE L'ÉDITEUR AVEC GESTIONNAIRE DE POLICES")
    print("=" * 55)
    
    try:
        # Importer les modules nécessaires
        from lib.text_formatting_editor import TextFormattingEditor
        from lib.font_manager import get_font_manager
        
        # Test du gestionnaire de polices
        fm = get_font_manager()
        info = fm.get_font_info()
        
        print(f"📊 Polices disponibles: {info['total_fonts']}")
        print(f"🎨 Polices personnalisées: {info['custom_fonts_count']}")
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.title("Test Éditeur de Formatage")
        root.geometry("1200x800")
        
        # Données de carte d'exemple
        card_data = {
            'nom': 'Carte de Test',
            'description': 'Description avec formatage personnalisé pour tester les nouvelles polices.',
            'img': 'test.png',
            'powerblow': 3,
            'title_x': 50,
            'title_y': 30,
            'title_font': 'Arial',
            'title_size': 16,
            'text_x': 50,
            'text_y': 100,
            'text_width': 200,
            'text_height': 150,
            'text_font': 'Times New Roman',
            'text_size': 12
        }
        
        print(f"✅ Données de test préparées")
        
        # Créer un bouton pour lancer l'éditeur
        def open_editor():
            try:
                editor = TextFormattingEditor(root, card_id=1, card_data=card_data)
                print(f"✅ Éditeur ouvert avec succès!")
                print(f"   {len(editor.available_fonts)} polices chargées")
                
                if editor.font_manager.get_custom_fonts():
                    print(f"🎨 Polices personnalisées disponibles:")
                    for font in editor.font_manager.get_custom_fonts():
                        print(f"   • {font}")
                else:
                    print(f"💡 Aucune police personnalisée trouvée")
                    print(f"   Ajoutez des fichiers .ttf/.otf dans fonts/ pour les tester")
                    
            except Exception as e:
                print(f"❌ Erreur ouverture éditeur: {e}")
                import traceback
                traceback.print_exc()
        
        # Interface de test
        info_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        info_frame.pack(fill="x")
        
        tk.Label(info_frame, text="🎨 Test du Gestionnaire de Polices", 
                font=("Arial", 16, "bold"), bg="#f0f0f0").pack()
        
        tk.Label(info_frame, text=f"Polices système: {info['system_fonts_count']}", 
                bg="#f0f0f0").pack()
        tk.Label(info_frame, text=f"Polices personnalisées: {info['custom_fonts_count']}", 
                bg="#f0f0f0").pack()
        tk.Label(info_frame, text=f"Total: {info['total_fonts']} polices", 
                bg="#f0f0f0").pack()
        
        # Boutons
        button_frame = tk.Frame(root, pady=20)
        button_frame.pack()
        
        tk.Button(button_frame, text="🎨 Ouvrir l'Éditeur de Formatage", 
                 command=open_editor, font=("Arial", 12), 
                 padx=20, pady=10).pack(side="left", padx=10)
        
        tk.Button(button_frame, text="❌ Fermer", 
                 command=root.quit, font=("Arial", 12), 
                 padx=20, pady=10).pack(side="left", padx=10)
        
        # Instructions
        instructions = tk.Text(root, height=15, wrap="word", padx=10, pady=10)
        instructions.pack(fill="both", expand=True, padx=20, pady=20)
        
        instructions.insert("1.0", f"""🎨 INSTRUCTIONS POUR TESTER LES POLICES PERSONNALISÉES

1. 📥 AJOUTER DES POLICES :
   • Copiez des fichiers .ttf ou .otf dans le dossier fonts/
   • Organisez-les dans les sous-dossiers : fonts/titre/, fonts/texte/, fonts/special/
   • Ou utilisez : python install_fonts.py

2. 🔄 ACTUALISER :
   • Cliquez sur "Ouvrir l'Éditeur de Formatage"
   • Dans l'éditeur, utilisez le bouton "🎨 Actualiser polices"

3. ✨ UTILISATION :
   • Les polices personnalisées apparaissent avec le préfixe 🎨
   • Elles sont listées en premier dans les menus déroulants
   • Testez-les sur le titre, le texte et l'énergie

4. 🎯 POLICES RECOMMANDÉES GRATUITES :
   • Google Fonts : fonts.google.com
   • Liberation Fonts (open source)
   • Font Squirrel : fontsquirrel.com

💡 Astuce : Redémarrez l'éditeur après avoir ajouté de nouvelles polices pour les voir apparaître.

Dossier polices actuel : {info['fonts_directory']}
""")
        
        instructions.config(state="disabled")
        
        print(f"✅ Interface de test prête")
        print(f"💡 Cliquez sur 'Ouvrir l'Éditeur de Formatage' pour tester")
        
        # Lancer l'interface
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR LORS DU TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_editor_with_fonts()
    if success:
        print(f"\n🎉 Test terminé !")
    else:
        print(f"\n❌ Test échoué")
        sys.exit(1)
