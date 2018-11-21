import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Settings from './views/Settings.vue';
import Login from './views/Login.vue';
import Register from './views/Register.vue';

import store from './store';

Vue.use(Router);

export const ROUTE_LOGIN = 'login';
export const ROUTE_REGISTER = 'register';
export const ROUTE_HOME = 'home';
export const ROUTE_SETTINGS = 'settings';
export const ROUTE_DEPLOYMENT = 'deployment';

const router = new Router({
    routes: [
        {
            path: '/',
            name: ROUTE_HOME,
            component: Home
        },
        {
            path: '/login',
            name: ROUTE_LOGIN,
            component: Login,
            meta: { isPublic: true, noNavbar: true }
        },
        {
            path: '/register',
            name: ROUTE_REGISTER,
            component: Register,
            meta: { isPublic: true, noNavbar: true }
        },
        {
            path: '/settings',
            name: ROUTE_SETTINGS,
            component: Settings
        }
    ]
});

router.beforeEach((to, from, next) => {
    const canVisit = !store.getters.isAuthenticated && !to.meta.isPublic;
    if (canVisit) {
        next({ path: '/login' });
    } else {
        next();
    }
});

export default router;
