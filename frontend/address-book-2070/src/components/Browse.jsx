import React from "react";
import {faPencilAlt, faTrash, faPlus} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';

export default class Browse extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            searchQuery: ''
        };
        this.updateQuery = this.updateQuery.bind(this);
    }

    updateQuery(e) {
        this.setState({
            searchQuery: e.target.value
        });
    }

    SearchBar = () => {
        return (
            <form id="search-form" onSubmit={(e) => this.props.searchFn(this.state.searchQuery, e)}>
                <div className="input-group mb-3 search-col">
                    <div className="input-group-prepend">
                        <button className="btn btn-success " type="button" onClick={() => this.props.addFn()}>
                            <FontAwesomeIcon icon={faPlus} size="lg"/>
                        </button>
                    </div>
                    <input type="text" className="form-control" placeholder="Search"
                           aria-label="Search" onChange={this.updateQuery}/>
                    <div className="input-group-append">
                        <button className="btn btn-primary" type="submit">Search
                        </button>
                    </div>
                </div>
            </form>
        )
    };

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
                                <this.SearchBar/>
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