<template>
  <div>
    <component :is="docAlias[docType]['item']" :id="id"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import DocIncomeItem from './DocIncomeItem.vue';
import {aliases} from './aliases.js';


export default {
  name: 'DocItem',
  components: {
    DocIncomeItem,

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

