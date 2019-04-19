<template>
  <div style="position:relative;display:block">
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
          <b-button v-if="active" size="sm" variant="light" v-b-modal="type + '-modal'">O</b-button>
          <b-button v-if="active" size="sm" variant="light" v-b-modal="type + '-modal'">...</b-button>
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

export default {
  name: 'CatlgWidget',
  components: {
    CoolSelect
  },
  props: {
    model: Number,
    items: Object,
    type: String
  },

  data () {
    return {
     'active': false
    }
  },
  methods: {
    blur: function () {
      var vm=this
      setTimeout(function() { vm.active=false }, 1);
    }

  },
  mounted: function () {

  }
  
}
</script>