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


class Contact:
    table = 'CONTACT'
    contact_id = 'contact_id'
    fname = 'fname'
    lname = 'lname'
    mname = 'mname'
    columns = (contact_id, fname, mname, lname)

    @staticmethod
    def create_table_query():
        return """CREATE TABLE IF NOT EXISTS CONTACT (
                                    contact_id int primary key, 
                                    fname text not null, 
                                    mname text, 
                                    lname not null);"""

class Address:
    table = 'ADDRESS'
    address_id = 'address_id'
    contact_id = 'contact_id'
    address_type = 'address_type'
    address = 'address'
    city = 'city'
    state = 'state'
    zip = 'zip'

    @staticmethod
    def create_table_query():
        return """CREATE TABLE IF NOT EXISTS ADDRESS (
                                           address_id int primary key, 
                                           contact_id int, 
                                           address_type text, 
                                           address text, 
                                           city text,
                                           state text,
                                           zip int,
                                           FOREIGN KEY (contact_id),
                                           REFERENCES CONTACT(contact_id));"""
