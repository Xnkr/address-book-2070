import React from 'react';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPlus} from "@fortawesome/free-solid-svg-icons";

export default class SearchBar extends React.Component {

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

    render() {
        return (
            <form id="search-form" onSubmit={(e) => this.props.searchFn(this.state.searchQuery, e)}>
                <div className="input-group mb-3 search-col">
                    <div className="input-group-prepend">
                        <button className="btn btn-success " type="button" onClick={() => this.props.addFn()}>
                            <FontAwesomeIcon icon={faPlus} size="lg"/>
                        </button>
                    </div>
                    <input type="search" className="form-control" placeholder="Search"
                           aria-label="Search" onChange={this.updateQuery}/>
                    <div className="input-group-append">
                        <button className="btn btn-primary" type="submit">Search
                        </button>
                    </div>
                </div>
            </form>
        )
    }


}