<template>
  <div class="container">
    <b-modal id="device-modal" size="xl" scrollable title="Устройства" @show="showModal('device')" @hidden="hideModal('device')">
      <catlg-device-list v-if="showCatlg['device']"></catlg-device-list>
    </b-modal>
    
    <b-modal id="person-modal">
      Person Modal
    </b-modal>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
import {EventBus} from './event-bus.js'
var _ = require('lodash');
import CatlgDeviceList from './CatlgDeviceList.vue';

export default {
  name: 'CatlgWidgetModal',
  components: {
    CatlgDeviceList,
  },
  /*
  props: {
    catlgs: Object
  },
*/
  data () {
    return {
      showCatlg:{
        'device': false,
        'person': false
      }
    }
  },
  methods: {
    showModal: function (catlgType) {
      var vm = this
      vm.showCatlg[catlgType] = true
      EventBus.$emit('reloadCatlgList', catlgType)
      console.log('Open Modal ' + catlgType)
    },
    
    hideModal: function (catlgType){
      var vm = this
      vm.showCatlg[catlgType] = false
    },
  },
  mounted: function () {

  }
  
}
</script>