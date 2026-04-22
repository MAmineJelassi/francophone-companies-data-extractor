import os
import platform

class Config:
    """Configuration for LinkedIn Sales Navigator Automation."""

    # --- Chrome Profile Paths (per OS) ---
    CHROME_PROFILE_PATHS = {
        'Windows': os.path.join(
            os.environ.get('LOCALAPPDATA', r'C:\Users\Default\AppData\Local'),
            'Google', 'Chrome', 'User Data'
        ),
        'Darwin': os.path.expanduser(
            '~/Library/Application Support/Google/Chrome'
        ),
        'Linux': os.path.expanduser('~/.config/google-chrome'),
    }

    # Profile directory inside the User Data folder (e.g. "Default", "Profile 1")
    CHROME_PROFILE_DIR = 'Default'

    # --- Target Roles ---
    TARGET_ROLES = {
        'en': [
            'Sales Director',
            'Commercial Director',
            'General Director',
            'IT Director',
        ],
        'fr': [
            'Directeur des Ventes',
            'Directeur Commercial',
            'Directeur Général',
            'Directeur IT',
        ],
    }

    # --- Browser Settings ---
    BROWSER_SETTINGS = {
        'headless': False,
        'window_width': 1920,
        'window_height': 1080,
        'page_load_timeout': 30,
        'implicit_wait': 10,
    }

    # --- File Paths ---
    FILE_PATHS = {
        'input': 'input_companies.xlsx',
        'output': 'output_results.xlsx',
        'log': 'automation.log',
    }

    def __init__(self):
        self.system = platform.system()
        self.chrome_profile_path = self.CHROME_PROFILE_PATHS.get(
            self.system, self.CHROME_PROFILE_PATHS['Linux']
        )

    @property
    def all_target_roles(self):
        """Return a flat list of all target role keywords."""
        return self.TARGET_ROLES['en'] + self.TARGET_ROLES['fr']