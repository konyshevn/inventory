<template>
  <div style="text-align: center">
    <component :is="catlgAlias[catlgType]['list']" :modal="modal"></component>
    <catlg-item-modal parent="list" :catlgType="catlgType"></catlg-item-modal>
  </div>
</template>


<script>
/* eslint-disable no-console */
import CatlgDeviceList from '@/components/Catlg/CatlgDevice/CatlgDeviceList.vue';
import CatlgPersonList from '@/components/Catlg/CatlgPerson/CatlgPersonList.vue';
import CatlgDepartmentList from '@/components/Catlg/CatlgDepartment/CatlgDepartmentList.vue';

import {aliases} from '@/components/common/aliases.js';

export default {
  name: 'CatlgList',
  components: {
    CatlgItemModal: () => import('@/components/Catlg/common/CatlgItemModal.vue'),
    CatlgDeviceList,
    CatlgPersonList,
    CatlgDepartmentList,
    CatlgStockList: () => import('@/components/Catlg/CatlgStock/CatlgStockList.vue'),
    CatlgDeviceTypeList: () => import('@/components/Catlg/CatlgDeviceType/CatlgDeviceTypeList.vue'),
    CatlgNomenclatureList: () => import('@/components/Catlg/CatlgNomenclature/CatlgNomenclatureList.vue'),


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
header { text-align: left; }
header > h2 { display: inline-block; }
header span { margin-left: 10px;}

</style>

