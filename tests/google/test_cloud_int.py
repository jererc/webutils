import os
from pprint import pprint
import tempfile
import unittest

from webutils.google.cloud import get_google_cloud


SECRETS_FILE = os.path.expanduser('~/gcs.json')


def makedirs(x):
    if not os.path.exists(x):
        os.makedirs(x)


class GoogleTestCase(unittest.TestCase):
    def setUp(self):
        self.gc = get_google_cloud(SECRETS_FILE)

    def test_drive(self):
        res = list(self.gc.iterate_file_meta())
        self.assertTrue(res)
        self.assertTrue(all(r['id'] and r['name'] for r in res))
        exportable = [r for r in res if r['exportable']]
        self.assertTrue(exportable)
        with tempfile.TemporaryDirectory() as temp_dir:
            for file_meta in exportable:
                pprint(file_meta)
                file = os.path.join(temp_dir, file_meta['path'])
                print(file)
                makedirs(os.path.dirname(file))
                self.gc.export_file(file_id=file_meta['id'],
                    path=file, mime_type=file_meta['mime_type'])
