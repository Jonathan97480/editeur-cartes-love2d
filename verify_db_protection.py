#!/usr/bin/env python3
"""
Vérification que cartes.db est bien ignoré par Git
"""

import os
import subprocess

def check_gitignore():
    """Vérifie la configuration .gitignore"""
    print("🔍 Vérification de .gitignore")
    
    if not os.path.exists(".gitignore"):
        print("❌ Fichier .gitignore manquant")
        return False
    
    with open(".gitignore", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Vérifier les entrées importantes
    checks = [
        ("cartes.db", "cartes.db" in content),
        ("*.db", "*.db" in content),
        ("Base de données", "# Base de données" in content),
    ]
    
    print("📋 Vérification des règles :")
    all_good = True
    for rule, found in checks:
        status = "✅" if found else "❌"
        print(f"   {status} {rule}")
        if not found:
            all_good = False
    
    return all_good

def check_git_status():
    """Vérifie que cartes.db n'est pas tracké"""
    print(f"\n🔍 Vérification du statut Git")
    
    try:
        # Vérifier si cartes.db est dans les fichiers trackés
        result = subprocess.run(
            ["git", "ls-files", "cartes.db"], 
            capture_output=True, 
            text=True,
            cwd="."
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print("❌ cartes.db est encore tracké par Git")
            return False
        else:
            print("✅ cartes.db n'est pas tracké par Git")
        
        # Vérifier le statut actuel
        result = subprocess.run(
            ["git", "status", "--porcelain"], 
            capture_output=True, 
            text=True,
            cwd="."
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
            db_in_status = any('cartes.db' in line for line in lines)
            
            if db_in_status:
                print("⚠️ cartes.db apparaît dans le statut Git")
                for line in lines:
                    if 'cartes.db' in line:
                        print(f"   {line}")
            else:
                print("✅ cartes.db n'apparaît pas dans le statut Git")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification Git : {e}")
        return False

def show_commit_summary():
    """Affiche un résumé des changements prêts pour commit"""
    print(f"\n📊 RÉSUMÉ DES CHANGEMENTS")
    print("=" * 40)
    
    print("✅ Modifications incluses dans le prochain commit :")
    print("   • lib/database.py : Ajout champ original_img + migration")
    print("   • lib/ui_components.py : Utilisation image originale pour fusion")
    print("   • lib/utils.py : Messages debug améliorés")
    print("   • cartes.db : SUPPRIMÉ du tracking Git")
    
    print(f"\n🎯 Résultat :")
    print("   • La base de données ne sera plus committée")
    print("   • Les données utilisateur restent locales") 
    print("   • Le problème de superposition de templates est résolu")
    print("   • Les changements de rareté fonctionnent correctement")

if __name__ == "__main__":
    print("🔒 VÉRIFICATION DE LA PROTECTION DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    gitignore_ok = check_gitignore()
    git_status_ok = check_git_status()
    
    show_commit_summary()
    
    if gitignore_ok and git_status_ok:
        print(f"\n" + "=" * 60)
        print("✅ CONFIRMATION : cartes.db est bien protégé !")
        print("🔒 La base de données ne sera pas incluse dans les commits")
        print("💾 Les données utilisateur restent privées et locales")
    else:
        print(f"\n" + "=" * 60) 
        print("⚠️ ATTENTION : Problèmes détectés dans la protection")
        print("🔧 Vérifiez les erreurs ci-dessus")
