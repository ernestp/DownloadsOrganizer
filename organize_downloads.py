#!/usr/bin/env python3
"""
Downloads Folder Organizer
Sorts files into categorized folders while preserving original timestamps.
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime


# Configuration
DOWNLOADS_PATH = Path.home() / "Downloads"

# Category definitions with target folder names and file extensions/patterns
CATEGORIES = {
    "3D Printing": {
        "extensions": {".stl", ".3mf", ".obj", ".gcode", ".scad", ".stp", ".step", ".lys"},
        "check_zip_contents": True,  # Check if ZIP contains STL files
        "check_folder_contents": True,  # Check if folder contains STL files
    },
    "3D Models": {
        "extensions": {
            ".fbx", ".blend", ".max", ".ma", ".mb", ".c4d", ".dae", ".usd", ".usda", 
            ".usdc", ".usdz", ".glb", ".gltf", ".3ds", ".skp", ".ply", ".x3d"},
    },
    "Packages": {
        "extensions": {".dmg", ".pkg", ".app", ".iso", ".apk", ".aab"},
        "check_zip_contents": True,
        "check_folder_contents": True,
    },
    "Images": {
        "extensions": {
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff", ".tif", ".ico", ".heic", 
            ".heif", ".raw", ".cr2", ".nef", ".psd", ".ai", ".eps", ".avif"
            },
    },
    "Screenshots": {
        "filename_patterns": ["Screenshot", "Screen Shot", "Capture"],
    },
    "Screen Recordings": {
        "filename_patterns": ["Screen Recording", "ScreenRecording"],
    },
    "Video": {
        "extensions": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".mpeg", ".mpg"},
    },
    "Documents": {
        "extensions": {
            ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
            ".pdf", ".txt", ".rtf", ".odt", ".ods", ".odp",
            ".csv", ".pages", ".numbers", ".key", ".af", ".afdesign", ".afphoto"
        },
    },
    "Sources": {
        "extensions": {
            ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".hpp",
            ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala",
            ".html", ".css", ".scss", ".sass", ".less",
            ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".conf",
            ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd",
            ".sql", ".r", ".m", ".lua", ".pl", ".asm", ".aar", ".jar", ".md", ".so", ".a", ".lib", 
            ".bundle", ".patch", ".diff"
        },
        "check_zip_contents": True,
        "check_folder_contents": True,
    },
    "Music": {
        "extensions": {
            ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".aiff", ".alac", 
            ".m3u8", ".m3u", ".vital", ".vitalbank", ".aup3"
        },
    },
    "Hardware": {
        "extensions": {
            ".gbr", ".ger", ".gtl", ".gbl", ".gts", ".gbs", ".gto", ".gbo", ".gtp", ".gbp",
            ".drl", ".xln", ".nc",  # Drill files
            ".brd", ".sch", ".kicad_pcb", ".kicad_sch",  # PCB design files
        },
        "filename_patterns": ["BOM", "Pick_and_Place", "PickAndPlace", "Pick-and-Place", "PnP", "CPL", "3D_PCB"],
    },
    "Firmware": {
        "extensions": {".bin", ".img", ".hex", ".elf", ".uf2", ".dtb"},
    },
    "Archives": {
        "extensions": {".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z", ".tgz", ".tbz2", ".txz", ".tar.gz", ".tar.bz2", ".tar.xz", ".zipx", ".sit", ".sitx", ".z"},
    },
    "Unsorted": {
        "catch_all": True,
    },
}


def get_file_timestamps(path: Path) -> tuple:
    """Get creation and modification times of a file/folder."""
    stat = path.stat()
    return stat.st_birthtime, stat.st_mtime


def set_file_timestamps(path: Path, creation_time: float, modification_time: float):
    """Set creation and modification times of a file/folder."""
    os.utime(path, (modification_time, modification_time))
    # On macOS, set creation time using xattr
    try:
        import subprocess
        # Convert timestamp to macOS date format
        creation_date = datetime.fromtimestamp(creation_time)
        date_str = creation_date.strftime("%m/%d/%Y %H:%M:%S")
        subprocess.run(
            ["SetFile", "-d", date_str, str(path)],
            capture_output=True,
            check=False
        )
    except Exception:
        pass  # SetFile may not be available on all systems


def zip_contains_stl(zip_path: Path) -> bool:
    """Check if a ZIP file contains STL files."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for name in zf.namelist():
                if name.lower().endswith('.stl'):
                    return True
    except (zipfile.BadZipFile, Exception):
        pass
    return False


def folder_contains_3d_files(folder_path: Path) -> bool:
    """Check if a folder contains 3D printing files (STL, 3MF, etc.)."""
    extensions_3d = {".stl", ".3mf", ".obj", ".gcode", ".scad"}
    try:
        for item in folder_path.rglob("*"):
            if item.is_file() and item.suffix.lower() in extensions_3d:
                return True
    except Exception:
        pass
    return False


SOURCE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".hpp",
    ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala",
    ".html", ".css", ".scss", ".sass", ".less",
    ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd",
    ".sql", ".r", ".m", ".lua", ".pl", ".asm"
}


def folder_contains_source_files(folder_path: Path) -> bool:
    """Check if a folder contains source code files."""
    try:
        for item in folder_path.rglob("*"):
            if item.is_file() and item.suffix.lower() in SOURCE_EXTENSIONS:
                return True
    except Exception:
        pass
    return False


def zip_contains_source_files(zip_path: Path) -> bool:
    """Check if a ZIP file contains source code files."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for name in zf.namelist():
                ext = Path(name).suffix.lower()
                if ext in SOURCE_EXTENSIONS:
                    return True
    except (zipfile.BadZipFile, Exception):
        pass
    return False


def matches_filename_pattern(filename: str, patterns: list) -> bool:
    """Check if filename starts with any of the given patterns."""
    for pattern in patterns:
        if filename.startswith(pattern):
            return True
    return False


def categorize_item(item_path: Path) -> str | None:
    """Determine which category an item belongs to. Returns None if no match."""
    filename = item_path.name
    extension = item_path.suffix.lower()
    
    # Special handling for folders - check content-based categories
    if item_path.is_dir():
        if folder_contains_3d_files(item_path):
            return "3D Printing"
        if folder_contains_source_files(item_path):
            return "Sources"
    # Special handling for ZIP files - check contents
    elif extension == ".zip":
        if zip_contains_stl(item_path):
            return "3D Printing"
        if zip_contains_source_files(item_path):
            return "Sources"
    
    # Check each category (excluding catch_all categories)
    for category, rules in CATEGORIES.items():
        # Skip catch_all categories for now
        if rules.get("catch_all", False):
            continue
            
        # Check filename patterns first
        if "filename_patterns" in rules:
            if matches_filename_pattern(filename, rules["filename_patterns"]):
                return category
        
        # Check extensions
        if "extensions" in rules:
            if extension in rules["extensions"]:
                return category
    
    # If nothing matched, check catch_all categories
    for category, rules in CATEGORIES.items():
        if rules.get("catch_all", False):
            return category
    
    return None


def ensure_category_folder(category: str) -> Path:
    """Create category folder if it doesn't exist."""
    folder_path = DOWNLOADS_PATH / category
    folder_path.mkdir(exist_ok=True)
    return folder_path


def move_item(item_path: Path, category: str, dry_run: bool = False) -> bool:
    """Move an item to its category folder, preserving timestamps."""
    try:
        # Get original timestamps
        creation_time, modification_time = get_file_timestamps(item_path)
        
        # Determine destination
        category_folder = ensure_category_folder(category)
        destination = category_folder / item_path.name
        
        # Handle name conflicts
        if destination.exists():
            base = item_path.stem
            ext = item_path.suffix
            counter = 1
            while destination.exists():
                destination = category_folder / f"{base}_{counter}{ext}"
                counter += 1
        
        if dry_run:
            print(f"  [DRY RUN] Would move: {item_path.name} -> {category}/")
            return True
        
        # Move the item
        shutil.move(str(item_path), str(destination))
        
        # Restore timestamps
        set_file_timestamps(destination, creation_time, modification_time)
        
        print(f"  ✓ Moved: {item_path.name} -> {category}/")
        return True
        
    except Exception as e:
        print(f"  ✗ Error moving {item_path.name}: {e}")
        return False


def organize_downloads(dry_run: bool = False):
    """Main function to organize the Downloads folder."""
    print(f"\n{'=' * 60}")
    print(f"Downloads Folder Organizer")
    print(f"{'=' * 60}")
    print(f"Scanning: {DOWNLOADS_PATH}")
    if dry_run:
        print("Mode: DRY RUN (no files will be moved)")
    print()
    
    if not DOWNLOADS_PATH.exists():
        print(f"Error: Downloads folder not found at {DOWNLOADS_PATH}")
        return
    
    # Get all items in Downloads (excluding category folders we create)
    category_folders = set(CATEGORIES.keys())
    items = [
        item for item in DOWNLOADS_PATH.iterdir()
        if item.name not in category_folders and not item.name.startswith(".")
    ]
    
    # Statistics
    stats = {category: 0 for category in CATEGORIES}
    stats["Uncategorized"] = 0
    
    # Process each item
    for item in sorted(items, key=lambda x: x.name.lower()):
        category = categorize_item(item)
        
        if category:
            if move_item(item, category, dry_run):
                stats[category] += 1
        else:
            stats["Uncategorized"] += 1
    
    # Print summary
    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"{'=' * 60}")
    for category, count in stats.items():
        if count > 0:
            print(f"  {category}: {count} item(s)")
    
    total_moved = sum(v for k, v in stats.items() if k != "Uncategorized")
    print(f"\nTotal organized: {total_moved} item(s)")
    print(f"Uncategorized: {stats['Uncategorized']} item(s)")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Organize Downloads folder into categorized subfolders"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be done without actually moving files"
    )
    parser.add_argument(
        "--path", "-p",
        type=str,
        help="Custom path to organize (default: ~/Downloads)"
    )
    
    args = parser.parse_args()
    
    if args.path:
        DOWNLOADS_PATH = Path(args.path).expanduser()
    
    organize_downloads(dry_run=args.dry_run)
