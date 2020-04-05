<template>
  <div class="item-changed-badge">
    <b-badge v-if="itemChanged && !itemNew" variant="info">изменен</b-badge>
    <b-badge v-if="itemNew && inited" variant="info">новый</b-badge> 
  </div>
</template>


<script>
/* eslint-disable no-console */
var _ = require('lodash');
import {EventBus} from '@/components/common/event-bus.js'


export default {
  name: 'ItemChanged',

  components: {
  },

  props: {
    item: Object,
    status: Object,
  },
  
 
  data () {
    return {
      initItem: {},
      inited: false,
      eventName: {
        doc: 'stop-saving-doc',
        catlg: 'stop-saving-catlg',
      },
    }       
  },

  methods: {
  },

  computed: {
    itemChanged: function() {
      const vm = this
      Object.compare = function (obj1, obj2) {
        //Loop through properties in object 1
        for (var p in obj1) {
          //Check property exists on both objects
          if (obj1.hasOwnProperty(p) !== obj2.hasOwnProperty(p)) return false;
 
          switch (typeof (obj1[p])) {
            //Deep compare objects
            case 'object':
              if (!Object.compare(obj1[p], obj2[p])) return false;
              break;
            //Compare function code
            case 'function':
              if (typeof (obj2[p]) == 'undefined' || (p != 'compare' && obj1[p].toString() != obj2[p].toString())) return false;
              break;
            //Compare values
            default:
              if (obj1[p] != obj2[p]) return false;
          }
        }
 
        //Check object 2 for any extra properties
        for (let p in obj2) {
          if (typeof (obj1[p]) == 'undefined') return false;
        }
        return true;
      };

      return (!Object.compare(vm.initItem, vm.item) || !Object.compare(vm.item, vm.initItem))
    },

    itemNew: function() {
      const vm = this
      return (!vm.item.id)
    },

  },
  
  mounted: function () {
    // const vm = this
    // vm.initItem = _.cloneDeep(vm.item)
  },

  watch: {
    item: {
      handler(){
        const vm = this
        if (Object.keys(vm.item).length != 0 && !vm.inited) {
          vm.inited = true
          vm.initItem = _.cloneDeep(vm.item)          
        }
      },
    }
    // itemSaved: {
    //   handler(){
    //     const vm = this
    //     if (vm.itemSaved) {
    //       vm.initItem = _.cloneDeep(vm.item)
    //       let itemSaved = _.cloneDeep(vm.itemSaved)
    //       itemSaved = false
    //       vm.$emit('update:itemSaved', itemSaved)
    //     }
    //   },
    // },
  
  },

  created: function() {
    const vm = this
    let eventName, itemTypeLocal
    if ('docType' in vm.status) {
      eventName = vm.eventName['doc']
      itemTypeLocal = vm.status.docType
    } else if ('catlgType' in vm.status) {
      eventName = vm.eventName['catlg']
      itemTypeLocal = vm.status.catlgType
    }

    EventBus.$on(eventName, ({itemType, itemId, saved}) => {
      if (itemTypeLocal == itemType && vm.item.id == itemId && saved) {
        vm.initItem = _.cloneDeep(vm.item)     
      }
    })

  }, 

}
   



</script>

<style>
.item-changed-badge {
  display: inline;
}
</style>

