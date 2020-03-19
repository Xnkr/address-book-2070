import React from "react";
import {faMinus, faPlus} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import Contact from "./Templates";

export default class Detail extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            selectedContact: {}
        };
        this.handleFormChange = this.handleFormChange.bind(this);
        this.handleFormDetailChange = this.handleFormDetailChange.bind(this);
        this.addField = this.addField.bind(this);
        this.removeField = this.removeField.bind(this);
    }


    renderButton = (isView, contact_id) => {
        if (isView) {
            return (
                <div>
                    <button className="btn btn-success mr-2" type="button" onClick={() => this.props.editFn(contact_id)}>&nbsp;Edit&nbsp;</button>
                    <button className="btn btn-danger" type="button" onClick={() => this.props.deleteFn(contact_id)}>Delete</button>
                </div>
            )
        } else {
            return (
                <div>
                    <button className="btn btn-success mr-2" type="submit" form="contact-form">&nbsp;Save&nbsp;</button>
                    <button className="btn btn-danger" type="button" onClick={() => this.props.cancelFn(contact_id)}>Cancel</button>
                </div>
            )
        }
    };

    handleFormChange(formField, e) {
        const contact = JSON.parse(JSON.stringify(this.state.selectedContact));
        contact[formField] = e.target.value;
        this.setState({
            selectedContact: contact
        })
    }

    handleFormDetailChange(detail, id, formField, e) {
        const contact = JSON.parse(JSON.stringify(this.state.selectedContact));
        contact[detail][id][formField] = e.target.value;
        this.setState({
            selectedContact: contact
        })
    }

    addField(field) {
        const contact = JSON.parse(JSON.stringify(this.state.selectedContact));
        contact[field].push(new Contact().getEmptyField(field));
        this.setState({
            selectedContact: contact
        })
    }

    removeField(field, id) {
        const contact = JSON.parse(JSON.stringify(this.state.selectedContact));
        const contactField = contact[field].slice();
        contactField.splice(id, 1);
        contact[field] = contactField;
        this.setState({
            selectedContact: contact
        })
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (Object.keys(prevState).length === 0 ||
            this.props.contact.contact_id !== prevProps.contact.contact_id ||
            this.props.isEdit !== prevProps.isEdit
        ) {
            this.setState({
                selectedContact: this.props.contact
            })
        }
    }

    render() {
        const contact = this.state.selectedContact;
        const contact_id = contact.contact_id;
        if (contact_id === undefined){
            return (
                <div className="col pad-15">
                </div>
            );
        }
        const isEdit = this.props.isEdit;
        const isAdd = this.props.isAdd;
        const isView = !(isEdit || isAdd);
        const formClass = (isView) ? 'form-control-plaintext': 'form-control';
        const addresses = contact.addresses.map((address, id) => {
            let addressTypeId = 'addressType' + address.address_id;
            let streetId = 'street' + address.address_id;
            let cityId = 'city' + address.address_id;
            let stateId = 'state' + address.address_id;
            let zipId = 'zip' + address.address_id;
            let addShowHide = !isView && id === contact.addresses.length - 1 ? 'show': 'hide';
            let removeShowHide = !isView && contact.addresses.length !== 1 ? 'show': 'hide';
            return (
                <div key={id}>
                    <div className="form-row">
                        <div className="col-md-5 mb-3">
                            <label htmlFor={addressTypeId}>Address Type</label>
                            <input type="text" className={formClass} id={addressTypeId}
                                    value={address.address_type} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('addresses', id, 'address_type', e)}
                                   />

                        </div>
                        <div className="col-md-7 mb-3">
                            <label htmlFor={streetId}>Street</label>
                            <input type="text" className={formClass} id={streetId}
                                    value={address.address} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('addresses', id, 'address', e)}
                                   />

                        </div>
                    </div>
                    <div className="form-row">

                        <div className="col-md-6 mb-3">
                            <label htmlFor={cityId}>City</label>
                            <input type="text" className={formClass} id={cityId}
                                    value={address.city} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('addresses', id, 'city', e)}
                                   />

                        </div>
                        <div className="col-md-3 mb-3">
                            <label htmlFor={stateId}>State</label>
                            <input type="text" className={formClass} id={stateId}
                                    value={address.state} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('addresses', id, 'state', e)}
                                   />
                        </div>
                        <div className="col-md-2 mb-3">
                            <label htmlFor={zipId}>Zip</label>
                            <input type="text" className={formClass} id={zipId}
                                    value={address.zip} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('addresses', id, 'zip', e)}
                                   />

                        </div>
                        <div className="col-md-1">
                            <span className={`add-field ${addShowHide}`}
                                  onClick={() => this.addField('addresses')}>
                                <FontAwesomeIcon icon={faPlus} size="lg"/>
                            </span>
                            <span className={`remove-field ${removeShowHide}`}
                                  onClick={() => this.removeField('addresses', id)}>
                                <FontAwesomeIcon icon={faMinus} size="lg"/>
                            </span>
                        </div>
                    </div>
                </div>
            )
        });
        const phones = contact.phones.map((phone, id) => {
            let phoneTypeId = 'phoneType' + phone.phone_id;
            let areaCodeId = 'areaCode' + phone.phone_id;
            let numberId = 'number' + phone.phone_id;
            let addShowHide = !isView && id === contact.phones.length - 1 ? 'show': 'hide';
            let removeShowHide = !isView && contact.phones.length !== 1 ? 'show': 'hide';
            return (
                <div key={id}>
                    <div className="form-row">

                        <div className="col-md-5 mb-3">
                            <label htmlFor={phoneTypeId}>Phone Type</label>
                            <input type="text" className={formClass} id={phoneTypeId}
                                    value={phone.phone_type} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('phones', id, 'phone_type', e)}
                                   />

                        </div>
                        <div className="col-md-2 mb-3">
                            <label htmlFor={areaCodeId}>Area Code</label>
                            <input type="number" className={formClass} id={areaCodeId}
                                    value={phone.area} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('phones', id, 'area', e)}

                                   max="999"
                                   min="100"
                            />
                        </div>
                        <div className="col-md-4 mb-3">
                            <label htmlFor={numberId}>Phone</label>
                            <input type="number" className={formClass} id={numberId}
                                    value={phone.number} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('phones', id, 'number', e)}
                                   />
                        </div>
                        <div className="col-md-1">
                            <span className={`add-field ${addShowHide}`}
                                  onClick={() => this.addField('phones')}>
                                <FontAwesomeIcon icon={faPlus} size="lg"/>
                            </span>
                            <span className={`remove-field ${removeShowHide}`}
                                  onClick={() => this.removeField('phones', id)}>
                                <FontAwesomeIcon icon={faMinus} size="lg"/>
                            </span>
                        </div>
                    </div>
                </div>
            )
        });

        const dates = contact.dates.map((date, id) => {
            let dateTypeId = 'dateType' + date.date_id;
            let dateId = 'date' + date.date_id;
            let dateVal = date.date !== '' ? new Date(date.date).toISOString().slice(0,10) : '';
            let addShowHide = !isView && id === contact.dates.length - 1 ? 'show': 'hide';
            let removeShowHide = !isView && contact.dates.length !== 1 ? 'show': 'hide';
            return (
                <div key={id}>
                    <div className="form-row">
                        <div className="col-md-5 mb-3">
                            <label htmlFor={dateTypeId}>Date Type</label>
                            <input type="text" className={formClass} id={dateTypeId}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('dates', id, 'date_type', e)}
                                    value={date.date_type} readOnly={isView} />

                        </div>
                        <div className="col-md-6 mb-3">
                            <label htmlFor={dateId}>Date</label>
                            <input type="date" className={formClass} id={dateId}
                                   value={dateVal} readOnly={isView}
                                   onChange={(e) =>
                                       this.handleFormDetailChange('dates', id, 'date', e)}
                                   />
                        </div>
                        <div className="col-md-1">
                            <span className={`add-field ${addShowHide}`}
                                  onClick={() => this.addField('dates')}>
                                <FontAwesomeIcon icon={faPlus} size="lg"/>
                            </span>
                            <span className={`remove-field ${removeShowHide}`}
                                  onClick={() => this.removeField('dates', id)}>
                                <FontAwesomeIcon icon={faMinus} size="lg"/>
                            </span>
                        </div>
                    </div>
                </div>
            )
        });

        return (
            <div className="col pad-15">
                <div id="style-1" className="detail-panel">
                    <div className="h3 row contact-name-lg">
                        { isAdd && <p className="col-md-8">Add Contact</p>}
                        { !isAdd && <p className="col-md-8">{contact.fname} {contact.lname}</p>}
                        <div className="contact-action col-md-4">
                            {this.renderButton(isView, contact_id)}
                        </div>
                    </div>
                    <div className="contact-detail-form">
                        <form id="contact-form" onSubmit={(e) => this.props.saveFn(this.state.selectedContact, e)}>
                            <div className="form-row">
                                <div className="col-md-4 mb-3">
                                    <label htmlFor="fname">First name</label>
                                    <input type="text" className={formClass} id="fname"
                                            value={contact.fname}
                                           required
                                           onChange={(e) => this.handleFormChange('fname', e)}
                                           readOnly={isView}
                                    />
                                </div>
                                <div className="col-md-4 mb-3">
                                    <label htmlFor="mname">Middle name</label>
                                    <input type="text" className={formClass} id="mname"
                                           
                                           value={contact.mname === null || contact.mname === '' ? (isView ? ' ': '') : contact.mname}
                                           onChange={(e) => this.handleFormChange('mname', e)}
                                           readOnly={isView}
                                    />
                                </div>
                                <div className="col-md-4 mb-3">
                                    <label htmlFor="lname">Last name</label>
                                    <input type="text" className={formClass} id="lname"
                                            value={contact.lname}
                                           required
                                           onChange={(e) => this.handleFormChange('lname', e)}
                                           readOnly={isView}
                                    />
                                </div>
                            </div>

                            {addresses}
                            {phones}
                            {dates}
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}