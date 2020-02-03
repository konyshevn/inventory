<template>
  
  <tr>
    <td class="align-middle">{{filterOption.label}}</td>
    <td class="align-middle">
      <catlg-widget v-if="isCatlg" 
        :widgetType="filterOption.type.catlg"
        :model.sync="status.filterReq[filterOptionName]"
      ></catlg-widget>
      <datetime-widget v-if="isDate"
        :date-only="true"
        :model="status.filterReq[filterOptionName]" 
      ></datetime-widget>
    </td>
  </tr>

</template>


<script>
/* eslint-disable no-console */
// import RepCurrentLocation from '@/components/Report/RepCurrentLocation.vue';



export default {
  name: 'ReportFilterOption',
  components: {
    CatlgWidget: () => import('@/components/Catlg/common/Widget/CatlgWidget.vue'),
    DatetimeWidget: () => import('@/components/Catlg/common/Widget/DatetimeWidget.vue'),

  },

  props: {
    filterOption: Object,
    filterOptionName: String,
    status: Object,
  },
  
 
  data () {
    return {
    }       
  },

  methods: {

  },

  computed: {
    isCatlg: function(){
      const vm = this
      if (typeof vm.filterOption['type'] === 'object' && 'catlg' in vm.filterOption['type']) {
        return true
      } else {
        return false
      }
    },

    isDate: function(){
      const vm = this
      if (vm.filterOption['type'] == 'date') {
        return true
      } else {
        return false
      }
    },
  },
  
  mounted: function () {
  },

  created: function() {
  }, 

}
   



</script>

<style >

</style>

