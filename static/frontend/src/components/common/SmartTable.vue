<template>
  <div>
    <div class="search-input">
      <b-input-group class="mt-3">
      <b-form-input v-model="searchText" placeholder="Поиск" @input.native="tableSearch"></b-form-input>
      <b-input-group-append>
        <b-button variant="light" @click="searchText=''"><font-awesome-icon icon="times"/></b-button>
      </b-input-group-append>
      </b-input-group>
    </div>
    <table class="table table-bordered list">
      <thead>
        <tr>
          <th style="width: 5%"><font-awesome-icon icon="check-square"/></th>
          <sort-header v-for="field in fields" :key="field.key" 
          :field="field" 
          :sort-by="sortBy" 
          :sort-asc="sortAsc"
          :style="tableColWidth(field)"
          >
            {{field.label}}
          </sort-header>
        </tr>
      </thead>
      <tbody :style="tablePaddStyle">
        <tr v-for="item in itemsFilter" :key="item.id"
        @dblclick="dblclickRow(item.id)"
        @click="selectRow(item.id, $event)"
        :class="{'row-selected': isRowSelected(item.id)}">
          <td style="width: 5%">
            <b-form-checkbox
            v-model="selectedLocal"
            :value="item.id"
            @input="onInputCheckbox"
            class="row-checkbox">
            </b-form-checkbox>
          </td>
          <td v-for="field in fields" :key="field.key" :style="tableColWidth(field)">
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
      isInited: false,
      selectedLocal: [],
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
    dblclickRow: {
      type: Function
    },
    onInputCheckbox: {
      type: Function
    },
    selected: {
      type: Array,
      default: [],
    },
    selectedPlural: {
      type: Boolean,
      default: true,
    },
    tablePadd: {
      type: Number,
      default: 200,}
  },

  computed: {
    sortByField: function() {
      const vm = this
      return _.find(vm.fields, {key: vm.sortBy})
    },

    tablePaddStyle: function () {
      const vm = this
      let style = {
        height: `calc(100vh  - ${vm.tablePadd}px)`,
      }
      return style
    },

  },
  
  methods: {

    tableColWidth: function (field){
      const vm = this
      let style = {width: field.width}
      return style
    },

    formatterValue: function(item, field) {
      let value
      if (field.type == 'number') {
        value = Number(field.formatter(item[field.key], field.key))
      } else {
        value = String(field.formatter(item[field.key], field.key))
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

    async sortItemsFilter (field, changeOrder=true) {
      const vm = this 
      console.log('sortItemsFilter: field', field)
      if (changeOrder && (vm.sortBy == field.key)) {
        await vm.$emit('update:sortAsc', !vm.sortAsc)
      } else if (vm.sortBy != field.key) {
        await vm.$emit('update:sortAsc', true)
      }

      var order = vm.sortAsc ? -1 : 1
      
      function compareText(a, b) {
        if(a[field.key] === "" || a[field.key] === null) return 1;
        if(b[field.key] === "" || b[field.key] === null) return -1;
        if(a[field.key] === b[field.key]) return 0;
        return a[field.key] < b[field.key] ? 1 * order : -1 * order;
      }


      function compareFormatter(a, b) {
        let aFormatter = vm.formatterValue(a, field)
        let bFormatter = vm.formatterValue(b, field)

        if(aFormatter === "" || aFormatter === null) return 1;
        if(bFormatter === "" || bFormatter === null) return -1;
        if(aFormatter === bFormatter) return 0;
        return aFormatter < bFormatter ? 1 * order : -1 * order;
      }

      if ('formatter' in field) {
        vm.itemsFilter.sort(compareFormatter);
      } else if (field.type == 'text') {
        vm.itemsFilter.sort(compareText);
      }

      vm.$emit('update:sortBy', field.key)
      /*

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

      if (objType == "TU") {
        data.map(function(value, index){
          value.rowOrder = index + 1
        })
      }
      */    
    },

    selectRow: function (id, event) {
      const vm = this
      var result
      //var selectedLocal = vm.selected
      if (event.srcElement.className == 'custom-control-label') { return }
      if (vm.selectedPlural) {
        let idIndex = vm.selectedLocal.indexOf(id)
        if (idIndex >= 0) {
          vm.selectedLocal.splice(idIndex, 1)
        } else {
          vm.selectedLocal.push(id)
        }
        //result = (idIndex >= 0) ? vm.selectedLocal.splice(idIndex, 1) : vm.selectedLocal.push(id)
      } else {
        if (vm.selectedLocal == id) {
          vm.selectedLocal = []
        } else {
          vm.selectedLocal = [id]
        }
        //result = (vm.selectedLocal == id) ? null : [id]
      }
      vm.$emit('update:selected', vm.selectedLocal)
    },

    isRowSelected: function (id) {
      const vm = this
      let result = false
      let idIndex = vm.selectedLocal.indexOf(id)
      result = (idIndex >= 0) ? true : false
      return result
    },
  },

  watch: {
    itemsFilter: {
      handler(){
        const vm = this
        if ((vm.itemsFilter.length > 0) && !(vm.isInited)) {
          vm.sortItemsFilter(vm.sortByField, false)
          vm.isInited = true
        }
      },
      immediate: true,
    },
    searchText: {
      handler(){
        const vm = this
        if (vm.searchText == '') {
          vm.itemsFilter = vm.items
          vm.sortItemsFilter(vm.sortByField, false)
        }
      }
    },

  },

  mounted: function () {
    const vm = this
    vm.$root.$on('sort-table', event => {
      vm.sortItemsFilter(event)
    })
  },

  created: function () {
  },

  
}
</script>

<style scoped>
.search-input {
  width: 300px;
  float: right;
}

.row-selected {
background-color: #f2f2f2;
color: #000000;
font-weight: bold;
}

.list tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}

.list th, .list td {
padding: 0.25rem !important;
}

.list tbody {
  display:block;
  overflow-y:scroll;
  min-width: 1000px;
  width: 100%;
}

.list tbody tr {
  display:table;
  width:100%;
  table-layout:fixed;
}

.list thead tr {
  display:table;
  width: calc( 100% - 1em ) !important;
  cursor: pointer;
}



</style>