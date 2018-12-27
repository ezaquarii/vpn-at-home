import Vue from 'vue';
import Vuex from 'vuex';
import Api from '@/api';
import _ from 'lodash';

Vue.use(Vuex);

const STATUS_NONE = undefined;
// const STATUS_OK = 'ok';
// const STATUS_ERROR = 'error';
// const STATUS_PROGRESS = 'progress';

const api = new Api();

const INITIAL_STATE = {
    user: {
        authenticated: window.django.authenticated,
        email: '',
        permissions: [],
        superuser: false
    },
    servers: [],
    clients: [],
    blockLists: [],
    sshPublicKey: '',
    status: {
        sendingClientConfigEmail: [],
        sendingServerConfigEmail: [],
        appNotReady: window.django.app_not_ready,
        blockLists: STATUS_NONE
    },
    settings: {
        email_enabled: window.django.email_enabled,
        registration_enabled: window.django.registration_enabled
    }
};

const getters = {
    canRegister: (state) => state.settings.registration_enabled,
    hasServer: (state) => state.servers.length > 0,
    isAuthenticated: (state) => state.user.authenticated,
    isSuperuser: (state) => state.user.superuser,
    hasPermission: (state) => (permission) => _.includes(state.user.permissions, permission),
    isSendingClientConfigEmail: (state) => (id) => _.includes(state.status.sendingClientConfigEmail, id),
    email: (state) => state.user.email,
    canSendEmail: ({ settings, user }) => (email) => settings.email_enabled && (email === user.email || user.superuser)
};

const mutations = {

    login (state) {
        state.user.authenticated = true;
    },

    logout (state) {
        const newState = _.cloneDeep(INITIAL_STATE);
        _.assign(state, newState);
    },

    loginError (state) {
        state.auth.error = 'Error';
    },

    setUser (state, user) {
        state.user.email = user.email;
        state.user.permissions = user.permissions;
        state.user.superuser = _.includes(user.permissions, 'superuser');
    },

    setServers (state, servers) {
        state.servers = servers;
    },

    addServer (state, server) {
        state.servers.push(server);
    },

    deleteServer (state, server) {
        state.servers = _.filter(state.servers, (item) => item.id !== server.id);
    },

    setClients (state, clients) {
        state.clients = clients;
    },

    addClient (state, client) {
        state.clients.push(client);
    },

    setSendingClientConfigEmail (state, id) {
        state.status.sendingClientConfigEmail.push(id);
    },

    clearSendingClientConfigEmail (state, id) {
        state.status.sendingClientConfigEmail = _.filter(state.status.sendingClientConfigEmail, (i) => i !== id);
    },

    setSettings (state, settings) {
        state.settings = settings;
    },

    setBlockListSources (state, blockLists) {
        state.blockLists = blockLists;
    },

    setSshPublicKey (state, key) {
        state.sshPublicKey = key;
    }
};

const actions = {
    hydrate ({ dispatch }) {
        dispatch('getSettings');
        dispatch('getUser');
        dispatch('getServers');
        dispatch('getClients');
        dispatch('getBlockListSources');
    },

    getUser ({ commit }) {
        api.getUser(
            (user) => commit('setUser', user),
            (_) => {}
        );
    },

    getServers ({ commit }) {
        api.getServers(
            (servers) => commit('setServers', servers),
            (_) => {}
        );
    },

    getClients ({ commit }) {
        api.getClients(
            (servers) => commit('setClients', servers),
            (_) => {}
        );
    },

    addServer ({ commit }, server) {
        api.addServer(
            server,
            (server) => commit('addServer', server),
            (_) => {}
        );
    },

    deleteServer ({ dispatch }, server) {
        api.deleteServer(
            server,
            (_) => {
                dispatch('getServers');
                dispatch('getClients');
            },
            (_) => {}
        );
    },

    addClient ({ commit }, client) {
        api.addClient(
            client,
            (client) => commit('addClient', client),
            (_) => {}
        );
    },

    sendClientConfigEmail ({ commit }, id) {
        commit('setSendingClientConfigEmail', id);
        api.sendClientConfig(
            id,
            (id) => commit('clearSendingClientConfigEmail', id),
            (id) => commit('clearSendingClientConfigEmail', id)
        );
    },

    setSettings ({ commit }, settings) {
        api.setSettings(
            settings,
            (setting) => commit('setSettings', settings),
            (_) => {}
        );
    },

    getSettings ({ commit }) {
        api.getSettings(
            (settings) => commit('setSettings', settings),
            (_) => {}
        );
    },

    getBlockListSources ({ commit }) {
        api.getBlockListSources(
            (blockLists) => commit('setBlockListSources', blockLists),
            (_) => {}
        );
    },

    setBlockListSources ({ commit }, blockLists) {
        api.setBlockListSources(
            blockLists,
            (_) => commit('setBlockListSources', blockLists),
            (_) => {}
        );
    },

    getSshPublicKey ({ commit }) {
        api.getSshPublicKey(
            (key) => commit('setSshPublicKey', key),
            (_) => {}
        );
    }
};

const store = new Vuex.Store({
    state: _.cloneDeep(INITIAL_STATE),
    getters,
    mutations,
    actions
});

export default store;
