import React from 'react';
import '../assets/App.css';
import Browse from "./Browse";
import axios from "axios";
import Detail from "./Detail";
import Contact from "./Templates";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedContactId: 0,
            contacts: [],
            selectedContact: {},
            isEdit: false,
            isAdd: false
        };
        this.fetchContacts = this.fetchContacts.bind(this);
        this.fetchContactDetails = this.fetchContactDetails.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
        this.handleEdit = this.handleEdit.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleView = this.handleView.bind(this);
        this.handleAdd = this.handleAdd.bind(this);
        this.handleSave = this.handleSave.bind(this);
        this.handleFormChange = this.handleFormChange.bind(this);
        this.handleFormDetailChange = this.handleFormDetailChange.bind(this);
    }

    fetchContacts(contact_id) {
        //TODO: Remove limit
        axios.get('http://localhost:5000/contacts?fmt=minimal&limit=10')
            .then(
                res => {
                    const contacts = res.data;
                    this.setState({
                        contacts: contacts
                    });
                    this.fetchContactDetails(contact_id === undefined ? this.state.contacts[0].contact_id : contact_id, false);
                }
            );
    }

    fetchContactDetails(contactId, isEdit) {
        axios.get(`http://localhost:5000/contacts/${contactId}`)
            .then(
                res => {
                    const contactDetail = res.data;
                    this.setState({
                        selectedContactId: contactDetail.contact_id,
                        selectedContact: contactDetail,
                        isEdit: isEdit,
                        isAdd: false
                    })
                }
            )
    }

    componentDidMount() {
        this.fetchContacts();
    }

    handleEdit(contactId) {
        this.fetchContactDetails(contactId, true);
    }

    handleDelete(contactId) {
        axios.delete(`http://localhost:5000/contacts/${contactId}`)
            .then(
                res => {
                    this.fetchContacts();
                }
            )
    }

    handleView(contactId) {
        this.fetchContactDetails(contactId, false);
    }

    handleSearch(query, e) {
        e.preventDefault();
        axios.get(`http://localhost:5000/contacts?q=${query}&fmt=minimal`)
            .then(
                res => {
                    const searchResults = res.data;
                    this.setState({
                        isSearch: true,
                        searchQuery: query,
                        contacts: searchResults
                    })
                }
            )
    }

    handleAdd() {
        this.setState({
            isAdd: true,
            selectedContact: new Contact().emptyContact(),
            selectedContactId: 0
        })
    }

    handleSave(e){
        e.preventDefault();
        //TODO: Catch error
        const contact = this.state.selectedContact;
        const contactId = this.state.selectedContactId;
        if (this.state.isAdd) {
            axios.post('http://localhost:5000/contacts', contact).then(
                res => {
                    this.fetchContacts(res.data.contact_id);
                }
            )
        } else if (this.state.isEdit) {
            axios.put(`http://localhost:5000/contacts/${contactId}`, contact)
                .then(
                    res => {
                        this.fetchContacts(contactId);
                    }
                )
        }
    }

    handleFormChange(formField, e){
        // TODO: Immutable update
        const contact = this.state.selectedContact;
        contact[formField] = e.target.value;
        this.setState({
            selectedContact: contact
        })
    }

    handleFormDetailChange(detail, id, formField, e){
        // TODO: Immutable update
        const contact = this.state.selectedContact;
        contact[detail][id][formField] = e.target.value;
        this.setState({
            selectedContact: contact
        })
    }

    render() {
        const selectedContact = this.state.selectedContact;
        return (
            <div>
                <div className="container overall-header">
                    <div className="headline">
                        <h1 className="header">AddressBook 2070</h1>
                    </div>
                </div>
                <div className="container main-app">
                    <div className="row fill-height">
                        <Browse searchFn={(query, e) => this.handleSearch(query, e)}
                                contacts={this.state.contacts}
                                deleteFn={(contactId) => this.handleDelete(contactId)}
                                editFn={(contactId) => this.handleEdit(contactId)}
                                viewFn={(contactId) => this.handleView(contactId)}
                                addFn={() => this.handleAdd()}
                        />
                        <Detail contact={selectedContact}
                                isAdd={this.state.isAdd}
                                isEdit={this.state.isEdit}
                                editFn={(contactId) => this.handleEdit(contactId)}
                                deleteFn={(contactId) => this.handleDelete(contactId)}
                                saveFn={(e) => this.handleSave(e)}
                                handleFormChange={(formField, e) => this.handleFormChange(formField, e)}
                                handleFormDetailChange={(detail, id, formField, e) =>
                                    this.handleFormDetailChange(detail, id, formField, e)}
                                //TODO: Add field/Remove field
                        />
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
