<template>
  <div>
    <b-table-simple small class="table-borderless" style="width: 500px;">
      <report-filter-option v-for="(option, optionName, index) in status.filterOptions" :key="index"
        :filter-option="option"
        :filter-option-name="optionName"
        :status="status"
      >      
      </report-filter-option>
    </b-table-simple>
    
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

