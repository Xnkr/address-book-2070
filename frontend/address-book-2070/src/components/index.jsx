import React from 'react';
import '../assets/App.css';
import Browse from "./Browse";
import axios from "axios";
import Detail from "./Detail";


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedContactId: 0,
            contacts: [],
            selectedContact: {},
            isEdit: false
        };
        this.fetchContacts = this.fetchContacts.bind(this);
        this.fetchContactDetails = this.fetchContactDetails.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
        this.handleEdit = this.handleEdit.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleView = this.handleView.bind(this);
        this.handleAdd = this.handleAdd.bind(this);
    }

    fetchContacts() {
        axios.get('http://localhost:5000/contacts?fmt=minimal&limit=10')
            .then(
                res => {
                    const contacts = res.data;
                    this.setState({
                        contacts: contacts
                    });
                    this.fetchContactDetails(this.state.contacts[0].contact_id, false);
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
                        isEdit: isEdit
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

    handleSearch(query) {
        axios.get(`http://localhost:5000/contacts?q=${query}&fmt=minimal`)
            .then(
                res => {
                    const searchResults = res.data;
                    this.setState({
                        contacts: searchResults
                    })
                }
            )
    }

    handleAdd() {

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
                        <Browse searchFn={(query) => this.handleSearch(query)}
                                contacts={this.state.contacts}
                                deleteFn={(contactId) => this.handleDelete(contactId)}
                                editFn={(contactId) => this.handleEdit(contactId)}
                                viewFn={(contactId) => this.handleView(contactId)}
                                addFn={() => this.handleAdd()}
                        />
                        <Detail contact={this.state.selectedContact}
                                isEdit={this.state.isEdit} />
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
