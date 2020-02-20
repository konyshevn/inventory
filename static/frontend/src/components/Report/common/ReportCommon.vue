<template>
  <div>
  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';


export default {
  name: 'ReportCommon',
  components: {
  },

  mixins: [],
  
  props: {
  },
    
  data () {
    return {
    }       
  },

  methods: {
    ...mapMutations([
    ]),

    ...mapActions([
      'FETCHreport',
      'FETCHreportOptions',
    ]),

    async buildReport (){
      const vm = this
      vm.reportData = null
      vm.showSettings = false
      vm.loading = true
      let reportResponse = await vm.FETCHreport([vm.status.reportName, vm.status.filterReq])
      if (reportResponse.status >= 200 && reportResponse.status < 300) {
        vm.reportData = reportResponse.data
      }
      vm.loading = false 
    },
  },

  computed: {
    ...mapGetters([
      'GETcatlgItemLabel',
    ]),
  },


  async mounted () {
    const vm = this
    let reportOptionsResponse = await vm.FETCHreportOptions(vm.status.reportName)
    if (reportOptionsResponse.status >= 200 && reportOptionsResponse.status < 300) {
      vm.status.fieldsOptions = reportOptionsResponse.data[0].fields_options
      vm.status.filterOptions = reportOptionsResponse.data[0].filter_options
    }
  },

  created: function() {
  }, 

  beforeDestroy: function() {
  },

}
   

</script>


<style>
.loading-spinner {
  z-index: 999999; 
  position: fixed; 
  top: 50%; 
  left: 50%
}
</style>

