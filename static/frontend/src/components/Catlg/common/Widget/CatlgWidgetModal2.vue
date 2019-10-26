<template>
  <div >
    <b-modal :id="modalId" size="xl" scrollable @show="showModal=true" @hidden="showModal=false" @ok="handleOK">
      modal
      <component :is="catlgAlias[catlgType]['list']" :modal="true" v-if="showModal"></component>
    </b-modal>
    
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import CatlgDeviceList from '@/components/Catlg/CatlgDevice/CatlgDeviceList.vue';
import {aliases} from '@/components/common/aliases.js';

export default {
  name: 'CatlgWidgetModal',
  components: {
    CatlgDeviceList,
  },

  props: {
    uid: Number,
    catlgType: String,
  },

  data () {
    return {
      showModal: false,
      catlgAlias: aliases.catlgAlias,
    }
  },
  methods: {
    /*
    showModal: function () {
      var vm = this
      vm.showModal = true
    },
    
    hideModal: function () {
      var vm = this
      vm.showModal = false
    },
*/
    handleOk(bvModalEvt) {
        // Prevent modal from closing
        bvModalEvt.preventDefault()

      },
  },

  computed: {
    modalId: function () {
      let vm = this
      return `modal-${vm.catlgType}-${vm.uid}`
    }
  },

  mounted: function () {

  }
  
}
</script>