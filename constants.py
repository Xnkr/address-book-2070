import logging
import os
from os.path import join as opj
from logging.handlers import RotatingFileHandler

APP_NAME = 'Contact List 2070'
DB_FILE = 'contacts.sqlite'


def relative_path(x):
    return opj(os.getcwd(), x)


LOG_DIR = relative_path('logs')
LOG_FILE = opj(LOG_DIR, 'contact_list.log')

logger = logging.getLogger(APP_NAME)
if not logger.handlers:
    logger.setLevel(logging.INFO)
    logger.propagate = False
    os.makedirs(LOG_DIR, exist_ok=True)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=200000, backupCount=5)
    f_format = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    handler.setFormatter(f_format)
    logger.addHandler(handler)


class StandardResponses:
    SUCCESS_NO_RESPONSE = 204
    CREATED = 201
    SUCCESS_CODE = 200
    BAD_REQUEST_CODE = 400
    INVALID_CSV = {'Error': 'Invalid CSV'}
    NOT_FOUND_CODE = 404
    SERVER_ERROR_CODE = 500
    SERVER_ERROR = {'Error': 'Server Error occurred'}
