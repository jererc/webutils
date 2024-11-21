import logging
import os
import subprocess
import time

from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
    NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


CONFIGS = {
    'nt': {
        'brave': {
            'binary': r'C:\Program Files\BraveSoftware'
                r'\Brave-Browser\Application\brave.exe',
            'data_dir': os.path.expanduser(
                r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data'),
        },
        'chrome': {
            'binary': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'data_dir': os.path.expanduser(
                r'~\AppData\Local\Google\Chrome\User Data'),
        },
    },
    'posix': {
        'brave': {
            'binary': '/opt/brave.com/brave/brave',
            'data_dir': os.path.expanduser(
                '~/.config/BraveSoftware/Brave-Browser'),
        },
        'chrome': {
            'binary': '/opt/google/chrome/chrome',
            'data_dir': os.path.expanduser('~/.config/google-chrome'),
        },
    },
}[os.name]
KILL_CMD = {
    'nt': 'taskkill /IM {binary}',
    'posix': 'pkill {binary}',
}[os.name]
BROWSER_ID = 'chrome'
PROFILE_DIR = 'selenium'

logger = logging.getLogger(__name__)


class Browser:
    def __init__(self, browser_id=BROWSER_ID, profile_dir=PROFILE_DIR,
                 headless=False, page_load_strategy=None, implicitly_wait=1):
        self.profile_dir = profile_dir
        self.headless = headless
        self.page_load_strategy = page_load_strategy
        self.implicitly_wait = implicitly_wait
        config = self._get_config(browser_id)
        self.data_dir = config['data_dir']
        self.binary = config['binary']

    def _get_config(self, browser_id):
        if browser_id:
            try:
                return CONFIGS[browser_id]
            except KeyError:
                raise Exception(f'unsupported browser_id {browser_id}')
        for config in CONFIGS.values():
            if all(os.path.exists(p) for p in config.values()):
                return config
        raise Exception('no available browser')

    def _kill_running_browser(self):
        subprocess.call(KILL_CMD.format(
            binary=os.path.basename(self.binary)), shell=True)

    def get_driver(self):
        self._kill_running_browser()
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        if self.page_load_strategy:
            options.page_load_strategy = self.page_load_strategy
        options.add_argument(f'--user-data-dir={self.data_dir}')
        options.add_argument(f'--profile-directory={self.profile_dir}')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches',
            ['enable-automation'])
        options.add_experimental_option('detach', True)
        options.binary_location = self.binary
        driver = webdriver.Chrome(options=options)
        if self.implicitly_wait:
            driver.implicitly_wait(self.implicitly_wait)
        return driver


class DriverHelper:
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

    def _debug_driver(self, xpaths):
        for xpath in xpaths:
            els = self.driver.find_elements(By.XPATH, xpath)
            print(f'{xpath} elements: {len(els)}')
            for i, el in enumerate(els):
                print(f'element {i}:\n{el.get_attribute("outerHTML")}')

        file = os.path.join(os.path.expanduser('~'),
            '_selenium_screenshot.png')
        self.driver.save_screenshot(file)
        print(f'saved screenshot {file}')


def get_driver(*args, **kwargs):
    return Browser(*args, **kwargs).get_driver()
