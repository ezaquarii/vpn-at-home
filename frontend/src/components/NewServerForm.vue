<template>
    <div class="ui form">
        <div class="field">
            <label>Server Name</label>
            <div class="ui left icon input">
                <input v-model="form.name" placeholder="Ex. 'My Home Server'" type="text">
                <i aria-hidden="true" class="server icon"></i>
            </div>
        </div>
        <div class="fields">
            <div class="twelve wide field">
                <label>Server Host Address</label>
                <div class="ui left icon input">
                    <input v-model="form.hostname" placeholder="Ex. myvpn.net or 192.168.1.1" type="text">
                    <i aria-hidden="true" class="server icon"></i>
                </div>
            </div>
            <div class="four wide field">
                <label>Port</label>
                <input v-model="form.port" min="1" max="65535" type="number">
            </div>
        </div>
        <div class="field">
            <label>Transport Protocol</label>
            <select v-model="form.protocol">
                <option value="udp">UDP</option>
                <option value="tcp">TCP</option>
            </select>
        </div>
        <div class="field">
            <label>Internal VPN network (private IP range, CIDR notation)</label>
            <div class="ui left icon input">
                <input v-model="form.network" placeholder="Ex. 172.30.0.0/16" type="text">
                <i aria-hidden="true" class="server icon"></i>
            </div>
        </div>
    </div>
</template>

<script>
import {required} from 'vuelidate/lib/validators';

export default {
    name: 'NewServerForm',
    data () {
        return {
            open: false,
            form: {
                name: '',
                hostname: '',
                port: 1194,
                protocol: 'udp',
                network: '172.30.0.0/16'
            }
        };
    },
    validations: {
        form: {
            name: {required},
            hostname: {required},
            port: {required},
            protocol: {required},
            network: {required},
        }
    },
    computed: {
        isValid () {
            return !this.$v.$invalid;
        },
        value () {
            return {...this.form};
        }
    },
    mounted () {
        this.$emit('formUpdated', this.isValid);
        this.$watch('isValid', () => { this.$emit('formUpdated', this.isValid); });
    }
};
</script>

<style scoped lang="scss">
</style>
