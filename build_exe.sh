#!/bin/bash
echo "Installing required packages..."
pip install -r requirements.txt

echo "Building executable..."
pyinstaller --onefile --windowed --name "PoE-Launcher" poe_launcher.py

echo "Build complete! Check the 'dist' folder for PoE-Launcher executable"