<template>
    <div class="ui grid center aligned">
        <div class="row center aligned">
            <h1 class="title">Welcome to VPN@Home</h1>
        </div>
        <div class="row center aligned">
            <h3>The app requires some configuration</h3>
        </div>
        <div class="row">
            <div class="ten wide column left aligned">
                <div class="issue">
                    <div class="para">
                        Default, sane config can be bootstrapped with a single <span class="shell">init.sh</span> command.
                        Make sure you run it in the application working directory and as the application user:
                        <div class="example">
                            $ whoami<br>
                            {{user}}<br>
                            $ cd {{workingDir}}<br>
                            $ {{initSh}}<br>
                        </div>
                    </div>
                    <div class="para">
                    Application is initialized in <span class="shell">{{workingDir}}/data</span>, which will contain
                    everything the app needs to run. If you want to perform manual configuration, please follow the guide below.
                    Don't forget that <span class="important">you need to restart the server</span> to reload updated config.
                    </div>
                    <div class="para">
                        You can activate <i>virtual environement</i> to save yourself typing full paths:
                        <div class="example">
                            $ source {{virtualEnvDir}}/bin/activate<br>
                            (env) $ manage.py<br>
                            ...
                        </div>
                    </div>
                </div>

                <div class="issue">
                    <h2><i aria-hidden="true" class="green circular inverted info icon"> </i> Orientation</h2>
                    Here are some facts that you might find useful when trouble-shooting the app installation:
                    <div>
                        <table class="ui very basic collapsing celled table">
                            <tbody>
                                <tr>
                                    <td><b>User running the app</b></td>
                                    <td>{{user}}</td>
                                </tr>
                                <tr>
                                    <td><b>Working directory</b></td>
                                    <td>{{workingDir}}</td>
                                </tr>
                                <tr>
                                    <td><b>App data directory</b></td>
                                    <td>{{workingDir}}/data</td>
                                </tr>
                                <tr>
                                    <td><b>Python virtual environment</b></td>
                                    <td>{{virtualEnvDir}}</td>
                                </tr>
                                <tr>
                                    <td><b>App supplied scripts</b></td>
                                    <td>{{virtualEnvDir}}/bin</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="para">
                        Data directory contains everything you need to backup and restore application state. Just
                        copy it and keep safe. When you move the app to a new place, just restore it and you'll be
                        ready to go. No fancy database dump/restoration is needed.
                    </div>
                </div>

                <div class="issue">
                    <div v-if="hasSettingsFile">
                        <h2><i aria-hidden="true" class="green circular inverted check icon"> </i> Has settings file</h2>
                        <p>
                            Configuration file <span class="shell">settings.json</span> is present in th deployment directory.
                        </p>
                    </div>
                    <div v-else>
                        <h2><i aria-hidden="true" class="red circular inverted times icon"> </i> No settings file yet</h2>
                        <div>
                          OpenVPN@Home is configured through a JSON <span class="shell">settings.json</span> file placed in deployment
                          directory. File can be generated with a management command:
                          <p class="example">
                            $ {{virtualEnvDir}}/bin/manage.py configure<br>
                            cat data/settings.json
                          </p>
                          You can also check <span class="shell">manage.py configure --help</span> for details.
                        </div>
                    </div>
                </div>

                <div class="issue">
                    <div v-if="isEmailConfigured">
                        <h2><i aria-hidden="true" class="green circular inverted check icon"> </i> E-mail configured</h2>
                        <p v-if="isEmailEnabled">E-mail is <span class="green bold">enabled</span> and configured.</p>
                        <p v-else>E-mail is <span class="red bold">disabled.</span> You won't receive error logs nor you can send config files.</p>
                    </div>
                    <div v-else>
                        <h2><i aria-hidden="true" class="red circular inverted times icon"> </i> You must configure e-mail</h2>
                        <div>
                            E-mail is <span class="green bold">enabled</span> but not fully configured yet. If you don't want to use
                            e-mail, set <span class="shell">enabled</span> to <span class="shell">false</span> and you can skip the configuration.
                            Open <span class="shell">settings.json</span> and fill email related fields:
                            <div class="example">
                                {<br>&nbsp;&nbsp;...<br>
                                    &nbsp;&nbsp;"email": {<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;"enabled": <i>true / false</i>,<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;"server_from": <i>e-mail showing in From:</i>,<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;"admin_emails": <i>[list of e-mails to send crash logs to]</i><br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;"smtp": {<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"server": <i>"your.smtp.host"</i>,<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"port": <i>TLS port</i>,<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"user": <i>most likely your e-mail address</i>,<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"password": <i>password</i>,<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;}<br>
                                &nbsp;&nbsp;...<br>}
                            </div>
                            Your <span class="shell">server_from</span> should be set to a valid e-mail address. Many SMTP servers
                            will refuse to send e-mail with bogus <i>From</i> field. <span class="important">You must restart the service to pick up new configuration.</span>
                        </div>
                    </div>
                </div>

                <div class="issue">
                    <div v-if="isDatabaseInitialized">
                        <h2><i aria-hidden="true" class="green circular inverted check icon"> </i> Database is ready</h2>
                        <p>
                            Database is initialized and up-to-date.
                        </p>
                    </div>
                    <div v-else>
                        <h2><i aria-hidden="true" class="red circular inverted times icon"> </i> Database is not initialized (migrated) yet</h2>
                        <div>
                            Database must be initialized (migrated) before the app is usable. Use standard Django migration utility.
                            <div class="example">
                                $ {{virtualEnvDir}}/bin/manage.py migrate
                            </div>
                        </div>
                    </div>
                </div>

                <div class="issue">
                    <div v-if="hasAdminUser">
                        <h2><i aria-hidden="true" class="green circular inverted check icon"> </i> Admin user is configured</h2>
                        <p>
                            Admin user is configured, has a password and is activated.
                        </p>
                    </div>
                    <div v-else>
                        <h2><i aria-hidden="true" class="red circular inverted times icon"> </i> Admin user is not configured yet</h2>
                        <div>
                            Admin user is a must. You want to use your real e-mail address and sane password for this one.
                            <div class="example">
                                $ {{virtualEnvDir}}/bin/manage.py set_admin my@email.com my-secret-password
                            </div>
                        </div>
                    </div>
                </div>

                <div class="issue">
                    <div v-if="isConfigured">
                        <h2><i aria-hidden="true" class="green circular inverted check icon"> </i> Settings reviewed and accepted</h2>
                        <p>Settings file is reviewed and accepted.</p>
                    </div>
                    <div v-else>
                        <h2><i aria-hidden="true" class="red circular inverted times icon"> </i> You must review and accept settings first</h2>
                        <div>
                            Settings file must be reviewed and accepted before proceeding. Open <span class="shell">settings.json</span> in
                            your favorite editor and set <span class="shell">configured</span> flag to <span class="shell">true</span>.
                            Most interesting part is your <span class="shell">email</span> section.
                            <div class="example">
                                {<br>&nbsp;&nbsp;...<br>&nbsp;&nbsp;"configured": "true"<br>&nbsp;&nbsp;...<br>&nbsp;&nbsp;"email": { ... }<br>&nbsp;&nbsp;...<br>}
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>

export default {
    computed: {
        hasSettingsFile () {
            return this.$store.state.status.appNotReady.has_settings_file;
        },

        isConfigured () {
            return this.$store.state.status.appNotReady.is_configured && this.hasSettingsFile;
        },

        isDatabaseInitialized () {
            return this.$store.state.status.appNotReady.is_migrated;
        },

        managePy () {
            return this.$store.state.status.appNotReady.manage_py;
        },

        initSh () {
            return this.$store.state.status.appNotReady.init_sh;
        },

        deploymentDir () {
            return this.$store.state.status.appNotReady.deployment_dir;
        },

        hasAdminUser () {
            return this.$store.state.status.appNotReady.has_active_admin;
        },

        isEmailConfigured () {
            return this.$store.state.status.appNotReady.is_email_configured;
        },

        isEmailEnabled () {
            return this.$store.state.status.appNotReady.is_email_enabled;
        },

        virtualEnvDir () {
            return this.$store.state.status.appNotReady.virtual_env;
        },

        workingDir () {
            return this.$store.state.status.appNotReady.working_dir;
        },

        user () {
            return this.$store.state.status.appNotReady.user;
        }
    }
};

</script>

<style scoped lang="scss">
    @import "assets/main";

    .issue {
        margin: 24px;
    }

    .ui.label {
        font-family: monospace, monospace;
    }

    .example {
        margin-top: 1em;
        margin-bottom: 1em;
        border-radius: 12px;
        padding: 10px;
        background: $terminal-bg;
        color: greenyellow;
        white-space: normal;
        font-family: monospace, monospace;
        font-weight: bold;
    }

    .important {
        color: orangered;
        font-weight: bold;
    }

    .bold {
        font-weight: bold;
    }

    .red {
        color: orangered;
    }

    .green {
        color: green;
    }

    .note {
        margin-top: 1em;
        margin-bottom: 1em;
        border-radius: 12px;
        padding: 10px;
        background: lightyellow;
        color: black;
        white-space: normal;
        border-style: solid;
        border-width: 1px;
        border-color: orange;
    }

    .para {
        margin-top: 0.5em;
    }

    .title {
        margin-top: 2em;
    }

</style>
