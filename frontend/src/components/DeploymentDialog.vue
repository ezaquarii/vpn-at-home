<template>
    <div>
        <sui-modal v-model="open" v-bind:closable="false">
            <sui-modal-header>Deploy OpenVPN server</sui-modal-header>
            <sui-modal-content scrolling ref="outputContainer">
                <sui-container>
                    <div class="output">
                        <div v-for="(line, index) in output" :key="index">{{ line }}</div>
                    </div>
                </sui-container>
            </sui-modal-content>
            <sui-modal-actions>
                <sui-button floated="right" compact positive @click="onDeploy" :loading="isRunning" :disabled="isRunning">Deploy</sui-button>
                <sui-button v-if="!finished" floated="right" compact negative @click="onReject">Cancel</sui-button>
                <sui-button v-else floated="right" compact negative @click="onReject">Close</sui-button>
            </sui-modal-actions>
        </sui-modal>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import {
    DeploymentRemoteProcess
} from '@/deployment';

@Component({
    data () {
        return {
            isRunning: false,
            finished: false,
            open: false,
            output: []
        };
    }
})
export default class DeploymentDialog extends Vue {

    show (server) {
        this.isRunning = false;
        this.output = [];
        this.process = null;
        this.server = server;
        this.open = true;
    }

    onDeploy () {
        this.process = new DeploymentRemoteProcess(this.server.hostname);
        this.process.onStart = this.onStart;
        this.process.onFinish = this.onFinish;
        this.process.onOutput = this.onOutput;
        this.process.connect(`ws://${window.location.host}/ws/deployment/`);
        this.isRunning = true;
        this.finished = false;
    }

    onReject () {
        this.open = false;
        if (this.process) {
            this.process.close();
        }
    }

    onStart () {
        this.pushAutoScroll([ 'Deployment started', "Ignore first '[ERROR]:' line - this is harmless Ansible bug. :o)" ]);
    }

    onFinish () {
        this.pushAutoScroll([ 'Deployment finished.' ]);
        this.isRunning = false;
        this.finished = true;
    }

    onOutput (output) {
        this.pushAutoScroll(output);
    }

    pushAutoScroll (output) {
        const outputContainer = this.$refs.outputContainer.$el;
        const autoScrollSnapMargin = 5;
        const shouldScroll = outputContainer.scrollTop >= outputContainer.scrollHeight - outputContainer.clientHeight - autoScrollSnapMargin;

        this.output.push(...output);
        if (shouldScroll) {
            this.$nextTick(function () { outputContainer.scrollTop = outputContainer.scrollHeight - outputContainer.clientHeight; });
        }
    }

}
</script>

<style scoped lang="scss">
    .button {
        margin-bottom: 12px;
        width: 75px;
    }

    .output {
        height: 300px;
        font-family: monospace;
    }
</style>
