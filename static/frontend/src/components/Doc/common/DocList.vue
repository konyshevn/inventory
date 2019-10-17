<template>
  <div>
    <component :is="docAlias[docType]['list']"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import DocIncomeList from '@/components/Doc/DocIncome/DocIncomeList.vue';
import {aliases} from '@/components/common/aliases.js';


export default {
  name: 'DocList',
  components: {
    DocIncomeList,

  },
  props: {
    id: Number,
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

