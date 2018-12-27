<template>
    <div>
        <sui-modal v-model="open" v-bind:closable="false">
            <sui-modal-header>New OpenVPN Server</sui-modal-header>
            <sui-modal-content>
                <sui-container>
                    <NewServerForm v-if="open" ref="form" @formUpdated="onFormUpdated"/>
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
import NewServerForm from '@/components/NewServerForm';

@Component({
    components: {
        NewServerForm
    },
    data () {
        return {
            open: false,
            isValid: false
        };
    }

})
export default class NewServerDialog extends Vue {

    toggle () {
        this.open = true;
    }

    onFormUpdated (valid) {
        this.isValid = valid;
    }

    onAccept () {
        this.$store.dispatch('addServer', this.$refs.form.value);
        this.open = false;
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
