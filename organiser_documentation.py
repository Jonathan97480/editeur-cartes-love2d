#!/usr/bin/env python3
"""
Organisation des guides et rapports dans des dossiers spécialisés
"""

import os
import shutil
import glob
from datetime import datetime

def creer_dossiers_documentation():
    """Crée les dossiers pour organiser la documentation"""
    
    dossiers = {
        "docs": "Documentation principale (.md)",
        "guides": "Guides d'utilisation (.py et .md)",
        "rapports": "Rapports et analyses (.py)"
    }
    
    for dossier, description in dossiers.items():
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            print(f"📁 Créé : {dossier}/ ({description})")
        else:
            print(f"📁 Existe : {dossier}/ ({description})")
    
    return dossiers

def organiser_guides_rapports():
    """Organise tous les guides et rapports"""
    
    print("📚 ORGANISATION DES GUIDES ET RAPPORTS")
    print("=" * 45)
    print(f"📅 {datetime.now().strftime('%d %B %Y à %H:%M')}")
    print()
    
    # Créer les dossiers
    dossiers = creer_dossiers_documentation()
    print()
    
    # Définir les patterns et destinations
    patterns_fichiers = {
        # Guides Python
        "guide_*.py": "guides",
        
        # Rapports Python  
        "rapport_*.py": "rapports",
        "resume_*.py": "rapports",
        "bilan_*.py": "rapports",
        "generate_*.py": "rapports",
        "corrections_*.py": "rapports",
        "documentation_*.py": "rapports",
        "analyser_*.py": "rapports",
        "organiser_*.py": "rapports",
        "nettoyer_*.py": "rapports",
        "finaliser_*.py": "rapports",
        
        # Documentation Markdown (sauf README.md, LICENSE, CHANGELOG.md)
        "GUIDE*.md": "guides",
        "TECHNICAL*.md": "docs",
        "AMELIORATIONS*.md": "docs",
        "DIMENSIONS*.md": "docs",
        "MODES*.md": "docs",
        "SECURITE*.md": "docs",
        "GESTION*.md": "docs",
        "PROBLEME*.md": "docs",
        "DOSSIER*.md": "docs",
        "SOLUTION*.md": "docs",
        "BUILD*.md": "docs",
        "UPDATE*.md": "docs",
        "RAPPORT*.md": "rapports",
        "TOUTES*.md": "docs",
        "GIT_INFO.md": "docs"
    }
    
    # Fichiers à exclure (garder en racine)
    fichiers_racine = {
        "README.md", "LICENSE", "CHANGELOG.md", "requirements.txt"
    }
    
    fichiers_deplaces = 0
    echecs = 0
    
    print("🔄 DÉPLACEMENT DES FICHIERS :")
    print("-" * 30)
    
    for pattern, destination in patterns_fichiers.items():
        fichiers = glob.glob(pattern)
        
        if fichiers:
            print(f"\n📄 Pattern '{pattern}' → {destination}/ :")
            
            for fichier in fichiers:
                if os.path.basename(fichier) in fichiers_racine:
                    print(f"⏭️ {fichier} (gardé en racine)")
                    continue
                
                try:
                    if os.path.isfile(fichier):
                        dest_path = os.path.join(destination, os.path.basename(fichier))
                        
                        # Éviter d'écraser un fichier existant
                        if os.path.exists(dest_path):
                            base, ext = os.path.splitext(dest_path)
                            counter = 1
                            while os.path.exists(f"{base}_{counter}{ext}"):
                                counter += 1
                            dest_path = f"{base}_{counter}{ext}"
                        
                        shutil.move(fichier, dest_path)
                        print(f"✅ {fichier} → {dest_path}")
                        fichiers_deplaces += 1
                        
                except Exception as e:
                    print(f"❌ Erreur avec {fichier}: {e}")
                    echecs += 1
    
    return fichiers_deplaces, echecs

def mettre_a_jour_gitignore():
    """Met à jour .gitignore pour les nouveaux dossiers"""
    
    print()
    print("📝 MISE À JOUR DE .GITIGNORE :")
    print("-" * 30)
    
    try:
        gitignore_path = ".gitignore"
        
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
        else:
            contenu = ""
        
        # Nouvelles règles pour la documentation
        nouvelles_regles = [
            "",
            "# Dossiers de documentation générée",
            "rapports/",
            "# Note: docs/ et guides/ sont conservés dans Git pour la documentation"
        ]
        
        # Vérifier si les règles existent déjà
        regles_a_ajouter = []
        for regle in nouvelles_regles:
            if regle and regle not in contenu:
                regles_a_ajouter.append(regle)
        
        if regles_a_ajouter:
            if contenu and not contenu.endswith('\n'):
                contenu += '\n'
            contenu += '\n'.join(nouvelles_regles) + '\n'
            
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            print(f"✅ Règles ajoutées à .gitignore")
            print("   • rapports/ (exclus du Git)")
            print("   • docs/ et guides/ (inclus dans Git)")
        else:
            print("✅ .gitignore déjà à jour")
            
    except Exception as e:
        print(f"❌ Erreur .gitignore: {e}")

def analyser_resultat():
    """Analyse le résultat de l'organisation"""
    
    print()
    print("📊 ANALYSE DU RÉSULTAT :")
    print("-" * 25)
    
    # Compter les fichiers dans chaque dossier
    stats = {}
    dossiers = ["docs", "guides", "rapports"]
    
    for dossier in dossiers:
        if os.path.exists(dossier):
            fichiers = glob.glob(f"{dossier}/*")
            stats[dossier] = len(fichiers)
            print(f"📁 {dossier}/ : {len(fichiers)} fichiers")
        else:
            stats[dossier] = 0
            print(f"📁 {dossier}/ : 0 fichiers")
    
    # Vérifier les fichiers restants en racine
    md_racine = [f for f in glob.glob("*.md") if f not in ["README.md", "CHANGELOG.md"]]
    py_guides_racine = glob.glob("guide_*.py") + glob.glob("rapport_*.py")
    
    print()
    print("🏠 FICHIERS RESTANTS EN RACINE :")
    print("-" * 35)
    print(f"📄 .md (hors README/CHANGELOG) : {len(md_racine)}")
    print(f"📄 guides/rapports .py : {len(py_guides_racine)}")
    
    if md_racine:
        print("   📋 Fichiers .md restants :")
        for f in md_racine[:5]:
            print(f"      • {f}")
        if len(md_racine) > 5:
            print(f"      • ... et {len(md_racine) - 5} autres")
    
    if py_guides_racine:
        print("   📋 Scripts restants :")
        for f in py_guides_racine[:5]:
            print(f"      • {f}")
        if len(py_guides_racine) > 5:
            print(f"      • ... et {len(py_guides_racine) - 5} autres")
    
    return stats

def main():
    """Fonction principale"""
    
    # Organiser les fichiers
    fichiers_deplaces, echecs = organiser_guides_rapports()
    
    # Mettre à jour .gitignore
    mettre_a_jour_gitignore()
    
    # Analyser le résultat
    stats = analyser_resultat()
    
    print()
    print("🎯 RÉSUMÉ FINAL :")
    print("-" * 20)
    print(f"✅ Fichiers déplacés : {fichiers_deplaces}")
    print(f"❌ Échecs : {echecs}")
    print(f"📁 docs/ : {stats.get('docs', 0)} fichiers")
    print(f"📁 guides/ : {stats.get('guides', 0)} fichiers") 
    print(f"📁 rapports/ : {stats.get('rapports', 0)} fichiers")
    
    print()
    print("📁 NOUVELLE STRUCTURE DOCUMENTAIRE :")
    print("-" * 40)
    print("📁 docs/               ← Documentation technique (.md)")
    print("📁 guides/             ← Guides d'utilisation")
    print("📁 rapports/           ← Rapports et analyses")
    print("📁 tests/              ← Tests organisés")
    print("📁 dbBackup/           ← Backups BD")
    print("📁 luaBackup/          ← Backups Lua")
    print("📁 imagesBackup/       ← Backups images")
    print("📄 README.md           ← Documentation principale")
    print("📄 test.py             ← Application")
    
    print()
    print("🚀 AVANTAGES :")
    print("-" * 15)
    print("• 📚 Documentation organisée par type")
    print("• 🔍 Navigation facilitée")
    print("• 🧹 Racine du projet plus propre")
    print("• 📈 Maintenance simplifiée")
    print("• 🗂️ Structure professionnelle")

if __name__ == "__main__":
    main()
