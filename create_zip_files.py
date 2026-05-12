#!/usr/bin/env python3
"""
Create zip archives of split files for easy download
"""
import zipfile
import shutil
from pathlib import Path

def create_zips():
    split_dir = Path('split_files')
    
    if not split_dir.exists() or not any(split_dir.iterdir()):
        print("No split files to zip")
        return
    
    print("=" * 60)
    print("CREATING ZIP ARCHIVES")
    print("=" * 60)
    
    for folder in split_dir.iterdir():
        if not folder.is_dir():
            continue
            
        print(f"\nProcessing: {folder.name}")
        
        zip_path = split_dir / f"{folder.name}.zip"
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in sorted(folder.iterdir()):
                    if file.is_file():
                        zipf.write(file, file.name)
                        size_mb = file.stat().st_size / (1024 * 1024)
                        print(f"  Added: {file.name} ({size_mb:.1f} MB)")
                
                readme_content = "FILE REASSEMBLY INSTRUCTIONS\n"
                readme_content += "=" * 40 + "\n\n"
                readme_content += f"This archive contains '{folder.name}' split into 90MB parts.\n\n"
                readme_content += "HOW TO REASSEMBLE:\n\n"
                readme_content += "Windows:\n"
                readme_content += "  1. Install 7-Zip from https://www.7-zip.org/\n"
                readme_content += "  2. Extract all files from this zip to a folder\n"
                readme_content += "  3. Right-click the .7z file and select '7-Zip > Extract Here'\n\n"
                readme_content += "Mac:\n"
                readme_content += "  brew install p7zip\n"
                readme_content += f"  7z x {folder.name}.7z\n\n"
                readme_content += "Linux:\n"
                readme_content += "  sudo apt-get install p7zip-full\n"
                readme_content += f"  7z x {folder.name}.7z\n\n"
                readme_content += "PARTS INCLUDED:\n"
                readme_content += "-" * 20 + "\n"
                
                for file in sorted(folder.iterdir()):
                    if file.is_file():
                        readme_content += f"  - {file.name}\n"
                
                zipf.writestr("README.txt", readme_content)
            
            zip_size = zip_path.stat().st_size / (1024 * 1024)
            print(f"Created: {zip_path.name} ({zip_size:.2f} MB)")
            
            shutil.rmtree(folder)
            print(f"Cleaned up: {folder.name}/")
            
        except Exception as e:
            print(f"Error creating zip: {str(e)}")
    
    print("\nZip creation complete!")

if __name__ == "__main__":
    create_zips()
