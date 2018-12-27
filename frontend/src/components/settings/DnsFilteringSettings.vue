<template>
    <form class="ui form" @submit.prevent="handleSubmit">
        <div class="field" v-for="item in settings">
            <div class="ui checkbox">
                <input v-model="item.enabled" type="checkbox">
                <label>{{ item.url }}</label>
            </div>
        </div>
        <div class="field">
            <button type="submit" class="ui button" role="button" @submit="{}">Save</button>
        </div>
    </form>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import _ from 'lodash';

@Component({
    name: 'DnsFilteringSettings'
})
export default class DnsFilteringSettings extends Vue {

    settings = {};

    handleSubmit () {
        this.$store.dispatch('setBlockListSources', this.settings);
    }

    mounted () {
        this.settings = _.cloneDeep(this.$store.state.blockLists);
    }

}
</script>

<style scoped lang="scss">

</style>
