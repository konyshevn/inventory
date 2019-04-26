<template>
  <div calss = "catlg-device-list container">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Тип</th>
          <th>Наименование</th>
          <th>Серийный номер</th>
          <th>Инвентарный номер</th>
          <th>Комментарий</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="device in catlgs['device']" :key="device['id']">
          <td>
            {{displayCatlgItem('devicetype', device['device_type'])}}
          </td>
          <td>
            {{displayCatlgItem('device', device['id'])}}
          </td>
          <td>
            {{device['serial_num']}}
          </td>
          <td>
            {{device['inv_num']}}
          </td>
          <td>
            {{device['comment']}}
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
var _ = require('lodash');
import CatlgCommon from './CatlgCommon.vue';

export default {
  name: 'CatlgDeviceList',
  
  components: {
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

  },
  mounted: function () {
    var vm = this
    vm.fetchCatlg('nomenclature')
    .then(function(){
      vm.fetchCatlg('devicetype')
    })
    .then(function(){
      vm.fetchCatlg('device')
    })

  },

  
}
</script>