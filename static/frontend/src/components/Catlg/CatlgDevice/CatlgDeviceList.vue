<template>
  <div class = "catlg-device-list container">
    <div class="fixed-header2">
      <h2 v-if="!modal" align="left">{{catlgTitle(status.catlgType, 'plural')}}</h2>
      <b-container class="text-left">
        <catlg-list-control-panel :status.sync="status"></catlg-list-control-panel>
      </b-container>
    </div>
    <smart-table 
      :table-padd="250"
      :selected-plural="modal ? false : true"
      :selectAll="modal ? false : true"
      :selected.sync="status.selected"
      :dblclick-row="CatlgClickRow"
      :on-input-checkbox="CatlgSelectedInput"
      :sort-by.sync="status.sortBy"
      :sort-asc.sync="status.sortAsc"
      :items="GETcatlg(status.catlgType)"
      :fields="[
        {key: 'deviceType', label: 'Тип', type: 'text', width: '20%',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'nomenclature', label: 'Наименование', type: 'text', width: '20%',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'serial_num', label: 'Серийный номер', type: 'text', width: '25%',},
        {key: 'inv_num', label: 'Инвентарный номер', type: 'text', width: '15%',},
        {key: 'comment', label: ' Комментарий', type: 'text', width: '15%',},
      ]"
    >
      
    </smart-table>
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import SmartTable from '@/components/common/SmartTable.vue'

import CatlgListControlPanel from '@/components/Catlg/common/ControlPanel/CatlgListControlPanel.vue'
import {EventBus} from '@/components/common/event-bus.js'
var _ = require('lodash');
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';


export default {
  name: 'CatlgDeviceList',
  
  components: {
    CatlgListControlPanel,
    SmartTable,
  },

  mixins: [CatlgCommon],
  
  data () {
    return {
      status: {
        selected: [],
        catlgType: 'device',
        modal: null,
        sortAsc: true,
        sortBy: 'deviceType',
      },
    }
  },

  props: {
    modal: null,
  },

  methods: {
    ...mapActions([
      'FETCHcatlg',
    ]),

  },

  computed: {
    ...mapGetters([
      'GETcatlg',
      'GETcatlgItemLabel',
    ]),
  },
  
  mounted: function () {
    const vm = this
    vm.status.modal = vm.modal
    this.FETCHcatlg([vm.status.catlgType]);
  },

  created: function () {
  },

  
}
</script>

<style scoped>


.fixed-header {
  position: -webkit-sticky;
  position: sticky;
  top: 55px;
  z-index: 10;
  background: white;
  padding-top: 10px;
}


</style>