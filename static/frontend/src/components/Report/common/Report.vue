<template>
  <div>
    <component :is="reportName"></component>
  </div>
</template>


<script>
/* eslint-disable no-console */
import RepCurrentLocation from '@/components/Report/RepCurrentLocation.vue';



export default {
  name: 'Report',
  components: {
    RepCurrentLocation,

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

</style>

