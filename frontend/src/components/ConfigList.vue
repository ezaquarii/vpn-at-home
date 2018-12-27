<template>
    <div class="config-table">
        <table class="ui celled striped table">
            <col width="40%"/>
            <col width="15%"/>
            <col width="15%"/>
            <col width="25%"/>
            <col width="5%"/>
            <thead>
                <tr>
                    <th>{{title}}</th>
                    <th>Created</th>
                    <th>Expires</th>
                    <th>E-Mail</th>
                    <th>
                        <sui-button circular size="mini" color="green" v-bind:class="{ disabled: addDisabled }" icon="plus" @click="onClickedAdd"/>
                    </th>
                </tr>
            </thead>
            <tbody>
                <ConfigListItem v-for="item in items"
                                :item="item"
                                :key="item.id"
                                :emailEnabled="emailEnabled"
                                :deploymentEnabled="deploymentEnabled"
                                :isClient="isClient"
                                :isServer="isServer"/>
            </tbody>
        </table>
    </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import ConfigListItem from '@/components/ConfigListItem';

@Component({
    name: 'ConfigList',
    props: ['items', 'title', 'emailEnabled', 'deploymentEnabled', 'isClient', 'isServer', 'addDisabled', 'onClickedAdd'],
    components: { ConfigListItem }
})
export default class ConfigList extends Vue {

}
</script>

<style scoped lang="scss">
    .config-table {
        margin-top: 16px;
    }
    .center {
        text-align: center !important;
    }
</style>
