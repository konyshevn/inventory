<template>
  <div class = "catlg-device-list container">
    <div class="fixed-header">
    <h2 v-if="!modal" align="left">{{catlgTitle(status.catlgType, 'plural')}}</h2>
    <b-container class="text-left">
      <catlg-list-control-panel :status="status"></catlg-list-control-panel>
    </b-container>
  </div>
    <smart-table 
      :selected-plural="modal ? false : true"
      :selected.sync="status.selected"
      :dblclick-row="clickRow"
      :on-input-checkbox="selectedInput"
      :sort-by.sync="status.sortBy"
      :sort-asc.sync="status.sortAsc"
      :items="GETcatlg('device')"
      :fields="[
        {key: 'deviceType', label: 'Тип', type: 'text',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'nomenclature', label: 'Наименование', type: 'text',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'serial_num', label: 'Серийный номер', type: 'text'},
        {key: 'inv_num', label: 'Инвентарный номер', type: 'text'},
        {key: 'comment', label: ' Комментарий', type: 'text'},
      ]"
    >
      
    </smart-table>
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import SortHeader from '@/components/common/SortHeader.vue'
import SmartTable from '@/components/common/SmartTable.vue'

import CatlgListControlPanel from '@/components/Catlg/common/ControlPanel/CatlgListControlPanel.vue'
import {EventBus} from '@/components/common/event-bus.js'
var _ = require('lodash');
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';


export default {
  name: 'CatlgDeviceList',
  
  components: {
    SortHeader,
    CatlgListControlPanel,
    SmartTable,
  },

  mixins: [CatlgCommon],
  
  data () {
    return {
      searchText: '',
      status: {
        selected: [],
        catlgType: 'device',
        modal: null,
        items: [],
        itemsFilter: [],
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

    selectedInput: function (value) {
      const vm = this
      if (vm.modal) {
        EventBus.$emit('modalItemSelected', {modalId: vm.modal, id: value, handleOk: false})
      }
    },

    tableSearch: function() {
      const vm = this
      var findItem = false
      var itemsFilter
      if (vm.searchText.length <= 0) {
        itemsFilter = vm.status.items
      } else {
        itemsFilter = _.filter(vm.status.items, function(item){
          findItem = false
          for (let key in item) {
            if (String(item[key]).toLowerCase().indexOf(vm.searchText.toLowerCase()) >= 0) {findItem = true}
          }
          return findItem
        })

      }
      //console.log('tableSearch: itemsFilter', itemsFilter)
      vm.status.itemsFilter = itemsFilter
      
    },
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
    this.FETCHcatlg(['device']);
    vm.status.itemsFilter = vm.GETcatlg('device');
    vm.status.items = vm.GETcatlg('device');
  },

  created: function () {
  },

  
}
</script>

<style scoped>
.catlg-list td:nth-child(1), .catlg-list th:nth-child(1) {
  width: 5%;
}
.catlg-list td:nth-child(2), .catlg-list th:nth-child(2) {
  width: 20%;
}
.catlg-list td:nth-child(3), .catlg-list th:nth-child(3) {
  width: 20%;
}
.catlg-list td:nth-child(4), .catlg-list th:nth-child(4) {
  width: 25%;
}
.catlg-list td:nth-child(5), .catlg-list th:nth-child(5) {
  width: 15%;
}
.catlg-list td:nth-child(6), .catlg-list th:nth-child(6) {
  width: 15%;
}

.catlg-list tbody{
  display:block;
  overflow-y:scroll;
  min-width: 1000px;
  width: 100%;
  height: calc(100vh  - 220px);
}

.catlg-list thead tr{
  display:table;
  width: calc( 100% - 1em ) !important;
  cursor: pointer;
}

.catlg-list tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}

.catlg-list th, .catlg-list td {
padding-top: 0.25rem !important;
padding-bottom: 0.25rem !important;
}

.fixed-header {
  position: -webkit-sticky;
  position: sticky;
  top: 55px;
  z-index: 10;
  background: white;
  padding-top: 10px;
}


</style>