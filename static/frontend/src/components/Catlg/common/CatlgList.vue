<template>
  <div>
    <component :is="catlgAlias[catlgType]['list']" :modal="modal"></component>
    <catlg-item-modal></catlg-item-modal>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import CatlgDeviceList from '@/components/Catlg/CatlgDevice/CatlgDeviceList.vue';
import CatlgItemModal from '@/components/Catlg/common/CatlgItemModal.vue';
import {aliases} from '@/components/common/aliases.js';


export default {
  name: 'CatlgList',
  components: {
    CatlgItemModal,
    CatlgDeviceList,

  },
  props: {
    id: Number,
    catlgType: String,
    modal: null,
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

