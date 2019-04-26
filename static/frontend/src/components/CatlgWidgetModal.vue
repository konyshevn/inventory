<template>
  <div class="container">
    <b-modal id="device-modal" size="xl" scrollable title="Устройства">
      <catlg-device-list></catlg-device-list>
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
    }
  },
  methods: {

  },
  mounted: function () {

  }
  
}
</script>