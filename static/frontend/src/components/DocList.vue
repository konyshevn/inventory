<template>
  <div>
    <component :is="docAlias[docType]['list']"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import DocIncomeList from './DocIncomeList.vue';
import {aliases} from './aliases.js';


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

