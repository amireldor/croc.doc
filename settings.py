import os

if os.environ.get('CROC_FARM_DEV') == '1':
    DEBUG = True
else:
    DEBUG = False

MAX_DOC_SIZE = 4096
