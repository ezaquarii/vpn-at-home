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
        <div class="fields">
            <div class="eight wide field">
                <label>Certificate validity period</label>
                <input v-model="form.validity_time" min="1" max="1000" type="number">
            </div>
            <div class="eight wide field">
                <label>Time unit</label>
                <select v-model="form.validity_time_unit">
                    <option value="days">Days</option>
                    <option value="months">Months</option>
                    <option value="years">Years</option>
                </select>
            </div>
        </div>
        <div class="field">
            <div class="ui checked checkbox">
                <input v-model="form.deploy_dns" type="checkbox">
                <label>Enable DNS server</label>
            </div>
        </div>
    </div>
</template>

<script>
import { maxValue, minValue, required } from 'vuelidate/lib/validators';
import _ from 'lodash';

function isTimeUnitValid (value) {
    return _.indexOf(['days', 'months', 'years'], value) !== -1;
}

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
                network: '172.30.0.0/16',
                deploy_dns: false,
                validity_time: 1,
                validity_time_unit: 'years'
            }
        };
    },
    validations: {
        form: {
            name: { required },
            hostname: { required },
            port: { required },
            protocol: { required },
            network: { required },
            deploy_dns: { required },
            validity_time: {
                minValue: minValue(1),
                maxValue: maxValue(1000)
            },
            validity_time_unit: {
                timeUnitValid: isTimeUnitValid
            }
        }
    },
    computed: {
        isValid () {
            return !this.$v.$invalid;
        },
        value () {
            return { ...this.form };
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
