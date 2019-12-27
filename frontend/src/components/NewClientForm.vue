<template>
    <div class="ui form">
        <div class="field">
            <label>Server</label>
            <select v-model="form.server">
                <option v-for="item in servers" :key="item.id" :value="item.id">{{ item.name }}</option>
            </select>
        </div>
        <div class="field">
            <label>Client Name</label>
            <div class="ui left icon input">
                <input v-model="form.name" placeholder="Ex. 'My Home Server'" type="text">
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
    </div>
</template>

<script>
import { required, minValue, maxValue } from 'vuelidate/lib/validators';
import _ from 'lodash';

function isTimeUnitValid (value) {
    return _.indexOf(['days', 'months', 'years'], value) !== -1;
}

export default {
    name: 'NewClientForm',
    props: {
        servers: Array
    },
    data () {
        return {
            open: false,
            form: {
                name: '',
                server: this.servers[0].id,
                validity_time: 1,
                validity_time_unit: 'years'
            }
        };
    },
    validations: {
        form: {
            name: { required },
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
