import os

class Config:
    # Chrome profile settings (uses existing logged-in session)
    # Update CHROME_PROFILE_PATH to match your system before running:
    #   Windows: C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data
    #   Mac:     /Users/YOUR_USERNAME/Library/Application Support/Google/Chrome
    #   Linux:   /home/YOUR_USERNAME/.config/google-chrome
    CHROME_PROFILE_PATH = os.environ.get(
        'CHROME_PROFILE_PATH',
        r'C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data'
    )
    CHROME_PROFILE_DIRECTORY = 'Default'

    # Target roles to extract (English and French)
    TARGET_ROLES = [
        'CEO', 'Chief Executive Officer',
        'CFO', 'Chief Financial Officer',
        'COO', 'Chief Operating Officer',
        'Directeur Général', 'Directeur Financier',
        'Directeur des Opérations', 'PDG',
    ]

    # Browser settings
    PAGE_LOAD_TIMEOUT = 30
    IMPLICIT_WAIT = 10
    EXTRACTION_DELAY = 2

    # File paths
    INPUT_FILE = 'input_companies.xlsx'
    OUTPUT_DIR = '.'

    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'automation.log'
