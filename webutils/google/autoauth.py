import logging

from google_auth_oauthlib.flow import InstalledAppFlow
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from webutils.browser import DriverHelper, get_driver


logger = logging.getLogger(__name__)


class Autoauth(DriverHelper):
    def __init__(self, client_secrets_file, scopes, **browser_args):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.headless = browser_args.get('headless', True)
        self.driver = get_driver(**browser_args)

    def _requires_manual_auth(self):
        try:
            return bool(self.driver.find_element(By.XPATH,
                '//input[@type="email"]'))
        except NoSuchElementException:
            return False

    def _fetch_code(self, auth_url):
        self.driver.get(auth_url)
        if self._requires_manual_auth():
            if self.headless:
                raise Exception('requires manual login')
            logger.info('waiting for manual login...')
            if not self._click_if_exists(
                    '//span[contains(text(), "Continue")]',
                    timeout=120, poll_frequency=2):
                raise Exception('login timeout')
        else:
            if self._click_if_exists('//button[@id="choose-account-0"]'):
                self._click_if_exists(
                    '//button[@id="submit_approve_access" and not(@disabled)]')
            else:
                self._click_if_exists('//div[@data-authuser="0"]')
                self._click_if_exists('//span[contains(text(), "Continue")]')

        if self._click_if_exists(
                '//input[@type="checkbox" and @aria-label="Select all"]'):
            self._click_if_exists('//button[contains(., "Continue")]')

        el_textarea = self.driver.find_element(By.XPATH, '//textarea')
        self._wait_for_element(el_textarea)
        return el_textarea.get_attribute('innerHTML')

    def acquire_credentials(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file=self.client_secrets_file,
            scopes=self.scopes,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob',
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        logger.debug(f'auth url: {auth_url}')
        try:
            code = self._fetch_code(auth_url)
        finally:
            self.driver.quit()
        flow.fetch_token(code=code)
        return flow.credentials
