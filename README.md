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
1. Download `PoE-Launcher.exe`
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

**Windows:**
```bash
build_exe.bat
```

**Linux/Mac (for development):**
```bash
./build_exe.sh
```

The executable will be created in the `dist/` folder.

#### Configuration
Settings are automatically saved to:
- **Windows**: `%LOCALAPPDATA%\PoELauncher\config.json`
- **Linux/Mac**: `~/.config/PoeLauncher/config.json`

## Default Paths
The application comes with common default paths:
- **Steam**: `C:\Program Files (x86)\Steam\steam.exe`
- **Standalone PoE**: `C:\Program Files (x86)\Grinding Gear Games\Path of Exile\PathOfExile.exe`
- **Awakened PoE Trade**: `C:\Program Files\Awakened PoE Trade\Awakened PoE Trade.exe`
- **PoE Lurker**: `C:\Program Files\PoE Lurker\Poe Lurker.exe`
- **Chaos Recipe Enhancer**: `C:\Program Files\Chaos Recipe Enhancer\ChaosRecipeEnhancer.exe`

Simply browse and update these paths to match your actual installation locations.

## Language Support
- **English** (default for most systems)
- **German** (default for German systems)
- Language can be changed in the dropdown menu

## Troubleshooting
- Make sure all program paths are correct
- Run as administrator if you have permission issues
- Check Windows Defender/antivirus if the executable is blocked