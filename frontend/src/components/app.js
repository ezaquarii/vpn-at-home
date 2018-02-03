import React from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {Route, Switch, Redirect} from "react-router-dom";

import {Container} from "semantic-ui-react";

import {ClientsList, AddClient} from "./clients";
import {ServersList, AddServer} from "./servers";

import {Login, Recovery} from "./login";
import {Registration} from "./registration";
import {StatusBar} from "./statusbar";
import {Settings} from "./settings";

import {
    fetchClients,
    addClient,
    fetchServers,
    addServer,
    login,
    hydrate,
    sendClientConfig,
} from "../actions";

import {
    selectFeatures
} from "../reducers/selectors";


class AppComponent extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            adding_client: false,
            adding_server: false
        };
    }

    componentWillMount() {
        // TODO: fix this crude, temporary workaround
        const {hydrated, authenticated} = window.django;
        if(authenticated && !hydrated) {
            this.props.hydrate();
            window.django.hydrated = false;
        }
    }

    onClickedLogout() {
        this.props.logout();
    }

    onClickedAddClient() {
        this.setState({adding_client: true});
    }

    onAddClient(form) {
        this.setState({adding_client: false});
        this.props.addClient(form);
    }

    onClickedAddServer() {
        this.setState({adding_server: true});
    }

    onAddServer(form) {
        this.setState({adding_server: false});
        this.props.addServer({name: form.vpn_name, hostname: form.vpn_hostname, protocol: form.vpn_protocol});
    }

    renderAuthenticated() {
        return (
            <div>
                <StatusBar account={this.props.account}
                    features={this.props.features}
                    onLogout={this.onClickedLogout.bind(this)}
                    onAddClient={this.onClickedAddClient.bind(this)}
                    onAddServer={this.onClickedAddServer.bind(this)}
                />

                <Container style={{paddingTop: 64}}>
                    <Switch>
                        <Route exact path='/'   render={()=><ClientsList clients={this.props.clients.clients}
                            sending={this.props.clients.sending}
                            email_enabled={this.props.features.can_send_emails}
                            onSendClientConfig={this.props.sendClientConfig}/>}
                        />
                        <Route path='/servers'  render={()=><ServersList servers={this.props.servers}/>}/>
                        <Route path='/settings' render={()=><Settings onSubmit={(form)=>console.log(form)}/>}/>
                        <Redirect to='/'/>
                    </Switch>
                </Container>

                {this.state.adding_client && <AddClient onSubmit={this.onAddClient.bind(this)}
                    onDiscard={()=> this.setState({adding_client: false})}/>}

                {this.state.adding_server && <AddServer onSubmit={this.onAddServer.bind(this)}
                    onDiscard={()=> this.setState({adding_server: false})}/>}
            </div>
        );
    }

    renderAnonymous() {
        return(
            <div className={"full-height"}>
                <Switch>
                    <Route exact path='/' component={Login}/>
                    <Route path='/registration' component={Registration}/>
                    <Route path='/recovery' component={Recovery}/>
                    <Redirect to='/'/>
                </Switch>
            </div>
        );
    }

    render() {
        const {authenticated} = this.props.account;
        if(authenticated) {
            return this.renderAuthenticated();
        } else {
            return this.renderAnonymous();
        }
    }
}

function mapStateToProps(state) {
    return {
        account: state.account,
        clients: state.clients,
        servers: state.servers,
        features: selectFeatures(state),
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators({
        hydrate,
        login,
        fetchClients,
        addClient,
        fetchServers,
        addServer,
        sendClientConfig
    }, dispatch);
}

export const App = connect(mapStateToProps, mapDispatchToProps)(AppComponent);
