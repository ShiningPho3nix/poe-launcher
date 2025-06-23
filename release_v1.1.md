# Path of Exile Launcher v1.1 Release Notes

## 🎯 Major Feature: Automatic Program Detection

### What's New
The biggest update yet! The launcher now automatically finds your installed programs, eliminating the need for manual path entry in most cases.

### ✨ Auto-Detection Features

**🔍 Intelligent Detection System**
- **Registry Scanning**: Searches Windows uninstall entries for all programs
- **Multi-Drive Support**: Finds programs on C:\, D:\, E:\, or any drive
- **Steam Library Detection**: Parses Steam configuration for custom library locations
- **Real-World Patterns**: Based on actual user installation data

**🎮 Supported Programs**
- Steam installation (steam.exe)
- Path of Exile Standalone & Steam versions
- Awakened PoE Trade
- PoE Lurker (including AppData installations)
- Chaos Recipe Enhancer

**⚡ User Experience**
- **Startup Detection**: Automatically runs when launcher opens (only if paths are missing)
- **Manual Re-scan**: "Auto-Detect Programs" button for on-demand detection
- **Smart Status**: Shows detection progress and results
- **Non-Blocking**: Runs in background, doesn't freeze the interface

### 🛠 Technical Improvements

**Detection Methods**
1. **Windows Registry**: Fast detection from uninstall entries
2. **Filesystem Patterns**: Comprehensive multi-drive scanning
3. **Steam Integration**: Custom Steam library folder support
4. **Known Locations**: Handles common installation variations

**Real Installation Support**
- Awakened PoE Trade: `C:\Program Files\Awakened PoE Trade\`
- PoE Lurker: `%LOCALAPPDATA%\PoeLurker\current\`
- Custom drive installations (D:\Games\, E:\Steam\, etc.)
- Steam PoE: Direct executable launch from Steam library folders
- Standalone PoE: Traditional executable detection

**Cross-Platform Compatibility**
- Graceful fallback on non-Windows systems
- Safe registry access with error handling
- Performance optimized for quick detection

### 🌍 Language Support
- **English**: "Auto-Detect Programs" button
- **German**: "Programme Automatisch Erkennen" button

## 📋 How It Works

### First Launch
1. Launch the application
2. If paths are empty, auto-detection runs automatically
3. Found programs populate the interface
4. Checkboxes enable for valid installations

### Manual Detection
1. Click "Auto-Detect Programs" button anytime
2. Status shows "Detecting installed programs..."
3. Results display: "Auto-detection complete: X programs found"
4. Paths update automatically

### Smart Behavior
- **Preserves Manual Settings**: Won't overwrite user-configured paths
- **Validates Paths**: Only enables programs with valid executable files
- **Background Processing**: Doesn't block UI during detection
- **Error Handling**: Graceful fallback if detection fails

## 🎯 Benefits

**For New Users**
- Zero manual configuration in most cases
- Immediate usability out of the box
- Automatic discovery of companion programs

**For Existing Users**
- Easy re-detection after program updates
- Support for new installation locations
- No disruption to existing configurations

**For Advanced Users**
- Manual override capabilities preserved
- Multi-drive and custom path support
- Technical details in console output

## 🔧 Installation

Download the latest release and run - auto-detection will handle the rest!

**System Requirements**
- Windows 7 or later
- .NET Framework 4.8+ (for detected programs)
- Python 3.7+ (for launcher source)

## 🐛 Bug Fixes & Improvements

**🎮 Steam Version Launch Fix**
- Steam version now launches Path of Exile executable directly from Steam library
- Dual detection: finds both steam.exe and PathOfExile.exe in Steam installations
- Faster and more reliable game startup (no Steam protocol overhead)
- Smart fallback to Steam URL protocol if direct executable not available
- Supports custom Steam library locations automatically

**🔧 General Improvements**
- Enhanced path validation for companion programs
- Improved error handling during program launches
- Better status messaging throughout the interface
- Optimized startup performance
- Persistent storage of detected Steam PoE path

## 🚀 Coming Soon

- Program update detection
- Installation health checks
- Enhanced Steam library management
- Additional companion program support

---

**Download**: [Latest Release](https://github.com/ShiningPho3nix/poe-launcher/releases)  
**Report Issues**: [GitHub Issues](https://github.com/ShiningPho3nix/poe-launcher/issues)  
**Source Code**: [GitHub Repository](https://github.com/ShiningPho3nix/poe-launcher)

*This release represents a major step forward in user experience, making the launcher truly plug-and-play for Path of Exile enthusiasts!*