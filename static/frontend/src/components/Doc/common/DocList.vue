<template>
  <div>
    <component :is="docAlias[docType]['list']"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
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

<style>
.select-row {
  vertical-align: middle; 
  text-align: center;
}

header { text-align: left; }
header > h2 { display: inline-block; }
header span { margin-left: 10px;}

.doc-list tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}


.doc-list th, .doc-list td {
padding: 0.25rem !important;
}
</style>

