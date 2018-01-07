import {FETCH_SETTINGS, UPDATE_SETTINGS} from "../actions";

export const INITIAL_STATE = {
    email_enabled: false,
};

const fetchSettings = function(old_state, settings) {
    return settings;
};

const updateSettings = function(old_state, settings) {
    return settings;
};

export const settingsReducer = function(state = INITIAL_STATE, action) {
    switch (action.type) {
    case FETCH_SETTINGS:
        return fetchSettings(state, action.settings);
    case UPDATE_SETTINGS:
        return updateSettings(state, action.settings);
    default:
        return state;
    }
};
