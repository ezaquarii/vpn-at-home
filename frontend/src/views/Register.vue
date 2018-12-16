<template>
    <div class="login top-space">
        <div class="ui grid center aligned">
            <div class="row center aligned">
                <h1 class="ui header green center aligned">Register<br>VPN@Home</h1>
            </div>
            <div class="row">
                <div class="six wide column left aligned">
                    <form class="ui form" @submit.prevent="handleSubmit">
                        <div class="field">
                            <label>Registration E-mail</label>
                            <input type="email" name="login" placeholder="E-mail" v-model="login">
                        </div>
                        <div class="field">
                            <label class="">Password</label>
                            <input type="password" name="password" placeholder="Password (min 8 chars)" v-model="password">
                        </div>
                        <button class="ui button" v-bind:disabled="invalid">Register</button>
                    </form>
                </div>
            </div>
            <div class="row center aligned">
                <router-link to="/login">Login</router-link>
            </div>
            <div v-if="error" class="row center aligned">
                Registration failed
            </div>
        </div>
    </div>
</template>

<script lang="js">
import { Component, Vue } from 'vue-property-decorator';
import { required, email, minLength } from 'vuelidate/lib/validators';

@Component({
    components: {
    },
    validations: {
        login: { required, email },
        password: { required, minLength: minLength(8) }
    }
})
export default class Login extends Vue {

    login = '';
    password = '';
    error = false;

    handleSubmit () {
        this.$api.register(
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

}
</script>

<style lang="css">
    .top-space {
        margin-top: 150px;
    }
</style>
