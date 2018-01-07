import axios from "axios";
import Cookies from "universal-cookie";

export const FETCH_USER = "FETCH_USER";
export const HYDRATE = "HYDRATE";
export const LOGIN = "LOGIN";
export const LOGOUT = "LOGOUT";
export const REGISTER = "REGISTER";
export const ADD_CLIENT = "ADD_CLIENT";
export const FETCH_SERVERS = "FETCH_SERVERS";
export const ADD_SERVER = "ADD_SERVER";
export const FETCH_CLIENTS = "FETCH_CLIENTS";
export const FETCH_SETTINGS = "FETCH_SETTINGS";
export const UPDATE_SETTINGS = "UPDATE_SETTINGS";

export const SENDING_CONFIG_STARTED = "SENDING_CONFIG_STARTED";
export const SENDING_CONFIG_FINISHED = "SENDING_CONFIG_FINISHED";

const cookies = new Cookies();

const client = function() {
    return axios.create({
        headers: {"X-CSRFToken": cookies.get("csrftoken")}
    });
};

export function hydrate() {
    return (dispatch) => {
        dispatch(fetchUser());
        dispatch(fetchServers());
        dispatch(fetchClients());
    };
}

export function fetchUser() {
    return (dispatch) => {
        const url = "/api/accounts/user/";
        return axios.get(url).then(
            response => {
                dispatch({type: FETCH_USER, user: response.data});
            },
            error => {
                dispatch({type: FETCH_USER, user: undefined});
            }
        );
    };
}

export function fetchServers() {
    const url = "/api/openvpn/servers/";
    const request = axios.get(url);
    return {
        type: FETCH_SERVERS,
        payload: request
    };
}

export function fetchClients() {
    const url = "/api/openvpn/clients/";
    const request = axios.get(url);
    return {
        type: FETCH_CLIENTS,
        payload: request
    };
}

export function addClient(form) {
    console.log("addClient", form);
    const url = "/api/openvpn/clients/";
    const request = client().post(url, form);
    return {
        type: ADD_CLIENT,
        payload: request
    };
}

export function addServer(form) {
    const url = "/api/openvpn/servers/";
    const request = client().post(url, form);
    return {
        type: ADD_SERVER,
        payload: request
    };
}

export function login(credentials) {
    return (dispatch, getState) => {
        const url = "/api/accounts/login/";
        return axios.post(url, credentials).then(
            response => {
                console.log("Login:", response);
                dispatch({type: LOGIN});
                dispatch(hydrate());
            },
            error => {
                console.log("Login error", error.response);
                alert("Login error");
            }
        );
    };
}

export function register(credentials) {
    return (dispatch, getState) => {
        const url = "/api/accounts/register/";
        return axios.post(url, credentials).then(
            response => {
                dispatch({type: REGISTER, success: true});
                dispatch(hydrate());
            },
            error => {
                console.log("Registration error", error.response);
                alert("Registration error");
            }
        );
    };
}

export function fetchSettings() {
    return (dispatch) => {
        const url = "/api/management/settings/";
        return client().get(url).then(
            response => {
                dispatch({type: FETCH_SETTINGS, settings: response.data});
            },
            error => {
                console.log("NOT IMPLEMENTED: settings error", error);
                alert("NOT IMPLEMENTED: settings error");
            }
        );
    };
}

export function updateSettings(settings) {
    return (dispatch) => {
        const url = "/api/management/settings/";
        return client().patch(url, settings).then(
            response => {
                dispatch({type: UPDATE_SETTINGS, settings: response.data});
            },
            error => {
                console.log("NOT IMPLEMENTED: settings error", error);
                alert("NOT IMPLEMENTED: settings error");
            }
        );
    };
}

export function sendClientConfig(id) {
    return (dispatch) => {
        const url = `/api/openvpn/clients/${id}/send/`;
        dispatch({type: SENDING_CONFIG_STARTED, id: id});
        return client().post(url).then(
            response => {
                console.log("Client config sent");
                alert("Client config sent");
                dispatch({type: SENDING_CONFIG_FINISHED, id: id});
            },
            error => {
                console.log("NOT IMPLEMENTED: sendClientConfig error", error);
                alert("NOT IMPLEMENTED: sendClientConfig error");
                dispatch({type: SENDING_CONFIG_FINISHED, id: id});
            }
        );
    };
}