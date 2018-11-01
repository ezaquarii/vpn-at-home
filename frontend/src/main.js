import 'jquery';
import 'semantic-ui-css/semantic.js';
import 'semantic-ui-css/semantic.css';

import Vue from 'vue';
import Vuelidate from 'vuelidate';

import App from './App.vue';
import AppNotReady from './AppNotReady.vue';
import router from './router';
import store from './store';
import { ApiPlugin } from '@/api';
import SuiVue from 'semantic-ui-vue';

Vue.config.productionTip = false;

Vue.use(ApiPlugin);
Vue.use(Vuelidate);
Vue.use(SuiVue);

if (store.state.status.appNotReady) {
    new Vue({ store, render: h => h(AppNotReady) }).$mount('#app');
} else {
    new Vue({ router, store, render: h => h(App) }).$mount('#app');
}
