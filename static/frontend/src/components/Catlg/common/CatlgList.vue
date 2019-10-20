<template>
  <div>
    <component :is="catlgAlias[catlgType]['list']"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import CatlgDeviceList from '@/components/Catlg/CatlgDevice/CatlgDeviceList.vue';
import {aliases} from '@/components/common/aliases.js';


export default {
  name: 'DocList',
  components: {
    CatlgDeviceList,

  },
  props: {
    id: Number,
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

<style>
.catlg-list tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}

.catlg-list {
  display: inline-grid;
  grid-template-areas: 
  "head-fixed" 
  "body-scrollable";
}

.catlg-list thead {
  grid-area: head-fixed;
  /* fallback */
 /* width: 100%;
  /* minus scroll bar width */
  width: calc( 100% - 1em ) !important;/* scrollbar is average 1em/16px width, remove it from thead width */
  cursor: pointer;
}

.catlg-list tbody {
  grid-area: body-scrollable;
  overflow-y: scroll;
  height: calc(90vh  - 140px);
}

.catlg-list thead, .catlg-list tbody tr {
    display:table;
    table-layout:fixed;/* even columns width , fix width of table too*/
}
</style>

