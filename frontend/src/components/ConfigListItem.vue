<template>
    <tr>
        <td>{{item.name}}</td>
        <td>{{relativeCreated}}</td>
        <td>{{relativeValid}}</td>
        <td>{{item.email}}</td>
        <td class="center">
            <span><a v-bind:href="item.download_url"><i aria-hidden="true" class="icon download"></i> </a></span>
        </td>
        <td v-if="emailEnabled" class="center">
            <span v-if="canSendEmail">
                <a v-if="!isSending" v-bind:href="item.download_url" @click.prevent="sendMail"><i aria-hidden="true" class="icon mail"></i> </a>
                <div v-if="isSending" class="ui active inline tiny loader"></div>
            </span>
            <span v-else>
                <i aria-hidden="true" class="icon ban"></i>
            </span>
        </td>
    </tr>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import moment from 'moment';

@Component({
    name: 'ConfigListItem',
    props: ['item', 'emailEnabled'],
})
export default class ConfigListItem extends Vue {

    get relativeCreated () {
        return moment(this.item.created).fromNow();
    }

    get relativeValid () {
        return moment(this.item.validity_end).fromNow();
    }

    get isSending () {
        return this.$store.getters.isSendingClientConfigEmail(this.item.id);
    }

    get canSendEmail () {
        return this.$store.getters.canSendEmail(this.item.email);
    }

    sendMail() {
        console.log('ConfigListItem.sendMail()', this.item);
        this.$store.dispatch('sendClientConfigEmail', this.item.id);
    }

};
</script>

<style scoped lang="scss">
    .center {
        text-align: center !important;
    }
</style>
