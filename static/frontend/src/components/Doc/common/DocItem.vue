<template>
  <div>
    <component :is="docAlias[docType]['item']" :id="id"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
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

<style >
.select-row {
  vertical-align: middle; 
  text-align: center;
}

header { text-align: left; }
header > h2 { display: inline-block; }
header span { margin-left: 10px;}

.table_unit tbody tr:hover {
    background-color: #f2f2f2;
    color: #000000
  }

.table_unit td, .table_unit th {
  padding: 0.30rem !important;
}

</style>

