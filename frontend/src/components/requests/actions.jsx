import React from 'react';
import './styles/actions.scss';

export default class RequestsActions extends React.Component {

    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.doAction = this.doAction.bind(this);
        this.state = { value: '' };
    }

    handleChange(event) {
        this.setState({ value: event.target.value });
    }

    doAction() {
        if (!!this.state.value) {
            this.props.onAction(this.state.value);
        }
    }

    render() {

        const options = this.props.events.map((event, index) => {
            return <option key={index} value={event}>{ event.name }</option>;
        });

        return (
            <div className="requests-actions panel">
                <label>Select action</label>
                <select onChange={ this.handleChange }>
                    <option> - Select - </option>
                    { options }
                </select>
                <button disabled={ !this.state.value } onClick={ this.doAction }>Submit</button>
            </div>
        );
    }

}
