import React from "react";
import {
    reduxForm,
    Field as ReduxFormField
} from "redux-form";

import {ConfigList} from "./config_list";
import {InputField} from "./forms";

import {Button, Icon, Modal, Container} from "semantic-ui-react";


export class ClientsList extends React.Component {

    render() {
        return(
            <div>
                <ConfigList items={this.props.clients} sending={this.props.sending}
                    onSendEmail={this.props.onSendClientConfig}/>
            </div>
        );
    }
}

const AddClientForm = function (props) {

    const {onDiscard, handleSubmit, valid} = props;
    return(
        <Modal open as='form' className="form" onSubmit={handleSubmit}>

            <Modal.Header>Add new client</Modal.Header>
            <Modal.Content>

                <Container>
                    <ReduxFormField component={InputField} icon='server' iconPosition='left' name='name' placeholder={"VPN Server Name"}/>
                </Container>

            </Modal.Content>

            <Modal.Actions>
                <Button positive disabled={!valid} type='submit'>
                    <Icon name='checkmark' /> Add client
                </Button>
                <Button negative onClick={onDiscard}>
                    <Icon name='remove' /> Cancel
                </Button>
            </Modal.Actions>

        </Modal>
    );
};

const addClientValidator = function (values) {
    console.log("validate", values);
    const errors = {};

    if(!values.name || values.name.length === 0) {
        errors.name = "Client name is required";
    }

    return errors;
};

export const AddClient = reduxForm({form: "add-client-form", validate: addClientValidator})(AddClientForm);
