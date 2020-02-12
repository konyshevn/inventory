<template>
  <div>
    <b-tabs content-class="mt-3">
      <b-tab title="Фильтр" active>
        <b-container>
          <report-filter-option v-for="(option, optionName, index) in status.filterOptions" :key="index"
          :filter-option="option"
          :filter-option-name="optionName"
          :filter-value.sync="status.filterReq[optionName]">      
          </report-filter-option>
        </b-container>
      </b-tab>
      
      <b-tab title="Поля">
      </b-tab>
    

    </b-tabs>
    
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

