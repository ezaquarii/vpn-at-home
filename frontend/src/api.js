import axios from 'axios';
import Cookies from 'js-cookie';
import store from '@/store.js';

const LOGIN_URL = '/api/accounts/login/';
const REGISTER_URL = '/api/accounts/register/';
const USER_URL = '/api/accounts/user/';
const LOGOUT_URL = '/api/accounts/logout/';
const SERVERS_URL = '/api/openvpn/servers/';
const CLIENTS_URL = '/api/openvpn/clients/';

const SETTINGS_URL = '/api/management/settings/';

export default class Api {

    login (email, password, onSuccess, onError) {
        this.client().post(LOGIN_URL, { email, password }).then(
            (response) => {
                onSuccess();
            },
            (_) => {
                onError();
            }
        );
    }

    register (email, password, onSuccess, onError) {
        this.client().post(REGISTER_URL, { email, password }).then(
            (response) => {
                onSuccess();
            },
            (_) => {
                onError();
            }
        );
    }

    logout (onLogout) {
        this.client().get(LOGOUT_URL).then(
            (response) => {
                onLogout();
            }
        );
    }

    getUser (onSuccess, onFailure) {
        this.client().get(USER_URL).then(
            (response) => onSuccess(response.data),
            (_) => onFailure()
        );
    }

    getServers (onSuccess, onFailure) {
        this.client().get(SERVERS_URL).then(
            (response) => { onSuccess(response.data); },
            (_) => { onFailure(); }
        );
    }

    addServer (server, onSuccess, onFailure) {
        this.client().post(SERVERS_URL, server).then(
            (response) => onSuccess(response.data),
            (_) => onFailure()
        );
    }

    getClients (onSuccess, onFailure) {
        this.client().get(CLIENTS_URL).then(
            (response) => { onSuccess(response.data); },
            (_) => { onFailure(); }
        );
    }

    addClient (client, onSuccess, onFailure) {
        this.client().post(CLIENTS_URL, client).then(
            (response) => onSuccess(response.data),
            (_) => onFailure()
        );
    }

    getSettings (onSuccess, onError) {
        this.client().get(SETTINGS_URL).then(
            (response) => {
                onSuccess(response.data);
            },
            (_) => {
                onError();
            }
        );
    }

    setSettings (settings, onSuccess, onError) {
        this.client().patch(SETTINGS_URL, settings).then(
            (response) => {
                onSuccess();
            },
            (_) => {
                onError();
            }
        );
    }

    sendClientConfig (id, onSuccess, onFailure) {
        const url = `/api/openvpn/clients/${id}/send/`;
        this.client().post(url, {}).then(
            (response) => onSuccess(id),
            (_) => onFailure(id)
        );
    }

    client () {
        const token = Cookies.get('csrftoken');
        return axios.create({
            headers: { 'X-CSRFToken': token }
        });
    }

}

export function ApiPlugin (Vue) {
    Vue.prototype.$api = new Api(store);
}
