<template>
  
  <tr>
    <td class="align-middle">{{filterOption.label}}</td>
    <td class="align-middle">
      <catlg-widget v-if="isCatlgMulti" 
        :widgetType="filterOption.type.catlg"
        :multi="true"
        :model-multi.sync="filterValueLocal"
      ></catlg-widget>

      <catlg-widget v-if="isCatlgSingle" 
        :widgetType="filterOption.type.catlg"
        :model.sync="filterValueLocal"
      ></catlg-widget>

      <datetime-widget v-if="isDate"
        :date-only="true"
        :model.sync="filterValueLocal" 
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
    // status: Object,
    filterValue: null,
  },
  
 
  data () {
    return {
      filterValueLocal: this.filterValue,
      modelMulti: [],
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

    isCatlgSingle: function(){
      const vm = this
      if (vm.isCatlg && (('list' in vm.filterOption && !vm.filterOption['list']) || !('list' in vm.filterOption) )) {
        return true
      } else {
        return false
      }
    },

    isCatlgMulti: function(){
      const vm = this
      if (vm.isCatlg && 'list' in vm.filterOption && vm.filterOption['list']) {
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

    isDatetime: function(){
      const vm = this
      if (vm.filterOption['type'] == 'datetime') {
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

  watch: {
    filterValueLocal: {
      handler(){
        const vm = this
        vm.$emit('update:filter-value', vm.filterValueLocal)
      }
    },
  },
}
   



</script>

<style >

</style>

