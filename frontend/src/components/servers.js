import PropTypes from "prop-types";
import React from "react";
import {
    reduxForm,
    Field as ReduxFormField
} from "redux-form";

import {Button, Icon, Modal, Container} from "semantic-ui-react";

import {ConfigList} from "./config_list";
import {InputField, SelectField} from "./forms";


export class ServersList extends React.Component {

    render() {
        return(
            <div>
                <ConfigList items={this.props.servers}/>
            </div>
        );
    }
}

ServersList.propTypes = {
    servers: PropTypes.array
};

const AddServerForm = function (props) {

    const {onDiscard, handleSubmit, valid} = props;

    const protocolOptions = [
        {key: "udp", value: "udp", text: "UDP"},
        {key: "tcp", value: "tcp", text: "TCP"},
    ];

    return(
        <Modal open as='form' className="form" onSubmit={handleSubmit}>

            <Modal.Header>Add new server</Modal.Header>
            <Modal.Content>

                <Container>
                    <ReduxFormField component={InputField} label="VPN Server Name" icon='user' iconPosition='left' name='vpn_name' placeholder={"VPN Server Name"}/>
                    <ReduxFormField component={InputField} label="VPN Server IP Address Or Hostname" icon='server' iconPosition='left' name='vpn_hostname' placeholder={"VPN Server IP Address Or Hostname"}/>
                    <ReduxFormField component={SelectField} label="VPN carrier protocol" name="vpn_protocol" options={protocolOptions} placeholder={"VPN carrier protocol"}/>
                </Container>

            </Modal.Content>

            <Modal.Actions>
                <Button positive disabled={!valid} type='submit'>
                    <Icon name='checkmark' /> Add server
                </Button>
                <Button negative onClick={onDiscard}>
                    <Icon name='remove' /> Cancel
                </Button>
            </Modal.Actions>

        </Modal>
    );
};

AddServerForm.propTypes = {
    onDiscard: PropTypes.func.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    valid: PropTypes.bool
};

const addServerValidator = function (values) {
    const errors = {};

    if(!values.vpn_name || values.vpn_name.length === 0) {
        errors.name = "Client name is required";
    }

    if(!values.vpn_hostname || values.vpn_hostname.length === 0) {
        errors.vpn_hostname = "Hostname is required";
    }

    return errors;
};

export const AddServer = reduxForm({
    form: "add-server-form",
    validate: addServerValidator,
    initialValues: {vpn_protocol: "udp"}
})(AddServerForm);
