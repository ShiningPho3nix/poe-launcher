@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Building executable...
echo Trying direct pyinstaller command...
pyinstaller --onefile --windowed --name "PoE-Launcher" poe_launcher.py

if %errorlevel% neq 0 (
    echo Direct pyinstaller failed, trying Python module method...
    python -m PyInstaller --onefile --windowed --name "PoE-Launcher" poe_launcher.py
    
    if %errorlevel% neq 0 (
        echo Both methods failed. Please check your Python and PyInstaller installation.
        echo You can try manually: python -m PyInstaller --onefile --windowed --name "PoE-Launcher" poe_launcher.py
        pause
        exit /b 1
    )
)

echo Build complete! Check the 'dist' folder for PoE-Launcher.exe
pause