<template>
  <div>
    <b-container >
      <report-filter-option v-for="(option, optionName, index) in status.filterOptions" :key="index"
        :filter-option="option"
        :filter-option-name="optionName"
        :filter-value.sync="status.filterReq[optionName]"
      >      
      </report-filter-option>
    </b-container>
    
  </div>

</template>


<script>
/* eslint-disable no-console */
import ReportFilterOption from '@/components/Report/common/ReportFilterOption.vue';



export default {
  name: 'ReportControlPanel',
  components: {
    ReportFilterOption,
  },

  props: {
    status: Object,
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

