#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration automatique des hooks Git avec système de sécurité
"""

import os
import stat
from pathlib import Path

def setup_secure_git_hooks():
    """Configure les hooks Git avec sécurité intégrée"""
    print("🔒 CONFIGURATION HOOKS GIT SÉCURISÉS")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    hooks_dir = project_root / ".git" / "hooks"
    
    if not hooks_dir.exists():
        print("❌ Dossier .git/hooks non trouvé")
        print("   Assurez-vous d'être dans un dépôt Git")
        return False
    
    # Hook pré-commit avec sécurité
    pre_commit_hook = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Hook pré-commit avec système de sécurité intégré
\"\"\"

import sys
import subprocess
import os

def get_python_executable():
    conda_python = r"C:/Users/berou/AppData/Local/NVIDIA/ChatWithRTX/env_nvd_rag/python.exe"
    if os.path.exists(conda_python):
        return conda_python
    return sys.executable

def main():
    print("🔒 Hook pré-commit avec sécurité activé")
    
    python_exe = get_python_executable()
    
    # Lancer le système de sécurité
    result = subprocess.run([
        python_exe, "pre_commit_security.py"
    ], cwd=os.path.dirname(os.path.dirname(__file__)))
    
    if result.returncode == 0:
        print("✅ Sécurité validée - Commit autorisé")
        return 0
    else:
        print("❌ Sécurité échouée - Commit bloqué")
        print("📄 Consultez les rapports dans commit_reports/")
        return 1

if __name__ == "__main__":
    sys.exit(main())
"""
    
    # Hook post-commit avec rapport
    post_commit_hook = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Hook post-commit avec génération de rapport
\"\"\"

import subprocess
import os
import sys
from datetime import datetime

def main():
    print("📊 Hook post-commit - Génération rapport")
    
    # Afficher les derniers rapports
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "commit_reports")
    if os.path.exists(reports_dir):
        print(f"📁 Rapports disponibles dans: {reports_dir}")
        
        # Trouver le dernier rapport
        import glob
        today = datetime.now().strftime("%Y%m%d")
        recent_reports = glob.glob(os.path.join(reports_dir, f"commit_report_{today}*_summary.txt"))
        
        if recent_reports:
            latest_report = max(recent_reports)
            print(f"📄 Dernier rapport: {os.path.basename(latest_report)}")
            
            # Afficher un résumé
            try:
                with open(latest_report, 'r', encoding='utf-8') as f:
                    summary = f.read()
                    print("\\n" + "="*30)
                    print(summary)
                    print("="*30)
            except Exception as e:
                print(f"⚠️ Erreur lecture rapport: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
    
    # Écrire les hooks
    hooks_created = []
    
    # Hook pré-commit
    pre_commit_path = hooks_dir / "pre-commit"
    with open(pre_commit_path, 'w', encoding='utf-8') as f:
        f.write(pre_commit_hook)
    
    # Rendre exécutable (Windows)
    try:
        st = os.stat(pre_commit_path)
        os.chmod(pre_commit_path, st.st_mode | stat.S_IEXEC)
    except:
        pass
    
    hooks_created.append("pre-commit")
    print("✅ Hook pré-commit sécurisé créé")
    
    # Hook post-commit
    post_commit_path = hooks_dir / "post-commit"
    with open(post_commit_path, 'w', encoding='utf-8') as f:
        f.write(post_commit_hook)
    
    try:
        st = os.stat(post_commit_path)
        os.chmod(post_commit_path, st.st_mode | stat.S_IEXEC)
    except:
        pass
    
    hooks_created.append("post-commit")
    print("✅ Hook post-commit avec rapport créé")
    
    print(f"\n🎯 Hooks Git sécurisés configurés:")
    for hook in hooks_created:
        print(f"   🔒 {hook}")
    
    print(f"\n📋 Fonctionnalités activées:")
    print("   🧪 Tests automatiques avant commit")
    print("   🔒 Audit de sécurité complet")
    print("   📄 Rapports détaillés générés")
    print("   🛡️ Blocage automatique si erreurs")
    
    return True

if __name__ == "__main__":
    setup_secure_git_hooks()
