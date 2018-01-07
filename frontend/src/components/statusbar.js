import React from "react";
import ReactDOM from "react-dom";
import {Route, Switch, Link} from "react-router-dom";
import Dashboard from "./clients";
import LoginView from "./login";
import { Container, Button, Divider, Dropdown, Grid, Header, Image, List, Menu, Segment } from "semantic-ui-react";

import OpenVpnIcon from "../icons/openvpn.png";

export class StatusBar extends React.Component {

    handleItemClick(args) {
        this.props.history.push("/servers");
    }

    render() {

        const {onLogout, onAddClient, onAddServer, history, features, account} = this.props;

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
