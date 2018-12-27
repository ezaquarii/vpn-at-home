<template>
    <div class="ui form" @submit.prevent="handleSubmit">

        <div class="field">
            <sui-message info>
                Your SSH deployment key is located in <span class="shell">${DATA_DIR}/ssh/vpnathome_server_deployment_key.pub</span>.<br>
                Make sure you upload the public key to your target deployment server.
            </sui-message>
        </div>

        <div class="field"><label>Public SSH deployment key (select all and copy)</label>
            <div class="ui input">
                <input v-model="sshPublicKey" type="text" readonly>
            </div>
        </div>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component({
    name: 'SshKeysSettings'
})
export default class SshKeysSettings extends Vue {

    get sshPublicKey () {
        return this.$store.state.sshPublicKey;
    }

    handleSubmit () {}

    mounted () {
        this.$store.dispatch('getSshPublicKey');
    }

}
</script>

<style scoped lang="scss">

</style>
