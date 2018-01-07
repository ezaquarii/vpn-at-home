import _ from "lodash";
import {
    ADD_SERVER,
    FETCH_SERVERS
} from "../actions";

export const INITIAL_STATE = [];

function addServers(old_state, response) {
    if(response.status === 201) {
        const new_state = _.cloneDeep(old_state);
        new_state.push(response.data);
        return new_state;
    } else {
        return old_state;
    }
}

function fetchServers(old_state, response) {
    if(response.status === 200) {
        return response.data;
    } else {
        return old_state;
    }
}

export const serversReducer = function(state = INITIAL_STATE, action) {
    switch (action.type) {
    case ADD_SERVER:
        return addServers(state, action.payload);
    case FETCH_SERVERS:
        return fetchServers(state, action.payload);
    default:
        return state;
    }
};
