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
- Chaos Recipe Enhancer: `C:\Program Files (x86)\Chaos Recipe Enhancer\`
- Custom drive installations (D:\Games\, E:\Steam\, etc.)
- Steam: Simplified detection using steam.exe only
- Standalone PoE: Version-specific detection when selected

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
3. Detailed results dialog shows:
   - ✅ Found programs with their file paths
   - ❌ Missing programs with specific suggestions
   - 🔍 Searched locations (Registry, Program Files, etc.)
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

**🎮 Steam Version Simplified**
- Steam version uses standard Steam protocol for reliable game launching
- Only requires steam.exe detection (no complex game executable detection)
- Faster and more reliable startup with Steam's built-in game management
- Supports custom Steam library locations automatically

**🔧 UI & UX Improvements**
- **Larger Window**: Increased default height from 750px to 800px for better button visibility
- **Info Icons**: Added ℹ buttons next to Steam/Game paths explaining their purpose
- **Complete Language Switching**: All UI elements now update when changing EN ↔ DE
- **Fixed Label Truncation**: Program names no longer cut off by input fields
- **Consistent Path Display**: All paths use Windows backslashes (\) format

**🎯 Enhanced Auto-Detection**
- **Version-Specific Detection**: Only searches for programs relevant to selected version
- **Improved CRE Detection**: Properly finds Chaos Recipe Enhancer in Program Files (x86)
- **Detailed User Feedback**: Comprehensive results dialog showing what was found/missing
- **Enhanced Search Methods**: Desktop, Downloads, portable app location scanning
- **False Positive Prevention**: Removed unreliable process detection
- **Actionable Suggestions**: Specific tips for finding missing programs

**🛠 Technical Fixes**
- Fixed path separator inconsistencies (C:/ vs C:\)
- Removed hardcoded paths for better detection accuracy
- Enhanced error handling during program launches
- Improved startup performance and reliability

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