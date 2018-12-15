<template>
    <div>
        <sui-modal class="kurwix" v-model="open" v-bind:closable="false">
            <sui-modal-header>Delete server?</sui-modal-header>
            <sui-modal-content>
                <sui-container>
                    <div>
                        Delete server <b>{{server.name}} - {{server.hostname}}</b>? This will also delete all associated clients.
                    </div>
                </sui-container>
            </sui-modal-content>
            <sui-modal-actions>
                <sui-button floated="right" compact positive @click="onAccept">OK</sui-button>
                <sui-button floated="right" compact negative @click="onReject">Cancel</sui-button>
            </sui-modal-actions>
        </sui-modal>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component({
    data () {
        return {
            server: {},
            open: false
        };
    }
})
export default class DeleteServerDialog extends Vue {

    show (server) {
        this.server = server;
        this.open = true;
    }

    onAccept () {
        this.open = false;
        this.$store.dispatch('deleteServer', this.server);
    }

    onReject () {
        this.open = false;
    }

}
</script>

<style scoped lang="scss">
    .button {
        margin-bottom: 12px;
        width: 75px;
    }
</style>
