"""
Configuration management for Python Commander
Handles default settings and user-specific configurations
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

class ConfigManager:
    def __init__(self):
        self.app_name = "Python Commander"
        self.config_filename = "config.json"
        
        # Default configuration
        self.defaults = {
            "version": "0.1.0",
            "settings": {
                "dark_mode": False,
                "auto_refresh": True,
                "refresh_interval": 5,  # seconds
                "show_hidden_files": False,
                "default_script_template": "script-template.py"
            },
            "monitored_paths": [
                str(Path.home() / "Documents" / "Python Scripts"),
                str(Path.home() / "Desktop"),
            ],
            "recent_scripts": [],
            "favorites": []
        }
        
        # Initialize paths
        self._setup_paths()
        
        # Load configuration
        self.config = self._load_config()
    
    def _setup_paths(self):
        """Set up configuration file paths for macOS app bundle"""
        if getattr(sys, 'frozen', False):
            # Running as packaged app
            bundle_dir = Path(sys.executable).parent.parent.parent
            self.bundle_resources = bundle_dir / "Resources"
            self.default_config_path = self.bundle_resources / "default_config.json"
        else:
            # Running in development
            app_dir = Path(__file__).parent.parent
            self.bundle_resources = app_dir / "resources"
            self.default_config_path = self.bundle_resources / "default_config.json"
        
        # User configuration in Application Support
        app_support = Path.home() / "Library" / "Application Support" / self.app_name
        app_support.mkdir(parents=True, exist_ok=True)
        self.user_config_path = app_support / self.config_filename
        
        print(f"Config paths:")
        print(f"  Default config: {self.default_config_path}")
        print(f"  User config: {self.user_config_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with fallbacks"""
        config = self.defaults.copy()
        
        # Try to load default config from app bundle
        if self.default_config_path.exists():
            try:
                with open(self.default_config_path, 'r') as f:
                    bundle_config = json.load(f)
                    config.update(bundle_config)
                print(f"Loaded default config from: {self.default_config_path}")
            except Exception as e:
                print(f"Error loading default config: {e}")
        
        # Load user config (overrides defaults)
        if self.user_config_path.exists():
            try:
                with open(self.user_config_path, 'r') as f:
                    user_config = json.load(f)
                    config.update(user_config)
                print(f"Loaded user config from: {self.user_config_path}")
            except Exception as e:
                print(f"Error loading user config: {e}")
        else:
            # Create initial user config
            self._save_user_config(config)
            print(f"Created initial user config at: {self.user_config_path}")
        
        return config
    
    def _save_user_config(self, config: Dict[str, Any] = None):
        """Save user configuration"""
        if config is None:
            config = self.config
        
        try:
            with open(self.user_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"Saved user config to: {self.user_config_path}")
        except Exception as e:
            print(f"Error saving user config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value with dot notation support"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value with dot notation support"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the final value
        config[keys[-1]] = value
        
        # Save to user config
        self._save_user_config()
    
    def add_monitored_path(self, path: str):
        """Add a path to monitor for Python scripts"""
        paths = self.config.get("monitored_paths", [])
        if path not in paths:
            paths.append(path)
            self.set("monitored_paths", paths)
    
    def remove_monitored_path(self, path: str):
        """Remove a monitored path"""
        paths = self.config.get("monitored_paths", [])
        if path in paths:
            paths.remove(path)
            self.set("monitored_paths", paths)
    
    def get_monitored_paths(self) -> List[str]:
        """Get list of monitored paths"""
        return self.config.get("monitored_paths", [])
    
    def add_recent_script(self, script_path: str):
        """Add script to recent scripts list"""
        recent = self.config.get("recent_scripts", [])
        
        # Remove if already exists
        if script_path in recent:
            recent.remove(script_path)
        
        # Add to beginning
        recent.insert(0, script_path)
        
        # Keep only last 10
        recent = recent[:10]
        
        self.set("recent_scripts", recent)
    
    def get_recent_scripts(self) -> List[str]:
        """Get recent scripts list"""
        return self.config.get("recent_scripts", [])
    
    def toggle_dark_mode(self):
        """Toggle dark mode setting"""
        current = self.get("settings.dark_mode", False)
        self.set("settings.dark_mode", not current)
        return not current
    
    def is_dark_mode(self) -> bool:
        """Check if dark mode is enabled"""
        return self.get("settings.dark_mode", False)

# Global config instance
config = ConfigManager() 