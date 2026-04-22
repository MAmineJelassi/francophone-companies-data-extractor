# LinkedIn Automation Configuration

# Path to Chrome profile
CHROME_PROFILE_PATH = '/path/to/chrome/profile'

# Target Roles in English and French
TARGET_ROLES = {
    'en': ['Sales Director', 'Commercial Director', 'General Director', 'IT Director'],
    'fr': ['Directeur des Ventes', 'Directeur Commercial', 'Directeur Général', 'Directeur IT']
}

# Browser Settings
BROWSER_SETTINGS = {
    'headless': False,
    'window_size': '1920x1080',
    'timeout': 30
}

# File Paths
FILE_PATHS = {
    'data_export': 'path/to/data_export.csv',
    'error_log': 'path/to/error_log.txt'
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'DEBUG',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'handlers': ['console', 'file'],
    'file_handler': {
        'filename': 'path/to/logfile.log',
        'maxBytes': 10485760,  # 10 MB
        'backupCount': 5
    }
}