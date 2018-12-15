<template>
    <tr>
        <!-- Title -->
        <td v-if="isServer">{{item.name}}</td>
        <td v-else-if="isClient">
            {{item.name}} @ {{item.server_name}}
        </td>
        <td v-else>id:{{item.id}}</td>
        <!-- ----- -->
        <td>{{relativeCreated}}</td>
        <td>{{relativeValid}}</td>
        <td>{{item.email}}</td>
        <td class="center">
            <sui-dropdown class="icon" icon="ellipsis vertical">
                <sui-dropdown-menu>
                    <a class="item" v-bind:href="item.download_url">
                        <sui-icon name="download"/>Download config
                    </a>
                    <sui-dropdown-item v-if="emailEnabled && canSendEmail && isClient" @click="onSendMailClicked">
                        <sui-icon name="mail"/>Send via e-mail
                    </sui-dropdown-item>
                    <sui-dropdown-item v-if="deploymentEnabled && canDeploy" @click="onDeployClicked">
                        <sui-icon name="play"/>Deploy to server
                    </sui-dropdown-item>
                    <sui-dropdown-item v-if="isServer" @click="onDeleteClicked">
                        <sui-icon name="trash"/>Delete
                    </sui-dropdown-item>
                </sui-dropdown-menu>
            </sui-dropdown>
        </td>
    </tr>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import moment from 'moment';
import _ from 'lodash';
import {
    EVENT_CLICKED_DEPLOY_SERVER,
    EVENT_CLICKED_DELETE_SERVER
} from '@/eventbus';

@Component({
    name: 'ConfigListItem',
    props: ['item', 'emailEnabled', 'deploymentEnabled', 'isClient', 'isServer']
})
export default class ConfigListItem extends Vue {

    get relativeCreated () {
        return moment(this.item.created).fromNow();
    }

    get relativeValid () {
        return moment(this.item.validity_end).fromNow();
    }

    get isSending () {
        return this.$store.getters.isSendingClientConfigEmail(this.item.id);
    }

    get canSendEmail () {
        return this.$store.getters.canSendEmail(this.item.email);
    }

    get canDeploy () {
        return _.has(this.item, 'network');
    }

    onSendMailClicked () {
        this.$store.dispatch('sendClientConfigEmail', this.item.id);
    }

    onDeployClicked () {
        this.$root.$emit(EVENT_CLICKED_DEPLOY_SERVER, this.item);
    }

    onDeleteClicked () {
        this.$root.$emit(EVENT_CLICKED_DELETE_SERVER, this.item);
    }

}
</script>

<style scoped lang="scss">
    @import '@/assets/main.scss';

    .center {
        text-align: center !important;
    }

    .play-button {
        color: $green;
        cursor: pointer;
    }
</style>
