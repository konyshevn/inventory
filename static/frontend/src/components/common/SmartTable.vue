<template>
  <div>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th><font-awesome-icon icon="check-square"/></th>

          <sort-header :obj-type="{catlg: 'device'}" field-type="widget" sort-field="deviceType">
            Тип
          </sort-header>
          <sort-header :obj-type="{catlg: 'device'}" field-type="text" sort-field="label">
            Наименование
          </sort-header>
          <sort-header :obj-type="{catlg: 'device'}" field-type="text" sort-field="serial_num">
            Серийный номер
          </sort-header>
          <sort-header :obj-type="{catlg: 'device'}" field-type="text" sort-field="inv_num">
            Инвентарный номер
          </sort-header>
          <sort-header :obj-type="{catlg: 'device'}" field-type="text" sort-field="comment">
            Комментарий
          </sort-header>

        </tr>
      </thead>
      <tbody>
        <tr v-for="device in status.itemsFilter" :key="device.id" 
        @dblclick="clickRow(device.id, $event)" 
        @click="selectRow(device.id, $event)"
        :class="{'row-selected': isRowSelected(device.id)}">
          <td>
            <b-form-checkbox
            v-model="status.selected"
            :value="device.id"
            @input="selectedInput"
            class="row-checkbox">
            </b-form-checkbox>
          </td>
          <td>
            {{GETcatlgItemLabel('deviceType', device.deviceType)}}
          </td>
          <td>
            {{GETcatlgItemLabel('nomenclature', device.nomenclature)}}
          </td>
          <td>
            {{device.serial_num}}
          </td>
          <td>
            {{device.inv_num}}
          </td>
          <td>
            {{device.comment}}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import SortHeader from '@/components/common/SortHeader.vue'
import {EventBus} from '@/components/common/event-bus.js'
var _ = require('lodash');

import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';


export default {
  name: 'CatlgDeviceList',
  
  components: {
    SortHeader,
  },

  mixins: [],
  
  data () {
    return {
      itemsFilter: [],
      searchText: '',
    }
  },

  props: {
    items: [],
    fields: [],
  },

  computed: {
  },
  
  methods: {

    tableSearch: function() {
      const vm = this
      var findItem
      var itemsFilter
      if (vm.searchText.length <= 0) {
        itemsFilter = vm.items
      } else {
        itemsFilter = _.filter(vm.items, function(item){
          findItem = false
          for (let key in item) {
            if (String(item[key]).toLowerCase().indexOf(vm.searchText.toLowerCase()) >= 0) {findItem = true}
          }
          return findItem
        })
      }
      vm.itemsFilter = itemsFilter
    },

    sortItemsFilter: (state, [objType, field, fieldType, changeOrder = true]) => {
      var status, data 
      if (objType == "TU") {
        status = state.currentDoc.status.tableUnit.sort
        data = state.currentDoc.data.table_unit
      } else if (objType == "docs") {
        status = state.docs.status.sort
        data = state.docs.data
      } else if ('catlg' in objType) {
        status = state.catlgs[objType.catlg].status.sort
        data = state.catlgs[objType.catlg].data
      }

      if (status.field != field) {
        status.order = -1
      }
      if (changeOrder) {
        status.order *= -1
      }
      status.field = field
      status.fieldType = fieldType
      var order = status.order

      function compareTUrowWidget(a, b) {
        if (!a[field]) return 1;
        if (!b[field]) return -1;

        
        let catlgItemA = _.find(state.catlgs[field]['data'], {id: a[field]})
        let catlgItemB = _.find(state.catlgs[field]['data'], {id: b[field]})
        var aLabel = catlgItemA.label
        var bLabel = catlgItemB.label
        return aLabel < bLabel ? -1 * order : 1 * order;
      }

      function compareTUrowNumber(a, b) {
        return Number(a[field]) < Number(b[field]) ? -1 * order : 1 * order;
      }

      function compareTUrowText(a, b) {
        if(a[field] === "" || a[field] === null) return 1;
        if(b[field] === "" || b[field] === null) return -1;
        if(a[field] === b[field]) return 0;
        return a[field] < b[field] ? -1 * order : 1 * order;
      }
      
      if (fieldType == 'widget') {
        data.sort(compareTUrowWidget);
      } else if (fieldType == 'number') {
        data.sort(compareTUrowNumber);
      } else if (fieldType == 'text') {
        data.sort(compareTUrowText);
      }

      if (objType == "TU") {
        data.map(function(value, index){
          value.rowOrder = index + 1
        })
      }
    },
  },

  mounted: function () {
    const vm = this
    vm.itemsFilter = vm.items
  },

  created: function () {
  },

  
}
</script>

<style scoped>



</style>