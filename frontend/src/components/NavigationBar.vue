<template>
    <nav class="ui top fixed menu">
        <div class="ui container">
            <router-link active-class="active" class="item" to="/" exact><i class="icon home"></i> Home</router-link>
            <router-link v-if="isSuperuser" active-class="active" class="item" to="/settings" exact><i class="icon cog"></i> Settings</router-link>
            <a v-if="isSuperuser" class="item" href="/admin/"><i class="icon cogs"></i> Admin</a>
            <a class="item" href="https://www.vultr.com/?ref=7515725" target="_blank"><i class="icon server"></i> Vultr</a>
            <a class="item" href="https://www.patreon.com/ezaquarii" target="_blank"><i class="icon patreon"></i> Support Us</a>
            <div class="right menu">
                <div class="ui item">
                    <span :class="{'superuser': isSuperuser}"><b>{{email}}</b></span>
                </div>
                <div class="ui item no-padding-right">
                    <div class="ui primary button icon compact negative" @click="onClickedLogout"><i class="icon sign-out"></i></div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component({
    name: 'NavigationBar',
    components: {
    }
})
export default class NavigationBar extends Vue {

    onClickedLogout () {
        this.$api.logout(this.onLogoutCompleted.bind(this));
    }

    onLogoutCompleted () {
        this.$store.commit('logout');
        this.$router.push({ path: '/login' });
    }

    get isSuperuser () {
        return this.$store.getters.isSuperuser;
    }

    get email () {
        return this.$store.state.user.email;
    }

}
</script>

<style lang="scss" scoped>
@import "../assets/main.scss";

.superuser {
    color: $red;
}

.no-padding-right {
    padding-right: 0 !important;
}

</style>
