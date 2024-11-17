import logging
import time

from google_auth_oauthlib.flow import InstalledAppFlow
from selenium.common.exceptions import (ElementNotInteractableException,
    NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from webutils.browser import get_driver


logger = logging.getLogger(__name__)


class Autoauth:
    def __init__(self, client_secrets_file, scopes, **browser_args):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.headless = browser_args.get('headless', True)
        self.driver = get_driver(**browser_args)

    def _wait_for_element(self, element):
        wait = WebDriverWait(self.driver, timeout=5, poll_frequency=.2,
            ignored_exceptions=[ElementNotInteractableException,
                NoSuchElementException])
        wait.until(lambda x: element.is_displayed())

    def _click_if_exists(self, xpath, timeout=2, poll_frequency=.2):
        end_ts = time.time() + timeout
        while time.time() < end_ts:
            try:
                self.driver.find_element(By.XPATH, xpath).click()
                logger.info(f'clicked: {xpath}')
                return True
            except NoSuchElementException:
                time.sleep(poll_frequency)
        logger.info(f'not found: {xpath}')
        return False

    def _requires_manual_auth(self):
        try:
            self.driver.find_element(By.XPATH, '//input[@type="email"]')
            return True
        except NoSuchElementException:
            return False

    def _fetch_code(self, auth_url):
        self.driver.get(auth_url)
        if self._requires_manual_auth():
            if self.headless:
                raise Exception('requires manual auth')
            if not self._click_if_exists('//span[contains(text(), "Continue")]',
                    timeout=120, poll_frequency=2):
                raise Exception('login timeout')
        else:
            if not self._click_if_exists('//div[@data-authuser="0"]'):
                self._click_if_exists('//button[@id="choose-account-0"]')
            self._click_if_exists('//button[@id="submit_approve_access"]')
            self._click_if_exists('//span[contains(text(), "Continue")]')

        if self._click_if_exists(
                '//input[@type="checkbox" and @aria-label="Select all"]'):
            self._click_if_exists('//button[contains(., "Continue")]')
        self._click_if_exists('//button[@id="submit_approve_access"]')
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
