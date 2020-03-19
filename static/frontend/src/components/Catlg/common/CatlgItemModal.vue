<template>
  <div align="left">
    <b-modal :id="modalId" size="lg" scrollable 
    ok-only 
    ok-variant="secondary" 
    ok-title="Закрыть"
    @show="showModal=true" 
    @hidden="showModal=false"
    >
      <catlg-item :id="id" :catlgType="catlgType" v-if="showModal" :modal="true"></catlg-item>
    </b-modal>
  </div>
</template>


<script>
/* eslint-disable no-console */
import CatlgItem from '@/components/Catlg/common/CatlgItem.vue';
import {EventBus} from '@/components/common/event-bus.js'


export default {
  name: 'CatlgItemModal',
  components: {
    CatlgItem,
  },

  props: {
    parent: String,
    catlgType: String,
  },
  
  data () {
    return {
      showModal: false,
      id: null,
      //catlgType: ''
    }       
  },

  methods: {
  },

  computed: {
    modalId: function () {
      let vm = this
      return `catlg-item-modal-${vm.catlgType}-${vm.parent}`
    }
  },
  
  mounted: function () {
  },

  created: function() {
    const vm = this
    EventBus.$on('editCatlgItemModal', event => {
      //console.log('$on.editCatlgItemModal: event', event)
      if (event.modalId == vm.modalId) {
        vm.id = event.id
        //vm.catlgType = event.catlgType
        vm.$root.$emit('bv::show::modal', vm.modalId)
      }
    })
    EventBus.$on('closeCatlgItemModal', event => {
      if (event.modalId == vm.modalId) {
        vm.$root.$emit('bv::hide::modal', vm.modalId)
      }
    })
  }, 

}
   



</script>

<style scoped>

</style>

