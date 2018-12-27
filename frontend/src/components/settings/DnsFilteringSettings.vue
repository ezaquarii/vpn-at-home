<template>
    <form class="ui form">
        <div class="field">
            <sui-message info>
                Here you can select hosts lists for
                <a href="https://en.wikipedia.org/wiki/Ad_blocking#DNS_filtering" target="_blank"><u><b>DNS ad blocking</b></u>&nbsp;<i class="icon external alternate"> </i></a>.
                Those lists are uploaded to VPN server when DNS deployment is enabled.
            </sui-message>
        </div>
        <div class="field" v-for="item in list">
            <div class="ui checkbox">
                <input v-model="item.enabled" :disabled="isRunning" type="checkbox">
                <label v-if="item.count">{{ item.url }} ({{ item.count }} domains)</label>
                <label v-else>{{ item.url }}</label>
            </div>
        </div>
        <div class="field">
            <sui-button class="settings-button" @click.prevent="handleSubmit" :disabled="isRunning">Save</sui-button>
            <sui-button class="settings-button" @click.prevent="onClickedUpdate" :loading="isRunning" :disabled="isRunning">Update</sui-button>
        </div>
    </form>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import { DeploymentRemoteProcess } from '@/deployment';
import _ from 'lodash';

@Component({
    name: 'DnsFilteringSettings',
    data () {
        return {
            isRunning: false,
            process: null
        };
    },
    computed: {
        list () {
            return _.cloneDeep(this.$store.state.blockLists);
        }
    }
})
export default class DnsFilteringSettings extends Vue {

    onClickedUpdate () {
        this.process = new DeploymentRemoteProcess();
        this.process.onStart = this.onStartUpdate;
        this.process.onFinish = this.onFinishedUpdate;
        this.process.connect(`ws://${window.location.host}/ws/update_block_lists/`);
        this.isRunning = true;
    }

    onStartUpdate () {
        this.isRunning = true;
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
