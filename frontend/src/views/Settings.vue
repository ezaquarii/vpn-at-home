<template>
    <div class="settings">
        <sui-tab :menu="{ vertical: true, fluid: true, tabular: true }">
            <sui-tab-pane icon="mail" title="E-Mail">
                <EmailSettings/>
            </sui-tab-pane>

            <sui-tab-pane icon="user" title="Registration">
                <RegistrationSettings/>
            </sui-tab-pane>

            <sui-tab-pane icon="filter" title="DNS filtering">
                <DnsFilteringSettings/>
            </sui-tab-pane>

            <sui-tab-pane icon="key" title="SSH keys">
                <SshKeysSettings/>
            </sui-tab-pane>
        </sui-tab>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import EmailSettings from '@/components/settings/EmailSettings';
import RegistrationSettings from '@/components/settings/RegistrationSettings';
import DnsFilteringSettings from '@/components/settings/DnsFilteringSettings';
import SshKeysSettings from '@/components/settings/SshKeysSettings';

@Component({
    name: 'Settings',
    components: {
        EmailSettings,
        RegistrationSettings,
        DnsFilteringSettings,
        SshKeysSettings
    }
})
export default class Settings extends Vue {
}

</script>

<style scoped lang="scss">
    .settings {
        padding-top: 16px;
    }
</style>
