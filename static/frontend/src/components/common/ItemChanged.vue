<template>
  <div class="item-changed-badge">
    <b-badge v-if="itemChanged" variant="info">изменен</b-badge> 
  </div>
</template>


<script>
/* eslint-disable no-console */
var _ = require('lodash');


export default {
  name: 'ItemChanged',

  components: {
  },

  props: {
    itemSaved: {
      type: Boolean,
      default: false,
    },
    item: Object,
  },
  
 
  data () {
    return {
      initItem: {},
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

  },
  
  mounted: function () {
    const vm = this
    vm.initItem = _.cloneDeep(vm.item)
  },

  watch: {
    itemSaved: {
      handler(){
        const vm = this
        if (vm.itemSaved) {
          console.log('itemSaved')
          vm.initItem = _.cloneDeep(vm.item)
          let itemSaved = _.cloneDeep(vm.itemSaved)
          itemSaved = false
          vm.$emit('update:itemSaved', itemSaved)
        }
      },
    },
  },

  created: function() {
  }, 

}
   



</script>

<style>
.item-changed-badge {
  display: inline;
}
</style>

