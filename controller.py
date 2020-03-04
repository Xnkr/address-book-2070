from constants import *
from db_manager import DBManager
from models import *
import csv
from utils import get_null_or_string


class ContactMgr:

    @staticmethod
    def add_contact(body):
        return 0

    @staticmethod
    def delete_contact(contact_id):
        pass

    @staticmethod
    def update_contact(contact_id, body):
        pass

    @staticmethod
    def get_contact(contact_id):
        pass

    @staticmethod
    def is_valid_contact(contact_id):
        pass

    @staticmethod
    def get_all_contacts():
        with DBManager.create_session_scope() as session:
            records = session.query(*ContactSchema.select_columns)\
                .outerjoin(Address, Address.contact_id == Contact.contact_id)\
                .outerjoin(Phone, Phone.contact_id == Contact.contact_id)\
                .outerjoin(Date, Date.contact_id == Contact.contact_id).all()
            return records

    @staticmethod
    def process_bulk_import(file_path):
        def add_contact_from_file(columns, row, session):
            contact = Contact(fname=row['fname'], mname=get_null_or_string(row['mname']),
                              lname=row['lname'])
            session.add(contact)
            session.flush()
            if 'address_type' in columns:
                address = Address(contact_id=contact.contact_id, address_type=row['address_type'],
                                  address=row['address'], city=row['city'], state=row['state'],
                                  zip=row['zip'])
                session.add(address)
            if 'phone_type' in columns:
                phone = Phone(contact_id=contact.contact_id, phone_type=row['phone_type'], area=row['area'],
                              number=row['number'])
                session.add(phone)
            if 'date_type' in columns:
                date = Date(contact_id=contact.contact_id, date_type=row['date_type'], date=row['date'])
                session.add(date)
        try:
            with open(file_path) as fd, DBManager.create_session_scope(autoflush=True) as session:
                reader = csv.DictReader(fd)
                columns = reader.fieldnames
                try:
                    for row in reader:
                        add_contact_from_file(columns, row, session)
                except KeyError:
                    logger.exception("Incorrect key")
                    return StandardResponses.BAD_REQUEST_CODE
        except FileNotFoundError:
            logger.exception("File not found")
            return StandardResponses.SERVER_ERROR_CODE
        return StandardResponses.SUCCESS_CODE

if __name__ == '__main__':
    ContactMgr.process_bulk_import('DbProj.csv')