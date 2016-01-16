import os

if os.environ.get('DEBUG') == '1':
    DEBUG = True
else:
    DEBUG = False

MAX_DOC_SIZE = 4096
