import os
from pprint import pprint
import shutil
import unittest

from webutils.google.cloud import get_google_cloud


WORK_PATH = os.path.join(os.path.expanduser('~'), '_tests', 'webutils')
SECRETS_FILE = os.path.join(os.path.expanduser('~'), 'gcs.json')


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


class GoogleTestCase(unittest.TestCase):
    def setUp(self):
        self.gc = get_google_cloud(SECRETS_FILE)

    def test_drive(self):
        res = list(self.gc.iterate_file_meta())
        self.assertTrue(res)
        self.assertTrue(all(r['id'] and r['name'] for r in res))
        exportable = [r for r in res if r['exportable']]
        self.assertTrue(exportable)
        for file_meta in exportable:
            pprint(file_meta)
            file = os.path.join(WORK_PATH, file_meta['path'])
            print(file)
            makedirs(os.path.dirname(file))
            self.gc.export_file(file_id=file_meta['id'],
                path=file, mime_type=file_meta['mime_type'])
