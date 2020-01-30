<template>
  <div class="container">
    <vue-headful title="Отчет: Местоположение на дату"/>
    <smart-table 
      :table-padd="200"
      :selected-plural="true"
      :selectAll="true"
      :sort-by.sync="status.sortBy"
      :sort-asc.sync="status.sortAsc"
      :items="reportData"
      :fields="[
        {key: 'device', label: 'Устройство', type: 'text', width: '40%',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'department', label: 'Подразделение', type: 'text', width: '20%',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'stock', label: 'Склад', type: 'text', width: '10%',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'person', label: 'Сотрудник', type: 'text', width: '15%',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'qty', label: 'Количество', type: 'number', width: '10%',
        },
      ]"
    >
      
    </smart-table>
  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
// import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
// import DocCommon from '@/components/Doc/common/DocCommon.vue';
// import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';
import SmartTable from '@/components/common/SmartTable.vue'
// import DatetimeWidget from '@/components/Catlg/common/Widget/DatetimeWidget.vue';



export default {
  name: 'RepCurrentLocation',
  components: {
    // CatlgWidget,
    // DatetimeWidget,
    SmartTable,
  },

  mixins: [],
  
  props: {
  },
    
  data () {
    return {
      status: {
        reportName: 'RepCurrentLocation',
        filterReq: {
          date_to: "31.12.2019 23:59:59",
        },
        fieldsOptions: {},
        sortBy: 'device',
        sortAsc: true,
      },
      reportData: null,
    }       
  },

  methods: {
    ...mapMutations([
    ]),

    ...mapActions([
      'FETCHreport',
      'FETCHreportOptions',
    ]),
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
      vm.status.fieldsOptions = reportOptionsResponse.data.fields_options
    }

    let reportResponse = await vm.FETCHreport([vm.status.reportName, vm.status.filterReq])
    if (reportResponse.status >= 200 && reportResponse.status < 300) {
      vm.reportData = reportResponse.data
    } 
  },

  created: function() {
  }, 

  beforeDestroy: function() {
    //this.DELcurrentDoc()
  },

}
   

</script>


<style>
</style>

