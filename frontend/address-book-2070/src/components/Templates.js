export default class Contact {
    contactTemplate = {
        contact_id: 0,
        fname: "",
        mname: "",
        lname: "",
        addresses: [],
        phones: [],
        dates: []
    };

    addressTemplate = {
        address_id: 0,
        address_type: "",
        address: "",
        city: "",
        state: "",
        zip: ""
    };

    phoneTemplate = {
        phone_id: 0,
        phone_type: "",
        area: '',
        number: ''
    };

    dateTemplate = {
        date_id: 0,
        date_type: "",
        date: ""
    };

    emptyContact() {
        let emptyContact = this.contactTemplate;
        emptyContact.addresses.push(this.addressTemplate);
        emptyContact.phones.push(this.phoneTemplate);
        emptyContact.dates.push(this.dateTemplate);
        return emptyContact;
    }
}