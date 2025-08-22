#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 INSTALLATEUR DE POLICES
=========================

Script pour installer facilement des polices dans l'éditeur de cartes.
"""

import os
import sys
import shutil
from pathlib import Path
from tkinter import messagebox, filedialog
import tkinter as tk

def install_font_file():
    """Interface graphique pour installer une police."""
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    
    try:
        # Sélectionner le fichier de police
        font_file = filedialog.askopenfilename(
            title="Sélectionner une police à installer",
            filetypes=[
                ("Polices", "*.ttf *.otf *.TTF *.OTF"),
                ("TrueType Font", "*.ttf *.TTF"),
                ("OpenType Font", "*.otf *.OTF"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if not font_file:
            print("❌ Aucun fichier sélectionné")
            return False
        
        # Sélectionner la catégorie
        category = select_category()
        if not category:
            print("❌ Aucune catégorie sélectionnée")
            return False
        
        # Installer la police
        success = install_font(font_file, category)
        
        if success:
            messagebox.showinfo(
                "✅ Installation réussie",
                f"Police installée avec succès !\n\n"
                f"📁 Catégorie: {category}\n"
                f"📄 Fichier: {Path(font_file).name}\n\n"
                f"💡 Redémarrez l'application pour utiliser la nouvelle police."
            )
            return True
        else:
            messagebox.showerror("❌ Erreur", "Impossible d'installer la police")
            return False
            
    except Exception as e:
        messagebox.showerror("❌ Erreur", f"Erreur lors de l'installation:\n{e}")
        return False
    finally:
        root.destroy()

def select_category():
    """Interface pour sélectionner la catégorie de police."""
    category_window = tk.Toplevel()
    category_window.title("Catégorie de police")
    category_window.geometry("300x200")
    category_window.resizable(False, False)
    
    # Centrer la fenêtre
    category_window.transient()
    category_window.grab_set()
    
    selected_category = tk.StringVar()
    
    # Instructions
    tk.Label(category_window, text="🎨 Choisissez la catégorie:", 
             font=("Arial", 12, "bold")).pack(pady=10)
    
    # Options de catégorie
    categories = [
        ("titre", "📝 Titre - Polices pour les noms de cartes"),
        ("texte", "📖 Texte - Polices pour les descriptions"),
        ("special", "✨ Spécial - Polices décoratives")
    ]
    
    for value, description in categories:
        tk.Radiobutton(
            category_window,
            text=description,
            variable=selected_category,
            value=value,
            anchor="w",
            justify="left"
        ).pack(anchor="w", padx=20, pady=5)
    
    # Boutons
    button_frame = tk.Frame(category_window)
    button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
    
    result = {"category": None}
    
    def ok_clicked():
        result["category"] = selected_category.get()
        category_window.destroy()
    
    def cancel_clicked():
        category_window.destroy()
    
    tk.Button(button_frame, text="✅ OK", command=ok_clicked).pack(side="right", padx=(5, 0))
    tk.Button(button_frame, text="❌ Annuler", command=cancel_clicked).pack(side="right")
    
    # Sélectionner "texte" par défaut
    selected_category.set("texte")
    
    # Attendre la fermeture de la fenêtre
    category_window.wait_window()
    
    return result["category"]

def install_font(font_file_path, category):
    """Installe une police dans la catégorie spécifiée."""
    try:
        source_path = Path(font_file_path)
        
        # Vérifier le fichier source
        if not source_path.exists():
            print(f"❌ Fichier inexistant: {font_file_path}")
            return False
        
        if source_path.suffix.lower() not in ['.ttf', '.otf']:
            print(f"❌ Format non supporté: {source_path.suffix}")
            return False
        
        # Créer le dossier de destination
        fonts_dir = Path("fonts") / category
        fonts_dir.mkdir(parents=True, exist_ok=True)
        
        # Chemin de destination
        dest_path = fonts_dir / source_path.name
        
        # Copier le fichier
        shutil.copy2(source_path, dest_path)
        
        print(f"✅ Police installée: {source_path.name} → fonts/{category}/")
        return True
        
    except Exception as e:
        print(f"❌ Erreur installation: {e}")
        return False

def download_sample_fonts():
    """Télécharge quelques polices d'exemple (si possible)."""
    print("🌐 TÉLÉCHARGEMENT DE POLICES D'EXEMPLE")
    print("=" * 40)
    
    # Note: En production, on pourrait ajouter des téléchargements automatiques
    # de polices open source depuis GitHub ou Google Fonts
    
    print("💡 Pour ajouter des polices, vous pouvez:")
    print("   1. Télécharger des polices depuis Google Fonts (fonts.google.com)")
    print("   2. Utiliser des polices open source (Liberation Fonts, etc.)")
    print("   3. Copier des polices depuis votre système")
    print()
    print("📁 Polices recommandées:")
    print("   • Liberation Sans/Serif (open source)")
    print("   • Open Sans (Google Fonts)")
    print("   • Roboto (Google Fonts)")
    print("   • Cinzel (Google Fonts, pour du style fantasy)")
    print("   • Nosifer (Google Fonts, pour du style horror)")

def main():
    """Fonction principale."""
    print("🎨 INSTALLATEUR DE POLICES")
    print("=" * 30)
    
    if len(sys.argv) > 1:
        # Mode ligne de commande
        font_file = sys.argv[1]
        category = sys.argv[2] if len(sys.argv) > 2 else "texte"
        
        success = install_font(font_file, category)
        if success:
            print(f"✅ Police installée avec succès!")
        else:
            print(f"❌ Échec de l'installation")
            sys.exit(1)
    else:
        # Mode interactif
        choice = input("Choisissez une option:\n"
                      "1. Installer une police depuis un fichier\n"
                      "2. Voir les polices recommandées\n"
                      "Votre choix (1-2): ")
        
        if choice == "1":
            # Vérifier si on peut lancer l'interface graphique
            try:
                success = install_font_file()
                if success:
                    print("✅ Installation terminée!")
                else:
                    print("❌ Installation annulée ou échouée")
            except Exception as e:
                print(f"❌ Impossible de lancer l'interface graphique: {e}")
                print("💡 Utilisez: python install_fonts.py chemin/vers/police.ttf [catégorie]")
        
        elif choice == "2":
            download_sample_fonts()
        
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()
