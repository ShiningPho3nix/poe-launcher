#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import subprocess
import psutil
import webbrowser
import locale
import sys
from pathlib import Path
import time
import threading
import glob
import string
try:
    import winreg
except ImportError:
    winreg = None

class PoELauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.load_translations()
        self.setup_config_path()
        self.create_widgets()
        self.load_settings()
        self.update_ui()
        
        # Auto-detect installations on startup (only if paths are empty)
        self.auto_detect_on_startup()
        
    def setup_window(self):
        self.root.title("Path of Exile Launcher")
        self.root.geometry("600x800")
        self.root.resizable(True, True)
        self.root.minsize(500, 650)
        
        # Dark theme colors
        self.colors = {
            'bg': '#1a1a2e',
            'bg_light': '#16213e',
            'accent': '#e94560',
            'secondary': '#4fbdba',
            'text': '#ffffff',
            'text_dim': '#cccccc',
            'button_bg': '#4fbdba',
            'button_hover': '#3fa9a7'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
    def setup_variables(self):
        # Game version
        self.game_version = tk.StringVar(value="steam")
        
        # Paths
        self.steam_path = tk.StringVar(value="")
        self.standalone_path = tk.StringVar(value="")
        
        # Companion programs
        self.awakened_path = tk.StringVar(value="")
        self.lurker_path = tk.StringVar(value="")
        self.chaos_recipe_path = tk.StringVar(value="")
        
        # Checkboxes
        self.start_awakened = tk.BooleanVar(value=False)
        self.start_lurker = tk.BooleanVar(value=False)
        self.start_chaos_recipe = tk.BooleanVar(value=False)
        self.open_filterblade = tk.BooleanVar(value=False)
        self.open_trade_site = tk.BooleanVar(value=False)
        
        # Language
        self.language = tk.StringVar(value="en")
        
        # Store checkbox references for enabling/disabling
        self.checkboxes = {}
        
        # Store detected Steam PoE path
        self.steam_poe_path = ""
        
    def load_translations(self):
        self.translations = {
            'en': {
                'title': 'Path of Exile Launcher',
                'game_version': 'Game Version',
                'steam_version': 'Steam Version',
                'standalone_version': 'Standalone Version',
                'steam_path': 'Steam Path:',
                'game_path': 'Game Path:',
                'companion_programs': 'Companion Programs',
                'awakened_trade': 'Awakened PoE Trade',
                'poe_lurker': 'Poe Lurker',
                'chaos_recipe': 'Chaos Recipe Enhancer',
                'websites': 'Websites',
                'filterblade': 'FilterBlade',
                'trade_site': 'Trade Site',
                'browse': 'Browse',
                'launch': 'Start',
                'start': 'Start',
                'language': 'Language:',
                'auto_detect': 'Auto-Detect Programs',
                'steam_path_info': 'Path to Steam executable (steam.exe)\n\nThis is used to start Steam if it\'s not already running.\nThe actual Path of Exile game will be launched automatically\nfrom your Steam library.',
                'game_path_info': 'Path to standalone Path of Exile executable\n(PathOfExile.exe)\n\nThis is the direct game executable for the\nstandalone (non-Steam) version of Path of Exile.',
                'launching': 'Launching programs...',
                'steam_starting': 'Starting Steam... Please wait...',
                'launched_successfully': 'Successfully launched: {}',
                'errors_occurred': 'Errors: {}',
                'file_not_found': '{} not found at: {}',
                'closing_in': ' (Closing in {} seconds...)'
            },
            'de': {
                'title': 'Path of Exile Launcher',
                'game_version': 'Spiel Version',
                'steam_version': 'Steam Version',
                'standalone_version': 'Standalone Version',
                'steam_path': 'Steam Pfad:',
                'game_path': 'Spiel Pfad:',
                'companion_programs': 'Begleitprogramme',
                'awakened_trade': 'Awakened PoE Trade',
                'poe_lurker': 'Poe Lurker',
                'chaos_recipe': 'Chaos Recipe Enhancer',
                'websites': 'Webseiten',
                'filterblade': 'FilterBlade',
                'trade_site': 'Handelsseite',
                'browse': 'Durchsuchen',
                'launch': 'Starten',
                'start': 'Starten',
                'language': 'Sprache:',
                'auto_detect': 'Programme Automatisch Erkennen',
                'steam_path_info': 'Pfad zur Steam-Anwendung (steam.exe)\n\nWird verwendet, um Steam zu starten, falls es noch nicht läuft.\nDas eigentliche Path of Exile Spiel wird automatisch\naus Ihrer Steam-Bibliothek gestartet.',
                'game_path_info': 'Pfad zur eigenständigen Path of Exile Anwendung\n(PathOfExile.exe)\n\nDies ist die direkte Spiel-Anwendung für die\neigenständige (Nicht-Steam) Version von Path of Exile.',
                'launching': 'Programme werden gestartet...',
                'steam_starting': 'Steam wird gestartet... Bitte warten...',
                'launched_successfully': 'Erfolgreich gestartet: {}',
                'errors_occurred': 'Fehler: {}',
                'file_not_found': '{} nicht gefunden unter: {}',
                'closing_in': ' (Schließt in {} Sekunden...)'
            }
        }
        
        # Detect system language
        try:
            system_lang = locale.getdefaultlocale()[0]
            if system_lang and system_lang.startswith('de'):
                self.language.set('de')
            else:
                self.language.set('en')
        except:
            self.language.set('en')
    
    def t(self, key):
        """Get translated text"""
        return self.translations[self.language.get()].get(key, key)
    
    def setup_config_path(self):
        """Setup configuration file path"""
        if os.name == 'nt':  # Windows
            config_dir = os.path.expanduser('~\\AppData\\Local\\PoELauncher')
        else:
            config_dir = os.path.expanduser('~/.config/PoeLauncher')
        
        os.makedirs(config_dir, exist_ok=True)
        self.config_file = os.path.join(config_dir, 'config.json')
        
        # Debug: Print config path to help with troubleshooting
        print(f"Config file path: {self.config_file}")
    
    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(main_frame, text=self.t('title'), 
                                   font=('Segoe UI', 20, 'bold'),
                                   fg=self.colors['accent'], bg=self.colors['bg'])
        self.title_label.pack(pady=(0, 20))
        
        # Language selection
        lang_frame = self.create_section_frame(main_frame)
        self.lang_title = tk.Label(lang_frame, text=self.t('language'),
                                  font=('Segoe UI', 12, 'bold'),
                                  fg=self.colors['secondary'], bg=self.colors['bg_light'])
        self.lang_title.pack(anchor='w', pady=(0, 10))
        
        lang_combo_frame = tk.Frame(lang_frame, bg=self.colors['bg_light'])
        lang_combo_frame.pack(fill='x')
        
        self.lang_combo = ttk.Combobox(lang_combo_frame, textvariable=self.language,
                                      values=['en', 'de'], state='readonly', width=10)
        self.lang_combo.pack(side='left')
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Auto-detect button
        self.auto_detect_btn = tk.Button(lang_combo_frame, text=self.t('auto_detect'),
                                        command=self.auto_detect_threaded,
                                        bg=self.colors['secondary'], fg='white',
                                        relief='flat', padx=15)
        self.auto_detect_btn.pack(side='right')
        
        # Game Version Section
        game_frame = self.create_section_frame(main_frame)
        self.game_version_title = self.create_section_title(game_frame, 'game_version')
        
        # Radio buttons for game version
        radio_frame = tk.Frame(game_frame, bg=self.colors['bg_light'])
        radio_frame.pack(fill='x', pady=(0, 10))
        
        self.steam_radio = tk.Radiobutton(radio_frame, text=self.t('steam_version'),
                                         variable=self.game_version, value='steam',
                                         command=self.update_ui,
                                         fg=self.colors['text'], bg=self.colors['bg_light'],
                                         selectcolor=self.colors['bg'], activebackground=self.colors['bg_light'])
        self.steam_radio.pack(side='left', padx=(0, 20))
        
        self.standalone_radio = tk.Radiobutton(radio_frame, text=self.t('standalone_version'),
                                              variable=self.game_version, value='standalone',
                                              command=self.update_ui,
                                              fg=self.colors['text'], bg=self.colors['bg_light'],
                                              selectcolor=self.colors['bg'], activebackground=self.colors['bg_light'])
        self.standalone_radio.pack(side='left')
        
        # Steam path with info icon
        self.steam_path_frame = self.create_path_input_with_info(game_frame, 'steam_path', self.steam_path, self.browse_steam_path, 'steam_path_info')
        
        # Standalone path with info icon
        self.standalone_path_frame = self.create_path_input_with_info(game_frame, 'game_path', self.standalone_path, self.browse_standalone_path, 'game_path_info')
        
        # Companion Programs Section
        companion_frame = self.create_section_frame(main_frame)
        self.companion_title = self.create_section_title(companion_frame, 'companion_programs')
        
        # Awakened PoE Trade
        self.create_program_input(companion_frame, 'awakened_trade', self.start_awakened, 
                                 self.awakened_path, self.browse_awakened_path)
        
        # PoE Lurker
        self.create_program_input(companion_frame, 'poe_lurker', self.start_lurker, 
                                 self.lurker_path, self.browse_lurker_path)
        
        # Chaos Recipe Enhancer
        self.create_program_input(companion_frame, 'chaos_recipe', self.start_chaos_recipe, 
                                 self.chaos_recipe_path, self.browse_chaos_recipe_path)
        
        # Websites Section
        websites_frame = self.create_section_frame(main_frame)
        self.websites_title = self.create_section_title(websites_frame, 'websites')
        
        # FilterBlade checkbox
        filterblade_frame = tk.Frame(websites_frame, bg=self.colors['bg_light'])
        filterblade_frame.pack(fill='x', pady=(0, 5))
        
        self.filterblade_check = tk.Checkbutton(filterblade_frame, text=self.t('filterblade'),
                                               variable=self.open_filterblade,
                                               fg=self.colors['text'], bg=self.colors['bg_light'],
                                               selectcolor=self.colors['bg'], activebackground=self.colors['bg_light'])
        self.filterblade_check.pack(side='left')
        
        # Trade Site checkbox
        trade_frame = tk.Frame(websites_frame, bg=self.colors['bg_light'])
        trade_frame.pack(fill='x')
        
        self.trade_check = tk.Checkbutton(trade_frame, text=self.t('trade_site'),
                                         variable=self.open_trade_site,
                                         fg=self.colors['text'], bg=self.colors['bg_light'],
                                         selectcolor=self.colors['bg'], activebackground=self.colors['bg_light'])
        self.trade_check.pack(side='left')
        
        # Launch Button
        self.launch_button = tk.Button(main_frame, text=self.t('launch'),
                                      command=self.launch_threaded,
                                      font=('Segoe UI', 14, 'bold'),
                                      fg='white', bg=self.colors['accent'],
                                      activeforeground='white', activebackground='#ff6b6b',
                                      relief='flat', pady=15)
        self.launch_button.pack(fill='x', pady=(20, 10))
        
        # Status Label
        self.status_label = tk.Label(main_frame, text="",
                                    font=('Segoe UI', 10),
                                    fg=self.colors['secondary'], bg=self.colors['bg'])
        self.status_label.pack(pady=(10, 0))
    
    def create_section_frame(self, parent):
        frame = tk.Frame(parent, bg=self.colors['bg_light'], relief='solid', bd=1)
        frame.pack(fill='x', pady=(0, 15))
        
        inner_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        inner_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        return inner_frame
    
    def create_section_title(self, parent, text_key):
        title = tk.Label(parent, text=self.t(text_key),
                        font=('Segoe UI', 12, 'bold'),
                        fg=self.colors['secondary'], bg=self.colors['bg_light'])
        title.pack(anchor='w', pady=(0, 10))
        return title
    
    def create_path_input(self, parent, label_key, path_var, browse_command):
        frame = tk.Frame(parent, bg=self.colors['bg_light'])
        frame.pack(fill='x', pady=(0, 10))
        
        label = tk.Label(frame, text=self.t(label_key), width=12,
                        fg=self.colors['text'], bg=self.colors['bg_light'])
        label.pack(side='left')
        
        entry = tk.Entry(frame, textvariable=path_var,
                        bg=self.colors['bg'], fg=self.colors['text'],
                        insertbackground=self.colors['text'])
        entry.pack(side='left', fill='x', expand=True, padx=(5, 5))
        
        browse_btn = tk.Button(frame, text=self.t('browse'),
                              command=browse_command,
                              bg=self.colors['button_bg'], fg='white',
                              relief='flat', padx=15)
        browse_btn.pack(side='right')
        
        return frame
    
    def create_path_input_with_info(self, parent, label_key, path_var, browse_command, info_key):
        frame = tk.Frame(parent, bg=self.colors['bg_light'])
        frame.pack(fill='x', pady=(0, 10))
        
        # Label with info icon
        label_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        label_frame.pack(side='left')
        
        label = tk.Label(label_frame, text=self.t(label_key), width=12,
                        fg=self.colors['text'], bg=self.colors['bg_light'])
        label.pack(side='left')
        
        # Info icon button
        info_btn = tk.Button(label_frame, text="ℹ", font=('Segoe UI', 8), width=2,
                            command=lambda: self.show_info(info_key),
                            bg=self.colors['secondary'], fg='white',
                            relief='flat', pady=0)
        info_btn.pack(side='left', padx=(2, 0))
        
        entry = tk.Entry(frame, textvariable=path_var,
                        bg=self.colors['bg'], fg=self.colors['text'],
                        insertbackground=self.colors['text'])
        entry.pack(side='left', fill='x', expand=True, padx=(5, 5))
        
        browse_btn = tk.Button(frame, text=self.t('browse'),
                              command=browse_command,
                              bg=self.colors['button_bg'], fg='white',
                              relief='flat', padx=15)
        browse_btn.pack(side='right')
        
        # Store references for language updates
        if not hasattr(self, 'path_labels'):
            self.path_labels = {}
        if not hasattr(self, 'browse_buttons'):
            self.browse_buttons = {}
            
        self.path_labels[label_key] = label
        self.browse_buttons[label_key] = browse_btn
        
        return frame
    
    def show_info(self, info_key):
        """Show info dialog for path fields"""
        info_text = self.t(info_key)
        messagebox.showinfo("Information", info_text)
    
    def create_program_input(self, parent, label_key, check_var, path_var, browse_command):
        frame = tk.Frame(parent, bg=self.colors['bg_light'])
        frame.pack(fill='x', pady=(0, 10))
        
        check = tk.Checkbutton(frame, text=self.t(label_key), variable=check_var,
                              width=15, anchor='w', state='disabled',
                              fg=self.colors['text'], bg=self.colors['bg_light'],
                              selectcolor=self.colors['bg'], activebackground=self.colors['bg_light'])
        check.pack(side='left')
        
        # Store checkbox reference for later enabling/disabling
        self.checkboxes[label_key] = check
        
        entry = tk.Entry(frame, textvariable=path_var,
                        bg=self.colors['bg'], fg=self.colors['text'],
                        insertbackground=self.colors['text'])
        entry.pack(side='left', fill='x', expand=True, padx=(5, 5))
        
        # Bind path change to validation
        path_var.trace('w', lambda *args: self.validate_path(label_key, path_var))
        
        browse_btn = tk.Button(frame, text=self.t('browse'),
                              command=lambda: self.browse_and_validate(path_var, browse_command, label_key),
                              bg=self.colors['button_bg'], fg='white',
                              relief='flat', padx=15)
        browse_btn.pack(side='right')
    
    def update_ui(self):
        """Update UI visibility based on game version selection"""
        if self.game_version.get() == 'steam':
            self.steam_path_frame.pack(fill='x', pady=(0, 10))
            self.standalone_path_frame.pack_forget()
        else:
            self.steam_path_frame.pack_forget()
            self.standalone_path_frame.pack(fill='x', pady=(0, 10))
    
    def on_language_change(self, event=None):
        """Handle language change"""
        self.save_settings()
        self.refresh_ui_text()
    
    def refresh_ui_text(self):
        """Refresh all UI text after language change"""
        self.root.title(self.t('title'))
        
        # Update main title and language label
        if hasattr(self, 'title_label'):
            self.title_label.config(text=self.t('title'))
        if hasattr(self, 'lang_title'):
            self.lang_title.config(text=self.t('language'))
        
        # Update section titles
        if hasattr(self, 'game_version_title'):
            self.game_version_title.config(text=self.t('game_version'))
        if hasattr(self, 'companion_title'):
            self.companion_title.config(text=self.t('companion_programs'))
        if hasattr(self, 'websites_title'):
            self.websites_title.config(text=self.t('websites'))
        
        # Update path labels
        if hasattr(self, 'path_labels'):
            for label_key, label in self.path_labels.items():
                label.config(text=self.t(label_key))
        
        # Update browse buttons
        if hasattr(self, 'browse_buttons'):
            for button_key, button in self.browse_buttons.items():
                button.config(text=self.t('browse'))
        
        # Update radio button texts
        if hasattr(self, 'steam_radio'):
            self.steam_radio.config(text=self.t('steam_version'))
        if hasattr(self, 'standalone_radio'):
            self.standalone_radio.config(text=self.t('standalone_version'))
        
        # Update checkbox texts
        if hasattr(self, 'checkboxes'):
            if 'awakened_trade' in self.checkboxes:
                self.checkboxes['awakened_trade'].config(text=self.t('awakened_trade'))
            if 'poe_lurker' in self.checkboxes:
                self.checkboxes['poe_lurker'].config(text=self.t('poe_lurker'))
            if 'chaos_recipe' in self.checkboxes:
                self.checkboxes['chaos_recipe'].config(text=self.t('chaos_recipe'))
        
        # Update website checkboxes
        if hasattr(self, 'filterblade_check'):
            self.filterblade_check.config(text=self.t('filterblade'))
        if hasattr(self, 'trade_check'):
            self.trade_check.config(text=self.t('trade_site'))
        
        # Update launch button
        if hasattr(self, 'launch_button'):
            self.launch_button.config(text=self.t('launch'))
        
        # Update auto-detect button
        if hasattr(self, 'auto_detect_btn'):
            self.auto_detect_btn.config(text=self.t('auto_detect'))
        
        print(f"UI language changed to: {self.language.get()}")
    
    def browse_steam_path(self):
        self.browse_file(self.steam_path, "Steam executable (steam.exe)")
    
    def browse_standalone_path(self):
        self.browse_file(self.standalone_path, "Path of Exile executable (PathOfExile.exe)")
    
    def browse_awakened_path(self):
        self.browse_file(self.awakened_path, "Awakened PoE Trade executable")
    
    def browse_lurker_path(self):
        self.browse_file(self.lurker_path, "PoE Lurker executable")
    
    def browse_chaos_recipe_path(self):
        self.browse_file(self.chaos_recipe_path, "Chaos Recipe Enhancer executable")
    
    def browse_file(self, var, title):
        filename = filedialog.askopenfilename(
            title=f"Select {title}",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            var.set(filename)
    
    def browse_and_validate(self, path_var, browse_command, label_key):
        """Browse for file and validate path"""
        browse_command()
        self.validate_path(label_key, path_var)
    
    def validate_path(self, label_key, path_var):
        """Validate path and enable/disable corresponding checkbox"""
        path = path_var.get().strip()
        if label_key in self.checkboxes:
            if path and os.path.exists(path):
                self.checkboxes[label_key].config(state='normal')
            else:
                self.checkboxes[label_key].config(state='disabled')
                # Uncheck if path becomes invalid
                if label_key == 'awakened_trade':
                    self.start_awakened.set(False)
                elif label_key == 'poe_lurker':
                    self.start_lurker.set(False)
                elif label_key == 'chaos_recipe':
                    self.start_chaos_recipe.set(False)
    
    def load_settings(self):
        """Load settings from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Load all settings
                self.game_version.set(config.get('game_version', 'steam'))
                self.steam_path.set(config.get('steam_path', self.steam_path.get()))
                self.standalone_path.set(config.get('standalone_path', self.standalone_path.get()))
                self.awakened_path.set(config.get('awakened_path', self.awakened_path.get()))
                self.lurker_path.set(config.get('lurker_path', self.lurker_path.get()))
                self.chaos_recipe_path.set(config.get('chaos_recipe_path', self.chaos_recipe_path.get()))
                
                self.start_awakened.set(config.get('start_awakened', False))
                self.start_lurker.set(config.get('start_lurker', False))
                self.start_chaos_recipe.set(config.get('start_chaos_recipe', False))
                self.open_filterblade.set(config.get('open_filterblade', False))
                self.open_trade_site.set(config.get('open_trade_site', False))
                
                self.language.set(config.get('language', self.language.get()))
                
                # Load detected Steam PoE path if available
                self.steam_poe_path = config.get('steam_poe_path', '')
                
                # Validate all paths after loading
                self.validate_all_paths()
                
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        # Always validate paths even if no config file exists
        if hasattr(self, 'checkboxes'):
            self.validate_all_paths()
    
    def validate_all_paths(self):
        """Validate all program paths and update checkbox states"""
        self.validate_path('awakened_trade', self.awakened_path)
        self.validate_path('poe_lurker', self.lurker_path)
        self.validate_path('chaos_recipe', self.chaos_recipe_path)
    
    def detect_from_registry(self):
        """Detect installed programs from Windows registry"""
        detected = {}
        
        # Skip registry detection on non-Windows platforms
        if os.name != 'nt' or winreg is None:
            return detected
        registry_roots = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        
        for hkey, subkey_path in registry_roots:
            try:
                with winreg.OpenKey(hkey, subkey_path) as key:
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    install_location = ""
                                    uninstall_string = ""
                                    
                                    try:
                                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    except FileNotFoundError:
                                        pass
                                    
                                    try:
                                        uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                    except FileNotFoundError:
                                        pass
                                    
                                    # Check for Steam
                                    if "steam" in display_name.lower():
                                        if install_location and os.path.exists(os.path.join(install_location, "steam.exe")):
                                            detected['steam'] = os.path.join(install_location, "steam.exe")
                                    
                                    # Check for Path of Exile
                                    if "path of exile" in display_name.lower():
                                        if install_location and os.path.exists(os.path.join(install_location, "PathOfExile.exe")):
                                            detected['poe_standalone'] = os.path.join(install_location, "PathOfExile.exe")
                                    
                                    # Check for Awakened PoE Trade
                                    if "awakened" in display_name.lower() and "poe" in display_name.lower():
                                        exe_path = self.find_exe_in_location(install_location, "Awakened PoE Trade.exe")
                                        if exe_path:
                                            detected['awakened_trade'] = exe_path
                                    
                                    # Check for PoE Lurker
                                    if "poe lurker" in display_name.lower() or "lurker" in display_name.lower():
                                        exe_path = self.find_exe_in_location(install_location, ["PoeLurker.exe", "Poe Lurker.exe"])
                                        if exe_path:
                                            detected['poe_lurker'] = exe_path
                                    
                                    # Check for Chaos Recipe Enhancer
                                    if "chaos" in display_name.lower() and "recipe" in display_name.lower():
                                        exe_path = self.find_exe_in_location(install_location, "ChaosRecipeEnhancer.exe")
                                        if exe_path:
                                            detected['chaos_recipe'] = exe_path
                                
                                except FileNotFoundError:
                                    pass
                            i += 1
                        except OSError:
                            break
            except OSError:
                continue
        
        return detected
    
    def find_exe_in_location(self, location, exe_names):
        """Find executable in given location, supports single name or list"""
        if not location or not os.path.exists(location):
            return None
        
        if isinstance(exe_names, str):
            exe_names = [exe_names]
        
        for exe_name in exe_names:
            exe_path = os.path.join(location, exe_name)
            if os.path.exists(exe_path):
                return exe_path
        
        return None
    
    def get_all_drives(self):
        """Get all available drive letters"""
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives
    
    def detect_from_filesystem(self):
        """Detect programs using filesystem patterns - only if registry detection failed"""
        detected = {}
        
        # Skip filesystem detection on non-Windows platforms
        if os.name != 'nt':
            return detected
            
        drives = self.get_all_drives()
        
        # Only define search patterns - no hardcoded paths
        search_locations = {
            'steam': [
                ('Program Files (x86)', 'Steam', 'steam.exe'),
                ('Program Files', 'Steam', 'steam.exe'),
                ('Steam', '', 'steam.exe')
            ],
            'poe_standalone': [
                ('Program Files (x86)', 'Grinding Gear Games', 'Path of Exile', 'PathOfExile.exe'),
                ('Program Files', 'Grinding Gear Games', 'Path of Exile', 'PathOfExile.exe'),
                ('Games', 'Path of Exile', '', 'PathOfExile.exe')
            ],
            'awakened_trade': [
                ('Program Files', 'Awakened PoE Trade', '', 'Awakened PoE Trade.exe'),
            ],
            'poe_lurker': [
                ('Program Files', 'Poe Lurker', '', 'Poe Lurker.exe'),
                ('Program Files (x86)', 'Poe Lurker', '', 'Poe Lurker.exe')
            ],
            'chaos_recipe': [
                ('Program Files', 'ChaosRecipeEnhancer', '', 'ChaosRecipeEnhancer.exe'),
                ('Program Files (x86)', 'ChaosRecipeEnhancer', '', 'ChaosRecipeEnhancer.exe'),
            ]
        }
        
        # Search each drive for each program
        for program, locations in search_locations.items():
            if program in detected:
                continue
                
            for drive in drives:
                for location_parts in locations:
                    # Build path using os.path.join for correct separators
                    path_parts = [drive] + [part for part in location_parts[:-1] if part] + [location_parts[-1]]
                    full_path = os.path.join(*path_parts)
                    
                    if os.path.exists(full_path):
                        detected[program] = full_path
                        break
                        
                if program in detected:
                    break
        
        # Special handling for AppData programs
        try:
            localappdata = os.path.expandvars('%LOCALAPPDATA%')
            
            # Awakened PoE Trade in AppData
            if 'awakened_trade' not in detected:
                appdata_awakened = os.path.join(localappdata, 'Programs', 'Awakened PoE Trade', 'Awakened PoE Trade.exe')
                if os.path.exists(appdata_awakened):
                    detected['awakened_trade'] = appdata_awakened
            
            # PoE Lurker with wildcard version folders
            if 'poe_lurker' not in detected:
                lurker_base = os.path.join(localappdata, 'PoeLurker')
                if os.path.exists(lurker_base):
                    for item in os.listdir(lurker_base):
                        lurker_path = os.path.join(lurker_base, item, 'PoeLurker.exe')
                        if os.path.exists(lurker_path):
                            detected['poe_lurker'] = lurker_path
                            break
            
            # Chaos Recipe Enhancer in AppData
            if 'chaos_recipe' not in detected:
                appdata_chaos = os.path.join(localappdata, 'Programs', 'ChaosRecipeEnhancer', 'ChaosRecipeEnhancer.exe')
                if os.path.exists(appdata_chaos):
                    detected['chaos_recipe'] = appdata_chaos
                    
        except Exception as e:
            print(f"Error checking AppData locations: {e}")
        
        return detected
    
    def detect_steam_games(self, steam_path):
        """Detect games in Steam libraries"""
        detected = {}
        if not steam_path or not os.path.exists(steam_path):
            return detected
        
        steam_dir = os.path.dirname(steam_path)
        
        # Check default Steam library
        default_library = os.path.join(steam_dir, 'steamapps', 'common', 'Path of Exile', 'PathOfExile.exe')
        if os.path.exists(default_library):
            detected['poe_steam'] = default_library
        
        # Check additional Steam libraries from libraryfolders.vdf
        try:
            libraryfolders_path = os.path.join(steam_dir, 'steamapps', 'libraryfolders.vdf')
            if os.path.exists(libraryfolders_path):
                with open(libraryfolders_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Parse VDF format for library paths
                import re
                path_matches = re.findall(r'"path"\s+"([^"]+)"', content)
                
                for lib_path in path_matches:
                    poe_path = os.path.join(lib_path, 'steamapps', 'common', 'Path of Exile', 'PathOfExile.exe')
                    if os.path.exists(poe_path):
                        detected['poe_steam'] = poe_path
                        break
        except Exception as e:
            print(f"Error parsing Steam library folders: {e}")
        
        return detected
    
    def auto_detect_installations(self):
        """Main auto-detection method combining all detection strategies"""
        print("Starting auto-detection of installations...")
        detected = {}
        
        # 1. Registry detection (fastest)
        try:
            registry_detected = self.detect_from_registry()
            detected.update(registry_detected)
            print(f"Registry detection found: {list(registry_detected.keys())}")
        except Exception as e:
            print(f"Registry detection failed: {e}")
        
        # 2. Filesystem pattern detection
        try:
            filesystem_detected = self.detect_from_filesystem()
            # Only add if not already detected
            for key, value in filesystem_detected.items():
                if key not in detected:
                    detected[key] = value
            print(f"Filesystem detection found: {list(filesystem_detected.keys())}")
        except Exception as e:
            print(f"Filesystem detection failed: {e}")
        
        # 3. Steam games detection (if Steam was found)
        steam_path = detected.get('steam')
        if steam_path:
            try:
                steam_games = self.detect_steam_games(steam_path)
                for key, value in steam_games.items():
                    if key not in detected:
                        detected[key] = value
                print(f"Steam games detection found: {list(steam_games.keys())}")
            except Exception as e:
                print(f"Steam games detection failed: {e}")
        
        # Apply detected paths to UI
        self.apply_detected_paths(detected)
        
        return detected
    
    def apply_detected_paths(self, detected):
        """Apply detected paths to the UI variables"""
        # Steam executable - only set if no Steam path currently set
        if 'steam' in detected and not self.steam_path.get():
            self.steam_path.set(self.normalize_path(detected['steam']))
        
        # Standalone PoE path - only set if no standalone path currently set
        if 'poe_standalone' in detected and not self.standalone_path.get():
            self.standalone_path.set(self.normalize_path(detected['poe_standalone']))
        
        # Steam PoE path - store separately, don't put in UI paths
        if 'poe_steam' in detected:
            self.steam_poe_path = self.normalize_path(detected['poe_steam'])
            print(f"Steam PoE found at: {self.steam_poe_path}")
        
        # Companion programs - only set if paths are currently empty
        if 'awakened_trade' in detected and not self.awakened_path.get():
            self.awakened_path.set(self.normalize_path(detected['awakened_trade']))
        
        if 'poe_lurker' in detected and not self.lurker_path.get():
            self.lurker_path.set(self.normalize_path(detected['poe_lurker']))
        
        if 'chaos_recipe' in detected and not self.chaos_recipe_path.get():
            self.chaos_recipe_path.set(self.normalize_path(detected['chaos_recipe']))
        
        # Validate all paths after setting them
        self.validate_all_paths()
        
        print(f"Applied detected paths: {len(detected)} programs found")
    
    def auto_detect_threaded(self):
        """Run auto-detection in a separate thread to avoid blocking UI"""
        self.show_status("Detecting installed programs...")
        thread = threading.Thread(target=self.run_auto_detect_manual)
        thread.daemon = True
        thread.start()
    
    def run_auto_detect_manual(self):
        """Run manual auto-detection and update status - forces re-detection"""
        try:
            detected = self.auto_detect_installations_force()
            count = len(detected)
            if count > 0:
                self.show_status(f"Auto-detection complete: {count} programs found")
            else:
                self.show_status("Auto-detection complete: No programs found")
            
            # Clear status after a few seconds
            def clear_status():
                time.sleep(3)
                self.show_status("")
            
            clear_thread = threading.Thread(target=clear_status)
            clear_thread.daemon = True
            clear_thread.start()
            
        except Exception as e:
            self.show_status(f"Auto-detection failed: {str(e)}")
            print(f"Auto-detection error: {e}")
    
    def auto_detect_installations_force(self):
        """Force auto-detection regardless of current paths"""
        print("Starting forced auto-detection of installations...")
        detected = {}
        
        # 1. Registry detection (fastest)
        try:
            registry_detected = self.detect_from_registry()
            detected.update(registry_detected)
            print(f"Registry detection found: {list(registry_detected.keys())}")
        except Exception as e:
            print(f"Registry detection failed: {e}")
        
        # 2. Filesystem pattern detection
        try:
            filesystem_detected = self.detect_from_filesystem()
            # Only add if not already detected
            for key, value in filesystem_detected.items():
                if key not in detected:
                    detected[key] = value
            print(f"Filesystem detection found: {list(filesystem_detected.keys())}")
        except Exception as e:
            print(f"Filesystem detection failed: {e}")
        
        # 3. Steam games detection (if Steam was found)
        steam_path = detected.get('steam')
        if steam_path:
            try:
                steam_games = self.detect_steam_games(steam_path)
                for key, value in steam_games.items():
                    if key not in detected:
                        detected[key] = value
                print(f"Steam games detection found: {list(steam_games.keys())}")
            except Exception as e:
                print(f"Steam games detection failed: {e}")
        
        # Apply detected paths to UI (force mode allows overwriting)
        self.apply_detected_paths_force(detected)
        
        return detected
    
    def normalize_path(self, path):
        """Normalize path to use consistent Windows backslashes"""
        if not path:
            return path
        # Convert forward slashes to backslashes and normalize
        return os.path.normpath(path.replace('/', '\\'))
    
    def apply_detected_paths_force(self, detected):
        """Apply detected paths to the UI variables - force mode overwrites existing"""
        # Steam executable
        if 'steam' in detected:
            self.steam_path.set(self.normalize_path(detected['steam']))
        
        # Standalone PoE path
        if 'poe_standalone' in detected:
            self.standalone_path.set(self.normalize_path(detected['poe_standalone']))
        
        # Steam PoE path - store separately
        if 'poe_steam' in detected:
            self.steam_poe_path = self.normalize_path(detected['poe_steam'])
            print(f"Steam PoE found at: {self.steam_poe_path}")
        
        # Companion programs
        if 'awakened_trade' in detected:
            self.awakened_path.set(self.normalize_path(detected['awakened_trade']))
        
        if 'poe_lurker' in detected:
            self.lurker_path.set(self.normalize_path(detected['poe_lurker']))
        
        if 'chaos_recipe' in detected:
            self.chaos_recipe_path.set(self.normalize_path(detected['chaos_recipe']))
        
        # Validate all paths after setting them
        self.validate_all_paths()
        
        print(f"Applied detected paths (force): {len(detected)} programs found")
    
    def auto_detect_on_startup(self):
        """Run auto-detection on startup only if paths are missing"""
        # Check if we need auto-detection (if main paths are empty)
        need_detection = (
            not self.steam_path.get() or 
            not self.standalone_path.get() or
            not self.awakened_path.get() or
            not self.lurker_path.get() or
            not self.chaos_recipe_path.get()
        )
        
        if need_detection:
            print("Running auto-detection on startup...")
            # Run detection in thread to avoid blocking UI startup
            thread = threading.Thread(target=self.auto_detect_installations)
            thread.daemon = True
            thread.start()
        else:
            print("Skipping auto-detection: all paths already configured")
    
    def save_settings(self):
        """Save settings to config file"""
        try:
            config = {
                'game_version': self.game_version.get(),
                'steam_path': self.steam_path.get(),
                'standalone_path': self.standalone_path.get(),
                'awakened_path': self.awakened_path.get(),
                'lurker_path': self.lurker_path.get(),
                'chaos_recipe_path': self.chaos_recipe_path.get(),
                'start_awakened': self.start_awakened.get(),
                'start_lurker': self.start_lurker.get(),
                'start_chaos_recipe': self.start_chaos_recipe.get(),
                'open_filterblade': self.open_filterblade.get(),
                'open_trade_site': self.open_trade_site.get(),
                'language': self.language.get(),
                'steam_poe_path': getattr(self, 'steam_poe_path', '')
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"Settings saved to: {self.config_file}")
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def is_process_running(self, process_name):
        """Check if a process is running"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                    return True
        except:
            pass
        return False
    
    def run_program(self, path):
        """Run a program and return success status"""
        try:
            if os.path.exists(path):
                # Set working directory to the program's directory to avoid path issues
                program_dir = os.path.dirname(path)
                subprocess.Popen([path], cwd=program_dir, shell=True)
                return True
        except Exception as e:
            print(f"Error running {path}: {e}")
        return False
    
    def launch_steam_game(self, steam_path, app_id):
        """Launch Steam game with specific app ID"""
        try:
            # Use Steam URL protocol to avoid security warnings
            steam_url = f"steam://rungameid/{app_id}"
            webbrowser.open(steam_url)
            return True
        except Exception as e:
            print(f"Error launching Steam game: {e}")
            # Fallback to old method if URL protocol fails
            try:
                subprocess.Popen([steam_path, f"-applaunch", app_id], shell=True)
                return True
            except:
                return False
    
    def show_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update()
    
    def launch_threaded(self):
        """Launch in separate thread to avoid blocking UI"""
        self.launch_button.config(state='disabled')
        thread = threading.Thread(target=self.launch)
        thread.daemon = True
        thread.start()
    
    def launch(self):
        """Launch all selected programs and websites"""
        self.save_settings()
        self.show_status(self.t('launching'))
        
        errors = []
        launched = []
        
        # Launch the game
        version = self.game_version.get()
        
        if version == 'steam':
            steam_path = self.steam_path.get()
            
            # Check if we have a detected Steam PoE executable
            if hasattr(self, 'steam_poe_path') and self.steam_poe_path and os.path.exists(self.steam_poe_path):
                # Launch PoE directly from Steam library
                if self.run_program(self.steam_poe_path):
                    launched.append("Path of Exile (Steam)")
                else:
                    errors.append(self.t('file_not_found').format("Path of Exile", self.steam_poe_path))
            elif steam_path and os.path.exists(steam_path):
                # Fallback to Steam URL protocol launch
                # Check if Steam is running
                if not self.is_process_running("steam.exe"):
                    self.run_program(steam_path)
                    self.show_status(self.t('steam_starting'))
                    time.sleep(5)  # Wait for Steam to start
                
                if self.launch_steam_game(steam_path, "238960"):
                    launched.append("Path of Exile (Steam)")
            else:
                errors.append(self.t('file_not_found').format("Steam", steam_path))
        else:
            standalone_path = self.standalone_path.get()
            if self.run_program(standalone_path):
                launched.append("Path of Exile (Standalone)")
            else:
                errors.append(self.t('file_not_found').format("Path of Exile", standalone_path))
        
        time.sleep(1)  # Small delay between launches
        
        # Launch companion programs
        if self.start_awakened.get():
            awakened_path = self.awakened_path.get()
            if not self.is_process_running("Awakened PoE Trade.exe"):
                if self.run_program(awakened_path):
                    launched.append("Awakened PoE Trade")
                else:
                    errors.append(self.t('file_not_found').format("Awakened PoE Trade", awakened_path))
        
        if self.start_lurker.get():
            lurker_path = self.lurker_path.get()
            if not self.is_process_running("Poe Lurker.exe"):
                if self.run_program(lurker_path):
                    launched.append("PoE Lurker")
                else:
                    errors.append(self.t('file_not_found').format("PoE Lurker", lurker_path))
        
        if self.start_chaos_recipe.get():
            chaos_path = self.chaos_recipe_path.get()
            if not self.is_process_running("ChaosRecipeEnhancer.exe"):
                if self.run_program(chaos_path):
                    launched.append("Chaos Recipe Enhancer")
                else:
                    errors.append(self.t('file_not_found').format("Chaos Recipe Enhancer", chaos_path))
        
        # Open websites
        if self.open_filterblade.get():
            webbrowser.open("https://www.filterblade.xyz")
            launched.append("FilterBlade")
        
        if self.open_trade_site.get():
            webbrowser.open("https://www.pathofexile.com/trade")
            launched.append("Trade Site")
        
        # Show results
        if errors:
            error_msg = self.t('errors_occurred').format(", ".join(errors))
            self.show_status(error_msg)
            if launched:
                time.sleep(3)
                success_msg = self.t('launched_successfully').format(", ".join(launched))
                self.show_status(success_msg + self.t('closing_in').format(3))
                time.sleep(3)
                self.root.quit()
        elif launched:
            success_msg = self.t('launched_successfully').format(", ".join(launched))
            self.show_status(success_msg)
            time.sleep(2)
            self.root.quit()
        
        self.launch_button.config(state='normal')
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PoELauncher()
    app.run()