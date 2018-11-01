<template>
    <div class="settings">
        <div class="ui container text" style="margin: 16px">
            <form class="ui form" @submit.prevent="handleSubmit">
                <div class="ui fluid card">
                    <div class="content">
                        <div class="field">
                            <div class="ui checked checkbox">
                                <input v-model="settings.email_enabled" type="checkbox">
                                <label>Enable e-mail</label>
                            </div>
                        </div>
                        <div v-if="settings.email_enabled">
                            <div class="field">
                                <label>From e-mail</label>
                                <div class="ui left icon input">
                                    <input v-model="settings.email_from" placeholder="From for automated e-mails sent by this system" type="text" key="email_from">
                                    <i aria-hidden="true" class="user icon"></i>
                                </div>
                            </div>
                            <div class="fields">
                                <div class="twelve wide field">
                                    <label>SMTP server (only with TLS support)</label>
                                    <div class="ui left icon input">
                                        <input v-model="settings.email_smtp_server" placeholder="Outgoing SMTP server" type="text">
                                        <i aria-hidden="true" class="server icon"></i>
                                    </div>
                                </div>
                                <div class="four wide field">
                                    <label>Port</label>
                                    <div class="ui left icon input">
                                        <input v-model="settings.email_smtp_port" placeholder="Outgoing SMTP server port" min="1" max="65535" type="number">
                                        <i aria-hidden="true" class="lock icon"></i>
                                    </div>
                                </div>
                            </div>
                            <div class="field"><label>SMTP login</label>
                                <div class="ui left icon input">
                                    <input v-model="settings.email_smtp_login" placeholder="Outgoing SMTP server login (e-mail address)" type="text">
                                    <i aria-hidden="true" class="user icon"></i>
                                </div>
                            </div>
                            <div class="field"><label>SMTP password</label>
                                <div class="ui left icon input">
                                    <input v-model="settings.email_smtp_password" placeholder="SMTP password is stored in database in plaintext" type="password">
                                    <i aria-hidden="true" class="lock icon"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="ui fluid card">
                    <div class="content">
                        <div class="field">
                            <div class="ui checkbox">
                                <input v-model="settings.registration_enabled" type="checkbox">
                                <label>New users registration</label>
                            </div>
                        </div>
                    </div>
                </div>
                <button type="submit" class="ui button" role="button" :disabled="!isValid" @submit="{}">Submit</button>
                <span v-if="status === 'error'" class="ui red header"><i aria-hidden="true" class="times icon"></i> Update failed</span>
                <span v-if="status === 'success'" class="ui green header"><i aria-hidden="true" class="check icon"></i> Settings updated</span>
            </form>
        </div>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import NavigationBar from '@/components/NavigationBar.vue';
import { required, email } from 'vuelidate/lib/validators';
import _ from 'lodash';

@Component({
    name: 'Settings',
    components: {
        NavigationBar
    },
    validations () {
        const validators = {
            registration_enabled: { required }
        };
        if (this.settings.email_enabled) {
            Object.assign(validators, {
                email_from: { required, email },
                email_smtp_server: { required },
                email_smtp_port: { required },
                email_smtp_login: { required },
                email_smtp_password: { required }
            });
        }
        return { settings: validators };
    }
})
export default class Settings extends Vue {

        settings = {
            email_enabled: false,
            email_from: '',
            email_smtp_server: '',
            email_smtp_port: 465,
            email_smtp_login: '',
            email_smtp_password: '',
            registration_enabled: false
        }
        status = null;

        get isValid () {
            return !this.$v.$invalid;
        }

        handleSubmit () {
            this.$store.dispatch('setSettings', this.settings);
        }

        onSuccess () {
            this.status = 'success';
        }

        onError () {
            this.status = 'error';
        }

        mounted () {
            this.settings = _.cloneDeep(this.$store.state.settings);
        }

}

</script>
