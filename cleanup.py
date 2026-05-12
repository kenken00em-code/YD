#!/usr/bin/env python3
"""
Cleanup download directories
"""
import shutil
from pathlib import Path

def cleanup_downloads():
    print("=" * 60)
    print("CLEANING UP DOWNLOADS")
    print("=" * 60)
    
    dirs_to_clean = ['downloads', 'split_files']
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            (dir_path / '.gitkeep').touch()
            print(f"Created {dir_name}/")
            continue
        
        files = list(dir_path.rglob('*'))
        file_count = len([f for f in files if f.is_file() and f.name != '.gitkeep'])
        
        if file_count > 0:
            for item in dir_path.iterdir():
                if item.name != '.gitkeep':
                    if item.is_file():
                        item.unlink()
                        print(f"Deleted: {item.name}")
                    elif item.is_dir():
                        shutil.rmtree(item)
                        print(f"Deleted: {item.name}/")
            
            print(f"Cleaned {dir_name}/ ({file_count} files removed)")
        else:
            print(f"{dir_name}/ is already empty")
        
        (dir_path / '.gitkeep').touch()
    
    print("\nCleanup complete!")
    print("=" * 60)

if __name__ == "__main__":
    cleanup_downloads()
