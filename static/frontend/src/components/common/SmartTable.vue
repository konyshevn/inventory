<template>
  <div>

    <b-input-group class="mt-3">
    <b-form-input v-model="searchText" placeholder="Поиск" @input.native="tableSearch"></b-form-input>
    <b-input-group-append>
      <b-button variant="light" @click="searchText=''"><font-awesome-icon icon="times"/></b-button>
    </b-input-group-append>
    </b-input-group>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th><font-awesome-icon icon="check-square"/></th>
          <sort-header v-for="field in fields" :key="field.key" 
          :field="field" 
          :sort-by="sortBy" 
          :sort-asc="sortAsc"
          >
            {{field.label}}
          </sort-header>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in itemsFilter" :key="item.id"
        @dblclick="dblclickRow(item.id)"
        @click="selectRow(item.id, $event)"
        >
          <td>
            <b-form-checkbox
            v-model="selectedLocal"
            :value="item.id"
            @input="onInputCheckbox"
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
  },

  computed: {
    sortByField: function() {
      const vm = this
      return _.find(vm.fields, {key: vm.sortBy})
    },
  },
  
  methods: {

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



</style>