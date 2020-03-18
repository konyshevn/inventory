<template>
  <div>
    <div class="search-input">
      <b-input-group>
      <b-form-input v-model="searchText" placeholder="Поиск"></b-form-input>
      <b-input-group-append>
        <b-button variant="light" @click="searchText=''" class="search-button"><font-awesome-icon icon="times"/></b-button>
      </b-input-group-append>
      </b-input-group>
    </div>
    <table class="table table-bordered list" :style="tableWidth">
      <thead>
        <tr>
          <th v-if="!disableSelect" style="width: 5%" @click="selectAllRows">
            <font-awesome-icon icon="check-square"/>
          </th>
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
        <tr v-for="item in itemsFilterActive" :key="item.id" :id="`${uid}-${item.id}`"
        @dblclick="dblclickRow(item.id)"
        @click="selectRow(item.id, $event)"
        :class="{'row-selected': isRowSelected(item.id)}">
          <td v-if="!disableSelect" style="width: 5%">
            <input type="checkbox" 
            :id="item.id" 
            v-model="selectedLocal"
            :value="item.id"
            class="row-checkbox"
            @input="onInputCheckbox"
            >

          </td>
          <td v-for="field in fields" :key="field.key" :style="tableColWidth(field)">
            <span v-if="('formatter' in field)">{{formatterValue(item, field)}}</span>
            <span v-else-if="field.type == 'boolean'"> 
              <span v-if="item.active"><font-awesome-icon icon="check"/></span>
              <span v-else></span>
            </span>
            <catlg-widget v-else-if="field.type == 'widget'" 
            :widget-type="field.widgetSettings.type"
            :required="('required' in field.widgetSettings) ? field.widgetSettings.required : null"
            :model.sync="item[field.key]"
            >
            </catlg-widget>
            <b-form-input v-else-if="field.type == 'input-number'" 
            v-model="item[field.key]" 
            type="number" 
            number
            >
            </b-form-input>
            <b-form-input v-else-if="field.type == 'input-text'"
            v-model="item[field.key]"
            type="text">
            </b-form-input>

            <span v-else>{{item[field.key]}}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/* eslint-disable no-console */
import SortHeader from '@/components/common/SortHeader.vue'
var _ = require('lodash');

import Vue from 'vue';
import { mapGetters } from 'vuex';

export default {
  name: 'SmartTable',
  
  components: {
    SortHeader,
    CatlgWidget: () => import('@/components/Catlg/common/Widget/CatlgWidget.vue'),

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
    items:  {
      type: Array,
      default: () => {return []},
    },
    fields:{
      type: Array,
      default: () => {return []},
    },
    sortBy: {
      type: String,
      default: '',
    },
    sortAsc: {
      type: Boolean,
      default: true,
    },
    dblclickRow: {
      type: Function,
      default: () => {return},
    },
    onInputCheckbox: {
      type: Function,
      default: () => {return},
    },
    selected: {
      type: Array,
      default: () => {return []},
    },
    selectedPlural: {
      type: Boolean,
      default: true,
    },
    selectAll: {
      type: Boolean,
      default: true,
    },
    tablePadd: {
      type: Number,
      default: 200,
    },
    minWidth: {
      type: Number,
      default: 1000,
    },
    maxWidth: {
      type: Number,
      default: 1400,
    },
    selectRowClick: {
      type: Boolean,
      default: true,
    },
    disableSelect: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    ...mapGetters([
      'GETcatlgItemLabel',
    ]),

    sortByField: function() {
      const vm = this
      return _.find(vm.fields, {key: vm.sortBy}) || ''
    },

    tablePaddStyle: function () {
      const vm = this
      let padd = vm.selectAll ? vm.tablePadd : vm.tablePadd + 100
      let style = {
        height: `calc(100vh  - ${padd}px)`,
      }
      return style
    },

    tableWidth: function () {
      const vm = this
      let style = {
        maxWidth: `${vm.maxWidth}px`,
        minWidth: `${vm.minWidth}px`,
      }
      return style
    },

    uid: function () {
      return String(this._uid)
    },

    itemsFilterActive: function () {
      const vm = this
      let result = []
      if (Array.isArray(vm.items)){
        let itemsFilter = vm.tableSearch2()
        if (vm.sortByField) {itemsFilter = vm.sortItemsFilter2(itemsFilter, vm.sortByField, vm.sortAsc)}
        if (itemsFilter) {result = itemsFilter.filter(item => !(('DELETE' in item) && (item.DELETE)))}
      }

      return result
    },

  },
  
  methods: {
    tableColWidth: function (field){
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



    tableSearch2: function() {
      const vm = this
      var findItem
      var itemsFilter
      var formatterSearch, field, itemValue
      if (vm.searchText.length <= 0) {
        itemsFilter = vm.items
      } else {
        itemsFilter = _.filter(vm.items, function(item){
          findItem = false
          for (let key in item) {
            if (_.findIndex(vm.fields, {key: key}) < 0) {continue}
            formatterSearch = true
            field = _.find(vm.fields, {key: key})
            if ('formatterSearch' in field){
              formatterSearch = field['formatterSearch']
            }
            if (('formatter' in field) && formatterSearch) {
              itemValue = vm.formatterValue(item, field)
            } else if (field.type == 'widget') {
              itemValue = vm.GETcatlgItemLabel(field.widgetSettings.type, item[key])
            } else {
              itemValue = item[key]
            }
            if (String(itemValue).toLowerCase().indexOf(vm.searchText.toLowerCase()) >= 0) {findItem = true}
          }
          return findItem
        })
      }
      return itemsFilter
    },

    sortItemsFilter2: function (itemsFilter, field, sortAsc) {
      const vm = this
      if (itemsFilter.length == 0) {return []}
      var order = sortAsc ? -1 : 1
      let formatterSort = true
      if ('formatterSort' in field) {
        formatterSort = field.formatterSort
      }
   
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

      function compareWidget(a, b) {
        if (!a[field.key]) return 1;
        if (!b[field.key]) return -1;
        var aLabel = vm.GETcatlgItemLabel(field.widgetSettings.type, a[field.key])
        var bLabel = vm.GETcatlgItemLabel(field.widgetSettings.type, b[field.key])
        return aLabel < bLabel ? 1 * order : -1 * order;
      }

      function compareNumber(a, b) {
        return Number(a[field.key]) < Number(b[field.key]) ? 1 * order : -1 * order;
      }

      let itemsFilterSort = _.cloneDeep(itemsFilter)
      if (('formatter' in field) && formatterSort) {
        itemsFilterSort.sort(compareFormatter);
      } else if (field.type == 'text' || field.type == 'boolean' || field.type == 'input-text') {
        itemsFilterSort.sort(compareText);
      } else if (field.type == 'number' || field.type == 'input-number') {
        itemsFilterSort.sort(compareNumber);
      } else if (field.type == 'widget') {
        itemsFilterSort.sort(compareWidget);
      }

      if ('rowOrder' in itemsFilterSort[0]) {
        itemsFilterSort.map(function(value, index){
          value.rowOrder = index + 1
        })
      }
          
      vm.$emit('update:sortBy', field.key)

      return itemsFilterSort
    },


    selectRow: function (id, event) {
      const vm = this
      if (!(vm.selectRowClick)) {
        return
      }
      if ((event.srcElement.className == 'custom-control-label')) { return }
      if (vm.selectedPlural) {
        let idIndex = vm.selectedLocal.indexOf(id)
        if (idIndex >= 0) {
          vm.selectedLocal.splice(idIndex, 1)
        } else {
          vm.selectedLocal.push(id)
        }
      } else {
        if (vm.selectedLocal == id) {
          vm.selectedLocal = []
        } else {
          vm.selectedLocal = [id]
        }
      }
    },

    selectAllRows: function () {
      const vm = this
      if (!(vm.selectAll)) {return}
      if (vm.selectedLocal >= 0) {
        vm.selectedLocal = []
        vm.itemsFilterActive.forEach(function(item){
          vm.selectedLocal.push(item.id)
        })
      } else {
        vm.selectedLocal = []
      }
    },

    isRowSelected: function (id) {
      const vm = this
      let result = false
      let idIndex = vm.selectedLocal.indexOf(id)
      result = (idIndex >= 0 && !vm.disableSelect) ? true : false
      return result
    },

    compareArray: function (otherArray){
      return function(current){
        return otherArray.filter(function(other){
          return other.id == current.id
        }).length == 0;
      }
    },
  },

  watch: {
    
    itemsFilterActive: {
      handler(newItems, oldItems){
        const vm = this
        if (Array.isArray(newItems) && Array.isArray(oldItems)){
          let diffItems = newItems.filter(vm.compareArray(oldItems))
          let row
          if (diffItems.length == 1) {
            Vue.nextTick(function () {
              row = document.getElementById(`${vm.uid}-${diffItems[0].id}`)
              row.scrollIntoView(true)
              if (vm.selectRowClick){vm.selectedLocal = [diffItems[0].id]}
            })
          }
        }
      }
    },

    selectedLocal: {
      handler(){
        const vm = this
        vm.$emit('update:selected', vm.selectedLocal)
        if (!(vm.selectedPlural)) {
          let event = {target: {value: vm.selectedLocal[0]}}
          vm.onInputCheckbox(event)
        }
      }
    },

    selected: {
      handler(){
        const vm = this
        vm.selectedLocal = vm.selected
      }
    },

  },

  mounted: function () {
    const vm = this
    vm.$root.$on('sort-table', event => {
      if (event.key == vm.sortBy) {
        vm.$emit('update:sortAsc', !vm.sortAsc)
      } else {
        vm.$emit('update:sortBy', event.key)
        vm.$emit('update:sortAsc', true)
      }


    })
  },

  created: function () {
  },

  
}
</script>

<style scoped>
.search-input {
  width: 300px;
  /*margin-left: auto;*/
}

.row-checkbox {
  width: 16px; 
  height: 16px;
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
  vertical-align: middle;
}

.list tbody {
  display:block;
  overflow-y:scroll;
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

.search-button {
  line-height: 1em;
}


</style>