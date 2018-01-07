import _ from "lodash";

import {
    ADD_CLIENT,
    FETCH_CLIENTS,
    SENDING_CONFIG_STARTED,
    SENDING_CONFIG_FINISHED
} from "../actions";


export const INITIAL_STATE = {
    clients: [],
    sending: new Set()
};

function fetchClients(old_state, response) {
    if(response.status === 200) {
        return {
            clients: response.data,
            sending: new Set()
        };
    } else {
        return old_state;
    }
}

function addClient(old_state, response) {
    if(response.status === 201) {
        const new_state = _.cloneDeep(old_state);
        new_state.clients.push(response.data);
        return new_state;
    } else {
        return old_state;
    }
}

function sendingClientConfigStarted(old_state, id) {
    const new_state = _.cloneDeep(old_state);
    new_state.sending.add(id);
    return new_state;
}

function sendingClientConfigFinished(old_state, id) {
    const new_state = _.cloneDeep(old_state);
    new_state.sending.delete(id);
    return new_state;
}

export const clientsReducer = function(state = INITIAL_STATE, action) {
    switch (action.type) {
    case FETCH_CLIENTS:
        return fetchClients(state, action.payload);
    case ADD_CLIENT:
        return addClient(state, action.payload);
    case SENDING_CONFIG_STARTED:
        return sendingClientConfigStarted(state, action.id);
    case SENDING_CONFIG_FINISHED:
        return sendingClientConfigFinished(state, action.id);
    default:
        return state;
    }
};
