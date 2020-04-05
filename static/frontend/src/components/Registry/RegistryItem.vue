<template>
  <div>
    <smart-table 
    disable-select
    :max-width="2000"
    :min-width="1400"
    :table-padd="200"
    :sort-by.sync="status.sortBy"
    :sort-asc.sync="status.sortAsc"
    :items="registryData"
    :fields="fields">
    </smart-table>
  </div>
</template>


<script>
/* eslint-disable no-console */
/* eslint-disable no-unused-vars */
import { mapActions } from 'vuex';
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import Common from '@/components/common/Common.vue';
import SmartTable from '@/components/common/SmartTable.vue'

export default {
  name: 'RegistryItem',
  components: {
    SmartTable,
  },

  mixins: [Common, CatlgCommon],
  
  props: {
    registryName: String,
    docType: String,
    docId: String,
  },
    
  data () {
    return {
      registryData: [],
      fieldsOption: {},
      status: {
        sortAsc: true,
        sortBy: '',
      },
    }       
  },

  methods: {
    ...mapActions([
      'FETCHregistry',
      'FETCHregistryFieldsOption',
    ]),
  },

  computed: {
    fields: function() {
      const vm = this
      let tableFields = []
      let fieldLabel, tableFieldItem, fieldWidth
      for (let field in vm.fieldsOption) {
        fieldWidth = 100/Object.keys(vm.fieldsOption).length + '%'
        fieldLabel = vm.fieldsOption[field]['label'] || field
        if (typeof vm.fieldsOption[field]['type'] === 'object' && vm.fieldsOption[field]['type'] !== null && 'catlg' in vm.fieldsOption[field]['type']) {
          tableFieldItem = {
            key: field, label: fieldLabel, type: 'text', width: fieldWidth,
            formatter: (value, key) => {return vm.GETcatlgItemLabel(key, value)}}
        } else if (vm.fieldsOption[field]['type'] == 'doc') {
          tableFieldItem = {
            key: field, label: fieldLabel, type: 'text', width: fieldWidth,
            formatter: (value, key) => {return vm.docItemTitle(value.docType, value.docId)}}
        } else if (vm.fieldsOption[field]['type'] == 'number') {
          tableFieldItem = {
            key: field, label: fieldLabel, type: 'number', width: fieldWidth,}
        } else if (vm.fieldsOption[field]['type'] == 'text') {
          tableFieldItem = {
            key: field, label: fieldLabel, type: 'text', width: fieldWidth,}
        } else if (vm.fieldsOption[field]['type'] == 'date') {
          tableFieldItem = {
            key: field, label: fieldLabel, type: 'text', width: fieldWidth,
            formatter: (value) => {return vm.formatDate(value)},
            formatterSort: false,}
        }
        tableFields.push(tableFieldItem)        
      }
      return tableFields
    },
  },

  async mounted() {
    const vm = this
    let responseRegistry = await vm.FETCHregistry([vm.registryName, vm.docType, vm.docId])
    if (responseRegistry.status >= 200 && responseRegistry.status < 300) {
      vm.registryData = responseRegistry.data
    }
    let responseOptions = await vm.FETCHregistryFieldsOption([vm.registryName])
    if (responseOptions.status >= 200 && responseOptions.status < 300) {
      vm.fieldsOption = responseOptions.data
    }

  },

  created: function() {
  }, 

  beforeDestroy: function() {
  },

}
   

</script>


<style>
</style>

