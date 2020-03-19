<template>
  <div align="left">
    <component :is="catlgAlias[catlgType]['item']" :id="id" :modal="modal"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import CatlgDeviceItem from '@/components/Catlg/CatlgDevice/CatlgDeviceItem.vue';
import CatlgPersonItem from '@/components/Catlg/CatlgPerson/CatlgPersonItem.vue';
import CatlgDepartmentItem from '@/components/Catlg/CatlgDepartment/CatlgDepartmentItem.vue';
import Common from '@/components/common/Common.vue';

import {aliases} from '@/components/common/aliases.js';


export default {
  name: 'CatlgItem',
  components: {
    CatlgDeviceItem,
    CatlgPersonItem,
    CatlgDepartmentItem,
    CatlgStockItem: () => import('@/components/Catlg/CatlgStock/CatlgStockItem.vue'),
    CatlgDeviceTypeItem: () => import('@/components/Catlg/CatlgDeviceType/CatlgDeviceTypeItem.vue'),
    CatlgNomenclatureItem: () => import('@/components/Catlg/CatlgNomenclature/CatlgNomenclatureItem.vue'),
  },

  mixins: [Common,],

  props: {
    id: null,
    catlgType: String,
    modal: {
      type: Boolean,
      default: false,
    },

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
header { text-align: left; }
header > h2 { display: inline-block; }
header span { margin-left: 10px;}

</style>

