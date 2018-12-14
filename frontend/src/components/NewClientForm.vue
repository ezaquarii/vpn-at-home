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
    </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators';

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
                server: this.servers[0].id
            }
        };
    },
    validations: {
        form: {
            name: { required }
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
