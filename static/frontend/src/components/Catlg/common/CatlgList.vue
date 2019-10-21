<template>
  <div>
    <component :is="catlgAlias[catlgType]['list']"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import CatlgDeviceList from '@/components/Catlg/CatlgDevice/CatlgDeviceList.vue';
import {aliases} from '@/components/common/aliases.js';


export default {
  name: 'DocList',
  components: {
    CatlgDeviceList,

  },
  props: {
    id: Number,
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

<style>

</style>

