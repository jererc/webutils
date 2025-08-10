import logging
import os

WORK_DIR = os.path.expanduser('~/tmp/tests/webutils')
os.makedirs(WORK_DIR, exist_ok=True)
logging.getLogger('').handlers.clear()
