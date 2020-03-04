from sqlalchemy import Column, String, Integer, ForeignKey

from constants import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'CONTACT'
    contact_id = Column('contact_id', Integer, primary_key=True)
    fname = Column('fname', String, nullable=False)
    mname = Column('mname', String)
    lname = Column('lname', String, nullable=False)

    def __repr__(self):
        return f"<Contact({self.contact_id} | {self.fname} | {self.mname} | {self.lname})>"


class Address(Base):
    __tablename__ = 'ADDRESS'
    address_id = Column('address_id', Integer, primary_key=True)
    contact_id = Column('contact_id', ForeignKey('CONTACT.contact_id', ondelete="CASCADE"))
    address_type = Column('address_type', String, nullable=False)
    address = Column('address', String, nullable=False)
    city = Column('city', String, nullable=False)
    state = Column('state', String, nullable=False)
    zip = Column('zip', String, nullable=False)

    def __repr__(self):
        return f"<Address({self.address_id} | {self.contact_id} | {self.address_type} | {self.address} " \
               f"| {self.city} | {self.state} | {self.zip})>"


class Phone(Base):
    __tablename__ = 'PHONE'
    phone_id = Column('phone_id', Integer, primary_key=True)
    contact_id = Column('contact_id', ForeignKey('CONTACT.contact_id', ondelete="CASCADE"))
    phone_type = Column('phone_type', String, nullable=False)
    area = Column('area', Integer, nullable=False)
    number = Column('number', Integer, nullable=False)

    def __repr__(self):
        return f"<Phone({self.phone_id} | {self.contact_id} | {self.phone_type} | {self.area} | {self.number})>"


class Date(Base):
    __tablename__ = "DATE"
    date_id = Column('date_id', Integer, primary_key=True)
    contact_id = Column('contact_id', ForeignKey('CONTACT.contact_id', ondelete="CASCADE"))
    date_type = Column('date_type', String, nullable=False)
    date = Column('date', String, nullable=False)

    def __repr__(self):
        return f"<Date({self.date_id} | {self.contact_id} | {self.date_type} | {self.date})>"


class ContactSchema:

    select_columns = (Contact.fname, Contact.lname, Contact.mname,
                      Address.address_type, Address.address, Address.city, Address.state, Address.zip,
                      Phone.phone_type, Phone.area, Phone.number,
                      Date.date_type, Date.date)

    def __init__(self, **kwargs):
        self.contact_id = kwargs.get('contact_id')
        self.fname = kwargs.get('fname')
        self.mname = kwargs.get('mname')
        self.lname = kwargs.get('lname')
        self.addresses = []
        self.phones = []
        self.dates = []

    def as_dict(self):
        data = {
            'contact_id': self.contact_id,
            'fname': self.fname,
            'mname': self.mname,
            'lname': self.lname,
            'addresses': self.addresses,
            'phones': self.phones,
            'dates': self.dates
        }
        return data

    def add_address(self, address):
        # TODO: Get address REST
        self.addresses.append(address.as_dict())

    def add_phones(self, phone):
        self.phones.append(phone.as_dict())

    def add_dates(self, date):
        self.dates.append(date.as_dict())