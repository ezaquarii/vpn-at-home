<template>
    <form class="ui form" @submit.prevent="handleSubmit">
        <div class="field"><label>Public SSH deployment key</label>
            <div class="ui input">
                <input v-model="sshPublicKey" type="text" readonly>
            </div>
        </div>
    </form>
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
