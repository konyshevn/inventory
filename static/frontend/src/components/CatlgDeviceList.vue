<template>
  <div class = "catlg-device-list container">
    <h1 align="left">Устройства</h1>
    <table class="table table-bordered">
      <thead>
        <tr>
          <sort-header :obj-type="{catlg: 'device'}" field-type="widget" sort-field="deviceType">
            Тип
          </sort-header>
          <th>Наименование</th>
          <th>Серийный номер</th>
          <th>Инвентарный номер</th>
          <th>Комментарий</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="device in GETcatlg('device')" :key="device.id">
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
import Vue from 'vue'
import {HTTP} from '../http-common'
import {EventBus} from './event-bus.js'
var _ = require('lodash');
import CatlgCommon from './CatlgCommon.vue';
import SortHeader from './SortHeader.vue'
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';


export default {
  name: 'CatlgDeviceList',
  
  components: {
    SortHeader,
  },

/*
  props: {
    catlgs: Object,
  },
*/

  mixins: [CatlgCommon],
  
  data () {
    return {
      type: 'CatlgList'
    }
  },
  methods: {
    ...mapActions([
      'FETCHcatlg',
    ]),
    
    async loadCatlgList () {
      var vm = this
      //await vm.fetchCatlg('nomenclature')
      //await vm.fetchCatlg('deviceType')
      await vm.fetchCatlg('device')
    },

    clearCatlgList: function () {
      var vm = this
      vm.catlgs['device'] = {}
      vm.catlgs['deviceType'] = {}
      vm.catlgs['nomenclature'] = {}
    }

  },
  computed: {
    ...mapGetters([
      'GETcatlg',
      'GETcatlgItemLabel',
    ]),
  },
  mounted: function () {
    //this.loadCatlgList()
    this.FETCHcatlg(['device']);
  },

  created: function () {
    var vm = this;
    EventBus.$on('reloadCatlgList', catlgType => {
      console.log('EventBus: showCatlg ' + catlgType)
      if (catlgType == 'device') {
        console.log('Refresh catalog')
        vm.clearCatlgList()
        vm.loadCatlgList()
      }
      
    });
  },

  
}
</script>