<template>
    <div>
        <sui-modal v-model="open" v-bind:closable="false">
            <sui-modal-header>New OpenVPN Client</sui-modal-header>
            <sui-modal-content>
                <sui-container>
                    <NewClientForm v-if="open" :servers="servers" ref="form" @formUpdated="onFormUpdated"/>
                </sui-container>
            </sui-modal-content>
            <sui-modal-actions>
                <sui-button floated="right" compact positive :disabled="!isValid" @click="onAccept">OK</sui-button>
                <sui-button floated="right" compact negative @click="onReject">Cancel</sui-button>
            </sui-modal-actions>
        </sui-modal>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import NewClientForm from '@/components/NewClientForm';

@Component({
    components: {
        NewClientForm
    },
    data () {
        return {
            open: false,
            isValid: false
        };
    }

})
export default class NewClientDialog extends Vue {

    toggle () {
        this.open = true;
    }

    onFormUpdated (valid) {
        this.isValid = valid;
    }

    onAccept () {
        this.$store.dispatch('addClient', this.$refs.form.value);
        this.open = false;
    }

    onReject () {
        this.open = false;
    }

    get servers () {
        return this.$store.state.servers;
    }

}
</script>

<style scoped lang="scss">
    .button {
        margin-bottom: 12px;
        width: 75px;
    }
</style>
