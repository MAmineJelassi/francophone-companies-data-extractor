import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class LinkedInNavigator:
    def __init__(self, config):
        self.config = config
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        options.add_argument(f"--user-data-dir={self.config.CHROME_PROFILE_PATH}")
        options.add_argument(f"--profile-directory={self.config.CHROME_PROFILE_DIRECTORY}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
        driver.implicitly_wait(self.config.IMPLICIT_WAIT)
        return driver

    def search_and_extract(self, company_name):
        """Navigate to LinkedIn Sales Navigator and extract contacts for a company."""
        encoded_name = quote(company_name)
        self.driver.get(
            f"https://www.linkedin.com/sales/search/people?query=(filters:List((type:CURRENT_COMPANY,values:List((text:{encoded_name})))))"
        )
        time.sleep(self.config.EXTRACTION_DELAY)
        # Placeholder: add XPath/CSS selector logic here to parse contact cards
        contacts = []
        return contacts

    def close(self):
        if self.driver:
            self.driver.quit()