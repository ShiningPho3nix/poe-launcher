# Path of Exile Launcher

A simple Windows executable launcher for Path of Exile and companion programs.

## Features

- **Game Version Support**: Steam or Standalone Path of Exile
- **Companion Programs**: 
  - Awakened PoE Trade
  - PoE Lurker
  - Chaos Recipe Enhancer
- **Website Integration**: Optional opening of FilterBlade and PoE Trade Site
- **Multi-language**: English and German (auto-detects system language)
- **Settings Persistence**: Saves all your settings automatically
- **Process Detection**: Avoids launching duplicate instances
- **Dark Theme**: Modern, Path of Exile themed interface

## How to Use

### For End Users
1. Download `PoE-Launcher.exe` from the [latest release](https://github.com/ShiningPho3nix/poe-launcher/releases)
2. Double-click to run
3. Set up your game paths and companion program paths
4. Select which programs/websites you want to launch
5. Click "Launch Path of Exile" to start everything

### For Developers

#### Requirements
- Python 3.7+
- tkinter (usually included with Python)
- Required packages: `pip install -r requirements.txt`

#### Building the Executable

**Method 1 - Using build script (Windows):**
```cmd
build_exe.bat
```

**Method 2 - Manual build (Windows):**
If the build script doesn't work, try manually:
```cmd
pip install pyinstaller psutil
python -m PyInstaller --onefile --windowed --name "PoE-Launcher" poe_launcher.py
```

**Linux/Mac (for development only):**
```bash
./build_exe.sh
```

The executable will be created in the `dist/` folder as `PoE-Launcher.exe`.

#### Configuration
Settings are automatically saved to:
- **Windows**: `%LOCALAPPDATA%\PoELauncher\config.json`
- **Linux/Mac**: `~/.config/PoeLauncher/config.json`

## Setup
On first launch, you'll need to configure the paths to your programs:
1. Select your game version (Steam or Standalone)
2. Browse and set the path to your game executable
3. Browse and set paths for any companion programs you want to use
4. Checkboxes are only enabled when valid program paths are set

## Language Support
- **English** (default for most systems)
- **German** (default for German systems)
- Language can be changed in the dropdown menu

## Troubleshooting

### For End Users
- Make sure all program paths are correct
- Run as administrator if you have permission issues
- Check Windows Defender/antivirus if the executable is blocked

### For Developers (Building Issues)
- **"pyinstaller command not found"**: Use `python -m PyInstaller` instead of `pyinstaller`
- **Permission errors**: PyInstaller may install to user directory - use the manual build method
- **Missing dependencies**: Make sure to install all requirements: `pip install pyinstaller psutil`
- **Build fails**: Try running commands individually instead of using the batch file