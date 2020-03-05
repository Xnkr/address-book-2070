from constants import *
from db_manager import DBManager
from models import *
import csv
from utils import get_null_or_string
from sqlalchemy import func


class ContactMgr:

    @staticmethod
    def add_contact(body):
        contact_parser = ContactRequestParser(body)
        contact = contact_parser.parsed_contact
        contact_id = -1
        with DBManager.create_session_scope() as session:
            session.add(contact)
            session.flush()
            contact_id = contact.contact_id
            if contact_parser.addresses:
                for address in contact_parser.addresses:
                    address.contact_id = contact.contact_id
                    session.add(address)
            if contact_parser.phones:
                for phone in contact_parser.phones:
                    phone.contact_id = contact.contact_id
                    session.add(phone)
            if contact_parser.dates:
                for date in contact_parser.dates:
                    date.contact_id = contact.contact_id
                    session.add(date)
        return contact_id

    @staticmethod
    def delete_contact(contact_id):
        with DBManager.create_session_scope() as session:
            session.query(Contact).filter(Contact.contact_id == contact_id).delete()

    @staticmethod
    def update_contact(contact_id, body):
        pass

    @staticmethod
    def get_contact(contact_id):
        with DBManager.create_session_scope() as session:
            contact = session.query(Contact).filter(Contact.contact_id == contact_id).first()
            response_builder = ContactResponseBuilder(contact)
            addresses = session.query(Address).filter(Address.contact_id == contact_id).all()
            for address in addresses:
                response_builder.build_address(address)
            phones = session.query(Phone).filter(Phone.contact_id == contact_id).all()
            for phone in phones:
                response_builder.build_phones(phone)
            dates = session.query(Date).filter(Date.contact_id == contact_id).all()
            for date in dates:
                response_builder.build_dates(date)
            return response_builder.as_dict()

    @staticmethod
    def is_valid_contact(contact_id):
        with DBManager.create_session_scope() as session:
            counter = session.query(func.count(Contact.contact_id))\
                .filter(Contact.contact_id == contact_id)
            return counter.scalar()

    @staticmethod
    def get_all_contacts(offset=0, limit=0):
        response = []
        with DBManager.create_session_scope() as session:
            contacts_query = session.query(Contact)
            if offset > 0:
                contacts_query = contacts_query.offset(offset)
            if limit > 0:
                contacts_query = contacts_query.limit(limit)
            for contact in contacts_query.all():
                contact_builder = ContactResponseBuilder(contact)
                addresses = session.query(Address).filter(contact.contact_id == Address.contact_id).all()
                phones = session.query(Phone).filter(contact.contact_id == Phone.contact_id).all()
                dates = session.query(Date).filter(contact.contact_id == Date.contact_id).all()
                for address in addresses:
                    contact_builder.build_address(address)
                for phone in phones:
                    contact_builder.build_phones(phone)
                for date in dates:
                    contact_builder.build_dates(date)
                response.append(contact_builder.as_dict())
        return response

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
