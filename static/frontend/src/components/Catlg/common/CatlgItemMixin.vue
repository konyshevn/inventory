<template>
  <div>
  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import * as CatlgConstructor from '@/components/Catlg/common/catlg-constructor.js'
import {EventBus} from '@/components/common/event-bus.js'


export default {
  name: 'CatlgItemMixin',
  components: {
  },

  mixins: [],
  
  props: {
  },
    
  data () {
    return {
    }       
  },

methods: {
    ...mapActions([
      'FETCHcatlgItem',
    ])
  },

  computed: {
    ...mapGetters([
      'GETcatlgItem',
      'widgetsIsValid',
    ]),

  },

   async mounted () {
    var vm = this
    if (vm.id == 'new') {
      vm.item = new CatlgConstructor[vm.status.catlgType]
    } else {
      await vm.FETCHcatlgItem([vm.status.catlgType, vm.id])
      vm.item = vm.GETcatlgItem(vm.status.catlgType, vm.id)
    }
  },

  created: function() {
    const vm = this
    EventBus.$on('start-saving-catlg', ({itemType, itemId}) => {
      if (vm.status.catlgType == itemType && vm.item.id == itemId) {
        vm.status.itemSaving = true
      }
    })
    EventBus.$on('stop-saving-catlg', ({itemType, itemId}) => {
      if (vm.status.catlgType == itemType && vm.item.id == itemId) {
        vm.status.itemSaving = false
      }
    })

  }, 

}

</script>

<style>
</style>

