<template>
    <form class="ui form" @submit.prevent="handleSubmit">
        <div class="content">
            <div class="field">
                <sui-message info>
                    E-Mail settings are configured in <span class="shell">${DATA_DIR}/data/settings.json</span> and are used
                    to send logs, config files, etc. SMTP settings cannot be set here, but you can toggle e-mail sender.
                </sui-message>
            </div>
            <div class="field">
                <div class="ui checked checkbox">
                    <input v-model="settings.email_enabled" type="checkbox">
                    <label>Enable e-mail</label>
                </div>
            </div>
            <div class="field" v-if="settings.email_enabled">
                <div class="field">
                    <label>From e-mail</label>
                    <div class="ui left icon input disabled">
                        <input v-model="readOnly.email_from" placeholder="From for automated e-mails sent by this system" type="text" key="email_from">
                        <i aria-hidden="true" class="user icon"></i>
                    </div>
                </div>
                <div class="fields">
                    <div class="twelve wide field">
                        <label>SMTP server (only with TLS support)</label>
                        <div class="ui left icon input disabled">
                            <input v-model="readOnly.email_smtp_server" placeholder="Outgoing SMTP server" type="text">
                            <i aria-hidden="true" class="server icon"></i>
                        </div>
                    </div>
                    <div class="four wide field">
                        <label>Port</label>
                        <div class="ui left icon input disabled">
                            <input v-model="readOnly.email_smtp_port" placeholder="Outgoing SMTP server port" min="1" max="65535" type="number">
                            <i aria-hidden="true" class="lock icon"></i>
                        </div>
                    </div>
                </div>
                <div class="field"><label>SMTP login</label>
                    <div class="ui left icon input disabled">
                        <input v-model="readOnly.email_smtp_login" placeholder="Outgoing SMTP server login (e-mail address)" type="text">
                        <i aria-hidden="true" class="user icon"></i>
                    </div>
                </div>
                <div class="field"><label>SMTP password (hidden)</label>
                    <div class="ui left icon input disabled">
                        <input value="See settings.json" type="text">
                        <i aria-hidden="true" class="lock icon"></i>
                    </div>
                </div>
            </div>
            <div class="field">
                <button type="submit" class="ui button settings-button" role="button" @submit="{}">Save</button>
            </div>
        </div>
    </form>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import NavigationBar from '@/components/NavigationBar.vue';
import _ from 'lodash';

@Component({
    name: 'EmailSettings',
    components: {
        NavigationBar
    }
})
export default class EmailSettings extends Vue {

        settings = {
            email_enabled: false
        };

        readOnly = {
            email_from: undefined,
            email_smtp_server: undefined,
            email_smtp_port: 465,
            email_smtp_login: undefined,
            email_smtp_password: 'never available in ui'
        };

        handleSubmit () {
            this.$store.dispatch('setSettings', this.settings);
        }

        mounted () {
            this.settings.email_enabled = _.cloneDeep(this.$store.state.settings.email_enabled);
            this.readOnly = _.cloneDeep(_.pick(this.$store.state.settings, [
                'email_from',
                'email_smtp_server',
                'email_smtp_port',
                'email_smtp_login',
                'email_smtp_password'
            ]));
        }

}

</script>

<style scoped lang="scss">

</style>
