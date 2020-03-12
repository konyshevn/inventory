<template>
  <div>
    <component :is="reportName"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import RepCurrentLocation from '@/components/Report/RepCurrentLocation.vue';
import RepStatementDocs from '@/components/Report/RepStatementDocs.vue';



export default {
  name: 'Report',
  components: {
    RepCurrentLocation,
    RepStatementDocs,

  },
  props: {
    reportName: String,
  },
  
 
  data () {
    return {
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
.loading-spinner {
  z-index: 999999; 
  position: fixed; 
  top: 50%; 
  left: 50%
}
</style>

