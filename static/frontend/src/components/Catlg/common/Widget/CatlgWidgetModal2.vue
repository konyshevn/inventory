<template>
  <div >
    <b-modal :id="modalId" size="xl" scrollable
    ok-title="Выбрать"
    cancel-title="Отмена" 
    @show="showModal=true" 
    @hidden="showModal=false" 
    @ok="handleOk">
      modal
      <component :is="catlgAlias[catlgType]['list']" :modal="modalId" v-if="showModal"></component>
    </b-modal>
    
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import CatlgDeviceList from '@/components/Catlg/CatlgDevice/CatlgDeviceList.vue';
import {aliases} from '@/components/common/aliases.js';
import {EventBus} from '@/components/common/event-bus.js'

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
      selectedItemId: null,
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
    handleOk: function (bvModalEvt) {
      // Prevent modal from closing
      //bvModalEvt.preventDefault()
      const vm = this
      EventBus.$emit('catlgWidgetSetModel', {modalId: vm.modalId, id: vm.selectedItemId})
    },

  },

  computed: {
    modalId: function () {
      let vm = this
      return `modal-${vm.catlgType}-${vm.uid}`
    }
  },

  mounted: function () {
  },

  created: function () {
    var vm = this
    EventBus.$on('modalItemSelected', event => {
      if (event.modalId == vm.modalId) {
        vm.selectedItemId = event.id
        if (event.handleOk) { 
          vm.handleOk()
          vm.$root.$emit('bv::hide::modal', vm.modalId)
        }
      }
    })
  },
  
}
</script>