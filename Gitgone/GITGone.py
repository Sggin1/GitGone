# backup_project.py - Create timestamped backup excluding gitignore items
# Location: root/backup_project.py - Simple project backup tool
#
# 🚀 QUICK START GUIDE:
# ====================
# 1. Save this file to your project folder (same level as your code)
# 2. Open terminal/command prompt in that folder
# 3. Run: python backup_project.py (or python3 backup_project.py on some systems)
# 4. Find your backup in Desktop/_BU/ProjectName_MM-DD-YY-HHMM/
#
# 📁 WHAT IT DOES:
# - Creates timestamped backup of your entire project
# - Excludes junk files (venv, __pycache__, .git, etc.)
# - Respects .gitignore patterns automatically
# - Safe backup location: Desktop/_BU/
#
# ⚙️ REQUIREMENTS:
# - Python 3.6+ (comes with most systems)
# - No additional packages needed!
#
# 🛠️ CUSTOMIZATION:
# - Edit FORCE_EXCLUDE below to add/remove exclusion patterns
# - Backup location: Desktop/_BU (change in create_backup() if needed)
#
# 🚀 ADVANCED VERSIONS AVAILABLE:
# - CLI Version: Command-line with custom options (--dest, --exclude, etc.)
# - GUI Version: Easy point-and-click interface with drag-drop
# - Enterprise: Scheduled backups, cloud sync, compression options
# - Contact: sggin1@gmail.com for advanced features or custom versions
#
# ❓ TROUBLESHOOTING:
# - "python not found" → try "python3 backup_project.py"
# - Permission errors → run as administrator/sudo
# - Questions? Email: sggin1@gmail.com
#
# 💡 PRO TIP: Run this before making risky changes to your code!
#

# CONFIG - Edit these patterns as needed
# ===========================================
# 📂 FORCE_EXCLUDE: Always skip these files/folders (regardless of .gitignore)
FORCE_EXCLUDE = {
    # Python junk
    'venv', '.venv', '__pycache__', '*.pyc', '*.pyo', '*.pyd',
    
    # Git/Version control  
    '.git', '.svn', '.hg',
    
    # Node.js/JavaScript
    'node_modules', 'npm-debug.log',
    
    # Build/Compile outputs
    'build', 'dist', 'target', '*.exe', '*.dll',
    
    # IDE/Editor files
    '.vscode', '.idea', '*.swp', '*.swo',
    
    # OS junk
    '.DS_Store', 'Thumbs.db', 'desktop.ini'
}

import shutil
import os
from datetime import datetime
from pathlib import Path

def create_backup():
    """Backup project to Desktop/_BU with timestamp, respect .gitignore + config"""
    
    # Get paths
    root = Path.cwd()
    project_name = root.name
    timestamp = datetime.now().strftime("%m-%d-%y-%H%M")
    backup_name = f"{project_name}_{timestamp}"
    desktop = Path.home() / "Desktop"
    bu_dir = desktop / "_BU"
    backup_path = bu_dir / backup_name
    
    # Create _BU directory
    bu_dir.mkdir(exist_ok=True)
    
    # Read .gitignore patterns
    gitignore_file = root / ".gitignore"
    exclude_patterns = set(FORCE_EXCLUDE)  # Start with config
    
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    exclude_patterns.add(line.rstrip('/'))
    
    # Copy with exclusions
    def should_exclude(path):
        rel_path = path.relative_to(root)
        for pattern in exclude_patterns:
            if pattern in str(rel_path) or rel_path.name == pattern:
                return True
        return False
    
    backup_path.mkdir()
    for item in root.iterdir():
        if item.name != backup_path.name and not should_exclude(item):
            dest = backup_path / item.name
            if item.is_dir():
                shutil.copytree(item, dest, ignore=lambda d, files: [f for f in files if should_exclude(Path(d)/f)])
            else:
                shutil.copy2(item, dest)
    
    print(f"Backup created: {backup_path}")
    print(f"Excluded: {sorted(exclude_patterns)}")
    return backup_path

if __name__ == "__main__":
    create_backup()
