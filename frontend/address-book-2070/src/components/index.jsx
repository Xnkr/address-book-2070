import React from 'react';
import '../assets/App.css';
import Browse from "./Browse";
import axios from "axios";
import Detail from "./Detail";
import Contact from "./Templates";
import Loader from "react-loader";
import config from "../config";

const {baseURL} = config;

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedContactId: 0,
            contacts: [],
            selectedContact: {},
            isEdit: false,
            isAdd: false,
            isLoaded: true,
            isSearch: false
        };
        this.fetchContacts = this.fetchContacts.bind(this);
        this.fetchContactDetails = this.fetchContactDetails.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
        this.handleEdit = this.handleEdit.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleView = this.handleView.bind(this);
        this.handleAdd = this.handleAdd.bind(this);
        this.handleSave = this.handleSave.bind(this);
    }

    fetchContacts(contact_id) {
        this.setState({
            isLoaded: false
        }, () => {
            axios.get(`${baseURL}/contacts?fmt=minimal`)
                .then(
                    res => {
                        const contacts = res.data;
                        this.setState({
                            contacts: contacts,
                            isSearch: false
                        });
                        if (contacts.length !== 0)
                            this.fetchContactDetails(contact_id === undefined ? this.state.contacts[0].contact_id : contact_id, false);
                        else
                            this.setState({
                                selectedContact: {},
                                selectedContactId: 0
                            })
                    }
                ).catch(
                err => {
                    alert(err);
                }
            ).finally(
                () => {
                    this.setState({
                        isLoaded: true
                    })
                }
            )
        })
    }

    fetchContactDetails(contactId, isEdit) {
        this.setState({
            isLoaded: false
        }, () => {
            if (contactId === 0) {
                contactId = this.state.contacts[0].contact_id;
            }
            axios.get(`${baseURL}/contacts/${contactId}`)
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
                ).catch(
                err => {
                    alert(err.response.data.message);
                }
            ).finally(
                () => {
                    this.setState({
                        isLoaded: true
                    })
                }
            )
        })

    }

    componentDidMount() {
        this.fetchContacts();
    }

    handleEdit(contactId) {
        this.fetchContactDetails(contactId, true);
    }

    handleDelete(contactId) {
        this.setState({
            isLoaded: false
        }, () => {
            axios.delete(`${baseURL}/contacts/${contactId}`)
                .then(
                    res => {
                        this.fetchContacts();
                    }
                ).catch(
                err => {
                    alert(err.response.data.message);
                }
            )
        });
    }

    handleView(contactId) {
        this.fetchContactDetails(contactId, false);
    }

    handleSearch(query, e) {
        e.preventDefault();
        this.setState({
            isLoaded: false
        }, () => {
            axios.get(`${baseURL}/contacts?q=${query}&fmt=minimal`)
                .then(
                    res => {
                        const searchResults = res.data;
                        this.setState({
                            isSearch: true,
                            searchQuery: query,
                            contacts: searchResults
                        })
                    }
                ).catch(
                    err => {
                        alert(err)
                    }
            ).finally(() => {
                this.setState({
                    isLoaded: true
                })
            })
        })
    }

    handleAdd() {
        this.setState({
            isAdd: true,
            selectedContact: new Contact().emptyContact(),
            selectedContactId: 0
        })
    }

    handleSave(selectedContact, e) {
        e.preventDefault();
        const contactId = selectedContact.contact_id;
        this.setState({
            isLoaded: false
        }, () => {
            if (this.state.isAdd) {
                axios.post(`${baseURL}/contacts`, selectedContact).then(
                    res => {
                        this.fetchContacts(res.data.contact_id);
                    }
                ).catch(
                    err => {
                        alert(err.response.data.message);
                    }
                ).finally(
                    () => {
                        this.setState({
                            isLoaded: true
                        })
                    }
                )
            } else if (this.state.isEdit) {
                axios.put(`${baseURL}/contacts/${contactId}`, selectedContact)
                    .then(
                        res => {
                            this.fetchContacts(contactId);
                        }
                    ).catch(
                    err => {
                        alert(err.response.data.message);
                    }
                ).finally(() => {
                    this.setState({
                        isLoaded: true
                    })
                })
            }
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
                <Loader loaded={this.state.isLoaded} />
                    <div className="container-fluid main-app">
                        <div className="row fill-height">
                            <Browse searchFn={(query, e) => this.handleSearch(query, e)}
                                    contacts={this.state.contacts}
                                    deleteFn={(contactId) => this.handleDelete(contactId)}
                                    editFn={(contactId) => this.handleEdit(contactId)}
                                    viewFn={(contactId) => this.handleView(contactId)}
                                    addFn={() => this.handleAdd()}
                                    isSearch={this.state.isSearch}
                            />
                            <Detail contact={selectedContact}
                                    isAdd={this.state.isAdd}
                                    isEdit={this.state.isEdit}
                                    editFn={(contactId) => this.handleEdit(contactId)}
                                    deleteFn={(contactId) => this.handleDelete(contactId)}
                                    saveFn={(selectedContact, e) => this.handleSave(selectedContact, e)}
                                    handleFormChange={(formField, e) => this.handleFormChange(formField, e)}
                                    handleFormDetailChange={(detail, id, formField, e) =>
                                        this.handleFormDetailChange(detail, id, formField, e)}
                                    addField={(field) => this.addField(field)}
                                    removeField={(field, id) => this.removeField(field, id)}
                                    cancelFn={(contact_id => this.handleView(contact_id))}
                            />
                        </div>
                    </div>
            </div>
        );
    }
}

export default App;
