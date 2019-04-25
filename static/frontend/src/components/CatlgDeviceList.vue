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
        <tr v-for="device in catlgs['device']" :key="device.id">
          <td>
            {{displayCatlgItem('devicetype', device.id)}}
          </td>
          <td>
            
          </td>
          <td>
            
          </td>
          <td>
            
          </td>
          <td>
            
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
    }
  },
  methods: {

  },
  mounted: function () {
    this.fetchCatlg('device')
    //this.fetchCatlg('devicetype')
    //this.fetchCatlg('nomenclature')
  },

  
}
</script>