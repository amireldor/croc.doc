import os

if os.environ.get('DEBUG') == '1':
    DEBUG = True
else:
    DEBUG = False

# Server listening settings
HOST = '0.0.0.0'
PORT = 4444

MAX_DOC_SIZE = 4096
SECONDS_TO_EXPIRE = 60 * 60 * 24  # One day
SAVE_RETRIES = 100  # if we hit a protected doc, attempt a differnet name

BASE_URL = 'http://croc.farm/'

