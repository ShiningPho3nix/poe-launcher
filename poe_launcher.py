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
        
    def setup_window(self):
        self.root.title("Path of Exile Launcher")
        self.root.geometry("600x750")
        self.root.resizable(True, True)
        self.root.minsize(500, 600)
        
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
    
    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text=self.t('title'), 
                              font=('Segoe UI', 20, 'bold'),
                              fg=self.colors['accent'], bg=self.colors['bg'])
        title_label.pack(pady=(0, 20))
        
        # Language selection
        lang_frame = self.create_section_frame(main_frame)
        lang_title = tk.Label(lang_frame, text=self.t('language'),
                             font=('Segoe UI', 12, 'bold'),
                             fg=self.colors['secondary'], bg=self.colors['bg_light'])
        lang_title.pack(anchor='w', pady=(0, 10))
        
        lang_combo_frame = tk.Frame(lang_frame, bg=self.colors['bg_light'])
        lang_combo_frame.pack(fill='x')
        
        self.lang_combo = ttk.Combobox(lang_combo_frame, textvariable=self.language,
                                      values=['en', 'de'], state='readonly', width=10)
        self.lang_combo.pack(side='left')
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Game Version Section
        game_frame = self.create_section_frame(main_frame)
        self.create_section_title(game_frame, 'game_version')
        
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
        
        # Steam path
        self.steam_path_frame = self.create_path_input(game_frame, 'steam_path', self.steam_path, self.browse_steam_path)
        
        # Standalone path
        self.standalone_path_frame = self.create_path_input(game_frame, 'game_path', self.standalone_path, self.browse_standalone_path)
        
        # Companion Programs Section
        companion_frame = self.create_section_frame(main_frame)
        self.create_section_title(companion_frame, 'companion_programs')
        
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
        self.create_section_title(websites_frame, 'websites')
        
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
        # Note: In a full implementation, you'd update all text elements here
        # For now, restart is recommended for complete language change
    
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
                'language': self.language.get()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
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
            if not os.path.exists(steam_path):
                errors.append(self.t('file_not_found').format("Steam", steam_path))
            else:
                # Check if Steam is running
                if not self.is_process_running("steam.exe"):
                    self.run_program(steam_path)
                    self.show_status(self.t('steam_starting'))
                    time.sleep(5)  # Wait for Steam to start
                
                if self.launch_steam_game(steam_path, "238960"):
                    launched.append("Path of Exile (Steam)")
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