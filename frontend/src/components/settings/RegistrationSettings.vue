<template>
    <div>
        <form class="ui form" @submit.prevent="handleSubmit">
            <div class="field">
                <div class="ui checkbox">
                    <input v-model="settings.registration_enabled" type="checkbox">
                    <label>New users registration</label>
                </div>
            </div>
            <!--<div class="field">-->
                <!--<div class="ui checkbox">-->
                    <!--<input v-model="settings.admin_activation_required" type="checkbox">-->
                    <!--<label>Admin activation is required</label>-->
                <!--</div>-->
            <!--</div>-->
            <div class="field">
                <button type="submit" class="ui button settings-button" role="button" @submit="{}">Save</button>
            </div>
        </form>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import _ from 'lodash';

@Component({
    name: 'RegistrationSettings'
})
export default class RegistrationSettings extends Vue {

    settings = {
        registration_enabled: undefined
        // admin_activation_required: undefined
    };

    handleSubmit () {
        this.$store.dispatch('setSettings', this.settings);
    }

    mounted () {
        this.settings = _.cloneDeep(_.pick(this.$store.state.settings, ['registration_enabled', 'admin_activation_required']));
    }

}
</script>

<style scoped lang="scss">

</style>
