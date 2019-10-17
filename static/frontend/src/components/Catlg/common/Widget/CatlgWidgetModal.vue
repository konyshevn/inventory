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
import CatlgDeviceList from '@/components/Catlg/CatlgDevice/CatlgDeviceList.vue';

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