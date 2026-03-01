# Downloads Organizer

A Python script to automatically organize your Downloads folder into categorized subfolders while preserving original file timestamps.

## Features

- **Automatic categorization** of files into logical folders
- **Preserves timestamps** - maintains original creation and modification dates
- **Content-based detection** - analyzes ZIP archives and folders for smarter categorization
- **Dry-run mode** - preview changes before applying them
- **Custom path support** - organize any folder, not just Downloads

## Categories

| Category | File Types |
|----------|------------|
| **3D Printing** | `.stl`, `.3mf`, `.gcode`, `.stp`, `.step`, `.lys`, folders/ZIPs with 3D files |
| **3D Models** | `.fbx`, `.blend`, `.max`, `.glb`, `.gltf`, `.usd`, `.dae` |
| **Packages** | `.dmg`, `.pkg`, `.app`, `.iso`, `.apk`, `.aab` |
| **Images** | `.jpg`, `.png`, `.gif`, `.svg`, `.webp`, `.avif`, `.psd`, `.ai` |
| **Screenshots** | Files starting with "Screenshot", "Screen Shot", "Capture" |
| **Screen Recordings** | Files starting with "Screen Recording" |
| **Video** | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.txt`, `.csv`, `.af`, `.afdesign` |
| **Sources** | `.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.html`, `.css`, `.json`, `.md`, `.patch`, folders/ZIPs with source code |
| **Music** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`, `.vital` |
| **Hardware** | Gerber files, drill files, PCB designs, BOM, Pick and Place files |
| **Firmware** | `.bin`, `.img`, `.hex`, `.elf`, `.uf2`, `.dtb` |
| **Archives** | `.zip`, `.tar`, `.gz`, `.rar`, `.7z`, `.bz2`, `.xz` |
| **Unsorted** | Everything else (files and folders that don't match other categories) |

## Installation

```bash
git clone https://github.com/ernestp/DownloadsOrganizer.git
cd DownloadsOrganizer
```

No dependencies required - uses only Python standard library.

## Usage

### Basic Usage

Organize your Downloads folder:
```bash
python3 organize_downloads.py
```

### Dry Run (Preview)

See what would be organized without making changes:
```bash
python3 organize_downloads.py --dry-run
```

### Custom Path

Organize a different folder:
```bash
python3 organize_downloads.py --path /path/to/folder
```

### Examples

```bash
# Preview organization of Downloads
python3 organize_downloads.py -n

# Organize external drive Downloads folder
python3 organize_downloads.py --path '/Volumes/External/Downloads'

# Organize and see what was moved
python3 organize_downloads.py
```

## How It Works

1. **Content Analysis**: Checks inside ZIP files and folders to detect 3D printing files and source code
2. **Pattern Matching**: Identifies screenshots and recordings by filename patterns
3. **Extension Matching**: Categorizes files by their extensions
4. **Fallback**: Remaining items go to Unsorted folder
5. **Timestamp Preservation**: Maintains original creation and modification times using `os.utime()` and macOS `SetFile`

## Smart Features

- **ZIP Detection**: Automatically detects if a ZIP contains STL files or source code
- **Folder Detection**: Analyzes folder contents to categorize project folders
- **Conflict Resolution**: Automatically renames files if destination already exists
- **Category Exclusion**: Never processes already-organized category folders

## Requirements

- Python 3.9+
- macOS (for full timestamp preservation with `SetFile`)
- Works on Linux/Windows with partial timestamp support

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Feel free to:
- Add new file categories
- Improve detection logic
- Add new features
- Report bugs

## Author

Ernest Poletaev

## Repository

https://github.com/ernestp/DownloadsOrganizer
