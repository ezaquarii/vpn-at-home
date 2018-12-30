<template>
    <div id="app">
        <NavigationBar v-if="!$route.meta.noNavbar"/>
        <div class="ui container">
            <router-view/>
        </div>
    </div>
</template>

<script lang="js">
import NavigationBar from '@/components/NavigationBar';

export default {
    components: {
        NavigationBar
    },
    created: function () {
        if (this.$store.getters.isAuthenticated) {
            this.$store.dispatch('hydrate');
        }
    }
};
</script>

<style lang="scss">
    #app {
        padding-top: 48px;
    }
</style>
