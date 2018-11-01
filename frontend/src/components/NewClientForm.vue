<template>
    <div class="ui form">
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
    data () {
        return {
            open: false,
            form: {
                name: ''
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
