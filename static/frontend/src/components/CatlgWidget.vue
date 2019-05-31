<template>
  <div style="position:relative;display:block">

    <div style="float:left;width:100%">
      <cool-select 
      v-model="model" 
      :items="items"
      item-value="id"
      item-text="label"
      :arrowsDisableInstantSelection="true"
      :scrollItemsLimit="10"
      @focus="active=true"
      @blur="active=false"
      :loading="loading"
      disable-filtering-by-search
      @search="onSearch"
      @input="$emit('update:model', model)"
      >
        <template slot="no-data">
          <span>Не найдено</span>
        </template>
        <template slot="item" slot-scope="{ item }">
          <div class="item">
            <span class="item-name"> {{ item.label }} </span>
          </div>
        </template>
        <template slot="input-end">
          <b-button v-if="active" size="sm" variant="light" v-b-modal="widgetType + '-modal'">O</b-button>
          <b-button v-if="active" size="sm" variant="light" v-b-modal="widgetType + '-modal'">...</b-button>
        </template>
      </cool-select>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
var _ = require('lodash');
import { CoolSelect } from 'vue-cool-select'
import CatlgCommon from './CatlgCommon.vue';
import {EventBus} from './event-bus.js'

export default {
  name: 'CatlgWidget',
  components: {
    CoolSelect
  },
  mixins: [CatlgCommon],
  props: {
    model: Number,
    widgetType: String,
    initItem: Object,
    required : {
      type: Boolean,
      default: false,
    }
  },

  data () {
    return {
     //'catlgs': this.initCatlgs,
     //'initItem': this.model,
     'active': false,
     'items': [],
     'loading': false,
      searchFields: {
        'device': ['nomenclature__label', 'deviceType__label', 'serial_num', 'inv_num'],
        'person': ['name', 'surname'],
        'department': ['label'],
        'stock': ['label']
      }
    }
  },

  methods: {
    blur: function () {
      var vm=this
      setTimeout(function() { vm.active=false }, 1);
    },



    async onSearch(search) {
      var vm = this
      const lettersLimit = 2;
      Vue.set(vm, 'items', [])
      Vue.set(vm.catlgs, vm.widgetType, [])
      if (search.length < lettersLimit) {
        Vue.set(vm, 'items', [])
        Vue.set(vm.catlgs, vm.widgetType, [])
        vm.loading = false;
        return;
      }
      vm.loading = true;
      await vm.fetchCatlg(vm.widgetType, search, vm.searchFields[vm.widgetType])
      for (var key in vm.catlgs[vm.widgetType]) {
        vm.items.push(vm.catlgs[vm.widgetType][key])
      }
      vm.loading = false
    },

  },

  mounted: function () {
  },

  computed: {
  },

  watch: {
    initItem: { 
      handler(){
        var vm = this
        if (vm.initItem[vm.widgetType][vm.model]) {
          vm.items = []
          vm.items.push(vm.initItem[vm.widgetType][vm.model])
        }
      },
    deep: true
  }

  },

  created: function() {
  }
  
}
</script>