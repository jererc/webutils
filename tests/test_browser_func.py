from glob import glob
import os
from pprint import pprint
import shutil
import unittest

from tests import WORK_DIR
from webutils import browser as module


class ContextTestCase(unittest.TestCase):
    def setUp(self):
        self.state_file = os.path.join(WORK_DIR, 'state.json')
        self.save_dir = os.path.join(WORK_DIR, 'save')
        shutil.rmtree(self.save_dir, ignore_errors=True)
        os.makedirs(self.save_dir, exist_ok=True)

    def test_1(self):
        with module.playwright_context(self.state_file, headless=False) as context:
            page = context.new_page()
            page.goto('https://www.google.com')
            module.save_page(page, self.save_dir, 'test', save_content=True, save_screenshot=True)
        self.assertTrue(os.path.exists(self.state_file))
        save_files = glob(os.path.join(self.save_dir, f'{module.SAVE_PAGE_PREFIX}-*'))
        pprint(save_files)
        self.assertEqual(len(save_files), 2)
