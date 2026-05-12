#!/usr/bin/env python3
"""
Automatic file splitter - Splits files larger than 90MB into 90MB chunks
"""
import os
import subprocess
import shutil
from pathlib import Path

def split_large_files():
    SPLIT_SIZE = 90
    download_dirs = ['downloads/videos', 'downloads/audio']
    split_base = Path('split_files')
    
    print("=" * 60)
    print("AUTO-SPLIT LARGE FILES (90MB chunks)")
    print("=" * 60)
    
    total_split = 0
    
    for dir_path in download_dirs:
        dir_path = Path(dir_path)
        if not dir_path.exists():
            print(f"Directory not found: {dir_path}")
            continue
            
        for file_path in dir_path.iterdir():
            if not file_path.is_file():
                continue
                
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            
            if file_size_mb > SPLIT_SIZE:
                print(f"\nFile: {file_path.name}")
                print(f"Size: {file_size_mb:.2f} MB")
                print(f"Splitting into {SPLIT_SIZE}MB chunks...")
                
                file_split_dir = split_base / file_path.stem
                file_split_dir.mkdir(parents=True, exist_ok=True)
                
                chunk_size = f"{SPLIT_SIZE}m"
                
                try:
                    cmd = [
                        '7z', 'a',
                        '-v' + chunk_size,
                        '-mx=0',
                        f'{file_split_dir}/{file_path.stem}.7z',
                        str(file_path)
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        rename_split_parts(file_split_dir, file_path.stem)
                        
                        parts = list(file_split_dir.glob('*'))
                        total_size = sum(p.stat().st_size for p in parts) / (1024 * 1024)
                        
                        print(f"Split into {len(parts)} parts ({total_size:.2f} MB total)")
                        print(f"Location: {file_split_dir}/")
                        
                        total_split += 1
                    else:
                        print(f"Split failed: {result.stderr[:200]}")
                        
                except Exception as e:
                    print(f"Error splitting: {str(e)}")
            else:
                print(f"OK {file_path.name} ({file_size_mb:.2f} MB) - No split needed")
    
    print(f"\nSummary: {total_split} file(s) split into 90MB chunks")
    print("=" * 60)

def rename_split_parts(split_dir, base_name):
    import re
    
    pattern = re.compile(rf'{re.escape(base_name)}\.7z\.(\d+)')
    files = []
    
    for file in split_dir.iterdir():
        match = pattern.match(file.name)
        if match:
            files.append((int(match.group(1)), file))
    
    files.sort(key=lambda x: x[0])
    
    for i, (part_num, file_path) in enumerate(files):
        if i == 0:
            new_name = split_dir / f"{base_name}.7z"
        else:
            new_name = split_dir / f"{base_name}.z{str(i).zfill(2)}"
        
        file_path.rename(new_name)
        part_size = new_name.stat().st_size / (1024 * 1024)
        print(f"  Part {i+1}: {new_name.name} ({part_size:.1f} MB)")

if __name__ == "__main__":
    split_large_files()
