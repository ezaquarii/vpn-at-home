import PropTypes from "prop-types";
import React from "react";
import {Link} from "react-router-dom";
import {Container, Button, Menu} from "semantic-ui-react";

export class StatusBar extends React.Component {

    render() {
        const {onAddClient, onAddServer, features, account} = this.props;
        return(
            <Menu fixed='top' style={{backgroundColor: "white"}}>
                <Container>
                    <Menu.Item header>{account.email}</Menu.Item>
                    <Menu.Item as={Link} to='/'          name='Clients'  />
                    <Menu.Item as={Link} to='/servers/'  name='Servers'  />
                    {
                        features.can_set_settings &&
                        <Menu.Item as={Link} to='/settings/' name='Settings'/>
                    }
                    <Menu.Menu position='right'>
                        {
                            features.can_create_client &&
                            <Menu.Item>
                                <Button compact color='green' type='mini' onClick={onAddClient}>Add client</Button>
                            </Menu.Item>
                        }
                        {
                            features.can_create_server &&
                            <Menu.Item>
                                <Button compact color='green' type='mini' onClick={onAddServer}>Add server</Button>
                            </Menu.Item>
                        }
                        <Menu.Item as='a' name='logout' href='/api/accounts/logout/'></Menu.Item>
                    </Menu.Menu>
                </Container>
            </Menu>
        );
    }
}

StatusBar.propTypes = {
    onAddServer: PropTypes.func.isRequired,
    onAddClient: PropTypes.func.isRequired,
    features: PropTypes.object.isRequired,
    account: PropTypes.object.isRequired
};
