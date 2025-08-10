from contextlib import contextmanager
from glob import glob
import json
import logging
import os
import time

from playwright.sync_api import sync_playwright


DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                     "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
PAGE_FILE_PREFIX = 'browser_page'

logger = logging.getLogger(__name__)


class State:
    def __init__(self, file):
        self.file = file

    def load(self):
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def save(self, state):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(state))


@contextmanager
def playwright_context(state: State, headless=True, user_agent=DEFAULT_USER_AGENT,
                       locale='en-US', timezone='America/New_York', stealth=True):
    with sync_playwright() as p:
        context = None
        try:
            browser = p.chromium.launch(headless=headless,
                                        args=[
                                            '--disable-blink-features=AutomationControlled',
                                        ])
            context = browser.new_context(storage_state=state.load(),
                                          viewport={'width': 1920, 'height': 1080},
                                          user_agent=user_agent,
                                          locale=locale,
                                          timezone_id=timezone)
            if stealth:
                context.add_init_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined});""")
                context.add_init_script("""window.chrome = { runtime: {} };""")
                context.add_init_script("""Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});""")
                context.add_init_script("""Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});""")
            yield context
        finally:
            if context:
                state.save(context.storage_state())
                context.close()


def save_page(page, save_dir, name, save_content=True, save_screenshot=True,
              purge_delta=3600 * 24 * 30):
    os.makedirs(save_dir, exist_ok=True)
    list(map(os.remove, [f for f in glob(os.path.join(save_dir, f'{PAGE_FILE_PREFIX}-*'))
                         if os.stat(f).st_mtime < time.time() - purge_delta]))
    basename = f'{PAGE_FILE_PREFIX}-{int(time.time())}-{name}'
    if save_content:
        content_file = os.path.join(save_dir, f'{basename}.html')
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(page.content())
        logger.warning(f'saved page content to {content_file}')
    if save_screenshot:
        screenshot_file = os.path.join(save_dir, f'{basename}.png')
        page.screenshot(path=screenshot_file)
        logger.warning(f'saved page screenshot to {screenshot_file}')
