from constants import *


class ContactREST:

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
