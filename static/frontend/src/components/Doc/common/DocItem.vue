<template>
  <div>
    <component :is="docAlias[docType]['item']" :id="id"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import DocIncomeItem from '@/components/Doc/DocIncome/DocIncomeItem.vue';
import {aliases} from '@/components/common/aliases.js';
import CatlgWidgetModal from '@/components/Catlg/common/Widget/CatlgWidgetModal.vue';


export default {
  name: 'DocItem',
  components: {
    DocIncomeItem,
    CatlgWidgetModal,

  },
  props: {
    id: null,
    docType: String
  },
  
 
  data () {
    return {
      docAlias: aliases.docAlias
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

