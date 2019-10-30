<template>
  <div align="left">
    <component :is="catlgAlias[catlgType]['item']" :id="id"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import CatlgDeviceItem from '@/components/Catlg/CatlgDevice/CatlgDeviceItem.vue';
import CatlgPersonItem from '@/components/Catlg/CatlgPerson/CatlgPersonItem.vue';
import {aliases} from '@/components/common/aliases.js';


export default {
  name: 'CatlgItem',
  components: {
    CatlgDeviceItem,
    CatlgPersonItem,
  },

  props: {
    id: null,
    catlgType: String
  },
  
 
  data () {
    return {
      catlgAlias: aliases.catlgAlias
    }       
  },

  methods: {
  },

  computed: {
  },
  
  mounted: function () {
  },

  created: function() {
  }, 

}
   



</script>

<style scoped>

</style>

