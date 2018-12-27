<template>
    <form class="ui form">
        <div class="field">
            <sui-message info>
                <p>
                    Here you can select hosts lists for
                    <a href="https://en.wikipedia.org/wiki/Ad_blocking#DNS_filtering" target="_blank"><u><b>DNS ad blocking</b></u>&nbsp;<i class="icon external alternate"> </i></a>
                    (aka <i>DNS sinkhole</i>). Those lists are uploaded to VPN server when DNS deployment is enabled.
                </p>
                <p>
                    Servers are not automatically updated - only the internal database is. You must re-deploy servers to use updated lists.
                </p>
                <p>
                    Ping <b>gateway.vpnathome</b> to see if your VPN DNS server is used. It should resolve to your deployed VPN gateway.
                </p>
            </sui-message>
        </div>
        <div class="field" v-for="item in list" :key="item.id">
            <div class="ui checkbox">
                <input v-model="item.enabled" :disabled="isRunning" type="checkbox">
                <label v-if="item.count">{{ item.url }} ({{ item.count }} domains, {{ formatTime(item) }})</label>
                <label v-else>{{ item.url }}</label>
            </div>
        </div>
        <div class="field">
            <sui-button class="settings-button" @click.prevent="onClickedUpdate" :loading="isRunning" :disabled="isRunning">Update</sui-button>
            <span v-if="output">{{ output }}</span>
        </div>
    </form>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import { WebSocketProcess } from '@/deployment';
import moment from 'moment';
import _ from 'lodash';

@Component({
    name: 'DnsFilteringSettings',
    data () {
        return {
            isRunning: false,
            process: null,
            output: null
        };
    },
    computed: {
        list () {
            const list = _.cloneDeep(this.$store.state.blockLists);
            _.forEach(list, (item) => {
                item._last_updated = moment(item.last_updated).fromNow();
            });
            return list;
        }
    },
    methods: {
        formatTime (item) {
            return item.last_updated ? moment(item.last_updated).fromNow() : '';
        }
    }
})
export default class DnsFilteringSettings extends Vue {

    onClickedUpdate () {
        this.process = new WebSocketProcess({ sources: this.list });
        this.process.onStart = this.onStartUpdate;
        this.process.onOutput = this.onOutput;
        this.process.onFinish = this.onFinishedUpdate;
        this.process.onClose = this.onFinishedUpdate;
        this.process.onError = this.onFinishedUpdate;
        this.process.connect(`ws://${window.location.host}/ws/update_block_lists/`);
        this.isRunning = true;
    }

    onStartUpdate () {
        this.isRunning = true;
    }

    onOutput (output) {
        this.output = _.last(output);
    }

    onFinishedUpdate () {
        this.isRunning = false;
        this.$store.dispatch('getBlockListSources');
    }

    handleSubmit () {
        this.$store.dispatch('setBlockListSources', this.list);
    }

}
</script>

<style scoped lang="scss">

</style>
