# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Path of Exile Launcher - a Python tkinter GUI application that creates a Windows executable for launching Path of Exile and companion programs together. The project converts an existing HTA (HTML Application) into a standalone Windows executable.

## Build Commands

**Development (run directly):**
```bash
python poe_launcher.py
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Build Windows executable:**
```bash
# On Windows
build_exe.bat

# On Linux/Mac (for development)
./build_exe.sh
```

The executable will be created in the `dist/` folder as `PoE-Launcher.exe`.

## Architecture

**Single-file application structure:**
- `poe_launcher.py` - Main application containing the complete GUI and logic in one Python class
- `poe_launcher_hta.html` - Original HTA version used as reference (VBScript + JavaScript)
- Build scripts create standalone executables using PyInstaller

**Key components in PoELauncher class:**
- **GUI Setup**: `setup_window()`, `create_widgets()` - tkinter interface with dark theme
- **Settings Management**: `load_settings()`, `save_settings()` - JSON config persistence
- **Multi-language**: `load_translations()`, `t()` - English/German support with system detection  
- **Program Launching**: `launch()`, `run_program()` - Process management and Steam integration
- **Process Detection**: `is_process_running()` - Prevents duplicate launches using psutil

## Configuration

Settings are automatically saved to platform-specific locations:
- **Windows**: `%LOCALAPPDATA%\PoELauncher\config.json`
- **Linux/Mac**: `~/.config/PoeLauncher/config.json`

## Dependencies & Technology Stack

- **Python 3.7+** with tkinter (GUI framework)
- **psutil** - Process detection and management
- **PyInstaller** - Executable creation
- **Threading** - Non-blocking program launches
- **Platform-specific launcher integration** - Steam app launching, subprocess management

## Program Integration Points

The launcher manages multiple external programs:
- **Path of Exile**: Steam (via `-applaunch 238960`) or Standalone executable
- **Companion tools**: Awakened PoE Trade, PoE Lurker, Chaos Recipe Enhancer
- **Websites**: FilterBlade.xyz, pathofexile.com/trade via webbrowser module

## UI Architecture 

The interface uses a section-based layout with dynamic visibility:
- Game version radio buttons control path input visibility
- Checkboxes control which companion programs launch
- File browser dialogs for path selection
- Status label for launch feedback
- Language dropdown for runtime language switching