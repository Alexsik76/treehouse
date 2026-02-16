import os

# Список папок, які ми ігноруємо (можеш додати сюди щось своє)
IGNORE_DIRS = {
    'node_modules', 'venv', '.venv', 'env', '__pycache__', 
    '.git', 'dist', '.idea', '.vscode', 'build', 'coverage'
}

def print_tree(startpath):
    print(f"\n📂 PROJECT STRUCTURE: {os.path.basename(os.path.abspath(startpath))}")
    
    for root, dirs, files in os.walk(startpath):
        # Фільтруємо папки "на льоту", щоб os.walk не заходив всередину сміття
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        print(f'{indent}├── {os.path.basename(root)}/')
        
        subindent = '│   ' * (level + 1)
        for f in files:
            # Можна додати фільтр файлів, якщо треба
            if not f.endswith(('.pyc', '.log', '.lock')): 
                print(f'{subindent}├── {f}')

if __name__ == "__main__":
    print_tree('.')