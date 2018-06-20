<template>
    <div class="config-table">
        <table class="ui celled striped table">
            <col width="25%"/>
            <col width="20%"/>
            <col width="20%"/>
            <col width="25%"/>
            <col width="5%"/>
            <col v-if="emailEnabled" width="5%"/>
            <thead>
            <tr>
            <th>{{title}}</th>
            <th>Created</th>
            <th>Expires</th>
            <th>E-Mail</th>
            <th class="center"><i aria-hidden="true" class="icon download"></i></th>
            <th v-if="emailEnabled" class="center"><i aria-hidden="true" class="icon mail"></i></th>
            </tr></thead>
            <tbody>
                <ConfigListItem v-for="item in items" :item="item" v-bind:emailEnabled="emailEnabled"/>
            </tbody>
        </table>
    </div>
</template>

<script>
import { Component, Prop, Vue } from 'vue-property-decorator';
import ConfigListItem from '@/components/ConfigListItem';

@Component({
    name: 'ConfigList',
    props: ['items', 'title', 'emailEnabled'],
    components: {ConfigListItem}
})
export default class ConfigList extends Vue {}
</script>

<style scoped lang="scss">
    .config-table {
        margin-top: 16px;
    }
    .center {
        text-align: center !important;
    }
</style>
