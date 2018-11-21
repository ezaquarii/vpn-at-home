<template>
    <div>
        <div>
            <div class="info">
                <sui-message info>
                    Your SSH deployment key is located in <span class="shell">${INSTALL_DIR}/ssh/openvpnathome_server_deployment_key.pub</span>.<br>
                    Make sure you upload the public key to your target deployment server.
                </sui-message>
            </div>
            <ConfigList v-if="isSuperuser"
                        title="OpenVPN Servers"
                        :items="servers"
                        :emailEnabled="emailEnabled"
                        :deploymentEnabled="true"/>
            <ConfigList title="OpenVPN Clients"
                        :items="clients"
                        :emailEnabled="emailEnabled"
                        :deploymentEnabled="true"/>
            <NewServerDialog ref="newServerDialog"/>
            <NewClientDialog ref="newClientDialog"/>
            <DeploymentDialog ref="deploymentDialog"/>
        </div>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import NavigationBar from '@/components/NavigationBar.vue';
import ConfigList from '@/components/ConfigList.vue';
import NewServerDialog from '@/components/NewServerDialog.vue';
import NewClientDialog from '@/components/NewClientDialog.vue';
import DeploymentDialog from '@/components/DeploymentDialog.vue';

import {
    EVENT_CLICKED_ADD_CLIENT,
    EVENT_CLICKED_ADD_SERVER,
    EVENT_CLICKED_DEPLOY_SERVER
} from '@/eventbus';

@Component({
    name: 'Home',
    components: {
        NavigationBar,
        ConfigList,
        NewServerDialog,
        NewClientDialog,
        DeploymentDialog
    }
})
export default class Home extends Vue {

    constructor () {
        super();
        this.onClickedAddClient = this.onClickedAddClient.bind(this);
        this.onClickedAddServer = this.onClickedAddServer.bind(this);
        this.onClickedDeployServer = this.onClickedDeployServer.bind(this);
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

    onClickedDeployServer (server) {
        this.$refs.deploymentDialog.show(server);
    }

    mounted () {
        this.$root.$on(EVENT_CLICKED_ADD_CLIENT, this.onClickedAddClient);
        this.$root.$on(EVENT_CLICKED_ADD_SERVER, this.onClickedAddServer);
        this.$root.$on(EVENT_CLICKED_DEPLOY_SERVER, this.onClickedDeployServer);
    }

    beforeDestroy () {
        this.$root.$off(EVENT_CLICKED_ADD_CLIENT, this.onClickedAddClient);
        this.$root.$off(EVENT_CLICKED_ADD_SERVER, this.onClickedAddServer);
        this.$root.$off(EVENT_CLICKED_DEPLOY_SERVER, this.onClickedDeployServer);
    }

}
</script>

<style lang="scss">
    @import "@/assets/main.scss";
    .info {
        margin-top: 16px;
    }
</style>
