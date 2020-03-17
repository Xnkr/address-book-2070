import React from "react";
import {faMinus, faPlus} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';

export default class Detail extends React.Component {
    constructor(props) {
        super(props);
    }

    renderButton = (isView, contact_id) => {
        if (isView) {
            return (
                <button className="btn btn-success" type="button" onClick={() => this.props.editFn(contact_id)}>&nbsp;Edit&nbsp;</button>
            )
        } else {
            return (
                <button className="btn btn-success" type="button" onClick={() => this.props.saveFn(contact_id)}>&nbsp;Save&nbsp;</button>
            )
        }
    };

    render() {
        const contact = this.props.contact;
        const contact_id = contact.contact_id;
        if (contact_id === undefined){
            return (
                <div className="col pad-15">
                </div>
            );
        }
        const isView = !this.props.isEdit;
        const showOrHide = this.props.isEdit ? 'show' : 'hide';
        const formClass = this.props.isEdit ? 'form-control' : 'form-control-plaintext';
        const addresses = contact.addresses.map((address, id) => {
            let addressTypeId = 'addressType' + address.address_id;
            let streetId = 'street' + address.address_id;
            let cityId = 'city' + address.address_id;
            let stateId = 'state' + address.state_id;
            let zipId = 'zip' + address.address_id;
            return (
                <div key={id}>
                    <div className="form-row">
                        <div className="col-md-5 mb-3">
                            <label htmlFor={addressTypeId}>Address Type</label>
                            <input type="text" className={formClass} id={addressTypeId}
                                   placeholder="Work" value={address.address_type} readOnly={isView} required/>

                        </div>
                        <div className="col-md-7 mb-3">
                            <label htmlFor={streetId}>Street</label>
                            <input type="text" className={formClass} id={streetId}
                                   placeholder="Street" value={address.address} readOnly={isView} required/>

                        </div>
                    </div>
                    <div className="form-row">

                        <div className="col-md-6 mb-3">
                            <label htmlFor={cityId}>City</label>
                            <input type="text" className={formClass} id={cityId}
                                   placeholder="City" value={address.city} readOnly={isView} required/>

                        </div>
                        <div className="col-md-3 mb-3">
                            <label htmlFor={stateId}>State</label>
                            <input type="text" className={formClass} id={stateId}
                                   placeholder="State" value={address.state} readOnly={isView} required/>
                        </div>
                        <div className="col-md-2 mb-3">
                            <label htmlFor={zipId}>Zip</label>
                            <input type="text" className={formClass} id={zipId}
                                   placeholder="Zip" value={address.zip} readOnly={isView} required/>

                        </div>
                        <div className="col-md-1">
                              <span className={`add-field ${showOrHide}`}>
                                <FontAwesomeIcon icon={faPlus} size="lg"/>
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
            return (
                <div key={id}>
                    <div className="form-row">

                        <div className="col-md-5 mb-3">
                            <label htmlFor={phoneTypeId}>Phone Type</label>
                            <input type="text" className={formClass} id={phoneTypeId}
                                   placeholder="Home" value={phone.phone_type} readOnly={isView} required/>

                        </div>
                        <div className="col-md-2 mb-3">
                            <label htmlFor={areaCodeId}>Area Code</label>
                            <input type="text" className={formClass} id={areaCodeId}
                                   placeholder="469" value={phone.area} readOnly={isView} required/>
                        </div>
                        <div className="col-md-4 mb-3">
                            <label htmlFor={numberId}>Phone</label>
                            <input type="text" className={formClass} id={numberId}
                                   placeholder="987-9033" value={phone.number} readOnly={isView} required/>
                        </div>
                        <div className="col-md-1">
                          <span className={`add-field ${showOrHide}`}>
                            <FontAwesomeIcon icon={faPlus} size="lg"/>
                          </span>
                        </div>
                    </div>
                </div>
            )
        });

        const dates = contact.dates.map((date, id) => {
            let dateTypeId = 'dateType' + date.date_id;
            let dateId = 'date' + date.date_id;
            let dateVal = new Date(date.date).toISOString().slice(0,10);
            return (
                <div key={id}>
                    <div className="form-row">
                        <div className="col-md-5 mb-3">
                            <label htmlFor={dateTypeId}>Date Type</label>
                            <input type="text" className={formClass} id={dateTypeId}
                                   placeholder="Birthday" value={date.date_type} readOnly={isView} required/>

                        </div>
                        <div className="col-md-6 mb-3">
                            <label htmlFor="validationCustom04">Date</label>
                            <input type="date" className={formClass} id={dateId}
                                   placeholder="2019-09-09" value={dateVal} readOnly={isView} required/>
                        </div>
                        <div className="col-md-1">
                            <span className={`add-field ${showOrHide}`}>
                                <FontAwesomeIcon icon={faPlus} size="lg"/>
                            </span>
                        </div>
                    </div>
                </div>
            )
        });

        return (
            <div className="col pad-15">
                <div id="style-1 detail-panel">
                    <div className="h3 row contact-name-lg">
                        <p className="col-md-8">{contact.fname} {contact.lname}</p>
                        <div className="contact-action col-md-4">
                            {this.renderButton(isView, contact_id)}
                            <button className="btn btn-danger" type="button">Delete</button>
                        </div>
                    </div>
                    <div className="contact-detail-form">
                        <form>
                            <div className="form-row">
                                <div className="col-md-4 mb-3">
                                    <label htmlFor="fname">First name</label>
                                    <input type="text" className={formClass} id="fname"
                                           placeholder="First name" value={contact.fname}
                                           required
                                           readOnly={isView}
                                    />
                                </div>
                                <div className="col-md-4 mb-3">
                                    <label htmlFor="mname">Middle name</label>
                                    <input type="text" className={formClass} id="mname"
                                           placeholder="Middle name" value={contact.mname === null ? ' ' : contact.mname}
                                           readOnly={isView}
                                    />
                                </div>
                                <div className="col-md-4 mb-3">
                                    <label htmlFor="lname">Last name</label>
                                    <input type="text" className={formClass} id="lname"
                                           placeholder="Last name" value={contact.lname}
                                           required
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