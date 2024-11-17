import json
import logging
import os
import shutil
import unittest

from webutils import browser
from webutils.google import autoauth as module
from webutils.google.cloud import SCOPES


WORK_PATH = os.path.join(os.path.expanduser('~'), '_test_webutils')
SECRETS_FILE = os.path.join(os.path.expanduser('~'), 'gcs.json')

browser.logger.setLevel(logging.DEBUG)
module.logger.setLevel(logging.DEBUG)


def remove_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def makedirs(x):
    if not os.path.exists(x):
        os.makedirs(x)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        remove_path(WORK_PATH)
        makedirs(WORK_PATH)
        self.secrets_file = os.path.join(WORK_PATH, 'secrets.json')
        shutil.copyfile(SECRETS_FILE, self.secrets_file)


class AutoauthTestCase(BaseTestCase):
    def _check_output(self, output):
        self.assertTrue(output)
        creds_json = output.to_json()
        print(creds_json)
        creds_dict = json.loads(creds_json)
        self.assertTrue(creds_dict.get('token'))

    def test_no_headless(self):
        ao = module.Autoauth(self.secrets_file,
            scopes=SCOPES,
            browser_id='chrome',
            headless=False,
        )
        res = ao.acquire_credentials()
        self._check_output(res)

    def test_headless(self):
        ao = module.Autoauth(self.secrets_file,
            scopes=SCOPES,
            browser_id='chrome',
            headless=True,
        )
        res = ao.acquire_credentials()
        self._check_output(res)
