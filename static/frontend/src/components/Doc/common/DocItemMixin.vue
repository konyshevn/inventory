<template>
  <div>
  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import * as DocConstructor from '@/components/Doc/common/doc-constructor.js'
import {EventBus} from '@/components/common/event-bus.js'


export default {
  name: 'DocItemMixin',
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
      'FETCHdocItem',
    ]),
  },

  computed: {
    ...mapGetters([
      'widgetsIsValid',
      'GETdocItem',
    ]),

  },

  async mounted () {
    const vm = this
    vm.status.uid = vm.uid
    if (vm.id == "new") {
      vm.item = new DocConstructor[vm.status.docType]
    } else {
      await vm.FETCHdocItem([vm.status.docType, vm.id])
      vm.item = vm.GETdocItem(vm.status.docType, vm.id)
    }
  },

  created: function() {
    const vm = this
    EventBus.$on('start-saving-doc', ({itemType, itemId}) => {
      if (vm.status.docType == itemType && vm.item.id == itemId) {
        vm.status.itemSaving = true
      }
    })
    EventBus.$on('stop-saving-doc', ({itemType, itemId}) => {
      if (vm.status.docType == itemType && vm.item.id == itemId) {
        vm.status.itemSaving = false
      }
    })

  }, 

}

</script>

<style>
</style>

