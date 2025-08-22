#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide du bouton de formatage
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

print("🧪 Test intégration du bouton de formatage")
print("=" * 50)

try:
    print("📋 Import de l'application...")
    from app_simple import CardEditor
    import tkinter as tk
    
    print("✅ Création de l'interface...")
    root = tk.Tk()
    root.title("Test - Éditeur de Cartes")
    
    # Créer l'éditeur
    app = CardEditor(root)
    
    print("✅ Application créée avec succès")
    print("🎯 Vous pouvez maintenant tester le bouton '📝 Formatage'")
    print("💡 Si une carte est sélectionnée, le bouton devrait ouvrir l'éditeur de formatage")
    
    # Lancer l'interface
    root.mainloop()
    
except Exception as e:
    print(f"❌ Erreur : {e}")
    import traceback
    traceback.print_exc()
