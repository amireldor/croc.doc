import os

if os.environ.get('DEBUG') == '1':
    DEBUG = True
else:
    DEBUG = False

MAX_DOC_SIZE = 4096
PROTECTION_TIME = 60 * 60 * 24  # one day
SAVE_RETRIES = 100  # if we hit a protected doc, attempt a differnet name
