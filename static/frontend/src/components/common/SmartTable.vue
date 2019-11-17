<template>
  <div>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th><font-awesome-icon icon="check-square"/></th>
          <sort-header v-for="field in fields" :key="field.key" :field="field">
            {{field.label}}
          </sort-header>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in itemsFilter" :key="item.id">
          <td>
            <b-form-checkbox
            v-model="selected"
            :value="item.id"
            class="row-checkbox">
            </b-form-checkbox>
          </td>
          <td v-for="field in fields" :key="field.key">
            <span v-if="('formatter' in field)">{{formatterValue(item, field)}}</span>
            <span v-else>{{item[field.key]}}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import SortHeader from '@/components/common/SortHeader2.vue'
import {EventBus} from '@/components/common/event-bus.js'
var _ = require('lodash');

import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';


export default {
  name: 'SmartTable',
  
  components: {
    SortHeader,
  },

  mixins: [],
  
  data () {
    return {
      itemsFilter: this.items,
      searchText: '',
      selected: [],
      isInited: false,
    }
  },

  props: {
    items: Array,
    fields: Array,
    sortBy: String,
    sortAsc: {
      type: Boolean,
      default: true,
    },
  },

  computed: {
  },
  
  methods: {

    formatterValue: function(item, field) {
      return field.formatter(item[field.key], field.key)
    },

    itemValue: function (item, field) {
      const vm = this
      var value
      if ('formatter' in field){
        value = field.formatter(item[field.key], field.key)
      } else {
        value = item[field.key]
      }
      if (value == undefined) {
        value = ''
      }
      return value
    },

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

    sortItemsFilter: function(field) {
//    sortItemsFilter: (state, [objType, field, fieldType, changeOrder = true]) => {
      const vm = this 
      console.log('sortItemsFilter: field', field) 
      console.log('sortItemsFilter: sortAsc', vm.sortAsc) 
      var order = vm.sortAsc ? -1 : 1

      function compareTUrowText(a, b) {
        //console.log('compareTUrowText: a, b', a, b)
        if(a[field.key] === "" || a[field.key] === null) return 1;
        if(b[field.key] === "" || b[field.key] === null) return -1;
        if(a[field.key] === b[field.key]) return 0;
        return a[field.key] < b[field.key] ? 1 * order : -1 * order;
      }

      vm.itemsFilter.sort(compareTUrowText);

      /*
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
      */    



    },
  },

  watch: {
    itemsFilter: {
      handler(){
        var vm = this
        if ((vm.itemsFilter.length > 0) && !(vm.isInited)) {
          //vm.sortItemsFilter(vm.fields[2])
          vm.isInited = true
        }
      },
      immediate: true,
    }

  },

  mounted: function () {
    const vm = this
    vm.$root.$on('sort-table', event => {
      vm.sortItemsFilter(event)
    })
    vm.$root.$on('switch-sort-order', () => {
      vm.$emit('update:sortAsc', !vm.sortAsc)
    })

  },

  created: function () {
  },

  
}
</script>

<style scoped>



</style>