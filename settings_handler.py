# settings_handler.py
import json
import os

class SettingsHandler:
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = {
            "program_path": "",
            "execution_count": "1",
            "window_title": "",
            "window_width": "480",
            "window_height": "344",
            "remove_title": False,
            "remove_border": False,
            "bypass_limit": False
        }
        
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self.default_settings.copy()
        except Exception as e:
            print(f"載入設定時發生錯誤: {e}")
            return self.default_settings.copy()
            
    def save_settings(self, settings):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"儲存設定時發生錯誤: {e}")
            return False