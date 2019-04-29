<template>
  <div style="position:relative;display:block">
    {{model}}
    <div style="float:left;width:100%">
      <cool-select 
      v-model="model" 
      :items="items"
      item-value="id"
      item-text="label"
      arrowsDisableInstantSelection="true"
      scrollItemsLimit="10"
      @focus="active=true"
      @blur="active=false"
      :loading="loading"
      disable-filtering-by-search
      @search="onSearch"
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

export default {
  name: 'CatlgWidget',
  components: {
    CoolSelect
  },
  mixins: [CatlgCommon],
  props: {
    model: Number,
    widgetType: String
  },

  data () {
    return {
     'active': false,
     'items': [],
     'loading': false,
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
      vm.items = [];
      
      if (search.length < lettersLimit) {
        vm.items = [];
        vm.loading = false;
        return;
      }
      vm.loading = true;
      console.log(vm.widgetType)
      await vm.fetchCatlg(vm.widgetType)
      console.log(vm.catlgs)
      for (var key in vm.catlgs[vm.widgetType]) {
        vm.items.push(vm.catlgs[vm.widgetType][key])
      }
      vm.loading = false
      //clearTimeout(this.timeoutId);
      //this.timeoutId = setTimeout(async () => {
      //var response = await HTTP.get(`"${type}"?query="${search}"`)
      //var catlgItemFetch = response.data

      //}, 500);
    }



  },
  mounted: function () {

  }
  
}
</script>