<template>
  <div>
    <component :is="docAlias[docType]['item']" :id="id"></component>
    <catlg-widget-modal></catlg-widget-modal>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import DocIncomeItem from './DocIncomeItem.vue';
import {aliases} from './aliases.js';
import CatlgWidgetModal from './CatlgWidgetModal.vue';


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

