<template>
    <div class="ui grid center aligned">
        <div class="row center aligned">
            <h1>Welcome to OpenVPN@Home</h1>
        </div>
        <div class="row center aligned">
            <h3>The app requires some configuration</h3>
        </div>
        <div class="row">
            <div class="ten wide column left aligned">
                <div class="issue">
                    Default, sane config can be bootstrapped with a single command (must be run from <span class="important">root</span> account):
                    <div class="example">
                        # {{bootstrapSh}} my@email.com<br>
                        Provide admin password: (no echo)<br>
                        Repeat the password: (no echo)<br>
                        ... bootstrapping output...
                    </div>
                    If you want to modify the configuration, please follow the guide below. Don't forget
                    that <span class="important">you need to restart the server</span> to reload updated config.
                    <span class="shell">bootstrap.sh</span> will do it for you.
                    <p class="note">
                        For all below examples,
                        <span class="shell">${ROOT}</span> equals to <span class="shell">{{deploymentDir}}</span>,
                        where the app is currently deployed.
                    </p>
                </div>
                <div class="issue">
                    <div v-if="hasSettingsFile">
                        <h2><i aria-hidden="true" class="green circular inverted check icon"> </i> Has settings file</h2>
                        <p>
                            Configuration file <span class="shell">settings.json</span> is present in deployment directory.
                        </p>
                    </div>
                    <div v-else>
                        <h2><i aria-hidden="true" class="red circular inverted times icon"> </i> No settings file yet</h2>
                        <p>
                            OpenVPN@Home is configured through a JSON <span class="shell">settings.json</span> file placed in deployment
                            directory. File can be generated with a managemen command:
                            <p class="example">
                                # ${ROOT}/backend/manage.py configure<br>
                                cat settings.json
                            </p>
                            You can also check <span class="shell">./manage.py configure --help</span> for details.
                        </p>
                    </div>
                </div>

                <div class="issue">
                    <div v-if="isConfigured">
                        <h2><i aria-hidden="true" class="green circular inverted check icon"> </i> Settings reviewed and accepted</h2>
                        <p>Settings file is reviewed and accepted.</p>
                    </div>
                    <div v-else>
                        <h2><i aria-hidden="true" class="red circular inverted times icon"> </i> You must review and accept settings first</h2>
                        <p>
                            Settings file must be reviewed and accepted before proceeding. Open <span class="shell">settings.json</span> in
                            your favorite editor and set <span class="shell">configured</span> flag to <span class="shell">true</span>.
                            Most interesting part is your <span class="shell">database</span> field.
                            <div class="example">
                            {<br>&nbsp;&nbsp;...<br>&nbsp;&nbsp;"configured": "true"<br>&nbsp;&nbsp;"database": {...}<br>
                        &nbsp;&nbsp;...<br>}
                            </div>
                        </p>
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
                        <p>
                            Database must be initialized (migrated) before the app is usable. Use standard Django migration utility.
                            <div class="example">
                                # ${ROOT}/backend/manage.py migrate
                            </div>
                        </p>
                    </div>
                </div>

                <div class="issue">
                    <div v-if="hasAdminUser">
                        <h2><i aria-hidden="true" class="green circular inverted check icon"> </i> Admin user is configured</h2>
                        <p>
                            Admin user is configured, has properly set password and is activated.
                        </p>
                    </div>
                    <div v-else>
                        <h2><i aria-hidden="true" class="red circular inverted times icon"> </i> Admin user is not configured yet</h2>
                        <p>
                            Admin user is a must. You want to use your real e-mail address and sane password for this one.
                            <div class="example">
                                # ${ROOT}/backend/manage.py my@email.com my-secret-password
                            </div>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    computed: {
        hasSettingsFile() {
            return this.$store.state.status.appNotReady.has_settings_file;
        },

        isConfigured() {
            return this.$store.state.status.appNotReady.is_configured && this.hasSettingsFile;
        },

        isDatabaseInitialized() {
            return this.$store.state.status.appNotReady.is_migrated;
        },

        managePy() {
            return this.$store.state.status.appNotReady.manage_py
        },

        bootstrapSh() {
            return this.$store.state.status.appNotReady.bootstrap_sh;
        },

        deploymentDir() {
            return this.$store.state.status.appNotReady.deployment_dir;
        }
    },
}

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

    .shell {
        background: $lightgray;
        padding: 0.2em;
        border-radius: 0.2em;
        font-weight: bold;
        font-family: monospace, monospace;
    }


</style>
