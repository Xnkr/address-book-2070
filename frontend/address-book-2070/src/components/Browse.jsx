import React from "react";
import {faPencilAlt, faTrash} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import SearchBar from "./SearchBar";

export default class Browse extends React.Component {

    render() {
        const contacts = this.props.contacts.map((contact, id) => {
            const mName = contact.mname === null ? '' : contact.mname.charAt(0) + '.';
            return (
                <li className="list-item" key={contact.contact_id}>
                    <div className="row">
                        <div className="col-md-10 contact-select" onClick={() => this.props.viewFn(contact.contact_id)}>
                            {contact.fname} {mName} {contact.lname}
                        </div>
                        <div className="col-md-2">
                            <div className="list-action">
                              <span className="list-edit pr-2" onClick={() => this.props.editFn(contact.contact_id)}>
                                <FontAwesomeIcon icon={faPencilAlt} size="lg"/>
                              </span>
                                <span className="list-delete" onClick={() => this.props.deleteFn(contact.contact_id)}>
                                <FontAwesomeIcon icon={faTrash} size="lg"/>
                              </span>
                            </div>
                        </div>
                    </div>
                </li>
            )
        });
        return (
            <div className="col-md-4 zero-pad">
                <div className="table-responsive">
                    <table className="table">
                        <thead>
                        <tr>
                            <th>
                                <SearchBar addFn={this.props.addFn}
                                           searchFn={this.props.searchFn}
                                />
                            </th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>
                                <div id="style-1" className="contact-list search-col">
                                    <ol>
                                        {contacts}
                                    </ol>
                                </div>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}