<template>
    <div>
        <div>
            <ConfigList v-if="isSuperuser" title="OpenVPN Servers" v-bind:items="servers" :emailEnabled="emailEnabled"/>
            <ConfigList title="OpenVPN Clients" v-bind:items="clients" :emailEnabled="emailEnabled"/>
            <NewServerDialog ref="newServerDialog"/>
            <NewClientDialog ref="newClientDialog"/>
        </div>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import NavigationBar from '@/components/NavigationBar.vue';
import ConfigList from '@/components/ConfigList.vue';
import NewServerDialog from '@/components/NewServerDialog.vue';
import NewClientDialog from '@/components/NewClientDialog.vue';
import {
    EVENT_CLICKED_ADD_CLIENT,
    EVENT_CLICKED_ADD_SERVER
} from '@/eventbus';

@Component({
    name: 'Home',
    components: {
        NavigationBar,
        ConfigList,
        NewServerDialog,
        NewClientDialog
    }
})
export default class Home extends Vue {

    constructor () {
        super();
        this.onClickedAddClient = this.onClickedAddClient.bind(this);
        this.onClickedAddServer = this.onClickedAddServer.bind(this);
    }

    get servers () {
        return this.$store.state.servers;
    }

    get clients () {
        return this.$store.state.clients;
    }

    get isSuperuser () {
        return this.$store.getters.isSuperuser;
    }

    get emailEnabled () {
        return this.$store.state.settings.email_enabled;
    }

    onClickedAddClient () {
        this.$refs.newClientDialog.open = true;
    }

    onClickedAddServer () {
        this.$refs.newServerDialog.open = true;
    }

    mounted () {
        this.$root.$on(EVENT_CLICKED_ADD_CLIENT, this.onClickedAddClient);
        this.$root.$on(EVENT_CLICKED_ADD_SERVER, this.onClickedAddServer);
    }

    beforeDestroy () {
        this.$root.$off(EVENT_CLICKED_ADD_CLIENT, this.onClickedAddClient);
        this.$root.$off(EVENT_CLICKED_ADD_SERVER, this.onClickedAddServer);
    }

}
</script>

<style>

</style>
