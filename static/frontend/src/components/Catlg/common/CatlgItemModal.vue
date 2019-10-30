<template>
  <div align="left">
    <b-modal id="catlg-item-modal" size="lg" scrollable 
    ok-only 
    ok-variant="secondary" 
    ok-title="Закрыть"
    @show="showModal=true" 
    @hidden="showModal=false"
    >
      <catlg-item :id="id" :catlgType="catlgType" v-if="showModal"></catlg-item>
    </b-modal>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import CatlgItem from '@/components/Catlg/common/CatlgItem.vue';
import {EventBus} from '@/components/common/event-bus.js'


export default {
  name: 'CatlgItemModal',
  components: {
    CatlgItem,
  },

  props: {
  },
  
 
  data () {
    return {
      showModal: false,
      id: null,
      catlgType: ''
    }       
  },

  methods: {
  },

  computed: {
  },
  
  mounted: function () {
  },

  created: function() {
    const vm = this
    EventBus.$on('editCatlgItemModal', event => {
      console.log('$on.editCatlgItemModal: event', event)
      vm.id = event.id
      vm.catlgType = event.catlgType
      vm.$root.$emit('bv::show::modal', 'catlg-item-modal')
    })
    EventBus.$on('closeCatlgItemModal', event => {
      vm.$root.$emit('bv::hide::modal', 'catlg-item-modal')
    })
  }, 

}
   



</script>

<style scoped>

</style>

