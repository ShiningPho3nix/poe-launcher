@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Building executable...
pyinstaller --onefile --windowed --name "PoE-Launcher" --icon=icon.ico poe_launcher.py

echo Build complete! Check the 'dist' folder for PoE-Launcher.exe
pause