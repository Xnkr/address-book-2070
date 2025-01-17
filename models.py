from sqlalchemy import Column, String, Integer, ForeignKey

from constants import *
import re
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    """
        Model for Contact Table
    """
    __tablename__ = 'CONTACT'
    contact_id = Column('contact_id', Integer, primary_key=True)
    fname = Column('fname', String, nullable=False)
    mname = Column('mname', String)
    lname = Column('lname', String, nullable=False)

    def __repr__(self):
        return f"<Contact({self.contact_id} | {self.fname} | {self.mname} | {self.lname})>"

    def __eq__(self, other):
        """
            Compares two objects attributes
        """
        return all((self.contact_id == other.contact_id,
                    self.fname == other.fname,
                    self.lname == other.lname,
                    self.mname == other.mname))

    def update(self, other):
        """
            Sets self class attributes from other object
            :param other: object to update attributes from
        """
        self.fname = other.fname
        self.lname = other.lname
        self.mname = other.mname


class Address(Base):
    """
        Model for Address Table
    """
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

    def as_dict(self):
        """
            Returns class attributes as dictionary
        """
        data = {
            'address_id': self.address_id,
            'address_type': self.address_type,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }
        return data

    def update(self, other):
        """
            Sets self class attributes from other object
            :param other: object to update attributes from
        """
        self.address_type = other.address_type
        self.address = other.address
        self.city = other.city
        self.state = other.state
        self.zip = other.zip

    def __eq__(self, other):
        """
            Compares two objects attributes
        """
        return all((self.address_type == other.address_type,
                    self.address == other.address,
                    self.city == other.city,
                    self.state == other.state,
                    self.zip == other.zip))


class Phone(Base):
    """
        Model for Phone Table
    """
    __tablename__ = 'PHONE'
    phone_id = Column('phone_id', Integer, primary_key=True)
    contact_id = Column('contact_id', ForeignKey('CONTACT.contact_id', ondelete="CASCADE"))
    phone_type = Column('phone_type', String, nullable=False)
    area = Column('area', Integer, nullable=False)
    number = Column('number', Integer, nullable=False)

    def __repr__(self):
        return f"<Phone({self.phone_id} | {self.contact_id} | {self.phone_type} | {self.area} | {self.number})>"

    def update(self, other):
        """
            Sets self class attributes from other object
            :param other: object to update attributes from
        """
        self.phone_type = other.phone_type
        self.area = other.area
        self.number = other.number

    def __eq__(self, other):
        """
            Compares two objects attributes
        """
        return all((self.phone_type == other.phone_type,
                    self.area == other.area,
                    self.number == other.number))

    def as_dict(self):
        """
            Returns class attributes as dictionary
        """
        data = {
            'phone_id': self.phone_id,
            'phone_type': self.phone_type,
            'area': self.area,
            'number': self.number
        }
        return data


class Date(Base):
    """
        Model for Date Table
    """
    __tablename__ = "DATE"
    date_id = Column('date_id', Integer, primary_key=True)
    contact_id = Column('contact_id', ForeignKey('CONTACT.contact_id', ondelete="CASCADE"))
    date_type = Column('date_type', String, nullable=False)
    date = Column('date', String, nullable=False)

    def __repr__(self):
        return f"<Date({self.date_id} | {self.contact_id} | {self.date_type} | {self.date})>"

    def update(self, other):
        """
            Sets self class attributes from other object
            :param other: object to update attributes from
        """
        self.date_type = other.date_type
        self.date = other.date

    def __eq__(self, other):
        """
            Compares two objects attributes
        """
        return all((self.date_type == other.date_type,
                    self.date == other.date))

    def as_dict(self):
        """
            Returns class attributes as a Dictionary
        """
        data = {
            'date_id': self.date_id,
            'date_type': self.date_type,
            'date': self.date
        }
        return data


class ContactResponseBuilder:
    """
        Builder class for Constructing JSON response for GET requests
    """

    def __init__(self, contact: Contact):
        self.contact_id = contact.contact_id
        self.fname = contact.fname
        self.mname = contact.mname
        self.lname = contact.lname
        self.addresses = []
        self.phones = []
        self.dates = []

    def as_dict(self, minimal=False):
        data = {
            'contact_id': self.contact_id,
            'fname': self.fname,
            'mname': self.mname,
            'lname': self.lname
        }
        if not minimal:
            data['addresses'] = self.addresses
            data['phones'] = self.phones
            data['dates'] = self.dates
        return data

    def build_address(self, address: Address):
        self.addresses.append(address.as_dict())
        return self

    def build_phones(self, phone: Phone):
        self.phones.append(phone.as_dict())
        return self

    def build_dates(self, date: Date):
        self.dates.append(date.as_dict())
        return self


class ContactRequestParser:
    """
        Parser class for parsing JSON requests from POST/PUT requests
    """
    def __init__(self, contact_json, contact_id=0):
        self.contact_id = contact_id
        fname = contact_json[Contact.fname.name]
        mname = contact_json[Contact.mname.name]
        lname = contact_json[Contact.lname.name]
        if not mname:
            mname = None
        self.parsed_contact = Contact(fname=fname, mname=mname, lname=lname)
        if self.contact_id != 0:
            self.parsed_contact.contact_id = self.contact_id
        self.addresses = []
        self.phones = []
        self.dates = []
        self.parse_addresses(contact_json.get('addresses', []))
        self.parse_phones(contact_json.get('phones', []))
        self.parse_dates(contact_json.get('dates', []))
        self.attributes = {
            Address: self.addresses,
            Phone: self.phones,
            Date: self.dates
        }

    def parse_addresses(self, addresses_json):
        for address_json in addresses_json:
            address_id = address_json.get(Address.address_id.name, 0)
            address = address_json[Address.address.name]
            address_type = address_json[Address.address_type.name]
            city = address_json[Address.city.name]
            state = address_json[Address.state.name]
            zip = address_json[Address.zip.name]
            if all_empty(address, city, state, zip):
                continue
            address_obj = Address(contact_id=self.contact_id, address=address,
                                  address_type=address_type, city=city, state=state, zip=zip)
            if address_id != 0:
                address_obj.address_id = address_id
            self.addresses.append(address_obj)

    def parse_dates(self, dates_json):
        for date_json in dates_json:
            date_id = date_json.get(Date.date_id.name, 0)
            date = date_json[Date.date.name]
            if date != '' and not re.match(r'\d{4}-\d{2}-\d{2}', date):
                raise TypeError('Invalid date format. Expected yyyy-mm-dd')
            date_type = date_json[Date.date_type.name]
            if all_empty(date):
                continue
            date_obj = Date(date_type=date_type, contact_id=self.contact_id, date=date)
            if date_id != 0:
                date_obj.date_id = date_id
            self.dates.append(date_obj)

    def parse_phones(self, phones_json):
        for phone_json in phones_json:
            phone_id = phone_json.get(Phone.phone_id.name, 0)
            phone_type = phone_json[Phone.phone_type.name]
            area = phone_json[Phone.area.name]
            number = phone_json[Phone.number.name]
            if all_empty(area, number):
                continue
            if not isinstance(area, int) and not str.isnumeric(area):
                raise TypeError('Area must be numeric')
            if not isinstance(number, int) and not str.isnumeric(number):
                raise TypeError('Number must be numeric')
            phone_obj = Phone(phone_type=phone_type, contact_id=self.contact_id, area=int(area), number=int(number))
            if phone_id != 0:
                phone_obj.phone_id = phone_id
            self.phones.append(phone_obj)


def all_empty(*args):
    for arg in args:
        if not isinstance(arg, str) or arg != '':
            return False
    return True
