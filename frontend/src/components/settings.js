import PropTypes from "prop-types";
import {bindActionCreators} from "redux";
import {reduxForm, formValueSelector, Field} from "redux-form";

import React from "react";

import {
    connect
} from "react-redux";

import {
    Button,
    Card,
    Container,
    Form
} from "semantic-ui-react";

import {
    CheckboxField,
    InputField,
} from "./forms";

import {
    fetchSettings,
    updateSettings
} from "../actions";

class SettingsComponent extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {
        this.props.fetchSettings();
    }

    render() {
        const {handleSubmit, email_enabled} = this.props;
        return(
            <Container text>
                <Form onSubmit={handleSubmit((form)=>this.props.updateSettings(form))}>
                    <Card fluid={true}>
                        <Card.Content>

                            <Field component={CheckboxField}
                                name='email_enabled'
                                label={"Enable e-mail"}/>

                            {
                                email_enabled &&
                                <div>
                                    <Field disabled={!email_enabled}
                                        component={InputField}
                                        icon='user'
                                        placeholder='From for automated e-mails sent by this system'
                                        iconPosition='left'
                                        name='email_from'
                                        label={"From e-mail"}/>

                                    <Form.Group>
                                        <Field disabled={!email_enabled}
                                            component={InputField}
                                            icon='server'
                                            placeholder='Outgoing SMTP server'
                                            iconPosition='left'
                                            name='email_smtp_server'
                                            label={"SMTP server (only with TLS support)"}
                                            width={12}/>
                                        <Field disabled={!email_enabled}
                                            component={InputField}
                                            icon='lock'
                                            iconPosition='left'
                                            placeholder='Outgoing SMTP server port'
                                            label={"Port"}
                                            type={"number"}
                                            min={1}
                                            max={65535}
                                            width={4}
                                            name='email_smtp_port'/>
                                    </Form.Group>

                                    <Field disabled={!email_enabled}
                                        component={InputField}
                                        icon='user'
                                        placeholder='Outgoing SMTP server login (e-mail address)'
                                        iconPosition='left'
                                        name='email_smtp_login'
                                        label={"SMTP login"}/>

                                    <Field disabled={!email_enabled}
                                        component={InputField}
                                        icon='lock'
                                        placeholder='SMTP password is stored in database in plaintext'
                                        iconPosition='left'
                                        name='email_smtp_password'
                                        type='password'
                                        label={"SMTP password"}/>
                                </div>
                            }
                        </Card.Content>
                    </Card>

                    <Card fluid>
                        <Card.Content>
                            <Field component={CheckboxField}
                                name='registration_enabled'
                                label={"New users registration"}/>
                        </Card.Content>
                    </Card>

                    <Button type='submit'>Submit</Button>

                </Form>
            </Container>
        );
    }
}

SettingsComponent.propTypes = {
    fetchSettings: PropTypes.func.isRequired,
    updateSettings: PropTypes.func.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    email_enabled: PropTypes.bool
};

const selector = formValueSelector("settings-form");
function mapStateToProps(state) {
    return {
        email_enabled: selector(state, "email_enabled"),
        initialValues: state.settings,
        enableReinitialize: true
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators({
        fetchSettings,
        updateSettings,
    }, dispatch);
}

const SettingsFormComponent = reduxForm({form: "settings-form"})(SettingsComponent);
export const Settings = connect(mapStateToProps, mapDispatchToProps)(SettingsFormComponent);
