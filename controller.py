from constants import *
import csv

from sqlalchemy import func, or_
from sqlalchemy.inspection import inspect

from db_manager import DBManager
from models import *


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
        with DBManager.create_session_scope() as session:
            retrieved_contact = session.query(Contact).filter(Contact.contact_id == contact_id).first()
            if retrieved_contact is None:
                # Need to add contact
                contact_id = ContactMgr.add_contact(body)
                return contact_id, StandardResponses.CREATED
            else:
                # Need to update
                contact_parser = ContactRequestParser(body, contact_id)
                parsed_contact = contact_parser.parsed_contact
                if parsed_contact != retrieved_contact:
                    retrieved_contact.update(parsed_contact)
                    session.add(retrieved_contact)

                for attribute in contact_parser.attributes.keys():
                    retrieved_attributes = session.query(attribute).filter(attribute.contact_id == contact_id).all()
                    attr_primary_key = inspect(attribute).primary_key[0]
                    pk_name = attr_primary_key.name
                    retrieved_map = {
                        vars(r_attr)[pk_name]: r_attr for r_attr in retrieved_attributes
                    }
                    for p_attr in contact_parser.attributes[attribute]:
                        p_attr_id = vars(p_attr).get(attr_primary_key.name, 0)
                        ContactMgr.update_attribute(contact_id, p_attr, p_attr_id, attribute, attr_primary_key, session)
                        if p_attr_id in retrieved_map:
                            del retrieved_map[p_attr_id]
                    if retrieved_map:
                        for key_to_delete in retrieved_map.keys():
                            session.query(attribute).filter(attr_primary_key == key_to_delete).delete()

                return '', StandardResponses.SUCCESS_NO_RESPONSE

    @staticmethod
    def update_attribute(contact_id, parsed_attribute, parsed_attribute_id, attribute, attr_primary_key, session):
        if parsed_attribute_id == 0:
            parsed_attribute.contact_id = contact_id
            session.add(parsed_attribute)
        else:
            retrieved_attr = session.query(attribute).filter(attr_primary_key == parsed_attribute_id).first()
            if parsed_attribute != retrieved_attr:
                retrieved_attr.update(parsed_attribute)
                session.add(retrieved_attr)

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
            counter = session.query(func.count(Contact.contact_id)) \
                .filter(Contact.contact_id == contact_id)
            return counter.scalar()

    @staticmethod
    def search(q):
        response = []
        with DBManager.create_session_scope() as session:
            q = f'%{q}%'
            results = session.query(Contact).outerjoin(Address, Address.contact_id == Contact.contact_id) \
                .outerjoin(Phone, Phone.contact_id == Contact.contact_id).filter(
                or_(
                    Contact.fname.like(q),
                    Contact.mname.like(q),
                    Contact.lname.like(q),
                    Address.address.like(q),
                    Address.city.like(q),
                    Address.state.like(q),
                    Address.zip.like(q),
                    Phone.area.like(q),
                    Phone.number.like(q)
                )
            ).all()
            for result in results:
                built_contact = ContactMgr.build_response(result, session)
                response.append(built_contact.as_dict())
        return response

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
                built_contact = ContactMgr.build_response(contact, session)
                response.append(built_contact.as_dict())
        return response

    @staticmethod
    def process_bulk_import(file_path):
        def add_contact_from_file(columns, row, session):
            def get_null_or_string(string):
                return string if len(string) > 0 else None

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
                cols = reader.fieldnames
                try:
                    for row in reader:
                        add_contact_from_file(cols, row, session)
                except KeyError:
                    logger.exception("Incorrect key")
                    return StandardResponses.BAD_REQUEST_CODE
        except FileNotFoundError:
            logger.exception("File not found")
            return StandardResponses.SERVER_ERROR_CODE
        return StandardResponses.SUCCESS_CODE

    @staticmethod
    def build_response(contact, session):
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
        return contact_builder


if __name__ == '__main__':
    ContactMgr.process_bulk_import('DbProj.csv')
