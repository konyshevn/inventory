<template>
  <div align="left">
    <component :is="catlgAlias[catlgType]['item']" :id="id"></component>
    <catlg-widget-modal></catlg-widget-modal>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import CatlgDeviceItem from '@/components/Catlg/CatlgDevice/CatlgDeviceItem.vue';
import {aliases} from '@/components/common/aliases.js';
import CatlgWidgetModal from '@/components/Catlg/common/Widget/CatlgWidgetModal.vue';


export default {
  name: 'CatlgItem',
  components: {
    CatlgDeviceItem,
    CatlgWidgetModal,

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

