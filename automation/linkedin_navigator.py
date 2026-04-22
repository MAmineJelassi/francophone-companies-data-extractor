import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

SALES_NAV_BASE = 'https://www.linkedin.com/sales'
SEARCH_URL = (
    SALES_NAV_BASE
    + '/search/people?query=(filters:List((type:CURRENT_COMPANY,values:List((text:{company},'
    'selectionType:INCLUDED)))))'
)


class LinkedInNavigator:
    """
    Automates LinkedIn Sales Navigator using an existing Chrome profile.

    The browser must already be logged in to LinkedIn – no credentials are
    stored or used by this class.
    """

    def __init__(self, config):
        self.config = config
        self.driver = None
        self.wait = None

    # ------------------------------------------------------------------ #
    #  Driver lifecycle                                                    #
    # ------------------------------------------------------------------ #

    def _build_chrome_options(self) -> Options:
        opts = Options()
        opts.add_argument(f'--user-data-dir={self.config.chrome_profile_path}')
        opts.add_argument(f'--profile-directory={self.config.CHROME_PROFILE_DIR}')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_experimental_option('excludeSwitches', ['enable-automation'])
        opts.add_experimental_option('useAutomationExtension', False)
        w = self.config.BROWSER_SETTINGS
        opts.add_argument(
            f'--window-size={w["window_width"]},{w["window_height"]}'
        )
        if w.get('headless'):
            opts.add_argument('--headless=new')
        return opts

    def start(self) -> None:
        """Launch Chrome with the existing user profile."""
        if self.driver is not None:
            return
        try:
            opts = self._build_chrome_options()
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=opts)
            self.driver.execute_cdp_cmd(
                'Page.addScriptToEvaluateOnNewDocument',
                {
                    'source': (
                        'Object.defineProperty(navigator, "webdriver", '
                        '{get: () => undefined})'
                    )
                },
            )
            timeout = self.config.BROWSER_SETTINGS.get('page_load_timeout', 30)
            self.driver.set_page_load_timeout(timeout)
            self.wait = WebDriverWait(self.driver, timeout)
            logger.info('Chrome launched with existing profile.')
        except WebDriverException as exc:
            logger.error('Failed to start Chrome: %s', exc)
            raise

    def close(self) -> None:
        """Quit the browser if it is running."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info('Chrome closed.')
            except WebDriverException:
                pass
            finally:
                self.driver = None
                self.wait = None

    # ------------------------------------------------------------------ #
    #  Navigation helpers                                                  #
    # ------------------------------------------------------------------ #

    def _navigate_to_sales_nav(self) -> bool:
        """Open Sales Navigator home and verify the session is active."""
        try:
            self.driver.get(SALES_NAV_BASE + '/home')
            time.sleep(3)
            if 'linkedin.com/login' in self.driver.current_url:
                logger.error(
                    'Chrome profile is not logged in to LinkedIn. '
                    'Please log in manually and retry.'
                )
                return False
            logger.info('Sales Navigator loaded successfully.')
            return True
        except TimeoutException:
            logger.warning('Timed out loading Sales Navigator home.')
            return False

    def _search_company(self, company_name: str) -> None:
        """Navigate to the people search filtered by company name."""
        encoded = company_name.replace(' ', '%20').replace("'", '%27')
        url = SEARCH_URL.format(company=encoded)
        self.driver.get(url)
        time.sleep(3)

    # ------------------------------------------------------------------ #
    #  Extraction                                                          #
    # ------------------------------------------------------------------ #

    def _extract_contacts_from_page(self, company_name: str) -> list:
        """
        Extract contact cards visible on the current search-results page.

        NOTE: The XPath selectors below are illustrative placeholders.
        Adjust them to match the current Sales Navigator DOM structure.
        """
        contacts = []
        try:
            # Wait for at least one result card to appear
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//li[contains(@class,"result-lockup")]')
                )
            )
        except TimeoutException:
            logger.debug('No result cards found for "%s".', company_name)
            return contacts

        cards = self.driver.find_elements(
            By.XPATH, '//li[contains(@class,"result-lockup")]'
        )
        for card in cards:
            try:
                name = self._safe_text(
                    card, './/span[contains(@class,"result-lockup__name")]'
                )
                role = self._safe_text(
                    card, './/span[contains(@class,"result-lockup__highlight-keyword")]'
                )
                profile_url = self._safe_attr(
                    card,
                    './/a[contains(@href,"/sales/lead/")]',
                    'href',
                )
                contacts.append(
                    {
                        'name': name,
                        'role': role,
                        'email': 'N/A',   # requires profile page visit
                        'phone': 'N/A',   # requires profile page visit
                        'linkedin_url': profile_url,
                    }
                )
            except Exception as exc:
                logger.debug('Error parsing card: %s', exc)

        return contacts

    @staticmethod
    def _safe_text(parent, xpath: str) -> str:
        try:
            return parent.find_element(By.XPATH, xpath).text.strip()
        except NoSuchElementException:
            return 'N/A'

    @staticmethod
    def _safe_attr(parent, xpath: str, attr: str) -> str:
        try:
            return parent.find_element(By.XPATH, xpath).get_attribute(attr) or 'N/A'
        except NoSuchElementException:
            return 'N/A'

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def search_and_extract(self, company_name: str) -> list:
        """
        Search for a company on Sales Navigator and return its contacts.

        Parameters
        ----------
        company_name : str
            The company to search for.

        Returns
        -------
        list of dict
            Contacts found (may be empty if none matched or page changed).
        """
        if self.driver is None:
            self.start()
            if not self._navigate_to_sales_nav():
                return []

        logger.info('Searching contacts for "%s".', company_name)
        self._search_company(company_name)
        contacts = self._extract_contacts_from_page(company_name)
        logger.info('Found %d contact(s) for "%s".', len(contacts), company_name)
        return contacts