import csv
from db_manager import DBManager
from models import *


def get_contact(row):
    fname = row['first_name']
    mname = row['middle_name']
    lname = row['last_name']
    return Contact(fname=fname, mname=mname, lname=lname)


def get_addresses(row, contact_id):
    addresses = []
    types = ['home', 'work']
    for type in types:
        address_type = type.title()
        address = row[f'{type}_address']
        city = row[f'{type}_city']
        state = row[f'{type}_state']
        zip = row[f'{type}_zip']
        if not all_empty(address, city, state, zip):
            addresses.append(
                Address(contact_id=contact_id, address_type=address_type, address=address, city=city, state=state,
                        zip=zip))
    return addresses


def get_phones(row, contact_id):
    phones = []
    types = ['home', 'work', 'cell']
    for type in types:
        phone_type = type.title()
        splitNumber = row[f'{type}_phone'].split('-')
        area = ''
        number = ''
        if len(splitNumber) == 3:
            area = int(splitNumber[0])
            number = int(''.join(splitNumber[1:]))
        if not all_empty(area, number):
            phones.append(Phone(phone_type=phone_type, contact_id=contact_id, area=area, number=number))
    return phones


def get_dates(row, contact_id):
    type = 'birth'
    date_type = type.title()
    date = row[f'{type}_date']
    if date != '':
        return [Date(date_type=date_type, date=date, contact_id=contact_id)]
    return []


if __name__ == '__main__':
    """
         To load contacts from given CSV file
    """
    contacts_file = 'data/contacts-from-req.csv'
    with open(contacts_file, 'r') as fobj, DBManager.create_session_scope() as session:
        reader = csv.DictReader(fobj)
        for row in reader:
            contact = get_contact(row)
            session.add(contact)
            session.flush()
            addresses = get_addresses(row, contact.contact_id)
            phones = get_phones(row, contact.contact_id)
            dates = get_dates(row, contact.contact_id)
            for address in addresses:
                session.add(address)
            for phone in phones:
                session.add(phone)
            for date in dates:
                session.add(date)
