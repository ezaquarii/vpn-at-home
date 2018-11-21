<template>
    <div class="config-table">
        <table class="ui celled striped table">
            <col width="25%"/>
            <col width="20%"/>
            <col width="20%"/>
            <col width="20%"/>
            <col width="5%"/>
            <col v-if="emailEnabled" width="5%"/>
            <col v-if="deploymentEnabled" width="5%"/>
            <thead>
                <tr>
                    <th>{{title}}</th>
                    <th>Created</th>
                    <th>Expires</th>
                    <th>E-Mail</th>
                    <th class="center"><i aria-hidden="true" class="icon download"></i></th>
                    <th v-if="emailEnabled" class="center"><i aria-hidden="true" class="icon mail"></i></th>
                    <th v-if="deploymentEnabled" class="center"><i aria-hidden="true" class="icon play"></i></th>
                </tr>
            </thead>
            <tbody>
                <ConfigListItem v-for="item in items"
                                :item="item"
                                :key="item.id"
                                :emailEnabled="emailEnabled"
                                :deploymentEnabled="deploymentEnabled"/>
            </tbody>
        </table>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import ConfigListItem from '@/components/ConfigListItem';

@Component({
    name: 'ConfigList',
    props: ['items', 'title', 'emailEnabled', 'deploymentEnabled'],
    components: { ConfigListItem }
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
