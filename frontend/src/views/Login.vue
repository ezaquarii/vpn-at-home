<template>
    <div class="login top-space">
        <div class="ui grid center aligned">
            <div class="row center aligned">
                <h1 class="ui header green center aligned">Login<br>VPN@Home</h1>
            </div>
            <div class="row">
                <div class="six wide column left aligned">
                     <form class="ui form" @submit.prevent="handleSubmit">
                        <div class="field">
                            <label>Login E-mail</label>
                            <input type="email" name="login" placeholder="E-mail" v-model="login">
                        </div>
                        <div class="field">
                            <label class="">Password</label>
                            <input type="password" name="password" placeholder="Password (min 8 chars)" v-model="password">
                        </div>
                        <button class="ui button" v-bind:disabled="invalid">Login</button>
                    </form>
                </div>
            </div>
            <div v-if="canRegister" class="row center aligned">
                <router-link to="/register">Register</router-link>
            </div>
            <div v-if="error" class="row center aligned">
                Login failed
            </div>
        </div>
    </div>
</template>

<script lang="js">
import { Component, Vue } from 'vue-property-decorator';
import { required, minLength } from 'vuelidate/lib/validators';

@Component({
    components: {
    },
    validations: {
        login: { required },
        password: { required, minLength: minLength(8) }
    }
})
export default class Login extends Vue {

    login = '';
    password = '';
    error = false;

    handleSubmit () {
        this.$api.login(
            this.login,
            this.password,
            () => {
                this.$store.commit('login');
                this.$store.dispatch('hydrate');
                this.$router.push('/');
            },
            () => {
                this.error = true;
            }
        );
    }

    get invalid () {
        return this.$v.$invalid;
    }

    get canRegister () {
        return this.$store.getters.canRegister;
    }

}

</script>

<style lang="css">
    .top-space {
        margin-top: 150px;
    }
</style>
