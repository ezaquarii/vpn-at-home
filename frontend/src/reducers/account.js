import _ from "lodash";
import {FETCH_USER, LOGIN, REGISTER} from "../actions";

export const INITIAL_STATE = {
    authenticated: window.django.authenticated,
    email: undefined,
    permissions: new Set()
};

const loginReducer = function(old_state) {
    const new_state = _.cloneDeep(old_state);
    new_state.authenticated = true;
    return new_state;
};

const registerReducer = function(old_state) {
    const new_state = _.cloneDeep(old_state);
    new_state.authenticated = true;
    return new_state;
};

const fetchUser = function(old_state, user) {
    const new_state = _.cloneDeep(old_state);
    new_state.email = user.email;
    new_state.permissions = new Set(user.permissions);
    return new_state;
};

export const accountReducer = function(state = INITIAL_STATE, action) {
    switch (action.type) {
    case LOGIN:
        return loginReducer(state);
    case REGISTER:
        return registerReducer(state);
    case FETCH_USER:
        return fetchUser(state, action.user);
    default:
        return state;
    }
};
