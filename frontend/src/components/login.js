import {reduxForm, Field as ReduxFormField} from "redux-form";
import {bindActionCreators} from "redux";

import React from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";

import {Container, Divider, Dropdown, Grid, Header, Image, List, Menu, Segment, Button, Form, Message} from "semantic-ui-react";

import {login} from "../actions";
import {InputField} from "./forms";

const renderField = function(props) {
    const {input, label, custom, value, type, icon} = props;
    const {touched, error} = props.meta;
    return(
        <Form.Input fluid
            icon={icon}
            iconPosition='left'
            placeholder={label}
            type={type}
            {...input}/>

    );
};

class LoginComponent extends React.Component {

    constructor(props) {
        super(props);
        this.onClickedLogin = this.onClickedLogin.bind(this);
    }

    onClickedLogin(form) {
        this.props.login(form);
    }

    render() {
        const {handleSubmit} = this.props;
        return(
            <div className='login-form full-height'>
                <Grid className='full-height'
                    textAlign='center'
                    verticalAlign='middle'>

                    <Grid.Column style={{ maxWidth: 450 }}>
                        <Header as='h2' color='green' textAlign='center'>
                            OpenVPN@Home - Development<br/>
                            Log-in to your account
                        </Header>

                        <Form size='large' onSubmit={handleSubmit(this.onClickedLogin)}>
                            <Segment stacked>

                                <ReduxFormField component={InputField} icon='user' iconPosition='left' name='email' placeholder="E-Mail"/>
                                <ReduxFormField component={InputField} icon='lock' iconPosition='left' name='password' type='password' placeholder="Password"/>

                                <Button color='green' fluid size='large'>Login</Button>

                            </Segment>
                        </Form>

                        {
                            window.django.registration_enabled &&
                            <Message>
                                New to us? <Link to='/registration'>Register</Link>
                            </Message>
                        }
                    </Grid.Column>
                </Grid>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {

    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators({
        login
    }, dispatch);
}

const LoginFormComponent = reduxForm({form: "login-form"})(LoginComponent);
export const Login = connect(mapStateToProps, mapDispatchToProps)(LoginFormComponent);

export class Recovery extends React.Component {

    render() {
        return(
            <div>Recovery view</div>
        );
    }
}

