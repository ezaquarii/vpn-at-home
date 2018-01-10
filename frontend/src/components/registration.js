import PropTypes from "prop-types";
import {bindActionCreators} from "redux";
import {reduxForm, Field as ReduxFormField} from "redux-form";

import React from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";

import {Grid, Header, Segment, Button, Form, Message} from "semantic-ui-react";

import {InputField} from "./forms";
import {register} from "../actions";


class RegistrationComponent extends React.Component {

    constructor(props) {
        super(props);
        this.onClickedRegister = this.onClickedRegister.bind(this);
    }

    onClickedRegister(form) {
        this.props.register(form);
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
                            OpenVPN@Home<br/>
                            Register new user
                        </Header>


                        <Form size='large' onSubmit={handleSubmit(this.onClickedRegister)}>
                            <Segment stacked>

                                <ReduxFormField component={InputField} icon='user' iconPosition='left' name='email' placeholder="E-Mail"/>
                                <ReduxFormField component={InputField} icon='lock' iconPosition='left' name='password' type='password' placeholder="Password"/>

                                <Button color='green' fluid size='large'>Register</Button>

                            </Segment>
                        </Form>

                        <Message>
                            Already have account?  <Link to='/'>Login</Link>
                        </Message>
                    </Grid.Column>
                </Grid>
            </div>
        );
    }
}

RegistrationComponent.propTypes = {
    register: PropTypes.bool.isRequired,
    handleSubmit: PropTypes.func.isRequired
};

function mapStateToProps() {
    return {
        // nothing for now
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators({
        register
    }, dispatch);
}

const RegistrationFormComponent = reduxForm({form: "registration-form"})(RegistrationComponent);
export const Registration = connect(mapStateToProps, mapDispatchToProps)(RegistrationFormComponent);
